#!/bin/bash

# This test assumes lld is already installed.

set -ex

function verify_ld_bfd {

  # Verify that /usr/bin/ld points to ld.bfd.
  ls -l /etc/alternatives/ld | grep ld.bfd

  # Run ld and verify it invokes ld.bfd
  /usr/bin/ld --version | grep 'GNU ld'
}


# Verify ld.bfd is still the system linker when lld is installed
verify_ld_bfd

# Set lld as the system linker
update-alternatives --set ld /usr/bin/ld.lld

# Verify that /usr/bin/ld points to lld
ls -l /etc/alternatives/ld | grep ld.lld

# Run ld and verify it invokes lld
/usr/bin/ld --version | grep 'LLD'

# Uninstall lld and make sure the /usr/bin/ld is reset to ld.bfd
dnf -y remove lld

verify_ld_bfd
