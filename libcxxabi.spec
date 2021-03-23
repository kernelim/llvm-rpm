#%%global rc_ver 6
%global baserelease 1
%global libcxxabi_srcdir libcxxabi-%{version}%{?rc_ver:rc%{rc_ver}}.src
%bcond_with stage1
%global stage1ver 11.1.0
%global debug_package %{nil}

Name:		libcxxabi
Version:	10.0.0
Release:	%{baserelease}%{?rc_ver:.rc%{rc_ver}}%{?dist}
Summary:	Low level support for a standard C++ library
License:	MIT or NCSA
URL:		http://libcxxabi.llvm.org/
%if 0%{?rc_ver:1}
Source0:	https://prereleases.llvm.org/%{version}/rc%{rc_ver}/%{libcxxabi_srcdir}.tar.xz
Source3:	https://prereleases.llvm.org/%{version}/rc%{rc_ver}/%{libcxxabi_srcdir}.tar.xz.sig
%else
Source0:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/%{libcxxabi_srcdir}.tar.xz
Source3:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/%{libcxxabi_srcdir}.tar.xz.sig
%endif
Source4:	https://prereleases.llvm.org/%{version}/hans-gpg-key.asc

BuildRequires:	clang llvm-devel cmake llvm-static
BuildRequires:	libcxx-devel >= %{version}
BuildRequires:	compiler-rt

%if %{with stage1}
BuildRequires:  llvm-stage1-%{stage1ver}-libcxx
%endif

%if 0%{?rhel}
# libcxx-devel has this, so we need to as well.
ExcludeArch:	ppc64 ppc64le
%endif

%description
libcxxabi provides low level support for a standard C++ library.

%package devel
Summary:	Headers and libraries for libcxxabi devel
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}.

%package static
Summary:	Static libraries for libcxxabi

%description static
%{summary}.

%prep
%setup -q -n %{libcxxabi_srcdir}

sed -i 's|${LLVM_BINARY_DIR}/share/llvm/cmake|%{_libdir}/cmake/llvm|g' CMakeLists.txt

%build

%if %{with stage1}
export LD_LIBRARY_PATH=/opt/llvm-stage1-%{stage1ver}/lib
%endif

%ifarch armv7hl
# disable ARM exception handling
sed -i 's|#define _LIBCXXABI_ARM_EHABI||g' include/__cxxabi_config.h
%endif

mkdir _build
cd _build
%ifarch s390 s390x
%if 0%{?fedora} < 26
# clang requires z10 at minimum
# workaround until we change the defaults for Fedora
%global optflags %(echo %{optflags} | sed 's/-march=z9-109 /-march=z10 /')
%endif
%endif

# Filter out cflags not supported by clang.
%global optflags %(echo %{optflags} | sed -e 's/-mcet//g' -e 's/-fcf-protection//g' -e 's/-fstack-clash-protection//g')

%cmake .. \
	-DCMAKE_C_COMPILER=/usr/bin/clang \
	-DCMAKE_CXX_COMPILER=/usr/bin/clang++ \
	-DLLVM_CONFIG=%{_bindir}/llvm-config \
	-DCMAKE_CXX_FLAGS="-std=c++11" \
	-DLIBCXXABI_USE_COMPILER_RT=YES \
	-DLIBCXXABI_LIBCXX_INCLUDES=%{_includedir}/c++/v1/ \
%if 0%{?__isa_bits} == 64
	-DLIBCXXABI_LIBDIR_SUFFIX:STRING=64 \
%endif
	-DCMAKE_BUILD_TYPE=RelWithDebInfo


make %{?_smp_mflags}

%install
cd _build
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_includedir}
cd ..
cp -a include/* %{buildroot}%{_includedir}

%ldconfig_scriptlets

%files
%license LICENSE.TXT
%doc CREDITS.TXT
%{_libdir}/libc++abi.so.*

%files devel
%{_includedir}/*.h
%{_libdir}/libc++abi.so

%files static
%{_libdir}/libc++abi.a

%changelog
* Tue Mar 31 2020 sguelton@redhat.com - 10.0.0-1
- 10.0.0 final

* Wed Mar 25 2020 sguelton@redhat.com - 10.0.0-0.5.rc6
- 10.0.0 rc6

* Sat Mar 21 2020 sguelton@redhat.com - 10.0.0-0.4.rc5
- 10.0.0 rc5

* Sun Mar 15 2020 sguelton@redhat.com - 10.0.0-0.3.rc4
- 10.0.0 rc4

* Thu Mar 05 2020 sguelton@redhat.com - 10.0.0-0.2.rc3
- 10.0.0 rc3

* Fri Feb 14 2020 sguelton@redhat.com - 10.0.0-0.1.rc2
- 10.0.0 rc2

* Fri Jan 31 2020 sguelton@redhat.com - 10.0.0-0.1.rc1
- 10.0.0 rc1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Tom Stellard <tstellar@redhat.com> - 9.0.1-1
- 9.0.1 Release

* Mon Sep 23 2019 Tom Stellard <tstellar@redhat.com> - 9.0.0-1
- 9.0.0 Release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 25 2019 sguelton@redhat.com - 8.0.0-1
- 8.0.0 Release

* Tue Mar 12 2019 sguelton@redhat.com - 8.0.0-0.4.rc4
- 8.0.0 Release candidate 4

* Mon Mar 4 2019 sguelton@redhat.com - 8.0.0-0.3.rc3
- 8.0.0 Release candidate 3

* Sun Feb 24 2019 sguelton@redhat.com - 8.0.0-0.2.rc2
- 8.0.0 Release candidate 2

* Mon Feb 11 2019 sguelton@redhat.com - 8.0.0-0.1.rc1
- 8.0.0 Release candidate 1

* Wed Feb  6 2019 Tom Callaway <spot@fedoraproject.org> - 7.0.1-2
- remove -fstack-clash-protection

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 17 2018 sguelton@redhat.com - 7.0.1-1
- 7.0.1 Release

* Mon Dec 10 2018 sguelton@redhat.com - 7.0.1-0.1.rc3
- 7.0.1-rc3 Release

* Tue Dec 04 2018 sguelton@redhat.com - 7.0.0-2
- Ensure rpmlint passes on specfile

* Tue Sep 25 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-1
- 7.0.0 Release

* Wed Sep 12 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.1.rc3
- 7.0.0-rc3 Release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Tom Callaway <spot@fedoraproject.org> - 6.0.1-1
- update to 6.0.1

* Wed Mar 21 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-2
- Use default LDFLAGS/CXXFLAGS/CFLAGS and filter out flags not supported by
  clang

* Wed Mar 14 2018 Tom Callaway <spot@fedoraproject.org> - 6.0.0-1
- update to 6.0.0 final

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 21 2017 Tom Stellard <tstellar@redhat.com> - 6.0.0-0.1.rc1
- 6.0.1-rc1 Release

* Thu Dec 21 2017 Tom Stellard <tstellar@redhat.com> - 5.0.1-1
- 5.0.1 Release

* Tue Dec 19 2017 Tom Stellard <tstellar@redhat.com> - 5.0.0-2
- Fix disabling of ARM exception handling

* Fri Sep  8 2017 Tom Callaway <spot@fedoraproject.org> - 5.0.0-1
- update to 5.0.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 23 2017 Tom Callaway <spot@fedoraproject.org> - 4.0.1-1
- update to 4.0.1

* Sat Apr 22 2017 Tom Callaway <spot@fedoraproject.org> - 4.0.0-1
- update to 4.0.0

* Mon Feb 20 2017 Tom Callaway <spot@fedoraproject.org> - 3.9.0-1
- update to 3.9.0
- apply fixes from libcxx

* Wed Sep  7 2016 Tom Callaway <spot@fedoraproject.org> - 3.8.1-1
- update to 3.8.1

* Mon Jul 25 2016 Tom Callaway <spot@fedoraproject.org> - 3.8.0-2
- make static subpackage

* Tue May 3 2016 Tom Callaway <spot@fedoraproject.org> - 3.8.0-1
- initial package
