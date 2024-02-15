#!/usr/bin/env python3


import asyncio
from async_dict import async_dict


async def test_async_dict():

    d = async_dict(foo=10)

    assert len(d) == 1
    assert 'foo' in d
    assert list(d) == ['foo']
    assert await d['foo'] == 10
    assert not d.is_waiting('foo')
    del d['foo']
    assert not d

    assert await d.get('missing', timeout=.1) == None
    assert await d.get('missing', 123, timeout=.1) == 123
    try:
        async with asyncio.timeout(.1):
            await d.get('missing')
            assert False
    except TimeoutError:
        pass

    async def reader():
        assert await d['bar'] == 99
        assert 'bar' in d
        assert await d.pop('baz') == 'done'
        assert 'baz' not in d
        #with trio.move_on_after(.1):
        try:
            async with asyncio.timeout(.1):
                await asyncio.sleep(.1)
                await d['baz']
                assert False
        except TimeoutError:
            pass

    async def writer():
        await asyncio.sleep(.1)
        assert d.is_waiting('bar')
        d['bar'] = 99
        await asyncio.sleep(.1)
        assert d.is_waiting('baz')
        d['baz'] = 'done'

    #await trio.wait_all(reader, writer)
    async with asyncio.timeout(2):
        await asyncio.gather(reader(), writer())


if __name__ == "__main__":
    asyncio.run(test_async_dict())
