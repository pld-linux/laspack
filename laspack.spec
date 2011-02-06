#
# Conditional build:
%bcond_with	blas	# with ACML interface to BLAS instead of direct vector operations
#
Summary:	A package for solving large sparse systems of linear equations
Summary(pl.UTF-8):	Pakiet do rozwiązywania dużych, rzadkich układów równań liniowych
Name:		laspack
Version:	1.12.2
Release:	5%{?with_blas:BLAS}
License:	Freely distributable
Group:		Libraries
Source0:	http://www.netlib.org/linalg/%{name}.tgz
# Source0-md5:	fcfb3c86cc993e29eb477191b1136a8d
Source1:	%{name}-README.PLD
Patch0:		%{name}-automake_support.patch
Patch1:		%{name}-include.patch
Patch2:		%{name}-blas.patch
URL:		http://www.tu-dresden.de/mwism/skalicky/laspack/laspack.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%if %{with blas}
# ACML exists for AMD 64-bit CPU's only
ExclusiveArch:	%{x8664}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LASPack is a package for solving large sparse systems of linear
equations like those which arise from discretization of partial
differential equations. The primary aim of LASPack is the implementation
of efficient iterative methods for the solution of systems of linear
equations. 
Beside the obligatory Jacobi, succesive over-relaxation,
Chebyshev, and conjugate gradient solvers, LASPack contains selected
state-of-the-art algorithms which are commonly used for large sparse
systems:
  - CG-like methods for non-symmetric systems: CGN, GMRES, BiCG, QMR,
    CGS, and BiCGStab,
  - multilevel methods such as multigrid and conjugate gradient method
    preconditioned by multigrid and BPX preconditioners.
These algorithms are described in
http://www.netlib.org/linalg/html_templates/Templates.html 
LASPack is written in ANSI C and is thus largely portable.

%description -l pl.UTF-8
LASPack jest pakietem służącym do rozwiązywania dużych, rzadkich
układów równań liniowych. Podstawowym jego celem jest implementacja
wydajnych metod iteracyjnych.
Poza obligatoryjną metodą Jacobiego, relaksacji, Czebyszewa i
gradientową, LASPack zawiera wybrane nowoczesne algorytmy:
  - metody CG i podobne: CGN, GMRES, BiCG, QMR, CGS i BiCGStab,
  - metody wielopoziomowe takie jak multigrid i gradientowa, używane z
    preconditionerami typu multigrid i BPX.
Wymienione wyżej algorytmy zostały opisane w
http://www.netlib.org/linalg/html_templates/Templates.html
LASPack został napisany w ANSI C, jest więc bardzo przenośny.

%package devel
Summary:	LASPack development files
Summary(pl.UTF-8):	Pliki programistyczne LASPack
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
LASPack development files.

%description devel -l pl.UTF-8
Pliki programistyczne LASPack.

%package static
Summary:	Static LASPack library
Summary(pl.UTF-8):	Statyczna biblioteka LASPack
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LASPack library.

%description static -l pl.UTF-8
Statyczna biblioteka LASPack.

%package examples
Summary:	Example LASPack programs
Summary(pl.UTF-8):	Przykładowe programy korzystające z LASPack
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-xc-devel

%description examples
Example LASPack programs.

%description examples -l pl.UTF-8
Przykładowe programy korzystające z LASPack.

%package xc
Summary:	Extensions of C string handling and command line options
Summary(pl.UTF-8):	Rozszerzenia dla funkcji C działających na opcjach linii poleceń i łańcuchach znaków
Group:		Libraries

%description xc
Extensions of C string handling and command line options.

%description xc -l pl.UTF-8
Rozszerzenia dla funkcji C działających na opcjach linii poleceń i
łańcuchach znaków.

%package xc-devel
Summary:	Development files for xc extensions
Summary(pl.UTF-8):	Pliki programistyczne dla rozszerzeń xc
Group:		Development/Libraries
Requires:	%{name}-xc = %{version}-%{release}

%description xc-devel
Development files for xc extensions.

%description xc-devel -l pl.UTF-8
Pliki programistyczne dla rozszerzeń xc.

%package xc-static
Summary:	Static xc extensions library
Summary(pl.UTF-8):	Biblioteka statyczna z rozszerzeniami xc
Group:		Development/Libraries
Requires:	%{name}-xc-devel = %{version}-%{release}

%description xc-static
Static xc extensions library.

%description xc-static -l pl.UTF-8
Biblioteka statyczna z rozszerzeniami xc.

%prep
%setup -q -c LASPACK
%patch0 -p1
%patch1 -p1
%if %{with blas}
%patch2 -p1
%endif

cp %{SOURCE1} README.PLD

%build
cd laspack
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	%{?with_blas: LDFLAGS="-lg2c -lacml -lm"}

%{__make}

cd ../xc
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C laspack install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C xc install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	xc -p /sbin/ldconfig
%postun	xc -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc readme README.PLD
%attr(755,root,root) %{_libdir}/liblaspack.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblaspack.so
%doc laspack/doc/ laspack/html/
%{_libdir}/liblaspack.la
%{_includedir}/laspack

%files static
%defattr(644,root,root,755)
%{_libdir}/liblaspack.a

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%files xc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxc.so.*.*.*

%files xc-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxc.so
%{_libdir}/libxc.la
%{_includedir}/xc

%files xc-static
%defattr(644,root,root,755)
%{_libdir}/libxc.a
