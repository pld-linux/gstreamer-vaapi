#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
%define		gstapi	1.6
Summary:	GStreamer plugin to support Video Acceleration API
Summary(pl.UTF-8):	Wtyczka GStreamera obsługująca Video Acceleration API
Name:		gstreamer-vaapi
Version:	0.7.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://www.freedesktop.org/software/vaapi/releases/gstreamer-vaapi/%{name}-%{version}.tar.bz2
# Source0-md5:	ce2d4921b8d9c78edd609d95e8c502d3
URL:		http://www.freedesktop.org/wiki/Software/vaapi/
BuildRequires:	Mesa-libEGL-devel
BuildRequires:	Mesa-libGL-devel
BuildRequires:	Mesa-libGLES-devel
BuildRequires:	autoconf >= 2.66
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gstreamer-devel >= 1.6.0
BuildRequires:	gstreamer-plugins-bad-devel >= 1.6.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.6.0
BuildRequires:	gtk-doc >= 1.12
BuildRequires:	libdrm-devel
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libva-devel >= 1.6.0
BuildRequires:	libva-drm-devel >= 1.1.0
BuildRequires:	libva-wayland-devel >= 1.1.0
BuildRequires:	libva-x11-devel >= 1.0.3
BuildRequires:	pkgconfig
# libva API versions
BuildRequires:	pkgconfig(libva) >= 0.38.0
BuildRequires:	pkgconfig(libva-drm) >= 0.33.0
BuildRequires:	pkgconfig(libva-wayland) >= 0.33.0
BuildRequires:	pkgconfig(libva-x11) >= 0.31.0
BuildRequires:	udev-devel
BuildRequires:	wayland-devel >= 1.0.2
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel
%ifarch %{ix86} %{x8664} x32
BuildRequires:	yasm
%endif
Requires:	glib2 >= 1:2.32.0
Requires:	gstreamer >= 1.6.0
Requires:	gstreamer-plugins-bad >= 1.6.0
Requires:	gstreamer-plugins-base >= 1.6.0
Requires:	libva >= 1.6.0
Requires:	wayland >= 1.0.0
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
Requires:	gstreamer-devel >= 1.6.0
Requires:	gstreamer-plugins-base-devel >= 1.6.0
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

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-builtin-codecparsers \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make} V=1 \
	HAVE_GNU_STRIP=no \
	CC="%{__cc}" \
	LD="%{__cc}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# gstreamer module
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/libgst*.la
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
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
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstvaapi.so
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstvaapi_parse.so

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
