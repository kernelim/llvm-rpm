Name:		lld
Version:	4.0.0
Release:	1%{?dist}
Summary:	The LLVM Linker

License:	NCSA
URL:		http://llvm.org
Source0:	http://llvm.org/releases/%{version}/lld-%{version}.src.tar.xz

Patch0:		0001-CMake-Fix-pthread-handling-for-out-of-tree-builds.patch

BuildRequires: cmake
BuildRequires: llvm-static = %{version}
BuildRequires: llvm-devel = %{version}
BuildRequires: ncurses-devel
BuildRequires: zlib-devel
BuildRequires: chrpath

%description
The LLVM project linker.

%package devel
Summary:	Libraries and header files for LLD

%description devel
This package contains library and header files needed to develop new native
programs that use the LLD infrastructure.

%package libs
Summary:	LLD shared libraries

%description libs
Shared libraries for LLD.

%prep
%autosetup -n %{name}-%{version}.src -p1

%build

mkdir %{_target_platform}
cd %{_target_platform}

%cmake .. \
	-DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
%if 0%{?__isa_bits} == 64
	-DLLVM_LIBDIR_SUFFIX=64
%else
	-DLLVM_LIBDIR_SUFFIX=
%endif

%make_build

%install
cd %{_target_platform}
%make_install

# Remove rpath
chrpath --delete %{buildroot}%{_bindir}/*
chrpath --delete %{buildroot}%{_libdir}/*.so*

%check
# Need to install llvm utils for check to pass
#cd _build
#make %{?_smp_mflags} check-lld

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%{_bindir}/lld*
%{_bindir}/ld.lld

%files devel
%{_includedir}/lld
%{_libdir}/liblld*.so

%files libs
%{_libdir}/liblld*.so.*

%changelog
* Tue Mar 14 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-1
- lld 4.0.0 Final Release
