#!/bin/sh

git init

ref=90e58059ab5da6c91dcd2533de018c30c88b2de6

curl -L -o license.txt https://github.com/groove-x/trio-util/raw/$ref/LICENSE
curl -L -o async_dict.py https://github.com/groove-x/trio-util/raw/$ref/src/trio_util/_async_dictionary.py
curl -L -o test_async_dict.py https://github.com/groove-x/trio-util/raw/$ref/tests/test_async_dictionary.py
curl -L -O https://github.com/groove-x/trio-util/raw/$ref/.gitignore

git add .gitignore .init.sh license.txt async_dict.py test_async_dict.py

GIT_AUTHOR_NAME="John Belmonte" \
GIT_AUTHOR_EMAIL="john.belmonte@groove-x.com" \
GIT_AUTHOR_DATE="Wed Aug 14 14:12:06 2019 +0900" \
git commit -m "init from trio-util"
