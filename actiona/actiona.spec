Name:       actiona
Summary:    Cross-platform automation tool
License:    GPLv3
Version: 3.9.1
Release:    1%{?dist}
Url:        https://actiona.tools
Source0:    %{name}-%{version}.tar.gz

BuildRequires: desktop-file-utils
BuildRequires: gcc-c++
BuildRequires: qt5-qttools-devel
BuildRequires: boost-devel
BuildRequires: pkgconfig(Qt5Core) >= 5.2.0
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5XmlPatterns)
BuildRequires: pkgconfig(Qt5X11Extras)
BuildRequires: pkgconfig(Qt5Script)
BuildRequires: pkgconfig(Qt5Multimedia)
BuildRequires: pkgconfig(Qt5UiTools)
BuildRequires: pkgconfig(xtst)
BuildRequires: pkgconfig(libnotify)
BuildRequires: pkgconfig(opencv)


%description
Actiona is an application that allows you to execute many actions on your
computer such as emulating mouse clicks, key presses, showing message boxes,
editing text files, etc.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup


%build
%{_qt5_qmake} actiona.pro \
    PREFIX=%{_prefix} LIBDIR=%{_lib} \
    lupdate=lupdate-qt5 lrelease=lrelease-qt5
make %{?_smp_mflags} locale_release


%install
%make_install INSTALL_ROOT=%{buildroot}
%find_lang %{name} --with-qt --without-mo --all-name
desktop-file-validate %{buildroot}/%{_datadir}/applications/*.desktop


%post
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/mime/packages &> /dev/null || :


%postun
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/mime/packages &> /dev/null || :
    update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi


%posttrans
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :


%files -f %{name}.lang
%doc README CHANGELOG
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/actexec
%{_libdir}/actiona/actions/*
%{_libdir}/actiona/*.so.*
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/actexec.1*
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml


%files devel
%{_libdir}/actiona/*.so


%changelog

