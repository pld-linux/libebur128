#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	EBU R 128 standard for loudness normalisation
Summary(pl.UTF-8):	Standard normalizacji głośności EBU R 128
Name:		libebur128
Version:	1.2.6
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/jiixyj/libebur128/releases
Source0:	https://github.com/jiixyj/libebur128/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d38c5f86f5dccb37b5818b853ad49f32
URL:		https://github.com/jiixyj/libebur128
BuildRequires:	cmake >= 2.8.12
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libebur128 is a library that implements the EBU R 128 standard for
loudness normalisation.

%description -l pl.UTF-8
libebur128 to biblioteka implementująca standard normalizacji
głośności EBU R 128.

%package devel
Summary:	Header files for ebur128 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ebur128
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for ebur128 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ebur128.

%package static
Summary:	Static ebur128 library
Summary(pl.UTF-8):	Statyczna biblioteka ebur128
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ebur128 library.

%description static -l pl.UTF-8
Statyczna biblioteka ebur128.

%prep
%setup -q

%build
%if %{with static_libs}
install -d build-static
cd build-static
%cmake .. \
	-DBUILD_SHARED_LIBS=OFF \
	-DCMAKE_INSTALL_LIBDIR=%{_lib}

%{__make}
cd ..
%endif

install -d build
cd build
# .pc file expects relative CMAKE_INSTALL_LIBDIR
%cmake .. \
	-DBUILD_STATIC_LIBS=OFF \
	-DCMAKE_INSTALL_LIBDIR=%{_lib}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.md doc/license/R128Scan.txt
%attr(755,root,root) %{_libdir}/libebur128.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libebur128.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libebur128.so
%{_includedir}/ebur128.h
%{_pkgconfigdir}/libebur128.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libebur128.a
%endif
