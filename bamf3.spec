#
# Conditional build:
%bcond_without	dbusmenu	# exported window actions menus
%bcond_without	apidocs		# API documentation

Summary:	Application matching framework (GTK+ 3 library)
Summary(pl.UTF-8):	Szkielet do dopasowywania aplikacji (biblioteka GTK+ 3)
Name:		bamf3
Version:	0.5.6
Release:	1
# Library bits are LGPLv2 or LGPLv3 (but not open-ended LGPLv2+);
# non-lib bits are GPLv3.
# pbrobinson points out that three files in the lib are actually
# marked GPL in headers, making library GPL, though we think this
# may not be upstream's intention. For now, marking library as
# GPL.
# License:	LGPL v2.1 or LGPL v3
License:	GPL v2 or GPL v3
Group:		Libraries
Source0:	https://launchpad.net/bamf/0.5/%{version}/+download/bamf-%{version}.tar.gz
# Source0-md5:	49ed19dd5db0b4109f4dc2e4fe2ed13d
URL:		https://launchpad.net/bamf
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.38.0
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel >= 0.10.2
BuildRequires:	gtk+3-devel >= 3.0
BuildRequires:	gtk-doc >= 1.0
%if %{with dbusmenu}
BuildRequires:	libdbusmenu-devel >= 0.4
BuildRequires:	libdbusmenu-gtk3-devel >= 0.4
%endif
BuildRequires:	libgtop-devel >= 2.0
BuildRequires:	libtool >= 2:2
BuildRequires:	libwnck-devel >= 3.4.7
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3
BuildRequires:	python3-lxml
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.043
BuildRequires:	startup-notification-devel
BuildRequires:	vala
BuildRequires:	xorg-lib-libX11-devel
Requires:	glib2 >= 1:2.38.0
Requires:	libwnck >= 3.4.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BAMF removes the headache of applications matching into a simple DBus
daemon and C wrapper library. Currently features application matching
at amazing levels of accuracy (covering nearly every corner case).
This package contains the bamf library built against GTK+ 2.

%description -l pl.UTF-8
BAMF rozwiązuje problem dopasowywania aplikacji za pomocą prostego
demona DBus i biblioteki obudowującej w C. Aktualne możliwości to
dopasowywanie aplikacji z zaskakującym poziomem dokładności
(obejmującym prawie każdy przypadek brzegowy). Ten pakiet zawiera
bibliotekę bamf zbudowaną dla GTK+ 2.

%package devel
Summary:	Development files for BAMF library (GTK+ 3 build)
Summary(pl.UTF-8):	Pliki programistyczne biblioteki BAMF (dla GTK+ 3)
License:	GPL v2 or GPL v3
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.38.0

%description devel
This package contains header files for developing applications that
use BAMF with GTK+ 2.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących BAMF z GTK+ 2.

%package -n vala-libbamf3
Summary:	Vala API for BAMF library (GTK+ 3 build)
Summary(pl.UTF-8):	API języka Vala do biblioteki BAMF (dla GTK+ 3)
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description -n vala-libbamf3
Vala API for BAMF library (GTK+ 3 build).

%description -n vala-libbamf3 -l pl.UTF-8
API języka Vala do biblioteki BAMF (dla GTK+ 3).

%package apidocs
Summary:	BAMF API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki BAMF
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for BAMF library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki BAMF.

%package daemon
Summary:	Application matching framework
Summary(pl.UTF-8):	Szkielet do dopasowywania aplikacji
License:	GPL v3
Group:		Daemons
Requires:	glib2 >= 1:2.38.0
Obsoletes:	bamf-daemon < 0.4

%description daemon
BAMF removes the headache of applications matching into a simple DBus
daemon and C wrapper library. Currently features application matching
at amazing levels of accuracy (covering nearly every corner case).
This package contains the bamf daemon and supporting data.

%description daemon -l pl.UTF-8
BAMF rozwiązuje problem dopasowywania aplikacji za pomocą prostego
demona DBus i biblioteki obudowującej w C. Aktualne możliwości to
dopasowywanie aplikacji z zaskakującym poziomem dokładności
(obejmującym prawie każdy przypadek brzegowy). Ten pakiet zawiera
demona bamf i dane pomocnicze.

%prep
%setup -q -n bamf-%{version}

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir} \
	%{?with_dbusmenu:--enable-actions-menu} \
	--enable-gtk-doc

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbamf3.la
# resolve conflict with gtk+2 based bamf
%{__mv} $RPM_BUILD_ROOT%{_gtkdocdir}/{libbamf,libbamf3}
# upstart is dead
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/upstart

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc TODO
%attr(755,root,root) %{_libdir}/libbamf3.so.*.*.*
%ghost %{_libdir}/libbamf3.so.2
%{_libdir}/girepository-1.0/Bamf-3.typelib

%files devel
%defattr(644,root,root,755)
%{_libdir}/libbamf3.so
%{_includedir}/libbamf3
%{_pkgconfigdir}/libbamf3.pc
%{_datadir}/gir-1.0/Bamf-3.gir

%files -n vala-libbamf3
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libbamf3.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libbamf3
%endif

%files daemon
%defattr(644,root,root,755)
%dir %{_libexecdir}/bamf
%attr(755,root,root) %{_libexecdir}/bamf/bamfdaemon
%attr(755,root,root) %{_libexecdir}/bamf/bamfdaemon-dbus-runner
%{_datadir}/dbus-1/services/org.ayatana.bamf.service
%{systemduserunitdir}/bamfdaemon.service
