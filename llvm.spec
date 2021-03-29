%bcond_with bootstrap

%global maj_ver 11
%global min_ver 1
%global patch_ver 0
%global gitcommit 1fdec59bffc11ae37eb51a1b9869f0696bfd5312
%global stage1ver 10.0.1

%global baserelease 0
%if %{with bootstrap}
%global pkg_name llvm-stage1-%{maj_ver}.%{min_ver}.%{patch_ver}
%else
%global pkg_name llvm-%{maj_ver}.%{min_ver}.%{patch_ver}
%endif
%global instprefix /opt/%{pkg_name}
%define debug_package %{nil}

Name:		%{pkg_name}
Version:	%{maj_ver}.%{min_ver}.%{patch_ver}
Release:	%{baserelease}%{?rc_ver:.rc%{rc_ver}}%{?dist}
Summary:	The LLVM (Low Level Virtual Machine) packages

License:	NCSA
URL:		http://llvm.org
Source0:	https://github.com/llvm/llvm-project/archive/%{gitcommit}.tar.gz

BuildRequires:	cmake
BuildRequires:	zlib-devel
BuildRequires:	libffi-devel
BuildRequires:	ncurses-devel
BuildRequires:	libedit-devel

%if %{with bootstrap}
BuildRequires:  devtoolset-7-gcc
BuildRequires:  devtoolset-7-make
BuildRequires:  devtoolset-7-toolchain
BuildRequires:  devtoolset-7-gdb
%endif

%description

%package devel
Summary:	The LLVM (Low Level Virtual Machine) packages
%description devel

%package tools
Summary:	The LLVM (Low Level Virtual Machine) packages
%description tools

%package clang
Summary:	The LLVM (Low Level Virtual Machine) packages
%description clang

%package clang-tools
Summary:	The LLVM (Low Level Virtual Machine) packages
%description clang-tools

%package clang-devel
Summary:	The LLVM (Low Level Virtual Machine) packages
%description clang-devel

%package lld
Summary:	The LLVM (Low Level Virtual Machine) packages
%description lld

%package lld-devel
Summary:	The LLVM (Low Level Virtual Machine) packages
%description lld-devel

%package compiler-rt
Summary:	The LLVM (Low Level Virtual Machine) packages
%description compiler-rt

%package libcxx
Summary:	The LLVM (Low Level Virtual Machine) packages
%description libcxx

%prep
%build

%if %{with bootstrap}
source /opt/rh/devtoolset-7/enable
%endif

tar -xf %SOURCE0

mkdir build
cd build

cmake ../llvm-project-%{gitcommit}/llvm \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=ON \
  -DLLVM_BUILD_LLVM_DYLIB=ON \
  -DLLVM_TARGETS_TO_BUILD="X86;AArch64" \
  -DLLVM_TARGET_ARCH=X86 \
  -DLLVM_ENABLE_PROJECTS="clang;lld;compiler-rt;libcxx;libcxxabi" \
  -DCMAKE_INSTALL_PREFIX=%{instprefix} \

make %{?_smp_mflags}

%install

%if %{with bootstrap}
source /opt/rh/devtoolset-7/enable
%endif

cd build
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%check

%files
%{instprefix}/lib/libLLVM*
%{instprefix}/lib/libLTO*
%{instprefix}/lib/libRemarks*

%files devel
%{instprefix}/include/llvm
%{instprefix}/include/llvm-c
%{instprefix}/lib/cmake/llvm

%files tools
%{instprefix}/bin/bugpoint
%{instprefix}/bin/dsymutil
%{instprefix}/bin/llc
%{instprefix}/bin/lli
%{instprefix}/bin/llvm-*
%{instprefix}/bin/obj2yaml
%{instprefix}/bin/opt
%{instprefix}/bin/sancov
%{instprefix}/bin/sanstats
%{instprefix}/bin/verify-uselistorder
%{instprefix}/bin/yaml2obj
%{instprefix}/share/opt-viewer

%files clang
%{instprefix}/lib/clang/*/include
%{instprefix}/lib/cmake/clang
%{instprefix}/lib/libclang*
%{instprefix}/libexec/c++-analyzer
%{instprefix}/libexec/ccc-analyzer
%{instprefix}/bin/clang*

%files clang-tools
%{instprefix}/share/man/man1/scan-build.1
%{instprefix}/share/clang
%{instprefix}/share/scan-view
%{instprefix}/share/scan-build
%{instprefix}/bin/scan-build
%{instprefix}/bin/scan-view
%{instprefix}/bin/hmaptool
%{instprefix}/bin/diagtool
%{instprefix}/bin/git-clang-format
%{instprefix}/bin/c-index-test

%files clang-devel
%{instprefix}/include/clang
%{instprefix}/include/clang-c

%files lld
%{instprefix}/lib/liblld*
%{instprefix}/bin/lld*
%{instprefix}/bin/ld.lld
%{instprefix}/bin/ld64.lld
%{instprefix}/bin/wasm-ld
%{instprefix}/lib/cmake/lld

%files lld-devel
%{instprefix}/include/lld

%files libcxx
%{instprefix}/lib/libc++*
%{instprefix}/include/c++

%files compiler-rt
%{instprefix}/lib/clang/*/bin/hwasan_symbolize
%{instprefix}/lib/clang/*/lib/linux/*clang_rt*
%{instprefix}/lib/clang/*/share/*abilist*.txt
%{instprefix}/lib/clang/*/share/*blacklist*.txt

%changelog
