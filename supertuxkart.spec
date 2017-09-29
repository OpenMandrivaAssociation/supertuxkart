Summary:	Kart racing game
Name:		supertuxkart
Version:	0.9.2
Release:	2
License:	GPLv2+
Group:		Games/Arcade
Url:		http://supertuxkart.sourceforge.net/
Source0:	http://downloads.sourceforge.net/supertuxkart/%{name}-%{version}-src.tar.xz
Source100:	%{name}.rpmlintrc
Patch0:		supertuxkart-0.9-static.patch
Patch1:		supertuxkart-0.9-aarch64.patch
BuildRequires:	cmake
BuildRequires:	imagemagick
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(freealut)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fribidi)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libenet)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(zlib)

%description
SuperTuxKart is an improved version of TuxKart, a kart racing game
featuring Tux and friends. SuperTuxKart contains new characters, new
tracks and a reworked user interface.

%files
%doc AUTHORS CHANGELOG.md README.md TODO.md
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/appdata/supertuxkart.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}_*.png

#----------------------------------------------------------------------------

%prep
%setup -q
%apply_patches

%build
%cmake \
	-DSTK_INSTALL_BINARY_DIR=%{_gamesbindir} \
	-DSTK_INSTALL_DATA_DIR=%{_gamesdatadir}/%{name} \
	-DBUILD_SHARED_LIBS=OFF
%make

%install
%makeinstall_std -C build

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,64x64,128x128}/apps
convert -scale 16x16 data/%{name}_32.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert data/%{name}_32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 48x48 data/%{name}_128.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 64x64 data/%{name}_128.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
convert data/%{name}_128.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png

