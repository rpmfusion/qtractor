%ifarch %{ix86}
%global without_sse %{!?_without_sse:0}%{?_without_sse:1}
%endif
%ifarch ia64 x86_64
%global without_sse 0
%endif
%ifnarch %{ix86} ia64 x86_64
%global without_sse 1
%endif

Summary:       Audio/MIDI multi-track sequencer
Name:          qtractor
Version:       0.5.1
Release:       2%{?dist}
License:       GPLv2+
Group:         Applications/Multimedia
URL:           http://qtractor.sourceforge.net/
Source0:       http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: alsa-lib-devel
BuildRequires: desktop-file-utils
BuildRequires: dssi-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: ladspa-devel
BuildRequires: liblo-devel
BuildRequires: libmad-devel
BuildRequires: libsamplerate-devel
BuildRequires: libsndfile-devel
BuildRequires: libvorbis-devel
BuildRequires: qt-devel
BuildRequires: rubberband-devel
BuildRequires: slv2-devel

Requires:      hicolor-icon-theme

%description
Qtractor is an Audio/MIDI multi-track sequencer application written in C++ 
around the Qt4 toolkit using Qt Designer. The initial target platform will be
Linux, where the Jack Audio Connection Kit (JACK) for audio, and the Advanced
Linux Sound Architecture (ALSA) for MIDI, are the main infrastructures to 
evolve as a fairly-featured Linux Desktop Audio Workstation GUI, specially 
dedicated to the personal home-studio.

%prep
%setup -q

# Fix odd permissions
chmod -x src/qtractorMmcEvent.*

%build
export PATH=${PATH}:%{_libdir}/qt4/bin
%configure \
%if %{without_sse}
   --enable-sse=no
%endif

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%find_lang %{name} --with-qt

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%clean
rm -rf %{buildroot}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png


%changelog
* Thu Nov 03 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.5.1-2
- Rebuild for dist F-16

* Sat Oct 08 2011 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.5.1-1
- Update to 0.5.1

* Sat Jul 30 2011 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.5.0-1
- Update to 0.5.0

* Thu May 26 2011 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.4.9-1
- Update to 0.4.9

* Tue Jan 18 2011 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.4.8-1
- Update to 0.4.8

* Sat Oct 02 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.4.7-1
- Update to 0.4.7

* Sat Aug 21 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.4.6-4
- rebuilt

* Sun Aug 08 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.4.6-3
- Rebuild against new liblo-0.26 on F-14 again

* Tue Jul 20 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.4.6-2
- Rebuild against new liblo-0.26 on F-14

* Sun May 23 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.4.6-1
- Update to 0.4.6
- Drop upstreamed .desktop file modifications
- Drop old documentation

* Sun May 16 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.4.6-0.1.1568svn1565
- Update to 0.4.6 rc (svn1565)

* Sat Jan 30 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.4.5-1
- updated to 0.4.5.

* Fri Oct 23 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.4.3-1
- updated to 0.4.3.

* Fri Jun 05 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.4.2-1
- updated to 0.4.2.

* Wed May 27 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.4.1-4
- Explicitly disable SSE optimizations on non-"%%{ix86} ia64 x86_64" architectures

* Fri May 22 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.4.1-3
- preserve timestamps

* Thu May 21 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.4.1-2
- ship odt documentation instead of the pdf

* Sat Apr  4 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.4.1-1
- updated to 0.4.1.

* Tue Mar 24 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.4.0-1
- updated to 0.4.0.

* Fri Feb 20 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.3.0-1
- updated to 0.3.0. SPEC file adapted from PlanetCCRMA.

* Mon Oct  6 2008 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> - 0.2.2-1
- updated to 0.2.2

* Tue Sep 23 2008 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> - 0.2.1-1
- updated to 0.2.1

* Thu Jun 19 2008 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> - 0.1.3-1
- added patch for gcc43 build on fc9 (from gentoo).

* Fri May  2 2008 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> - 0.1.3-1
-  initial build
- x86_64 build needs an explicit path for the qmake binary to be found
