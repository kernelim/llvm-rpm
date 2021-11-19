# Optimized RPM packaging for the LLVM project

This repository provides an optimized build of LLVM and Clang. It is
self-bootstrapping for the target system and does not depend on a pre-built
version of LLVM.

Target system:

- RHEL/CentOS 7.x - x86_64 and aarch64 architectures.

**Why this is needed**: New and optimized versions of the LLVM toolchain are
not directly managed by maintainers of the older target LTS distributions, and
not always to the best of ways. Original LLVM builds target Debian-based
systems.

Notes:

- Clang is built as an [LTO](https://llvm.org/docs/LinkTimeOptimization.html) executable that links only to LLVM shared library, so it is fully optimized.
- Aims to backport and preserve original Fedora package work for LLVM packages.
- Target version 13.0.0, bootstrapped by building Clang 11.1.0;
- LLVM sub-projects `compiler-rt` and `lld` are also bootstrapped in this build
process.


# Instructions

**Notes:**

- Expect the build of this repository to take a few hours.
- Network access is needed for build. The network dependencies are:
    - Access to `github.com`.
    - Access to Fedora's source package servers.
    - Access to `docker.com` for base CentOS 7.x image.
    - Access to `mirror.centos.org` for SCLo repositories.
- A privileged docker instance is needed due to usage of [mock](https://github.com/rpm-software-management/mock/wiki) inside the container.


## Clone

```
git clone --depth 1 --recursive https://github.com/kernelim/llvm-rpm
```

## Build:

```
cd llvm-rpm
./run under-container build-all
```

Expected output is under `repo` sub directory:

```
$ ls -l repo/
total 40
drwxr-xr-x. 2 root root 4096 Mar 31 09:33 repodata
drwxrwxr-x. 3 root root 4096 Mar 30 23:07 results_clang
drwxrwxr-x. 3 root root 4096 Mar 30 22:29 results_cmake
drwxrwxr-x. 3 root root 4096 Mar 30 23:22 results_compiler-rt
drwxrwxr-x. 3 root root 4096 Mar 31 09:31 results_libcxx
drwxrwxr-x. 3 root root 4096 Mar 30 23:24 results_libcxxabi
drwxrwxr-x. 3 root root 4096 Mar 31 09:32 results_lld
drwxrwxr-x. 3 root root 4096 Mar 30 22:55 results_llvm
drwxrwxr-x. 3 root root 4096 Mar 30 22:49 results_llvm-11.1.0
drwxrwxr-x. 3 root root 4096 Mar 30 23:22 results_python-lit
```

Notes:

- Not all outputs are needed for successful usage of the built compiler.
- Specifically, bootstrapping compiler `results_llvm-11.1.0` can be removed.
- There is a run-time dependency over `libcxx` and `libcxxabi` by the built compiler.
- For repeated executions, some parameters can be provided to `under-container` to save setup time, e.g. `./run under-container -r -s`


## Building outside docker

It is also possible to build without depending on docker, directly on a CentOS
7.x system, provided that it has EPEL prerequisites such as `fedpkg` and
`mock`. 

The `root-setup` stage installs a mock configuration under `/etc/mock`, and
prepares an RPM a repo under `/opt/repo`, where the outputs will reside.

```
./run root-setup
./run build-all
```
