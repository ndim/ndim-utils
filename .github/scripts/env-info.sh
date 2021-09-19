#!/bin/sh

set -x

pwd

ls -d .git

git status
git branch -v
git tag --list
git tag --list -n10
git describe
git describe --always

$SHELL --version

automake --version
autoconf --version
libtoolize --version
gettextize --version
pkg-config --version

gcc --version
clang --version
make --version

:
