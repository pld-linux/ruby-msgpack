#
# Conditional build:
%bcond_with	tests		# build without tests

%define pkgname msgpack
Summary:	MessagePack, a binary-based efficient data interchange format
Name:		ruby-%{pkgname}
Version:	1.0.0
Release:	2
License:	Apache v2.0
Group:		Development/Languages
Source0:	https://rubygems.org/gems/%{pkgname}-%{version}.gem
# Source0-md5:	cb36a1d48c87edc83158fca092145229
URL:		https://github.com/msgpack/msgpack-ruby
BuildRequires:	gmp-devel
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	ruby-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MessagePack is a binary-based efficient object serialization library.
It enables to exchange structured objects between many languages like
JSON. But unlike JSON, it is very fast and small.

%package doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{pkgname}-%{version}

rm -r spec/jruby

%build
# write .gemspec
%__gem_helper spec

# binary pkgs:
cd ext/%{pkgname}
%{__ruby} extconf.rb
%{__make} \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	CFLAGS="%{rpmcflags} -fPIC"
cd -

%if %{with tests}
rspec -Ilib -I$RPM_BUILD_ROOT%{gem_extdir_mri} spec
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_vendorarchdir}/%{pkgname},%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
install -p ext/%{pkgname}/*.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}/%{pkgname}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rdoc msgpack.org.md ChangeLog
%{ruby_vendorlibdir}/%{pkgname}.rb
%{ruby_vendorlibdir}/%{pkgname}
%dir %{ruby_vendorarchdir}/%{pkgname}
%attr(755,root,root) %{ruby_vendorarchdir}/%{pkgname}/%{pkgname}.so
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
