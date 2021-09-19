#!/bin/sh

set -x

pwd

ls -d .git

git status
git branch -v
git describe
git describe --always

:
