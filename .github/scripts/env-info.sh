#!/bin/sh

set -x

pwd

ls -d .git

git status
git branch -v
git describe

git fetch -v

git status
git branch -v
git describe

git fetch -v --tags

git status
git branch -v
git describe

:
