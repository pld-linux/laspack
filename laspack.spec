Summary:	A package for solving large sparse systems of linear equations
Summary(pl):	Pakiet do rozwi±zywania du¿ych i rzadkich uk³adów równañ liniowych
Name:		laspack
Version:	1.12.2
Release:	1
License:	Freely distributable
Group:		Libraries
Source0:	http://www.netlib.org/linalg/%{name}.tgz
# Source0-md5:	fcfb3c86cc993e29eb477191b1136a8d
Patch0:		%{name}-automake_support.patch
URL:		http://www.tu-dresden.de/mwism/skalicky/laspack/laspack.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
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
LASPack is written in ANSI C and is thus largely portable.

%description -l pl
LASPack jest pakietem s³u¿±cym do rozwi±zywania du¿ych i rzadkich
uk³adów równañ liniowych. Podstawowym jego celem jest implementacja
wydajnych metod iteracyjnych.
Poza obligatoryjn± metod± Jacobiego, relaksacji, Czebyszewa i
gradientow±, LASPack zawiera wybrane nowoczesne algorytmy:
  - metody CG i podobne: CGN, GMRES, BiCG, QMR, CGS i BiCGStab,
  - metody wielopoziomowe takie jak multigrid i gradientowa, u¿ywane z
    preconditionerami typu multigrid i BPX.
LASPack zosta³ napisany w ANSI C, jest wiêc bardzo przeno¶ny.

%package devel
Summary:	LASPack development files
Summary(pl):	Pliki programistyczne LASPack
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
LASPack development files.

%description devel -l pl
Pliki programistyczne LASPack.

%package static
Summary:	Static LASPack library
Summary(pl):	Statyczna biblioteka LASPack
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LASPack library.

%description static -l pl
Statyczna biblioteka LASPack.

%package examples
Summary:	Example LASPack programs
Summary(pl):	Przyk³adowe programy korzystaj±ce z LASPack
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-xc-devel

%description examples
Example LASPack programs.

%description examples -l pl
Przyk³adowe programy korzystaj±ce z LASPack.

%package xc
Summary:	Extensions of C string handling and command line options
Summary(pl):	Rozszerzenia dla funkcji C dzia³aj±cych na opcjach linii poleceñ i ³añcuchach znaków
Group:		Libraries

%description xc
Extensions of C string handling and command line options.

%description xc -l pl
Rozszerzenia dla funkcji C dzia³aj±cych na opcjach linii poleceñ i
³añcuchach znaków.

%package xc-devel
Summary:	Development files for xc extensions
Summary(pl):	Pliki programistyczne dla rozszerzeñ xc
Group:		Development/Libraries
Requires:	%{name}-xc = %{version}-%{release}

%description xc-devel
Development files for xc extensions.

%description xc-devel -l pl
Pliki programistyczne dla rozszerzeñ xc.

%package xc-static
Summary:	Static xc extensions library
Summary(pl):	Biblioteka statyczna z rozszerzeniami xc
Group:		Development/Libraries
Requires:	%{name}-xc-devel = %{version}-%{release}

%description xc-static
Static xc extensions library.

%description xc-static -l pl
Biblioteka statyczna z rozszerzeniami xc.

%prep
%setup -q -c LASPACK
%patch -p1

%build
cd laspack
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure

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

cd laspack
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
cd ../xc
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -fr $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%post xc -p /sbin/ldconfig
%postun xc -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc readme
%attr(755,root,root) %{_libdir}/liblaspack.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblaspack.so
%doc laspack/doc/ laspack/html/
%{_libdir}/liblaspack.la
%{_includedir}/laspack/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/liblaspack.a

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}/*

%files xc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxc.so.*.*.*

%files xc-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxc.so
%{_includedir}/xc/*.h

%files xc-static
%defattr(644,root,root,755)
%{_libdir}/libxc.a
