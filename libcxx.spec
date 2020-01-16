# If you need to bootstrap this, turn this on.
# Otherwise, you have a loop with libcxxabi
%global bootstrap 0
#%%global rc_ver 4
%global baserelease 2

%global libcxx_srcdir libcxx-%{version}%{?rc_ver:rc%{rc_ver}}.src

Name:		libcxx
Version:	9.0.0
Release:	%{baserelease}%{?rc_ver:.rc%{rc_ver}}%{?dist}
Summary:	C++ standard library targeting C++11
License:	MIT or NCSA
URL:		http://libcxx.llvm.org/
Source0:	http://%{?rc_ver:pre}releases.llvm.org/%{version}/%{?rc_ver:rc%{rc_ver}}/%{libcxx_srcdir}.tar.xz
BuildRequires:	gcc-c++ llvm-devel cmake llvm-static
%if %{bootstrap} < 1
BuildRequires:	libcxxabi-devel
BuildRequires:	python3
%endif
# PPC64 (on EL7) doesn't like this code.
# /builddir/build/BUILD/libcxx-3.8.0.src/include/thread:431:73: error: '(9.223372036854775807e+18 / 1.0e+9)' is not a constant expression
# _LIBCPP_CONSTEXPR duration<long double> _Max = nanoseconds::max();
%if 0%{?rhel}
ExcludeArch:	ppc64 ppc64le
%endif

%description
libc++ is a new implementation of the C++ standard library, targeting C++11.

%package devel
Summary:	Headers and libraries for libcxx devel
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if %{bootstrap} < 1
Requires:	libcxxabi-devel
%endif

%description devel
%{summary}.

%package static
Summary:	Static libraries for libcxx

%description static
%{summary}.

%prep
%setup -q -n %{name}-%{version}%{?rc_ver:rc%{rc_ver}}.src

%build
mkdir _build
cd _build

%cmake .. \
	-DLLVM_CONFIG=%{_bindir}/llvm-config \
%if %{bootstrap} < 1
	-DLIBCXX_CXX_ABI=libcxxabi \
	-DLIBCXX_CXX_ABI_INCLUDE_PATHS=%{_includedir} \
	-DPYTHONINTERP_FOUND=ON \
	-DPYTHON_EXECUTABLE=%{_bindir}/python3 \
	-DLIBCXX_ENABLE_ABI_LINKER_SCRIPT=ON \
%endif
%if 0%{?__isa_bits} == 64
	-DLIBCXX_LIBDIR_SUFFIX:STRING=64 \
%endif
	-DCMAKE_BUILD_TYPE=RelWithDebInfo


make %{?_smp_mflags}

%install
cd _build
make install DESTDIR=%{buildroot}

%ldconfig_scriptlets

%files
%license LICENSE.TXT
%doc CREDITS.TXT TODO.TXT
%{_libdir}/libc++.so.*

%files devel
%{_includedir}/c++/
%{_libdir}/libc++.so

%files static
%license LICENSE.TXT
%{_libdir}/libc++*.a


%changelog
* Thu Jan 16 2020 Tom Stellard <tstellar@redhat.com> - 9.0.0-2
- Build with gcc on all arches

* Mon Sep 23 2019 Tom Stellard <tstellar@redhat.com> - 9.0.0-1
- 9.0.0 Release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 20 2019 sguelton@redhat.com - 8.0.0-1
- 8.0.0 final

* Tue Mar 12 2019 sguelton@redhat.com - 8.0.0-0.4.rc4
- 8.0.0 Release candidate 4

* Mon Mar 4 2019 sguelton@redhat.com - 8.0.0-0.3.rc3
- 8.0.0 Release candidate 3

* Sun Feb 24 2019 sguelton@redhat.com - 8.0.0-0.2.rc2
- 8.0.0 Release candidate 2

* Mon Feb 11 2019 sguelton@redhat.com - 8.0.0-0.1.rc1
- 8.0.0 Release candidate 1

* Wed Feb 06 2019 sguelton@redhat.com - 7.0.1-1
- 7.0.1 Release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.1-0.2.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 10 2018 sguelton@redhat.com - 7.0.1-0.1.rc3
- 7.0.1-rc3 Release

* Tue Sep 25 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-1
- 7.0.0 Release

* Wed Sep 12 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.1.rc3
- 7.0.0-rc3 Release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Tom Callaway <spot@fedoraproject.org> - 6.0.1-1
- update to 6.0.1

* Wed Mar 21 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-2
- Use default LDFLAGS/CXXFLAGS/CFLAGS and filter out flags not supported by clang

* Wed Mar 14 2018 Tom Callaway <spot@fedoraproject.org> - 6.0.0-1
- 6.0.0 final

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-0.1.rc1
- 6.0.0-rc1

* Thu Dec  21 2017 Tom Stellard <tstellar@redhat.com> - 5.0.1-1
- 5.0.1 Release

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

* Wed Mar  8 2017 Tom Callaway <spot@fedoraproject.org> - 3.9.1-1
- update to 3.9.1

* Fri Mar  3 2017 Tom Callaway <spot@fedoraproject.org> - 3.9.0-4
- LIBCXX_ENABLE_ABI_LINKER_SCRIPT=ON

* Wed Mar  1 2017 Tom Callaway <spot@fedoraproject.org> - 3.9.0-3
- disable bootstrap

* Tue Feb 21 2017 Dan Horák <dan[at]danny.cz> - 3.9.0-2
- apply s390(x) workaround only in Fedora < 26

* Mon Feb 20 2017 Tom Callaway <spot@fedoraproject.org> - 3.9.0-1
- update to 3.9.0 (match clang)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Aug 26 2016 Tom Callaway <spot@fedoraproject.org> - 3.8.1-1
- update to 3.8.1

* Thu Jun 09 2016 Dan Horák <dan[at]danny.cz> - 3.8.0-4
- exclude Power only in EPEL
- default to z10 on s390(x)

* Thu May 19 2016 Tom Callaway <spot@fedoraproject.org> - 3.8.0-3
- use gcc on el7, fedora < 24. use clang on el6 and f24+
  MAGIC.
- bootstrap on

* Tue May 3 2016 Tom Callaway <spot@fedoraproject.org> - 3.8.0-2
- bootstrap off

* Tue May 3 2016 Tom Callaway <spot@fedoraproject.org> - 3.8.0-1
- initial package
- bootstrap on
