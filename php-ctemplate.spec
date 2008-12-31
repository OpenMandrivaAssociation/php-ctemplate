Summary:	A PHP extension for the Google ctemplate library
Name:		php-ctemplate
Version:	1.3
Release:	%mkrel 4
Group:		Development/PHP
License:	BSD
URL:		http://code.google.com/p/php-ctemplate/
Source0:	http://php-ctemplate.googlecode.com/files/cTemplate-%{version}.tar.bz2
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	ctemplate-devel >= 0.90
BuildRequires:	libstdc++-devel
Provides:	php-cTemplate = %{version}-%{release}
Obsoletes:	php-cTemplate
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
php_ctemplate is a PHP extension for the Google ctemplate library. Most
functions have been implemented (about 90%).

%prep

%setup -q -n cTemplate-%{version}

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

# nuke this
perl -pi -e "s|-Werror -Wall -g||g" config.m4

%build
%serverbuild

export CTEMPLATE_SHARED_LIBADD="-lpthread"

phpize
%configure2_5x \
    --with-libdir=%{_lib} \
    --with-cTemplate=shared,%{_prefix}
%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 cTemplate.so %{buildroot}%{_libdir}/php/extensions/ctemplate.so

cat > %{buildroot}%{_sysconfdir}/php.d/A49_ctemplate.ini << EOF
extension = ctemplate.so
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
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS 
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/*_ctemplate.ini
%attr(0755,root,root) %{_libdir}/php/extensions/ctemplate.so
