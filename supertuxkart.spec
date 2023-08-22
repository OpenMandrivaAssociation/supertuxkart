%ifarch %{ix86}
%define _disable_ld_no_undefined 1
%define _disable_lto 1
%endif

%define tarname SuperTuxKart

Summary:	Kart racing game
Name:		supertuxkart
Version:	1.4
Release:	4
License:	GPLv2+
Group:		Games/Arcade
Url:		http://supertuxkart.sourceforge.net/
Source0:	http://downloads.sourceforge.net/supertuxkart/%{tarname}-%{version}-src.tar.xz
Source100:	%{name}.rpmlintrc
Patch0:		https://github.com/supertuxkart/stk-code/commit/0c2b81ac1f9ff29f5012a98f530880b87f416337.patch
Patch1:		supertuxkart-1.4-compile.patch
BuildRequires:	cmake
BuildRequires:	imagemagick
BuildRequires:	mcpp-devel
BuildRequires:	astc-encoder-devel
BuildRequires:	libsquish-devel
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(freealut)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glesv2)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libenet)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-cursor)
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	angelscript-devel
#BuildRequires:	glesv3-devel
BuildRequires:	wiiuse-devel
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(shaderc)

%description
SuperTuxKart is an improved version of TuxKart, a kart racing game
featuring Tux and friends. SuperTuxKart contains new characters, new
tracks and a reworked user interface.

%files
%doc CHANGELOG.md README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/metainfo/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
#{_datadir}/pixmaps/%{name}.png

#----------------------------------------------------------------------------

%prep
%autosetup -n %{tarname}-%{version}-src -p1

# remove bundled library, use system instead.
rm -rf lib/{jpeglib,libpng,wiiuse,zlib,libsquish,mcpp,angelscript,shaderc}

%build
# Switch to GCC because as of Clang 15.X and SuperTuxKart 1.4, game compiled with clang crashing at launch (after splash screen). GCC fix it.
#export CC=gcc
#export CXX=g++
export LDFLAGS="%{build_ldflags} -lcurl"

%cmake \
	-DBUILD_RECORDER:BOOL=OFF \
	-DSTK_INSTALL_BINARY_DIR=%{_bindir} \
	-DSTK_INSTALL_DATA_DIR=%{_datadir}/%{name} \
	-DBUILD_SHARED_LIBS=OFF \
	-DUSE_SYSTEM_ENET=OFF \
	-DUSE_SYSTEM_WIIUSE=ON \
	-DUSE_SYSTEM_ANGELSCRIPT=ON \
	-DUSE_SYSTEM_SQUISH=ON \
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
