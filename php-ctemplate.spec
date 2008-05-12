%define modname cTemplate
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A49_%{modname}.ini

Summary:	A PHP extension for the Google ctemplate library
Name:		php-%{modname}
Version:	1.2
Release:	%mkrel 2
Group:		Development/PHP
License:	BSD
URL:		http://code.google.com/p/php-ctemplate/
Source0:	http://php-ctemplate.googlecode.com/files/%{modname}-%{version}.tar.bz2
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	ctemplate-devel
BuildRequires:	libstdc++-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
php_ctemplate is a PHP extension for the Google ctemplate library. Most
functions have been implemented (about 90%).

%prep

%setup -q -n %{modname}-%{version}

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

# nuke this
perl -pi -e "s|-Werror -Wall -g||g" config.m4

%build
%serverbuild

export CTEMPLATE_SHARED_LIBADD="-lpthread"

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS 
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
