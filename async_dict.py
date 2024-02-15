import asyncio


class async_dict:
    """MutableMapping with waitable get and pop.

    aka "class AsyncDict"

    based on "class AsyncDictionary" from
    https://github.com/groove-x/trio-util/blob/cd8f273f62dbb301b504a3b7778bdd3069fecb6f/src/trio_util/_async_dictionary.py

    see also

    https://github.com/groove-x/trio-util/issues/4
    AsyncDict vs. cancellation
    AsyncDictionary has been removed from the package

    https://github.com/python-trio/trio/issues/467
    Add "one obvious way" for implementing the common multiplexed request/response pattern

    https://github.com/shmocz/pyra2yr/blob/main/pyra2yr/async_container.py

    https://github.com/f3at/feat/blob/15da93fc9d6ec8154f52a9172824e25821195ef8/src/feat/common/container.py#L744
    """

    def __init__(self, *args, **kwargs):
        self._store = dict(*args, **kwargs)
        self._pending = {}  # key: Event

    def __getitem__(self, key):
        return self._store[key]

    async def get_wait(self, key):
        """Return value of given key, blocking until populated."""
        if key in self._store:
            return self._store[key]
        if key not in self._pending:
            self._pending[key] = asyncio.Event()
        await self._pending[key].wait()
        return self._store[key]

    async def pop_wait(self, key):
        """Remove key and return its value, blocking until populated."""
        value = await self.get_wait(key)
        del self._store[key]
        return value

    def is_waiting(self, key) -> bool:
        """Return True if there is a task waiting for key."""
        return key in self._pending

    def __setitem__(self, key, value):
        self._store[key] = value
        if key in self._pending:
            self._pending.pop(key).set()

    def __delitem__(self, key):
        del self._store[key]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __repr__(self):
        return repr(self._store)
