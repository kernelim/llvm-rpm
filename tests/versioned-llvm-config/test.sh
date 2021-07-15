#!/bin/sh -eux

major=$(llvm-config --version | cut -d '.' -f1)

llvm-config-$major --version
