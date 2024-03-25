#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_with	api		# GST VA-API libraries API [no longer exported as of 1.6.0]

%define		gstapi		1.6
%define		gst_ver		1.24.0
%define		gstpb_ver	1.24.0
%define		gstpd_ver	1.24.0
Summary:	GStreamer plugin to support Video Acceleration API
Summary(pl.UTF-8):	Wtyczka GStreamera obsługująca Video Acceleration API
Name:		gstreamer-vaapi
Version:	1.24.1
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://gstreamer.freedesktop.org/src/gstreamer-vaapi/%{name}-%{version}.tar.xz
# Source0-md5:	76cecfa3c2fbd6251bf133cd89696aaa
URL:		https://gstreamer.freedesktop.org/
BuildRequires:	EGL-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-GLX-devel
BuildRequires:	OpenGLESv2-devel
BuildRequires:	OpenGLESv3-devel
BuildRequires:	glib2-devel >= 1:2.67.4
BuildRequires:	gstreamer-devel >= %{gst_ver}
BuildRequires:	gstreamer-gl-devel >= %{gstpb_ver}
# gstreamer-codecparsers
BuildRequires:	gstreamer-plugins-bad-devel >= %{gstpd_ver}
BuildRequires:	gstreamer-plugins-base-devel >= %{gstpb_ver}
%{?with_apidocs:BuildRequires:	hotdoc >= 0.11.0}
BuildRequires:	libdrm-devel >= 2.4.98
BuildRequires:	libva-devel >= 1.10.0
BuildRequires:	libva-drm-devel >= 1.1.0
BuildRequires:	libva-wayland-devel >= 1.1.0
BuildRequires:	libva-x11-devel >= 1.0.3
BuildRequires:	meson >= 1.1
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glesv2)
# libva API versions
BuildRequires:	pkgconfig(libva) >= 1.10
BuildRequires:	pkgconfig(libva-drm) >= 0.39.0
BuildRequires:	pkgconfig(libva-wayland) >= 0.39.0
BuildRequires:	pkgconfig(libva-x11) >= 0.39.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	wayland-devel >= 1.11.0
BuildRequires:	wayland-protocols >= 1.15
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xz
%ifarch %{ix86} %{x8664} x32
BuildRequires:	yasm
%endif
Requires:	glib2 >= 1:2.67.4
Requires:	gstreamer >= %{gst_ver}
Requires:	gstreamer-gl-libs >= %{gstpb_ver}
Requires:	gstreamer-plugins-bad >= %{gstpd_ver}
Requires:	gstreamer-plugins-base >= %{gstpb_ver}
Requires:	libdrm >= 2.4.98
Requires:	libva >= 1.10.0
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
Requires:	libva-devel >= 1.10.0
Requires:	libva-drm-devel >= 1.1.0
Requires:	libva-wayland-devel >= 1.1.0
Requires:	libva-x11-devel >= 1.0.3
Obsoletes:	gstreamer-vaapi-static < %{version}

%description devel
Header files for GStreamer VA-API helper libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek pomocniczych VA-API GStreamera.

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
%meson build \
	--default-library=shared \
	%{!?with_apidocs:-Ddoc=false}

%ninja_build -C build

%if %{with apidocs}
cd build/docs
LC_ALL=C.UTF-8 hotdoc run --conf-file vaapi-doc.json
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_docdir}/gstreamer-%{gstmver}
cp -pr build/docs/vaapi-doc $RPM_BUILD_ROOT%{_docdir}/gstreamer-%{gstmver}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with api}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%endif

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README RELEASE
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
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/gstreamer-%{gstmver}/vaapi-doc
%endif
