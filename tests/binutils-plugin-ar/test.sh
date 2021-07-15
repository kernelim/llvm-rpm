#!/bin/sh -eux

set pipefail

echo "void lto_function(){}" | clang -flto -O2 -c -x c -o foo.o -
ar crs foo.a foo.o
readelf -c foo.a | grep lto_function
