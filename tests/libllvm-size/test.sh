#!/bin/sh -eux

# There is a bug in the build process when it runs out of disk space
# while stripping binaries, which causes the strip to fail, but does
# not fail the build.  This results in a libLLVM.so that is over 2GB
# which breaks the nightly compose.  So this test checks that libLLVM.so
# is less than 100MB to ensure it was successfully stripped.
# https://bugzilla.redhat.com/show_bug.cgi?id=1793250

test $(stat -L -c %s /usr/lib64/libLLVM.so) -lt 104857600
