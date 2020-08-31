%ifarch %{ix86}
%define _disable_ld_no_undefined 1
%define _disable_lto 1
%endif

%define tarname SuperTuxKart

Summary:	Kart racing game
Name:		supertuxkart
Version:	1.2
Release:	1
License:	GPLv2+
Group:		Games/Arcade
Url:		http://supertuxkart.sourceforge.net/
Source0:	http://downloads.sourceforge.net/supertuxkart/%{tarname}-%{version}-src.tar.xz
Source100:	%{name}.rpmlintrc

BuildRequires:	cmake
BuildRequires:	imagemagick
BuildRequires:	jpeg-devel
BuildRequires:  mcpp-devel
BuildRequires:	pkgconfig(bluez)
BuildRequires:  pkgconfig(egl)
BuildRequires:	pkgconfig(freealut)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fribidi)
BuildRequires:	pkgconfig(gl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glew)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libenet)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(openssl)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(zlib)
#BuildRequires:	glesv3-devel
BuildRequires:  wiiuse-devel
BuildRequires:  pkgconfig(sqlite3)

# dirty fix for now...
Requires:	wiiuse-devel

%description
SuperTuxKart is an improved version of TuxKart, a kart racing game
featuring Tux and friends. SuperTuxKart contains new characters, new
tracks and a reworked user interface.

%files
%doc CHANGELOG.md README.md
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/metainfo/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png


#----------------------------------------------------------------------------

%prep
%setup -qn %{tarname}-%{version}-src
%autopatch -p1

# remove bundled library, use system instead.
rm -rf lib/{glew,jpeglib,libpng,wiiuse,zlib}


%build
%ifarch %{ix86}
export CC=gcc
export CXX=g++
%endif
%cmake \
	-DBUILD_RECORDER:BOOL=OFF \
	-DSTK_INSTALL_BINARY_DIR=%{_gamesbindir} \
	-DSTK_INSTALL_DATA_DIR=%{_gamesdatadir}/%{name} \
	-DBUILD_SHARED_LIBS=OFF \
	-DUSE_SYSTEM_ENET=OFF \
        -DUSE_SYSTEM_GLEW=ON \
	-DUSE_SYSTEM_WIIUSE=ON \
	-DOpenGL_GL_PREFERENCE=GLVND
	
%make_build

%install
%make_install -C build

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,64x64,128x128}/apps
convert -scale 16x16 data/%{name}_48.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert -scale 32x32 data/%{name}_128.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
cp data/%{name}_48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 64x64 data/%{name}_128.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
cp data/%{name}_128.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png
