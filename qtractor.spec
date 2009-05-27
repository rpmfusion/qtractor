Summary:       Audio/MIDI multi-track sequencer
Name:          qtractor
Version:       0.4.1
Release:       3%{?dist}
License:       GPLv2+
Group:         Applications/Multimedia
URL:           http://qtractor.sourceforge.net/
Source0:       http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:       http://downloads.sourceforge.net/%{name}/%{name}-0.3.0-user-manual.odt
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
cp -a %{SOURCE1} .
# Remove absolute paths from the desktop file:
sed -i 's|@ac_prefix@.*|%{name}|' %{name}.desktop.in

# Preserve timestamps:
sed -i 's|@install|install -p|' Makefile.in

%build
export PATH=${PATH}:%{_libdir}/qt4/bin
%configure 
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# move icon to freedesktop location
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
mv %{buildroot}%{_datadir}/pixmaps/%{name}.png \
   %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png

# install the desktop entry
RM_CAT="JACK ALSA MIDI"
ADD_CAT="X-Alsa X-Recorders X-Multitrack X-Jack X-MIDI Midi Sequencer"

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications    \
  `for c in ${RM_CAT} ; do echo "--remove-category $c " ; done` \
  `for c in ${ADD_CAT} ; do echo "--add-category $c " ; done` \
  %{name}.desktop  

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


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO *.odt
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png

%changelog
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
