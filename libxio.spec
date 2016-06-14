#
# spec file for package libxio
#
# Copyright (c) 2016 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%bcond_with devel_mode
%bcond_with kmod
%define debug_package %{nil}

Name:    libxio
Version: 1.6
Release: 2%{?dist}
Summary: Open Source I/O, Message, and RPC Acceleration Library
Group:   Productivity/Networking/System
License: GPL-2.0
Url:     http://www.accelio.org/
Source:  accelio-%{version}.tar.xz
ExclusiveArch: x86_64 aarch64

BuildRequires: autoconf, libtool
%if 0%{?fedora} || 0%{?rhel}
BuildRequires: numactl-devel
%endif
%if 0%{?suse_version}
BuildRequires: libnuma-devel
%endif
BuildRequires: libaio-devel
BuildRequires: libibverbs-devel
BuildRequires: librdmacm-devel
%if %{with kmod}
BuildRequires: kernel-devel
%endif

%description
Accelio (libxio) provides an easy-to-use, reliable, scalable,
and high performance data/message delivery middleware
that maximizes the efficiency of modern CPU and NIC hardware
and that reduces time-to-market of new scale-out applications.

This package contains the shared libraries.


%package devel
Summary: Development files for the libxio library
Group: Development/Libraries/C and C++
Requires: %{name} = %{version}-%{release} 
Requires: libibverbs-devel%{?_isa}
Requires: librdmacm-devel%{?_isa}

%description devel
Accelio (libxio) provides an easy-to-use, reliable, scalable,
and high performance data/message delivery middleware
that maximizes the efficiency of modern CPU and NIC hardware
and that reduces time-to-market of new scale-out applications.

This package contains development files for the libxio library.

%if 0%{with kmod}
%package kmod
Summary: Accelio Kernel Modules

%description kmod
Accelio (libxio) provides an easy-to-use, reliable, scalable,
and high performance data/message delivery middleware
that maximizes the efficiency of modern CPU and NIC hardware
and that reduces time-to-market of new scale-out applications.

This package contains the Accelio Kernel Modules.
%endif


%prep
%setup -q -n accelio-%{version}

%build
./autogen.sh

%configure \
	--disable-static \
%if 0%{with kmod}
	--enable-kernel-module \
%endif
%if 0%{without devel_mode}
	--enable-stat-counters=no \
	--enable-extra-checks=no \
%endif

make %{?_smp_mflags}


%install
make DESTDIR=%{buildroot} install

# remove unpackaged files from the buildroot
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%files
%defattr(-,root,root,-)
%if 0%{without kmod}
%{_bindir}/*
%{_libdir}/libxio.so*
%{_libdir}/libraio.so*
%endif
%exclude /usr/src/debug/*
%doc AUTHORS COPYING README

%files devel
%defattr(-,root,root,-)
%if 0%{with kmod}
/opt/*
%else
%{_includedir}/*
%exclude /usr/src/debug/*
%endif

%if 0%{with kmod}
%files kmod
%defattr(-,root,root,-)
/lib/modules/*
%exclude /usr/src/debug/*
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%if 0%{with kmod}
%post kmod
depmod -a

%postun kmod
depmod -a
%endif


%changelog
* Fri Jan 15 2016 Vladislav Odintsov <odivlad@gmail.com> 1.6-2
- Added devel mode build (enabled perfcounters and extra checks)
- Added support for kernel module build

* Tue Nov 17 2015 Mikhail Ushanov <gm.mephisto@gmail.com> 1.6-1
- Bump version accelio to 1.6

* Tue Nov 17 2015 Mikhail Ushanov <gm.mephisto@gmail.com> 1.5-1
- Initial spec file
