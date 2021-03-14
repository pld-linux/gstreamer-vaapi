#
# Conditional build:
%bcond_without	static_libs	# static libraries
%bcond_with	api		# GST VA-API libraries API [no longer exported as of 1.6.0]

%define		gstapi		1.6
%define		gst_ver		1.16.3
%define		gstpb_ver	1.16.3
%define		gstpd_ver	1.16.3
Summary:	GStreamer plugin to support Video Acceleration API
Summary(pl.UTF-8):	Wtyczka GStreamera obsługująca Video Acceleration API
Name:		gstreamer-vaapi
Version:	1.16.3
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://gstreamer.freedesktop.org/src/gstreamer-vaapi/%{name}-%{version}.tar.xz
# Source0-md5:	8c9b5a4d20afc04bc5e1536e81511f27
URL:		https://gstreamer.freedesktop.org/
BuildRequires:	Mesa-libEGL-devel
BuildRequires:	Mesa-libGL-devel
BuildRequires:	Mesa-libGLES-devel
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.14
BuildRequires:	glib2-devel >= 1:2.40.0
BuildRequires:	gstreamer-devel >= %{gst_ver}
BuildRequires:	gstreamer-gl-devel >= %{gstpb_ver}
# gstreamer-codecparsers
BuildRequires:	gstreamer-plugins-bad-devel >= %{gstpd_ver}
BuildRequires:	gstreamer-plugins-base-devel >= %{gstpb_ver}
BuildRequires:	gtk-doc >= 1.12
BuildRequires:	libdrm-devel
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libva-devel >= 1.6.0
BuildRequires:	libva-drm-devel >= 1.1.0
BuildRequires:	libva-wayland-devel >= 1.1.0
BuildRequires:	libva-x11-devel >= 1.0.3
BuildRequires:	pkgconfig
# libva API versions
BuildRequires:	pkgconfig(libva) >= 0.39.0
BuildRequires:	pkgconfig(libva-drm) >= 0.39.0
BuildRequires:	pkgconfig(libva-wayland) >= 0.39.0
BuildRequires:	pkgconfig(libva-x11) >= 0.39.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	wayland-devel >= 1.11.0
BuildRequires:	wayland-protocols >= 1.15
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xz
%ifarch %{ix86} %{x8664} x32
BuildRequires:	yasm
%endif
Requires:	glib2 >= 1:2.40.0
Requires:	gstreamer >= %{gst_ver}
Requires:	gstreamer-gl-libs >= %{gstpb_ver}
Requires:	gstreamer-plugins-bad >= %{gstpd_ver}
Requires:	gstreamer-plugins-base >= %{gstpb_ver}
Requires:	libva >= 1.6.0
Requires:	wayland >= 1.11.0
%if %{without api}
Obsoletes:	gstreamer-vaapi-devel < %{version}
Obsoletes:	gstreamer-vaapi-static < %{version}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gstreamer-vaapi consists in a collection of VA-API based plugins for
GStreamer and helper libraries.

%description -l pl.UTF-8
gstreamer-vaapi zawiera zestaw opartych ma VA-API wtyczek dla
GStreamera i bibliotek pomocniczych.

%package devel
Summary:	Header files for GStreamer VA-API libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek VA-API GStreamera
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gstreamer-devel >= %{gst_ver}
Requires:	gstreamer-plugins-base-devel >= %{gstpb_ver}
Requires:	libva-devel >= 1.6.0
Requires:	libva-drm-devel >= 1.1.0
Requires:	libva-wayland-devel >= 1.1.0
Requires:	libva-x11-devel >= 1.0.3

%description devel
Header files for GStreamer VA-API helper libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek pomocniczych VA-API GStreamera.

%package static
Summary:	Static GStreamer VA-API libraries
Summary(pl.UTF-8):	Statyczne biblioteki VA-API GStreamera
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GStreamer VA-API libraries.

%description static -l pl.UTF-8
Statyczne biblioteki VA-API GStreamera.

%package apidocs
Summary:	GStreamer VA-API plugins documentation
Summary(pl.UTF-8):	Dokumentacja do wtyczek GStreamera VA-API
Group:		Documentation
BuildArch:	noarch

%description apidocs
GStreamer VA-API plugins documentation.

%description apidocs -l pl.UTF-8
Dokumentacja do wtyczek GStreamera VA-API.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4 -I common/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# gstreamer module
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/libgst*.la
%if %{with api}
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with api}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%endif

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%if %{with api}
%attr(755,root,root) %{_libdir}/libgstcodecparsers_vpx.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstcodecparsers_vpx.so.0
%attr(755,root,root) %{_libdir}/libgstvaapi-%{gstapi}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstvaapi-%{gstapi}.so.1
%attr(755,root,root) %{_libdir}/libgstvaapi-drm-%{gstapi}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstvaapi-drm-%{gstapi}.so.1
%attr(755,root,root) %{_libdir}/libgstvaapi-egl-%{gstapi}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstvaapi-egl-%{gstapi}.so.1
%attr(755,root,root) %{_libdir}/libgstvaapi-glx-%{gstapi}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstvaapi-glx-%{gstapi}.so.1
%attr(755,root,root) %{_libdir}/libgstvaapi-wayland-%{gstapi}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstvaapi-wayland-%{gstapi}.so.1
%attr(755,root,root) %{_libdir}/libgstvaapi-x11-%{gstapi}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstvaapi-x11-%{gstapi}.so.1
%endif
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstvaapi.so

%if %{with api}
%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgstcodecparsers_vpx.so
%attr(755,root,root) %{_libdir}/libgstvaapi-%{gstapi}.so
%attr(755,root,root) %{_libdir}/libgstvaapi-drm-%{gstapi}.so
%attr(755,root,root) %{_libdir}/libgstvaapi-egl-%{gstapi}.so
%attr(755,root,root) %{_libdir}/libgstvaapi-glx-%{gstapi}.so
%attr(755,root,root) %{_libdir}/libgstvaapi-wayland-%{gstapi}.so
%attr(755,root,root) %{_libdir}/libgstvaapi-x11-%{gstapi}.so
%{_includedir}/gstreamer-1.0/gst/vaapi
%{_pkgconfigdir}/gstreamer-vaapi-1.0.pc
%{_pkgconfigdir}/gstreamer-vaapi-drm-1.0.pc
%{_pkgconfigdir}/gstreamer-vaapi-glx-1.0.pc
%{_pkgconfigdir}/gstreamer-vaapi-wayland-1.0.pc
%{_pkgconfigdir}/gstreamer-vaapi-x11-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgstcodecparsers_vpx.a
%{_libdir}/libgstvaapi-%{gstapi}.a
%{_libdir}/libgstvaapi-drm-%{gstapi}.a
%{_libdir}/libgstvaapi-egl-%{gstapi}.a
%{_libdir}/libgstvaapi-glx-%{gstapi}.a
%{_libdir}/libgstvaapi-wayland-%{gstapi}.a
%{_libdir}/libgstvaapi-x11-%{gstapi}.a
%endif
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gstreamer-vaapi-plugins-1.0
