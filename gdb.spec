# WARNING: This package is synced with FC
# Extract OpenMandriva Linux name and version
%define distro_version %(perl -ne '/^([.\\w\\s]+) \\(.+\\).+/ and print $1' < /etc/release)

%define Werror_cflags %nil

%if 0%{?omvver} >= 4000
# RPM 4.14 has soversion 8
%define rpmsover 8
%endif

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

%{?scl:%scl_package gdb}
%{!?scl:
 %global pkg_name %{name}
 %global _root_prefix %{_prefix}
 %global _root_datadir %{_datadir}
 %global _root_libdir %{_libdir}
}

Name: %{?scl_prefix}gdb

# Freeze it when GDB gets branched
%global snapsrc    20170420
# See timestamp of source gnulib installed into gdb/gnulib/ .
%global snapgnulib 20150822
%global tarname gdb-%{version}
Version: 8.1
%global gdb_version %{version}

# The release always contains a leading reserved number, start it at 1.
# `upstream' is not a part of `name' to stay fully rpm dependencies compatible for the testing.
Release: 4
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ and GPLv2+ with exceptions and GPL+ and LGPLv2+ and LGPLv3+ and BSD and Public Domain and GFDL
Group:   Development/Tools
# Do not provide URL for snapshots as the file lasts there only for 2 days.
# ftp://sourceware.org/pub/gdb/releases/FIXME{tarname}.tar.xz
Source0: ftp://sourceware.org/pub/gdb/releases/%{tarname}.tar.xz
URL: http://gnu.org/software/gdb/

# For our convenience
%global gdb_src %{tarname}
%global gdb_build build-%{_target_platform}

Conflicts: gdb-headless < 7.12-29

Summary: A stub package for GNU source-level debugger
Requires: gdb-headless = %{version}-%{release}

%description
'gdb' package is only a stub to install gcc-gdb-plugin for 'compile' commands.
See package 'gdb-headless'.

%package headless
Summary: A GNU source-level debugger for C, C++, Fortran, Go and other languages
Group:   Development/Tools

# Make sure we get rid of the old package gdb64, now that we have unified
# support for 32-64 bits in one single 64-bit gdb.
%ifarch ppc64
Obsoletes: gdb64 < 5.3.91
%endif

%ifarch %{arm}
%global have_inproctrace 0
%else
%global have_inproctrace 1
%endif

# eu-strip: -g recognizes .gdb_index as a debugging section. (#631997)
Conflicts: elfutils < 0.149

# Require an implementation of /usr/bin/debuginfo-install
Requires: pkg-command(debuginfo-install)

# GDB patches have the format `gdb-<version>-bz<red-hat-bz-#>-<desc>.patch'.
# They should be created using patch level 1: diff -up ./gdb (or gdb-6.3/gdb).

#=
#push=Should be pushed upstream.
#fedora=Should stay as a Fedora patch.
#fedoratest=Keep it in Fedora only as a regression test safety.

# Cleanup any leftover testsuite processes as it may stuck mock(1) builds.
#=push+jan
Source2: gdb-orphanripper.c

# Man page for gstack(1).
#=push+jan
Source3: gdb-gstack.man

# /etc/gdbinit (from Debian but with Fedora compliant location).
#=fedora
Source4: gdbinit

Source1001: gdb.rpmlintrc

# Work around out-of-date dejagnu that does not have KFAIL
#=push: That dejagnu is too old to be supported.
Patch1: gdb-6.3-rh-dummykfail-20041202.patch

# Match the Fedora's version info.
#=fedora
Patch2: gdb-6.3-rh-testversion-20041202.patch

Patch9: gdb-8.0.1-python-3.7.patch

# Better parse 64-bit PPC system call prologues.
#=push: Write new testcase.
Patch105: gdb-6.3-ppc64syscall-20040622.patch

# Include the pc's section when doing a symbol lookup so that the
# correct symbol is found.
#=push: Write new testcase.
Patch111: gdb-6.3-ppc64displaysymbol-20041124.patch

# Make upstream `set scheduler-locking step' as default.
#=push+jan: How much is scheduler-locking relevant after non-stop?
Patch260: gdb-6.6-scheduler_locking-step-is-default.patch

# Add a wrapper script to GDB that implements pstack using the
# --readnever option.
#=push
Patch118: gdb-6.3-gstack-20050411.patch

# VSYSCALL and PIE
#=fedoratest
Patch122: gdb-6.3-test-pie-20050107.patch

# Get selftest working with sep-debug-info
#=fedoratest
Patch125: gdb-6.3-test-self-20050110.patch

# Test support of multiple destructors just like multiple constructors
#=fedoratest
Patch133: gdb-6.3-test-dtorfix-20050121.patch

# Fix to support executable moving
#=fedoratest
Patch136: gdb-6.3-test-movedir-20050125.patch

# Test sibling threads to set threaded watchpoints for x86 and x86-64
#=fedoratest
Patch145: gdb-6.3-threaded-watchpoints2-20050225.patch

# Notify observers that the inferior has been created
#=fedoratest
Patch161: gdb-6.3-inferior-notification-20050721.patch

# Verify printing of inherited members test
#=fedoratest
Patch163: gdb-6.3-inheritancetest-20050726.patch

# Fix debuginfo addresses resolving for --emit-relocs Linux kernels (BZ 203661).
#=push+jan: There was some mail thread about it, this patch may be a hack.
Patch188: gdb-6.5-bz203661-emit-relocs.patch

# Support TLS symbols (+`errno' suggestion if no pthread is found) (BZ 185337).
#=push+jan: It should be replaced by Infinity project.
Patch194: gdb-6.5-bz185337-resolve-tls-without-debuginfo-v2.patch

# Fix TLS symbols resolving for shared libraries with a relative pathname.
# The testsuite needs `gdb-6.5-tls-of-separate-debuginfo.patch'.
#=fedoratest: One should recheck if it is really fixed upstream.
Patch196: gdb-6.5-sharedlibrary-path.patch

# Testcase for deadlocking on last address space byte; for corrupted backtraces.
#=fedoratest
Patch211: gdb-6.5-last-address-space-byte-test.patch

# Improved testsuite results by the testsuite provided by the courtesy of BEA.
#=fedoratest: For upstream it should be rewritten as a dejagnu test, the test of no "??" was useful.
Patch208: gdb-6.5-BEA-testsuite.patch

# Fix readline segfault on excessively long hand-typed lines.
#=fedoratest
Patch213: gdb-6.5-readline-long-line-crash-test.patch

# Fix bogus 0x0 unwind of the thread's topmost function clone(3) (BZ 216711).
#=fedora
Patch214: gdb-6.5-bz216711-clone-is-outermost.patch

# Test sideeffects of skipping ppc .so libs trampolines (BZ 218379).
#=fedoratest
Patch216: gdb-6.5-bz218379-ppc-solib-trampoline-test.patch

# Fix lockup on trampoline vs. its function lookup; unreproducible (BZ 218379).
#=fedora
Patch217: gdb-6.5-bz218379-solib-trampoline-lookup-lock-fix.patch

# Find symbols properly at their original (included) file (BZ 109921).
#=fedoratest
Patch225: gdb-6.5-bz109921-DW_AT_decl_file-test.patch

# Update PPC unwinding patches to their upstream variants (BZ 140532).
#=fedoratest
Patch229: gdb-6.3-bz140532-ppc-unwinding-test.patch

# Testcase for exec() from threaded program (BZ 202689).
#=fedoratest
Patch231: gdb-6.3-bz202689-exec-from-pthread-test.patch

# Testcase for PPC Power6/DFP instructions disassembly (BZ 230000).
#=fedoratest
Patch234: gdb-6.6-bz230000-power6-disassembly-test.patch

# Allow running `/usr/bin/gcore' with provided but inaccessible tty (BZ 229517).
#=fedoratest
Patch245: gdb-6.6-bz229517-gcore-without-terminal.patch

# Notify user of a child forked process being detached (BZ 235197).
#=push+jan: This is more about discussion if/what should be printed.
Patch247: gdb-6.6-bz235197-fork-detach-info.patch

# Avoid too long timeouts on failing cases of "annota1.exp annota3.exp".
#=fedoratest
Patch254: gdb-6.6-testsuite-timeouts.patch

# Support for stepping over PPC atomic instruction sequences (BZ 237572).
#=fedoratest
Patch258: gdb-6.6-bz237572-ppc-atomic-sequence-test.patch

# Test kernel VDSO decoding while attaching to an i386 process.
#=fedoratest
Patch263: gdb-6.3-attach-see-vdso-test.patch

# Test leftover zombie process (BZ 243845).
#=fedoratest
Patch271: gdb-6.5-bz243845-stale-testing-zombie-test.patch

# Fix displaying of numeric char arrays as strings (BZ 224128).
#=fedoratest: But it is failing anyway, one should check the behavior more.
Patch282: gdb-6.7-charsign-test.patch

# Test PPC hiding of call-volatile parameter register.
#=fedoratest
Patch284: gdb-6.7-ppc-clobbered-registers-O2-test.patch

# Testsuite fixes for more stable/comparable results.
#=fedoratest
Patch287: gdb-6.7-testsuite-stable-results.patch

# Test ia64 memory leaks of the code using libunwind.
#=fedoratest
Patch289: gdb-6.5-ia64-libunwind-leak-test.patch

# Test hiding unexpected breakpoints on intentional step commands.
#=fedoratest
Patch290: gdb-6.5-missed-trap-on-step-test.patch

# Test gcore memory and time requirements for large inferiors.
#=fedoratest
Patch296: gdb-6.5-gcore-buffer-limit-test.patch

# Test debugging statically linked threaded inferiors (BZ 239652).
#  - It requires recent glibc to work in this case properly.
#=fedoratest
Patch298: gdb-6.6-threads-static-test.patch

# Test GCORE for shmid 0 shared memory mappings.
#=fedoratest: But it is broken anyway, sometimes the case being tested is not reproducible.
Patch309: gdb-6.3-mapping-zero-inode-test.patch

# Test a crash on `focus cmd', `focus prev' commands.
#=fedoratest
Patch311: gdb-6.3-focus-cmd-prev-test.patch

# Test various forms of threads tracking across exec() (BZ 442765).
#=fedoratest
Patch315: gdb-6.8-bz442765-threaded-exec-test.patch

# Silence memcpy check which returns false positive (sparc64)
#=push: But it is just a GCC workaround, look up the existing GCC PR for it.
Patch317: gdb-6.8-sparc64-silence-memcpy-check.patch

# Test a crash on libraries missing the .text section.
#=fedoratest
Patch320: gdb-6.5-section-num-fixup-test.patch

# Fix register assignments with no GDB stack frames (BZ 436037).
#=push+jan: This fix is incorrect.
Patch330: gdb-6.8-bz436037-reg-no-longer-active.patch

# [RHEL5,RHEL6] Fix attaching to stopped processes.
# [RHEL5] Workaround kernel for detaching SIGSTOPped processes (BZ 809382).
#=fedora
Patch337: gdb-6.8-attach-signalled-detach-stopped.patch

# Test the watchpoints conditionals works.
#=fedoratest
Patch343: gdb-6.8-watchpoint-conditionals-test.patch

# Fix resolving of variables at locations lists in prelinked libs (BZ 466901).
#=fedoratest
Patch348: gdb-6.8-bz466901-backtrace-full-prelinked.patch

# New test for step-resume breakpoint placed in multiple threads at once.
#=fedoratest
Patch381: gdb-simultaneous-step-resume-breakpoint-test.patch

# Fix GNU/Linux core open: Can't read pathname for load map: Input/output error.
# Fix regression of undisplayed missing shared libraries caused by a fix for.
#=fedoratest: It should be in glibc: libc-alpha: <20091004161706.GA27450@.*>
Patch382: gdb-core-open-vdso-warning.patch

# Fix syscall restarts for amd64->i386 biarch.
#=push+jan
Patch391: gdb-x86_64-i386-syscall-restart.patch

# Fix stepping with OMP parallel Fortran sections (BZ 533176).
#=push+jan: It requires some better DWARF annotations.
Patch392: gdb-bz533176-fortran-omp-step.patch

# Fix regression by python on ia64 due to stale current frame.
#=push+jan
Patch397: gdb-follow-child-stale-parent.patch

# Workaround ccache making lineno non-zero for command-line definitions.
#=fedoratest: ccache is rarely used and it is even fixed now.
Patch403: gdb-ccache-workaround.patch

# Testcase for "Do not make up line information" fix by Daniel Jacobowitz.
#=fedoratest
Patch407: gdb-lineno-makeup-test.patch

# Test power7 ppc disassembly.
#=fedoratest
Patch408: gdb-ppc-power7-test.patch

# Workaround non-stop moribund locations exploited by kernel utrace (BZ 590623).
#=push+jan: Currently it is still not fully safe.
Patch459: gdb-moribund-utrace-workaround.patch

# Backport DWARF-4 support (BZ 601887, Tom Tromey).
#=fedoratest
Patch475: gdb-bz601887-dwarf4-rh-test.patch

# [delayed-symfile] Test a backtrace regression on CFIs without DIE (BZ 614604).
#=fedoratest
Patch490: gdb-test-bt-cfi-without-die.patch

# Provide /usr/bin/gdb-add-index for rpm-build (Tom Tromey).
#=push: Re-check against the upstream version.
Patch491: gdb-gdb-add-index-script.patch

# Out of memory is just an error, not fatal (uninitialized VLS vars, BZ 568248).
#=push+jan: Inferior objects should be read in parts, then this patch gets obsoleted.
Patch496: gdb-bz568248-oom-is-error.patch

# Verify GDB Python built-in function gdb.solib_address exists (BZ # 634108).
#=fedoratest
Patch526: gdb-bz634108-solib_address.patch

# New test gdb.arch/x86_64-pid0-core.exp for kernel PID 0 cores (BZ 611435).
#=fedoratest
Patch542: gdb-test-pid0-core.patch

# [archer-tromey-delayed-symfile] New test gdb.dwarf2/dw2-aranges.exp.
#=fedoratest
Patch547: gdb-test-dw2-aranges.patch

# [archer-keiths-expr-cumulative+upstream] Import C++ testcases.
#=fedoratest
Patch548: gdb-test-expr-cumulative-archer.patch

# Fix regressions on C++ names resolving (PR 11734, PR 12273, Keith Seitz).
#=fedoratest
Patch565: gdb-physname-pr11734-test.patch
#=fedoratest
Patch567: gdb-physname-pr12273-test.patch

# Toolchain on sparc is slightly broken and debuginfo files are generated
# with non 64bit aligned tables/offsets.
# See for example readelf -S ../Xvnc.debug.
#
# As a consenquence calculation of sectp->filepos as used in
# dwarf2_read_section (gdb/dwarf2read.c:1525) will return a non aligned buffer
# that cannot be used directly as done with MMAP.
# Usage will result in a BusError.
#
# While we figure out what's wrong in the toolchain and do a full archive
# rebuild to fix it, we need to be able to use gdb :)
#=push
Patch579: gdb-7.2.50-sparc-add-workaround-to-broken-debug-files.patch

# Test GDB opcodes/ disassembly of Intel Ivy Bridge instructions (BZ 696890).
#=fedoratest
Patch616: gdb-test-ivy-bridge.patch

# Work around PR libc/13097 "linux-vdso.so.1" warning message.
#=push+jan
Patch627: gdb-glibc-vdso-workaround.patch

# Hack for proper PIE run of the testsuite.
#=fedoratest
Patch634: gdb-runtest-pie-override.patch

# Work around readline-6.2 incompatibility not asking for --more-- (BZ 701131).
#=fedora
Patch642: gdb-readline62-ask-more-rh.patch

# Workaround PR libc/14166 for inferior calls of strstr.
#=fedora: Compatibility with RHELs (unchecked which ones).
Patch690: gdb-glibc-strstr-workaround.patch

# Include testcase for `Unable to see a variable inside a module (XLF)' (BZ 823789).
#=fedoratest
Patch698: gdb-rhel5.9-testcase-xlf-var-inside-mod.patch

# Testcase for `Setting solib-absolute-prefix breaks vDSO' (BZ 818343).
#=fedoratest
Patch703: gdb-rhbz-818343-set-solib-absolute-prefix-testcase.patch

# Import regression test for `gdb/findvar.c:417: internal-error:
# read_var_value: Assertion `frame' failed.' (RH BZ 947564) from RHEL 6.5.
#=fedoratest
Patch832: gdb-rhbz947564-findvar-assertion-frame-failed-testcase.patch

# Fix 'memory leak in infpy_read_memory()' (RH BZ 1007614)
#=fedoratest
Patch861: gdb-rhbz1007614-memleak-infpy_read_memory-test.patch

#=fedoratest
Patch888: gdb-vla-intel-tests.patch

# Continue backtrace even if a frame filter throws an exception (Phil Muldoon).
#=push
Patch918: gdb-btrobust.patch

# Display Fortran strings in backtraces.
#=fedoratest
Patch925: gdb-fortran-frame-string.patch

# Testcase for '[SAP] Recursive dlopen causes SAP HANA installer to
# crash.' (RH BZ 1156192).
#=fedoratest
Patch977: gdb-rhbz1156192-recursive-dlopen-test.patch

# Fix jit-reader.h for multi-lib.
#=push+jan
Patch978: gdb-jit-reader-multilib.patch

# Fix '`catch syscall' doesn't work for parent after `fork' is called'
# (Philippe Waroquiers, RH BZ 1149205).
#=fedoratest
Patch984: gdb-rhbz1149205-catch-syscall-after-fork-test.patch

# Fix 'backport GDB 7.4 fix to RHEL 6.6 GDB' [Original Sourceware bug
# description: 'C++ (and objc): Internal error on unqualified name
# re-set', PR 11657] (RH BZ 1186476).
#=fedoratest
Patch991: gdb-rhbz1186476-internal-error-unqualified-name-re-set-test.patch

# Test 'info type-printers' Python error (RH BZ 1350436).
#=fedoratest
Patch992: gdb-rhbz1350436-type-printers-error.patch

# Never kill PID on: gdb exec PID (Jan Kratochvil, RH BZ 1219747).
#=push+jan
Patch1053: gdb-bz1219747-attach-kills.patch

# Fix the pahole command breakage due to its Python3 port (RH BZ 1264532).
#=fedora
Patch1044: gdb-pahole-python2.patch

# Test clflushopt instruction decode (for RH BZ 1262471).
#=fedoratest
Patch1073: gdb-opcodes-clflushopt-test.patch

# [testsuite] Fix false selftest.exp FAIL from system readline-6.3+ (Patrick Palka).
#=fedoratest
Patch1075: gdb-testsuite-readline63-sigint.patch
#=fedoratest
Patch1119: gdb-testsuite-readline63-sigint-revert.patch

# [aarch64] Fix hardware watchpoints (RH BZ 1261564).
#=fedoratest
Patch1113: gdb-rhbz1261564-aarch64-hw-watchpoint-test.patch 

# New test for Python "Cannot locate object file for block" (for RH BZ 1325795).
#=fedoratest
Patch1123: gdb-rhbz1325795-framefilters-test.patch

# [dts+el7] [x86*] Bundle linux_perf.h for libipt (RH BZ 1256513).
#=fedora
Patch1143: gdb-linux_perf-bundle.patch
 
# Fix gdb-headless /usr/bin/ executables (BZ 1390251).
#=fedora
Patch1152: gdb-libexec-add-index.patch

# New testcase for: Fix <tab>-completion crash (Gary Benson, RH BZ 1398387).
#=fedoratest
Patch1155: gdb-rhbz1398387-tab-crash-test.patch

# [rhel dts libipt] Fix [-Werror=implicit-fallthrough=] with gcc-7.1.1.
#=push+jan
Patch1171: v1.6.1-implicit-fallthrough.patch

# Use inlined func name for printing breakpoints (RH BZ 1228556, Keith Seitz).
Patch1261: gdb-rhbz1228556-bpt-inlined-func-name-1of2.patch
Patch1262: gdb-rhbz1228556-bpt-inlined-func-name-2of2.patch

# RL_STATE_FEDORA_GDB would not be found for:
# Patch642: gdb-readline62-ask-more-rh.patch
# --with-system-readline

# OMV specific
Patch2000: gdb-8.1-guile-2.2.patch

BuildRequires: readline-devel >= 6.2-4
BuildRequires: ncurses-devel texinfo gettext flex bison
BuildRequires: pkgconfig(expat)
BuildRequires: pkgconfig(liblzma)
%if %{with rpm}
# dlopen() no longer makes rpm-libsFIXME{?_isa} (it's .so) a mandatory dependency.
BuildRequires: pkgconfig(rpm) >= 4.14.0-0
%endif
%global __python %{__python3}
BuildRequires:   pkgconfig(python3)
Requires:   python >= 3
%if %{with pdf}
# gdb-doc in PDF, see: https://bugzilla.redhat.com/show_bug.cgi?id=919891#c10
BuildRequires:   texlive
%endif
%if %{with babeltrace}
BuildRequires: libbabeltrace-devel
%endif
BuildRequires: pkgconfig(guile-2.2)
%global have_libipt 0
%ifarch %{ix86} x86_64
#global have_libipt 1
#BuildRequires: libipt-devel
%endif
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
%setup -q -n %{gdb_src}

# Files have `# <number> <file>' statements breaking VPATH / find-debuginfo.sh .
(cd gdb;rm -fv $(perl -pe 's/\\\n/ /' <Makefile.in|sed -n 's/^YYFILES = //p'))

# *.info* is needlessly split in the distro tar; also it would not get used as
# we build in %{gdb_build}, just to be sure.
find -name "*.info*"|xargs rm -f

# Apply patches defined above.

# Match the Fedora's version info.
%patch2 -p1

%patch9 -p1 -b .py37~

%patch1 -p1

%patch105 -p1
%patch111 -p1
%patch118 -p1
%patch122 -p1
%patch125 -p1
%patch133 -p1
%patch136 -p1
%patch145 -p1
%patch161 -p1
%patch163 -p1
%patch188 -p1
%patch194 -p1
%patch196 -p1
%patch208 -p1
%patch211 -p1
%patch213 -p1
%patch214 -p1
%patch216 -p1
%patch217 -p1
%patch225 -p1
%patch229 -p1
%patch231 -p1
%patch234 -p1
%patch245 -p1
%patch247 -p1
%patch254 -p1
%patch258 -p1
%patch260 -p1
%patch263 -p1
%patch271 -p1
%patch282 -p1
%patch284 -p1
%patch287 -p1
%patch289 -p1
%patch290 -p1
%patch296 -p1
%patch298 -p1
%patch309 -p1
%patch311 -p1
%patch315 -p1
%patch317 -p1
%patch320 -p1
%patch330 -p1
%patch343 -p1
%patch348 -p1
%patch381 -p1
%patch382 -p1
%patch391 -p1
%patch392 -p1
%patch397 -p1
%patch403 -p1
%patch407 -p1
%patch408 -p1
%patch459 -p1
%patch475 -p1
%patch490 -p1
%patch491 -p1
%patch496 -p1
%patch526 -p1
%patch542 -p1
%patch547 -p1
%patch548 -p1
%patch565 -p1
%patch567 -p1
%patch579 -p1
%patch616 -p1
%patch627 -p1
%patch634 -p1
%patch690 -p1
%patch698 -p1
%patch703 -p1
%patch832 -p1
%patch861 -p1
%patch888 -p1
%patch918 -p1
%patch925 -p1
%patch977 -p1
%patch978 -p1
%patch984 -p1
%patch991 -p1
%patch992 -p1
%patch1053 -p1
%patch1073 -p1
%patch642 -p1
%patch337 -p1
%patch1113 -p1
%patch1123 -p1
%patch1143 -p1
%patch1152 -p1
%patch1155 -p1

%patch1075 -p1

%patch2000 -p1

find -name "*.orig" | xargs rm -f
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

# RL_STATE_FEDORA_GDB would not be found for:
# Patch642: gdb-readline62-ask-more-rh.patch
# --with-system-readline
mv -f readline/doc readline-doc
rm -rf readline/*
mv -f readline-doc readline/doc

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

# Patch642: gdb-readline62-ask-more-rh.patch
CFLAGS="$CFLAGS -DNEED_RL_STATE_FEDORA_GDB"

# Patch337: gdb-6.8-attach-signalled-detach-stopped.patch
%if 0%{?rhel:1} && 0%{?rhel} <= 6
CFLAGS="$CFLAGS -DNEED_DETACH_SIGSTOP"
%endif

# --htmldir and --pdfdir are not used as they are used from %{gdb_build}.
../configure							\
	--prefix=%{_prefix}					\
	--libdir=%{_libdir}					\
	--sysconfdir=%{_sysconfdir}				\
	--mandir=%{_mandir}					\
	--infodir=%{_infodir}					\
	--with-system-gdbinit=%{_sysconfdir}/gdbinit		\
	--with-gdb-datadir=%{_datadir}/gdb			\
	--enable-gdb-build-warnings=,-Wno-unused		\
	--enable-build-with-cxx					\
	--disable-werror						\
	--with-separate-debug-dir=/usr/lib/debug		\
 	--disable-sim						\
	--disable-rpath						\
%if %{with babeltrace}
	--with-babeltrace					\
%endif
	--with-guile						\
	--with-system-readline				\
	--with-expat						\
$(: ppc64 host build crashes on ppc variant of libexpat.so )	\
	--without-libexpat-prefix				\
	--enable-tui						\
%if %{with python}
	--with-python=%{__python}				\
%else
	--without-python					\
%endif
%if %{with rpm}
	--with-rpm=librpm%{rpmsover}.so                         \
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
	%{_target_platform}

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

%makeinstall_std

mkdir -p $RPM_BUILD_ROOT%{_prefix}/libexec
mv -f $RPM_BUILD_ROOT%{_bindir}/gdb $RPM_BUILD_ROOT%{_prefix}/libexec/gdb
ln -s -r                                                 $RPM_BUILD_ROOT%{_prefix}/libexec/gdb  $RPM_BUILD_ROOT%{_bindir}/gdb

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gdbinit.d
touch -r %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/gdbinit.d
sed 's#%%{_sysconfdir}#%{_sysconfdir}#g' <%{SOURCE4} >$RPM_BUILD_ROOT%{_sysconfdir}/gdbinit
touch -r %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/gdbinit

for i in `find $RPM_BUILD_ROOT%{_datadir}/gdb/python/gdb -name "*.py"`
do
  # Files could be also patched getting the current time.
  touch -r $RPM_BUILD_DIR/%{gdb_src}/gdb/ChangeLog $i
done

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

# pstack obsoletion

cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_mandir}/man1/gstack.1
ln -s gstack.1 $RPM_BUILD_ROOT%{_mandir}/man1/pstack.1
ln -s gstack $RPM_BUILD_ROOT%{_bindir}/pstack

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

# Documentation only for development.
rm -f $RPM_BUILD_ROOT%{_infodir}/gdbint*
rm -f $RPM_BUILD_ROOT%{_infodir}/stabs*

# Delete this too because the dir file will be updated at rpm install time.
# We don't want a gdb specific one overwriting the system wide one.

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# These files are unrelated to Fedora Linux.
rm -f $RPM_BUILD_ROOT%{_datadir}/gdb/system-gdbinit/elinos.py
rm -f $RPM_BUILD_ROOT%{_datadir}/gdb/system-gdbinit/wrs-linux.py
rmdir $RPM_BUILD_ROOT%{_datadir}/gdb/system-gdbinit

rm -f $RPM_BUILD_ROOT%{_datadir}/gdb/python/gdb/FrameWrapper.py
rm -f $RPM_BUILD_ROOT%{_datadir}/gdb/python/gdb/backtrace.py
rm -f $RPM_BUILD_ROOT%{_datadir}/gdb/python/gdb/command/backtrace.py

%files
%doc COPYING3 COPYING COPYING.LIB COPYING3.LIB
%doc README NEWS
%{_bindir}/gdb
%{_bindir}/gcore
%{_mandir}/*/gcore.1*
%{_bindir}/gstack
%{_mandir}/*/gstack.1*
%{_bindir}/pstack
%{_mandir}/*/pstack.1*
# Provide gdb/jit-reader.h so that users are able to write their own GDB JIT
# plugins.
%{_includedir}/gdb

%files headless
%{_prefix}/libexec/gdb
%config %{_sysconfdir}/gdbinit
%{_mandir}/*/gdb.1*
%{_sysconfdir}/gdbinit.d
%{_mandir}/*/gdbinit.5*
%{_bindir}/gdb-add-index
%{_mandir}/*/gdb-add-index.1*
%{_datadir}/gdb

# don't include the files in include, they are part of binutils

%files gdbserver
%{_bindir}/gdbserver
%{_mandir}/*/gdbserver.1*
%if %{have_inproctrace}
%{_libdir}/libinproctrace.so
%endif # %{have_inproctrace}

%files doc
%if %{with pdf}
%doc %{gdb_build}/gdb/doc/{gdb,annotate}.{html,pdf}
%endif
%{_infodir}/annotate.info*
%{_infodir}/gdb.info*
