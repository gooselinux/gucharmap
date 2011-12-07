%define glib2_version 2.3.0
%define gtk2_version 2.6.0
%define desktop_file_utils_version 0.9

Name:           gucharmap
Version:        2.28.2
Release:        2%{?dist}
Summary:        Unicode character picker and font browser

Group:          Applications/System
License:        GPLv2+ and GFDL and MIT
# GPL for the source code, GFDL for the docs, MIT for Unicode data
URL:            http://live.gnome.org/Gucharmap
Source:         http://download.gnome.org/sources/gucharmap/2.28/gucharmap-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# update translations
# https://bugzilla.redhat.com/show_bug.cgi?id=575694
Patch0: gucharmap-translations.patch

BuildRequires: gnome-doc-utils >= 0.3.2
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: GConf2-devel
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: scrollkeeper
BuildRequires: gettext
BuildRequires: intltool

Requires(post):scrollkeeper
Requires(post): desktop-file-utils >= %{desktop_file_utils_version}
Requires(postun): scrollkeeper
Requires(postun): desktop-file-utils >= %{desktop_file_utils_version}

%description
This program allows you to browse through all the available Unicode
characters and categories for the installed fonts, and to examine their
detailed properties. It is an easy way to find the character you might
only know by its Unicode name or code point.

%package devel
Summary: Libraries and headers for libgucharmap
Group: Development/Libraries
Requires: glib2-devel >= %{glib2_version}
Requires: gtk2-devel >= %{gtk2_version}
Requires: gucharmap = %{version}-%{release}
Requires: pkgconfig

%description devel
The gucharmap-devel package contains header files and other resources
needed to use the libgucharmap library.

%prep
%setup -q
%patch0 -p1 -b .translations

%build
%configure --disable-gtk-immodules --disable-scrollkeeper
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT RUN_QUERY_IMMODULES_TEST=false

rm $RPM_BUILD_ROOT/%{_libdir}/*.la

sed -i -e "s#Icon=gucharmap.png#Icon=/usr/share/icons/hicolor/48x48/apps/gucharmap.png#" \
  $RPM_BUILD_ROOT%{_datadir}/applications/gucharmap.desktop

desktop-file-install --vendor gnome --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  $RPM_BUILD_ROOT%{_datadir}/applications/*

# save space by linking identical images in translated docs
helpdir=$RPM_BUILD_ROOT%{_datadir}/gnome/help/%{name}
for f in $helpdir/C/figures/*.png; do
  b="$(basename $f)"
  for d in $helpdir/*; do
    if [ -d "$d" -a "$d" != "$helpdir/C" ]; then
      g="$d/figures/$b"
      if [ -f "$g" ]; then
        if cmp -s $f $g; then
          rm "$g"; ln -s "../../C/figures/$b" "$g"
        fi
      fi
    fi
  done
done


%find_lang gucharmap --with-gnome


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig
scrollkeeper-update -q
update-desktop-database -q
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/gucharmap.schemas > /dev/null || :

%postun
/sbin/ldconfig
scrollkeeper-update -q
update-desktop-database -q
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%pre
if [ "$1" -gt 1 -a -f %{_sysconfdir}/gconf/schemas/gucharmap.schemas ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gucharmap.schemas > /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gucharmap.schemas > /dev/null || :
fi

%files -f gucharmap.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_bindir}/charmap
%{_bindir}/gucharmap
%{_bindir}/gnome-character-map
%{_libdir}/libgucharmap.so.*
%{_datadir}/applications/gnome-gucharmap.desktop
%{_sysconfdir}/gconf/schemas/gucharmap.schemas


%files devel
%defattr(-,root,root,-)
%{_includedir}/gucharmap-2
%{_libdir}/libgucharmap.so
%{_libdir}/pkgconfig/gucharmap-2.pc


%changelog
* Wed May  5 2010 Matthias Clasen <mclasen@redhat.com> - 2.28.2-2
- Update translations
Resolves: #575694

* Mon Jan  4 2010 Matthias Clasen <mclasen@redhat.com> - 2.28.2-1
- Update to 2.28.2

* Mon Oct 19 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.1-1
- Update to 2.28.1

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.3.1-2
- Fix some stubborn button images

* Sun Jul 12 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.3.1-1
- Update to 2.26.3.1

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Thu Jan 15 2009 Matthias Clasen <mclasen@redhat.com> - 2.24.3-1
- Update to 2.24.3

* Mon Oct 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Wed Oct  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Save some space

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Mon Aug  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.6-1
- Update to 2.23.6

* Tue Jul 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.23.4-2
- fix license tag

* Tue Jun 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Sun Mar  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Wed Jan 30 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Tue Jan 15 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.5-1
- Update to 2.21.5

* Tue Dec 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.4-1
- Update to 2.21.4

* Thu Dec  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.3-1
- Update to 2.21.3

* Tue Sep 18 2007 Matthias Clasen <mclasen@redhat.com> - 1.10.1-1
- Update to 1.10.1

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 1.10.0-2
- Update license field
- Use %%find_lang for help files

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 1.10.0-1
- Update to 1.10.0

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 1.8.0-1
- Update to 1.8.0
- Require pgkconfig for the -devel package

* Thu Aug 02 2006 Matthias Clasen <mclasen@redhat.com> 
- Rebuild 

* Wed Aug 02 2006 Behdad Esfahbod <besfahbo@redhat.com> - 1.7.0-1
- Update to 1.7.0

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.6.0-8.1
- rebuild

* Fri Jun  9 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-8
- Add missing BuildRequires

* Fri Jun  2 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-7
- Rebuild

* Tue Apr 18 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-6
- Make -devel require the exact n-v-r

* Tue Apr 18 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-5
- incorporate more package review feedback

* Mon Apr 17 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-4
- split off a -devel package

* Mon Apr 17 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-3
- fix issues pointed out in package review

* Tue Apr 11 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-2
- Initial revision
