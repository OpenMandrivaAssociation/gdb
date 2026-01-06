# WARNING: This package is synced with FC
# Extract OpenMandriva Linux name and version
%define distro_version %(perl -ne '/^([.\\w\\s]+) \\(.+\\).+/ and print $1' < /etc/release)

%define Werror_cflags %nil

%define rpmsover $(ls %{_libdir}/librpm.so.[0-9]* |head -n1 |cut -d. -f3)

# rpmbuild parameters:
# --with testsuite: Run the testsuite (biarch if possible).  Default is without.
# --with asan: gcc -fsanitize=address
# --without python: No python support.
# --with profile: gcc -fprofile-generate / -fprofile-use: Before better
#                 workload gets run it decreases the general performance now.
# --define 'scl somepkgname': Independent packages by scl-utils-build.
# --without rpm: Don't build rpm support (for aarch64 bootstrap)

%bcond_without rpm
%bcond_with testsuite
%bcond_without python
%bcond_with babeltrace
%bcond_with pdf
%bcond_with guile

%{?scl:%scl_package gdb}
%{!?scl:
 %global pkg_name %{name}
 %global _root_prefix %{_prefix}
 %global _root_datadir %{_datadir}
 %global _root_libdir %{_libdir}
}

Name: %{?scl_prefix}gdb

%global tarname gdb-%{version}
Version:	17.1
%global gdb_version %{version}

# The release always contains a leading reserved number, start it at 1.
# `upstream' is not a part of `name' to stay fully rpm dependencies compatible for the testing.
Release:	2
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ and GPLv2+ with exceptions and GPL+ and LGPLv2+ and LGPLv3+ and BSD and Public Domain and GFDL
Group:   Development/Tools
# Do not provide URL for snapshots as the file lasts there only for 2 days.
# ftp://sourceware.org/pub/gdb/releases/FIXME{tarname}.tar.xz
Source0: https://sourceware.org/pub/gdb/releases/%{tarname}.tar.xz
URL: https://gnu.org/software/gdb/

# For our convenience
%global gdb_src %{tarname}
%global gdb_build build-%{_target_platform}

Conflicts: gdb-headless < 7.12-29

Summary: A stub package for GNU source-level debugger
Requires: gdb-headless = %{version}-%{release}

%patchlist
# From fedora
https://src.fedoraproject.org/rpms/gdb/raw/rawhide/f/gdb-test-show-version.patch
https://src.fedoraproject.org/rpms/gdb/raw/rawhide/f/gdb-add-index.patch
https://src.fedoraproject.org/rpms/gdb/raw/rawhide/f/gdb-rpm-suggestion-script.patch

# OM only patches
gdb-12.1-readline-8.2.patch

%description
'gdb' package is only a stub to install gcc-gdb-plugin for 'compile' commands.
See package 'gdb-headless'.

%package headless
Summary: A GNU source-level debugger for C, C++, Fortran, Go and other languages
Group:   Development/Tools

%ifarch %{arm} riscv64
%global have_inproctrace 0
%else
%global have_inproctrace 1
%endif

# eu-strip: -g recognizes .gdb_index as a debugging section. (#631997)
Conflicts: elfutils < 0.149

# GDB patches have the format `gdb-<version>-bz<red-hat-bz-#>-<desc>.patch'.
# They should be created using patch level 1: diff -up ./gdb (or gdb-6.3/gdb).

#=
#push=Should be pushed upstream.
#fedora=Should stay as a Fedora patch.
#fedoratest=Keep it in Fedora only as a regression test safety.

# Cleanup any leftover testsuite processes as it may stuck mock(1) builds.
#=push+jan
Source2: gdb-orphanripper.c

# /etc/gdbinit (from Debian but with Fedora compliant location).
#=fedora
Source4: gdbinit

Source1001: gdb.rpmlintrc

# OMV specific
# NEEDS REBASE Patch2000: gdb-8.1-guile-2.2.patch
# NEEDS REBASE Patch2001: gdb-9.2-guile-3.0.patch

# RISC-V support patches from https://github.com/riscv/riscv-binutils-gdb
# (currently in sync with gdb git)

BuildRequires: readline-devel >= 6.2-4
BuildRequires: ncurses-devel texinfo gettext flex bison
BuildRequires: pkgconfig(expat)
BuildRequires: pkgconfig(liblzma)
%if %{with rpm}
# dlopen() no longer makes rpm-libsFIXME{?_isa} (it's .so) a mandatory dependency.
BuildRequires: pkgconfig(rpm) >= 4.14.0-0
%endif
BuildRequires:   pkgconfig(python3)
Requires:   python >= 3
%if %{with pdf}
# gdb-doc in PDF, see: https://bugzilla.redhat.com/show_bug.cgi?id=919891#c10
BuildRequires:   texlive
%endif
%if %{with babeltrace}
BuildRequires: libbabeltrace-devel
%endif
%if %{with guile}
BuildRequires: pkgconfig(guile-3.0)
%endif
%global have_libipt 0
%ifarch %{ix86} x86_64
#global have_libipt 1
#BuildRequires: libipt-devel
%endif
BuildRequires: make
BuildRequires: sharutils
BuildRequires: dejagnu
# gcc-objc++ is not covered by the GDB testsuite.
BuildRequires: gcc 
BuildRequires: gcc-c++ 
%if %{with testsuite}
BuildRequires: gcc-gfortran 
BuildRequires: gcc-objc
BuildRequires: rust
BuildRequires: fpc
%ifnarch armv5tl
BuildRequires: rust
%endif
%endif
BuildRequires: gcc-plugin-devel
BuildRequires: pkgconfig(zlib)
BuildRequires: dbginfod
BuildRequires: elfutils-devel

%description headless
GDB, the GNU debugger, allows you to debug programs written in C, C++,
Java, and other languages, by executing them in a controlled fashion
and printing their data.

%package gdbserver
Summary: A standalone server for GDB (the GNU source-level debugger)
Group:   Development/Tools
Conflicts: gdb <= 7.12-16.mga6

%description gdbserver
GDB, the GNU debugger, allows you to debug programs written in C, C++,
Java, and other languages, by executing them in a controlled fashion
and printing their data.

This package provides a program that allows you to run GDB on a different
machine than the one which is running the program being debugged.

%package doc
Summary: Documentation for GDB (the GNU source-level debugger)
License: GFDL
Group: Documentation
BuildArch: noarch
Conflicts: gdb < 7.11-5.mga6

%description doc
GDB, the GNU debugger, allows you to debug programs written in C, C++,
Java, and other languages, by executing them in a controlled fashion
and printing their data.

This package provides INFO, HTML and PDF user manual for GDB.


%prep
%autosetup -p1 -n %{gdb_src}

# Files have `# <number> <file>' statements breaking VPATH / find-debuginfo.sh .
(cd gdb;rm -fv $(perl -pe 's/\\\n/ /' <Makefile.in|sed -n 's/^YYFILES = //p'))

# *.info* is needlessly split in the distro tar; also it would not get used as
# we build in %{gdb_build}, just to be sure.
find -name "*.info*"|xargs rm -f

find -name "*.orig" -o -name "*~" | xargs rm -f
! find -name "*.rej" # Should not happen.

# Change the version that gets printed at GDB startup, so it is RH specific.
cat > gdb/version.in << _FOO
%{gdb_version}-%{release} (%{distro_version})
_FOO

# Remove the info and other generated files added by the FSF release
# process.
rm -f libdecnumber/gstdint.h
rm -f bfd/doc/*.info
rm -f bfd/doc/*.info-*
rm -f gdb/doc/*.info
rm -f gdb/doc/*.info-*

rm -rf zlib

%build

# Identify the build directory with the version of gdb as well as the
# architecture, to allow for mutliple versions to be installed and
# built.
# Initially we're in the %{gdb_src} directory.

for fprofile in %{?_with_profile:-fprofile} ""
do

mkdir %{gdb_build}$fprofile
cd %{gdb_build}$fprofile

export CFLAGS="$RPM_OPT_FLAGS %{?_with_asan:-fsanitize=address}"
export LDFLAGS="%{?__global_ldflags} %{?_with_asan:-fsanitize=address}"

CFLAGS="$CFLAGS -DDNF_DEBUGINFO_INSTALL"

%if 0%{?el6:1} && 0%{?scl:1}
CFLAGS="$CFLAGS -DGDB_INDEX_VERIFY_VENDOR"
%endif

# Cross compilation with python support is ****ed up because we
# get compiler flags from HOST python, potentially including
# things like -march=...
# So let's fake it -- --with-python=... is used only to launch
# python-config.py, so something stupid that just dumps the
# right answers is sufficient
%if %{cross_compiling}
cat >fakepython <<'EOF'
#!/bin/sh
case $2 in
--exec-prefix)
	echo %{_prefix}
	;;
--ldflags)
	echo -lpython%{pyver}
	;;
--includes)
	echo -I%{_includedir}/python%{pyver}
	;;
esac
EOF
chmod +x fakepython
%endif


# --htmldir and --pdfdir are not used as they are used from %{gdb_build}.
if ! ../configure							\
	--prefix=%{_prefix}					\
	--libdir=%{_libdir}					\
	--sysconfdir=%{_sysconfdir}				\
	--mandir=%{_mandir}					\
	--infodir=%{_infodir}					\
%if %{cross_compiling}
	--build=%{_build}					\
	--host=%{_target_platform}				\
	--target=%{_target_platform}				\
	--with-libgmp-prefix=%{_prefix}/%{_target_platform}	\
	--with-liblzma-prefix=%{_prefix}/%{_target_platform}	\
%endif
	--with-system-gdbinit=%{_sysconfdir}/gdbinit		\
	--with-gdb-datadir=%{_datadir}/gdb			\
	--with-debuginfod					\
	--enable-gdb-build-warnings=,-Wno-unused		\
	--enable-build-with-cxx					\
	--disable-werror					\
	--with-separate-debug-dir=/usr/lib/debug		\
 	--disable-sim						\
	--disable-rpath						\
%if %{with babeltrace}
	--with-babeltrace					\
%endif
%if %{with guile}
	--with-guile						\
%else
	--without-guile						\
%endif
	--with-system-readline				\
	--with-expat						\
$(: ppc64 host build crashes on ppc variant of libexpat.so )	\
	--without-libexpat-prefix				\
	--enable-tui						\
%if %{with python}
%if %{cross_compiling}
	--with-python=$(pwd)/fakepython				\
%else
	--with-python						\
%endif
%else
	--without-python					\
%endif
%if %{with rpm}
	--with-rpm=librpm.so.%{rpmsover}                        \
%else
	--without-rpm                                           \
%endif
	--with-lzma						\
%ifarch %{armx}
	--without-libunwind-ia64				\
%else
	--without-libunwind					\
%endif
	--enable-64-bit-bfd					\
%if %{have_inproctrace}
	--enable-inprocess-agent				\
%else
	--disable-inprocess-agent				\
%endif
	--with-system-zlib					\
%if %{have_libipt}
	--with-intel-pt						\
%else
	--without-intel-pt					\
%endif
	      --with-auto-load-dir='$debugdir:$datadir/auto-load%{?scl::%{_root_datadir}/gdb/auto-load}'	\
	--with-auto-load-safe-path='$debugdir:$datadir/auto-load%{?scl::%{_root_datadir}/gdb/auto-load}'	\
	%{_target_platform} ; then
	cat config.log >&2
	exit 1
fi

if [ -z "%{!?_with_profile:no}" ]
then
  # Run all the configure tests being incompatible with $FPROFILE_CFLAGS.
  %make configure-host configure-target
  %make clean

  # Workaround -fprofile-use:
  # linux-x86-low.c:2225: Error: symbol `start_i386_goto' is already defined
  %make -C gdb/gdbserver linux-x86-low.o
fi

# Global CFLAGS would fail on:
# conftest.c:1:1: error: coverage mismatch for function 'main' while reading counter 'arcs'
if [ "$fprofile" = "-fprofile" ]
then
  FPROFILE_CFLAGS='-fprofile-generate'
elif [ -z "%{!?_with_profile:no}" ]
then
  FPROFILE_CFLAGS='-fprofile-use'
  # We cannot use -fprofile-dir as the bare filenames clash.
  (cd ../%{gdb_build}-fprofile;
   # It was 333 on x86_64.
   test $(find -name "*.gcda"|wc -l) -gt 300
   find -name "*.gcda" | while read -r i
   do
     ln $i ../%{gdb_build}/$i
   done
  )
else
  FPROFILE_CFLAGS=""
fi

%make CFLAGS="$CFLAGS $FPROFILE_CFLAGS" LDFLAGS="$FPROFILE_CFLAGS"

if [ "$fprofile" = "-fprofile" ]
then
  cd gdb
  cp -p gdb gdb-withindex
  PATH="$PWD:$PATH" sh ../../gdb/gdb-add-index $PWD/gdb-withindex
  ./gdb -nx -ex q ./gdb-withindex
  ./gdb -nx -readnow -ex q ./gdb-withindex
  cd ..
fi

cd ..

done	# fprofile

cd %{gdb_build}

%if %{with pdf}
%make \
     -C gdb/doc {gdb,annotate}{.info,/index.html,.pdf} MAKEHTMLFLAGS=--no-split MAKEINFOFLAGS=--no-split
%endif

# Copy the <sourcetree>/gdb/NEWS file to the directory above it.
cp $RPM_BUILD_DIR/%{gdb_src}/gdb/NEWS $RPM_BUILD_DIR/%{gdb_src}

%check
# Initially we're in the %{gdb_src} directory.
cd %{gdb_build}

%if %{without testsuite}
echo ====================TESTSUITE DISABLED=========================
%else
echo ====================TESTING=========================
cd gdb
gcc -o ./orphanripper %{SOURCE2} -Wall -lutil -ggdb2
# Need to use a single --ignore option, second use overrides first.
# No `%{?_smp_mflags}' here as it may race.
# WARNING: can't generate a core file - core tests suppressed - check ulimit
# "readline-overflow.exp" - Testcase is broken, functionality is OK.
(
  # ULIMIT required for `gdb.base/auxv.exp'.
  ulimit -H -c
  ulimit -c unlimited || :

  # Setup $CHECK as `check//unix/' or `check//unix/-m64' for explicit bitsize.
  # Never use two different bitsizes as it fails on ppc64.
  echo 'int main (void) { return 0; }' >biarch.c
  CHECK=""
  for BI in -m64 -m32 -m31 ""
  do
    # Do not use size-less options if any of the sizes works.
    # On ia64 there is no -m64 flag while we must not leave a bare `check' here
    # as it would switch over some testing scripts to the backward compatibility
    # mode: when `make check' was executed from inside the testsuite/ directory.
    if [ -z "$BI" -a -n "$CHECK" ];then
      continue
    fi
    # Do not use $RPM_OPT_FLAGS as the other non-size options will not be used
    # in the real run of the testsuite.
    if ! gcc $BI -o biarch biarch.c
    then
      continue
    fi
    CHECK="$CHECK check//unix/$BI"
  done
  # Do not try -m64 inferiors for -m32 GDB as it cannot handle inferiors larger
  # than itself.
  # s390 -m31 still uses the standard ELF32 binary format.
  gcc $RPM_OPT_FLAGS -o biarch biarch.c
  RPM_SIZE="$(file ./biarch|sed -n 's/^.*: ELF \(32\|64\)-bit .*$/\1/p')"
  if [ "$RPM_SIZE" != "64" ]
  then
    CHECK="$(echo " $CHECK "|sed 's# check//unix/-m64 # #')"
  fi

  # Disable some problematic testcases.
  # RUNTESTFLAGS='--ignore ...' is not used below as it gets separated by the
  # `check//...' target spawn and too much escaping there would be dense.
  for test in				\
    gdb.base/readline-overflow.exp	\
    gdb.base/bigcore.exp		\
  ; do
    mv -f ../../gdb/testsuite/$test ../gdb/testsuite/$test-DISABLED || :
  done

  # Run all the scheduled testsuite runs also in the PIE mode.
  # See also: gdb-runtest-pie-override.exp
  ###CHECK="$(echo $CHECK|sed 's#check//unix/[^ ]*#& &/-fPIC/-pie#g')"

  ./orphanripper %make -k $CHECK || :
)
for t in sum log
do
  for file in testsuite*/gdb.$t
  do
    suffix="${file#testsuite.unix.}"
    suffix="${suffix%/gdb.$t}"
    ln $file gdb-%{_target_platform}$suffix.$t || :
  done
done
# `tar | bzip2 | uuencode' may have some piping problems in Brew.
tar cjf gdb-%{_target_platform}.tar.bz2 gdb-%{_target_platform}*.{sum,log}
uuencode gdb-%{_target_platform}.tar.bz2 gdb-%{_target_platform}.tar.bz2
cd ../..
echo ====================TESTING END=====================
%endif

%install
# Initially we're in the %{gdb_src} directory.
cd %{gdb_build}

%make_install

mkdir -p $RPM_BUILD_ROOT%{_prefix}/libexec
mv -f $RPM_BUILD_ROOT%{_bindir}/gdb $RPM_BUILD_ROOT%{_prefix}/libexec/gdb
ln -s -r                                                 $RPM_BUILD_ROOT%{_prefix}/libexec/gdb  $RPM_BUILD_ROOT%{_bindir}/gdb

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gdbinit.d
touch -r %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/gdbinit.d
sed 's#%%{_sysconfdir}#%{_sysconfdir}#g' <%{SOURCE4} >$RPM_BUILD_ROOT%{_sysconfdir}/gdbinit
touch -r %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/gdbinit

%if 0
for i in `find $RPM_BUILD_ROOT%{_datadir}/gdb/python/gdb -name "*.py"`
do
  # Files could be also patched getting the current time.
  touch -r $RPM_BUILD_DIR/%{gdb_src}/gdb/ChangeLog $i
done
%endif

# Remove the files that are part of a gdb build but that are owned and
# provided by other packages.
# These are part of binutils

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/
rm -f $RPM_BUILD_ROOT%{_infodir}/bfd*
rm -f $RPM_BUILD_ROOT%{_infodir}/standard*
rm -f $RPM_BUILD_ROOT%{_infodir}/configure*
# Just exclude the header files in the top directory, and don't exclude
# the gdb/ directory, as it contains jit-reader.h.
rm -rf $RPM_BUILD_ROOT%{_includedir}/*.h
rm -rf $RPM_BUILD_ROOT/%{_libdir}/lib{bfd*,opcodes*,iberty*}

# Packaged GDB is not a cross-target one.
(cd $RPM_BUILD_ROOT%{_datadir}/gdb/syscalls
 rm -f mips*.xml
%ifnarch sparc sparcv9 sparc64
 rm -f sparc*.xml
%endif
%ifnarch x86_64
 rm -f amd64-linux.xml
%endif
%ifnarch %{ix86} x86_64
 rm -f i386-linux.xml
%endif
)

# Static libraries without headers are useless
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

# Documentation only for development.
rm -f $RPM_BUILD_ROOT%{_infodir}/gdbint*
rm -f $RPM_BUILD_ROOT%{_infodir}/stabs*

# Delete this too because the dir file will be updated at rpm install time.
# We don't want a gdb specific one overwriting the system wide one.

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# Drop files that aren't needed in an OpenMandriva context
rm -f $RPM_BUILD_ROOT%{_datadir}/gdb/system-gdbinit/elinos.py
rm -f $RPM_BUILD_ROOT%{_datadir}/gdb/system-gdbinit/wrs-linux.py
rmdir $RPM_BUILD_ROOT%{_datadir}/gdb/system-gdbinit

%files
%doc COPYING3 COPYING COPYING.LIB COPYING3.LIB
%doc README NEWS
%{_bindir}/gdb
%{_bindir}/gcore
%{_bindir}/gstack
%doc %{_mandir}/*/gcore.1*
%doc %{_mandir}/*/gstack.1*
# Provide gdb/jit-reader.h so that users are able to write their own GDB JIT
# plugins.
%{_includedir}/gdb

%files headless
%{_prefix}/libexec/gdb
%config %{_sysconfdir}/gdbinit
%doc %{_mandir}/*/gdb.1*
%{_sysconfdir}/gdbinit.d
%doc %{_mandir}/*/gdbinit.5*
%{_bindir}/gdb-add-index
%doc %{_mandir}/*/gdb-add-index.1*
%{_datadir}/gdb

# don't include the files in include, they are part of binutils
%files gdbserver
%{_bindir}/gdbserver
%ifnarch riscv64
# inproctrace not ported yet on risc
# 22 March 2019
%if %{have_inproctrace}
%{_libdir}/libinproctrace.so
%endif # %{have_inproctrace}
%endif
%doc %{_mandir}/*/gdbserver.1*

%files doc
%if %{with pdf}
%doc %{gdb_build}/gdb/doc/{gdb,annotate}.{html,pdf}
%endif
%{_infodir}/annotate.info*
%{_infodir}/ctf-spec.info*
%{_infodir}/gdb.info*
%{_infodir}/sframe-spec.info*
