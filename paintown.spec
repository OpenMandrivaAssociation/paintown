%define _disable_ld_no_undefined 1

Name:		paintown
Version:	3.5.0
Release:	3
Summary:	2D Fighting Game
Group:		Games/Arcade
License:	GPLv2
URL:		https://paintown.sourceforge.net/
Source0:	http://paintown.sourceforge.net/%{name}-%{version}.tar.gz
Patch0:		paintown-3.5.0-static.patch
Patch1:		paintown-3.5.0-libpng15.patch
BuildRequires:	cmake
BuildRequires:	python-devel
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	imagemagick

%description
Paintown is a 2D engine for fighting games.
If you are looking for a side-scrolling, action packed game like you used
to play or if you are looking for an extensible engine to write your own game,
look no further. Paintown supports user created content through a mod system
and user defined functionality through scripting.

Warning! The game is buggy and requires some "magic moves" to play.
For example, with some langauges half of menu is blank...

Features
* Low CPU and GPU requirements
* Network play
* Dynamic lighting
* Joystick support
* mod/s3m/xm/it music modules
* Scripting with python
* M.U.G.E.N engine


%prep
%setup -q
%patch0 -p1
%patch1 -p1

find data/ -type f -exec chmod 0644 {} \;

%build
LIBSUFFIX=$(echo "%{_lib}" | sed 's|^lib||')
export CFLAGS="%{optflags} -Wall"
export CXXFLAGS="$CFLAGS"

%cmake -DUSE_SDL=ON

%make

%install
mkdir -p %{buildroot}%{_gamesbindir}
install -m 755 build/bin/%{name} %{buildroot}%{_gamesbindir}/%{name}
mkdir -p %{buildroot}%{_gamesdatadir}/%{name}
cp -af data %{buildroot}%{_gamesdatadir}/%{name}

mkdir -p %{buildroot}%{_datadir}/pixmaps
install -m 644 data/menu/%{name}.png %{buildroot}%{_datadir}/pixmaps
convert data/menu/%{name}.png -resize 48x48 %{buildroot}%{_datadir}/pixmaps/%{name}.png

# wrapper script
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/sh
exec %{_gamesbindir}/paintown -d %{_gamesdatadir}/%{name}/data
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

#menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=PainTown
Comment=2D Fighting Game
Exec=%{name}
Icon=%{name}
Type=Application
Terminal=false
Categories=Game;ArcadeGame;
EOF

%files 
%doc README LEGAL LICENSE TODO scripting.txt
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_datadir}/pixmaps/%{name}.png



%changelog
* Wed Mar 14 2012 Andrey Bondrov <abondrov@mandriva.org> 3.5.0-1
+ Revision: 785025
- imported package paintown

