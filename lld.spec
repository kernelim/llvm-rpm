%global rc_ver 2

%global lld_srcdir lld-%{version}%{?rc_ver:rc%{rc_ver}}.src

Name:		lld
Version:	7.0.0
Release:	0.3.rc%{rc_ver}%{?dist}
Summary:	The LLVM Linker

License:	NCSA
URL:		http://llvm.org
Source0:	http://%{?rc_ver:pre}releases.llvm.org/%{version}/%{?rc_ver:rc%{rc_ver}}/%{lld_srcdir}.tar.xz

Patch0:		0001-CMake-Check-for-gtest-headers-even-if-lit.py-is-not-.patch
Patch1:		0001-lld-Prefer-using-the-newest-installed-python-version.patch
Patch2:		0001-lld-Add-missing-REQUIRES-to-tests.patch
Patch3:		0001-MachO-Fix-out-of-bounds-memory-access-in-getString16.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires: cmake
BuildRequires: llvm-devel = %{version}
BuildRequires: ncurses-devel
BuildRequires: zlib-devel
BuildRequires: chrpath

# For make check:
BuildRequires: python3-lit
BuildRequires: llvm-googletest

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
%autosetup -n %{name}-%{version}%{?rc_ver:rc%{rc_ver}}.src -p1

%build

mkdir %{_target_platform}
cd %{_target_platform}

%cmake .. \
	-DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
	-DLLVM_DYLIB_COMPONENTS="all" \
	-DLLVM_INCLUDE_TESTS=ON \
	-DLLVM_MAIN_SRC_DIR=%{_datadir}/llvm/src \
	-DLLVM_EXTERNAL_LIT=%{_bindir}/lit \
	-DLLVM_LIT_ARGS="-sv \
		-DFileCheck=%{_libdir}/llvm/FileCheck \
		-Dcount=%{_libdir}/llvm/count \
		-Dnot=%{_libdir}/llvm/not \
		--path %{_libdir}/llvm" \
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
make -C %{_target_platform} %{?_smp_mflags} check-lld

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%{_bindir}/lld*
%{_bindir}/ld.lld
%{_bindir}/ld64.lld
%{_bindir}/wasm-ld

%files devel
%{_includedir}/lld
%{_libdir}/liblld*.so

%files libs
%{_libdir}/liblld*.so.*

%changelog
* Fri Aug 31 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.3.rc2
- 7.0.0-rc2 Release

* Thu Aug 30 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.2.rc1
- Enable make check

* Mon Aug 13 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.1.rc1
- 7.0.0-rc1 Release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-1
- 6.0.1 Release

* Fri May 11 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-0.1.rc1
- 6.0.1-rc1 Release

* Thu Mar 08 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-1
- 6.0.0 Release

* Tue Feb 13 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-0.3.rc2
- 6.0.0-rc2 Release

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-0.1.rc1
- 6.0.0-rc1 Release

* Thu Dec 21 2017 Tom Stellard <tstellar@redhat.com> - 5.0.1-1
- 5.0.1 Release

* Mon Sep 11 2017 Tom Stellard <tstellar@redhat.com> - 5.0.0-1
- 5.0.0 Release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 06 2017 Tom Stellard <tstellar@redhat.com> - 4.0.1-2
- Backport r307092

* Tue Jul 04 2017 Tom Stellard <tstellar@redhat.com> - 4.0.1-1
- 4.0.1 Release

* Tue Jul 04 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-4
- Fix build without llvm-static

* Wed May 31 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-3
- Remove llvm-static dependency

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Tue Mar 14 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-1
- lld 4.0.0 Final Release
