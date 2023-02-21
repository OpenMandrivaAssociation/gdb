# WARNING: This package is synced with FC
# Extract OpenMandriva Linux name and version
%define distro_version %(perl -ne '/^([.\\w\\s]+) \\(.+\\).+/ and print $1' < /etc/release)

%define Werror_cflags %nil

%if 0%{?omvver} >= 4000
# RPM 4.16 has soversion 9
%define rpmsover 9
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
# FIXME as of gdb 11.1, python 3.9.8,
# building with clang 13.0.0 or gcc 11.2,
# gdb crashes while generating backtraces using the
# python backtrace generator.
# Disabling python isn't a nice fix, but better than
# leaving gdb unusable...
%bcond_with python
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
Version:	13.1
%global gdb_version %{version}

# The release always contains a leading reserved number, start it at 1.
# `upstream' is not a part of `name' to stay fully rpm dependencies compatible for the testing.
Release:	1
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ and GPLv2+ with exceptions and GPL+ and LGPLv2+ and LGPLv3+ and BSD and Public Domain and GFDL
Group:   Development/Tools
# Do not provide URL for snapshots as the file lasts there only for 2 days.
# ftp://sourceware.org/pub/gdb/releases/FIXME{tarname}.tar.xz
Source0: https://sourceware.org/pub/gdb/releases/%{tarname}.tar.xz
URL: http://gnu.org/software/gdb/

# For our convenience
%global gdb_src %{tarname}
%global gdb_build build-%{_target_platform}

Conflicts: gdb-headless < 7.12-29

Summary: A stub package for GNU source-level debugger
Requires: gdb-headless = %{version}-%{release}

# Require dnf debuginfo-install to be installed
Requires: dnf-command(debuginfo-install)

# Match the Fedora's version info.
#=fedora
Patch001: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.3-rh-testversion-20041202.patch
# VLA (Fortran dynamic arrays) from Intel + archer-jankratochvil-vla tests.
#=push
# NEEDS REBASING Patch002: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-vla-intel-fortran-strides.patch
#=push
# NEEDS REBASING Patch003: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-vla-intel-fortran-vla-strings.patch
#=push+jan
# NEEDS REBASING Patch004: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-vla-intel-stringbt-fix.patch
# VSYSCALL and PIE
#=fedoratest
Patch006: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.3-test-pie-20050107.patch
# Get selftest working with sep-debug-info
#=fedoratest
#Patch007: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.3-test-self-20050110.patch
# Test support of multiple destructors just like multiple constructors
#=fedoratest
Patch008: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.3-test-dtorfix-20050121.patch
# Fix to support executable moving
#=fedoratest
Patch009: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.3-test-movedir-20050125.patch
# Test sibling threads to set threaded watchpoints for x86 and x86-64
#=fedoratest
Patch010: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.3-threaded-watchpoints2-20050225.patch
# Notify observers that the inferior has been created
#=fedoratest
Patch011: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.3-inferior-notification-20050721.patch
# Verify printing of inherited members test
#=fedoratest
Patch012: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.3-inheritancetest-20050726.patch
# Support TLS symbols (+`errno' suggestion if no pthread is found) (BZ 185337).
#=push+jan: It should be replaced by Infinity project.
#Patch013: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.5-bz185337-resolve-tls-without-debuginfo-v2.patch
# Fix TLS symbols resolving for shared libraries with a relative pathname.
# The testsuite needs `gdb-6.5-tls-of-separate-debuginfo.patch'.
#=fedoratest: One should recheck if it is really fixed upstream.
Patch014: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.5-sharedlibrary-path.patch
# Improved testsuite results by the testsuite provided by the courtesy of BEA.
#=fedoratest: For upstream it should be rewritten as a dejagnu test, the test of no "??" was useful.
Patch015: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.5-BEA-testsuite.patch
# Testcase for deadlocking on last address space byte; for corrupted backtraces.
#=fedoratest
Patch016: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.5-last-address-space-byte-test.patch
# Fix readline segfault on excessively long hand-typed lines.
#=fedoratest
Patch017: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.5-readline-long-line-crash-test.patch
# Test sideeffects of skipping ppc .so libs trampolines (BZ 218379).
#=fedoratest
Patch018: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.5-bz218379-ppc-solib-trampoline-test.patch
# Fix lockup on trampoline vs. its function lookup; unreproducible (BZ 218379).
#=fedora
# NEEDS REBASING Patch019: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.5-bz218379-solib-trampoline-lookup-lock-fix.patch
# Find symbols properly at their original (included) file (BZ 109921).
#=fedoratest
Patch020: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.5-bz109921-DW_AT_decl_file-test.patch
# Testcase for exec() from threaded program (BZ 202689).
#=fedoratest
Patch022: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.3-bz202689-exec-from-pthread-test.patch
# Testcase for PPC Power6/DFP instructions disassembly (BZ 230000).
#=fedoratest
Patch023: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.6-bz230000-power6-disassembly-test.patch
# Allow running `/usr/bin/gcore' with provided but inaccessible tty (BZ 229517).
#=fedoratest
Patch024: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.6-bz229517-gcore-without-terminal.patch
# Avoid too long timeouts on failing cases of "annota1.exp annota3.exp".
#=fedoratest
Patch025: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.6-testsuite-timeouts.patch
# Support for stepping over PPC atomic instruction sequences (BZ 237572).
#=fedoratest
Patch026: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.6-bz237572-ppc-atomic-sequence-test.patch
# Test kernel VDSO decoding while attaching to an i386 process.
#=fedoratest
Patch027: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.3-attach-see-vdso-test.patch
# Test leftover zombie process (BZ 243845).
#=fedoratest
Patch028: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.5-bz243845-stale-testing-zombie-test.patch
# New locating of the matching binaries from the pure core file (build-id).
#=push+jan
# NEEDS REBASING Patch029: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.6-buildid-locate.patch
# Fix loading of core files without build-ids but with build-ids in executables.
# Load strictly build-id-checked core files only if no executable is specified
# (Jan Kratochvil, RH BZ 1339862).
#=push+jan
# NEEDS REBASING Patch030: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.6-buildid-locate-solib-missing-ids.patch
#=push+jan
# NEEDS REBASING Patch031: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.6-buildid-locate-rpm.patch
# Fix displaying of numeric char arrays as strings (BZ 224128).
#=fedoratest: But it is failing anyway, one should check the behavior more.
Patch032: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.7-charsign-test.patch
# Test PPC hiding of call-volatile parameter register.
#=fedoratest
Patch033: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.7-ppc-clobbered-registers-O2-test.patch
# Testsuite fixes for more stable/comparable results.
#=fedoratest
Patch034: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.7-testsuite-stable-results.patch
# Test ia64 memory leaks of the code using libunwind.
#=fedoratest
Patch035: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.5-ia64-libunwind-leak-test.patch
# Test hiding unexpected breakpoints on intentional step commands.
#=fedoratest
Patch036: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.5-missed-trap-on-step-test.patch
# Test gcore memory and time requirements for large inferiors.
#=fedoratest
Patch037: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.5-gcore-buffer-limit-test.patch
# Test GCORE for shmid 0 shared memory mappings.
#=fedoratest: But it is broken anyway, sometimes the case being tested is not reproducible.
Patch038: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.3-mapping-zero-inode-test.patch
# Test a crash on `focus cmd', `focus prev' commands.
#=fedoratest
Patch039: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.3-focus-cmd-prev-test.patch
# Test various forms of threads tracking across exec() (BZ 442765).
#=fedoratest
Patch040: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.8-bz442765-threaded-exec-test.patch
# Test a crash on libraries missing the .text section.
#=fedoratest
Patch041: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.5-section-num-fixup-test.patch
# Fix resolving of variables at locations lists in prelinked libs (BZ 466901).
#=fedoratest
Patch042: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.8-bz466901-backtrace-full-prelinked.patch
# New test for step-resume breakpoint placed in multiple threads at once.
#=fedoratest
Patch043: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-simultaneous-step-resume-breakpoint-test.patch
# Fix stepping with OMP parallel Fortran sections (BZ 533176).
#=push+jan: It requires some better DWARF annotations.
Patch045: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-bz533176-fortran-omp-step.patch
# Workaround ccache making lineno non-zero for command-line definitions.
#=fedoratest: ccache is rarely used and it is even fixed now.
#Patch046: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-ccache-workaround.patch
#=push+jan: May get obsoleted by Tom's unrelocated objfiles patch.
# NEEDS REBASING Patch047: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-archer-pie-addons.patch
#=push+jan: Breakpoints disabling matching should not be based on address.
# NEEDS REBASING Patch048: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-archer-pie-addons-keep-disabled.patch
# Testcase for "Do not make up line information" fix by Daniel Jacobowitz.
#=fedoratest
Patch049: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-lineno-makeup-test.patch
# Test power7 ppc disassembly.
#=fedoratest
Patch050: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-ppc-power7-test.patch
# Workaround non-stop moribund locations exploited by kernel utrace (BZ 590623).
#=push+jan: Currently it is still not fully safe.
# NEEDS REBASING Patch051: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-moribund-utrace-workaround.patch
# Fix follow-exec for C++ programs (bugreported by Martin Stransky).
#=fedoratest
Patch052: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-archer-next-over-throw-cxx-exec.patch
# Backport DWARF-4 support (BZ 601887, Tom Tromey).
#=fedoratest
Patch053: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-bz601887-dwarf4-rh-test.patch
#=push+jan
# NEEDS REBASING Patch054: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.6-buildid-locate-core-as-arg.patch
# Workaround librpm BZ 643031 due to its unexpected exit() calls (BZ 642879).
#=push+jan
# NEEDS REBASING Patch055: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.6-buildid-locate-rpm-librpm-workaround.patch
# [delayed-symfile] Test a backtrace regression on CFIs without DIE (BZ 614604).
#=fedoratest
Patch056: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-test-bt-cfi-without-die.patch
# Verify GDB Python built-in function gdb.solib_address exists (BZ # 634108).
#=fedoratest
Patch057: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-bz634108-solib_address.patch
# New test gdb.arch/x86_64-pid0-core.exp for kernel PID 0 cores (BZ 611435).
#=fedoratest
Patch058: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-test-pid0-core.patch
# [archer-tromey-delayed-symfile] New test gdb.dwarf2/dw2-aranges.exp.
#=fedoratest
Patch059: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-test-dw2-aranges.patch
# [archer-keiths-expr-cumulative+upstream] Import C++ testcases.
#=fedoratest
Patch060: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-test-expr-cumulative-archer.patch
# Fix regressions on C++ names resolving (PR 11734, PR 12273, Keith Seitz).
#=fedoratest
Patch061: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-physname-pr11734-test.patch
# Fix regressions on C++ names resolving (PR 11734, PR 12273, Keith Seitz).
#=fedoratest
Patch062: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-physname-pr12273-test.patch
# Test GDB opcodes/ disassembly of Intel Ivy Bridge instructions (BZ 696890).
#=fedoratest
Patch063: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-test-ivy-bridge.patch
# Hack for proper PIE run of the testsuite.
#=fedoratest
Patch064: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-runtest-pie-override.patch
# Print reasons for failed attach/spawn incl. SELinux deny_ptrace (BZ 786878).
#=push+jan
# NEEDS REBASING Patch065: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-attach-fail-reasons-5of5.patch
# Workaround PR libc/14166 for inferior calls of strstr.
#=fedoratest: Compatibility with RHELs (unchecked which ones).
Patch066: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-glibc-strstr-workaround.patch
# Include testcase for `Unable to see a variable inside a module (XLF)' (BZ 823789).
#=fedoratest
Patch067: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-rhel5.9-testcase-xlf-var-inside-mod.patch
# Testcase for `Setting solib-absolute-prefix breaks vDSO' (BZ 818343).
#=fedoratest
Patch068: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-rhbz-818343-set-solib-absolute-prefix-testcase.patch
# Import regression test for `gdb/findvar.c:417: internal-error:
# read_var_value: Assertion `frame' failed.' (RH BZ 947564) from RHEL 6.5.
#=fedoratest
Patch069: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-rhbz947564-findvar-assertion-frame-failed-testcase.patch
# Fix crash of -readnow /usr/lib/debug/usr/bin/gnatbind.debug (BZ 1069211).
#=push+jan
# NEEDS REBASING Patch070: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-gnat-dwarf-crash-3of3.patch
# Fix 'memory leak in infpy_read_memory()' (RH BZ 1007614)
#=fedoratest
Patch071: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-rhbz1007614-memleak-infpy_read_memory-test.patch
# Fix 'gdb gives highly misleading error when debuginfo pkg is present,
# but not corresponding binary pkg' (RH BZ 981154).
#=push+jan
Patch072: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.6-buildid-locate-misleading-warning-missing-debuginfo-rhbz981154.patch
#=fedoratest
# NEEDS REBASE Patch073: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-archer-vla-tests.patch
#=fedoratest
# NEEDS REBASE Patch074: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-vla-intel-tests.patch
# Continue backtrace even if a frame filter throws an exception (Phil Muldoon).
#=push
Patch075: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-btrobust.patch
# Display Fortran strings in backtraces.
#=fedoratest
Patch076: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-fortran-frame-string.patch
# Testcase for '[SAP] Recursive dlopen causes SAP HANA installer to
# crash.' (RH BZ 1156192).
#=fedoratest
Patch077: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-rhbz1156192-recursive-dlopen-test.patch
# Fix jit-reader.h for multi-lib.
#=push+jan
Patch078: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-jit-reader-multilib.patch
# Fix '`catch syscall' doesn't work for parent after `fork' is called'
# (Philippe Waroquiers, RH BZ 1149205).
#=fedoratest
Patch079: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-rhbz1149205-catch-syscall-after-fork-test.patch
# Fix 'backport GDB 7.4 fix to RHEL 6.6 GDB' [Original Sourceware bug
# description: 'C++ (and objc): Internal error on unqualified name
# re-set', PR 11657] (RH BZ 1186476).
#=fedoratest
Patch080: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-rhbz1186476-internal-error-unqualified-name-re-set-test.patch
# Test 'info type-printers' Python error (RH BZ 1350436).
#=fedoratest
#Patch081: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-rhbz1350436-type-printers-error.patch
# Fix '[ppc64] and [s390x] wrong prologue skip on -O2 -g code' (Jan
# Kratochvil, RH BZ 1084404).
#=fedoratest
Patch082: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-rhbz1084404-ppc64-s390x-wrong-prologue-skip-O2-g-3of3.patch
# Never kill PID on: gdb exec PID (Jan Kratochvil, RH BZ 1219747).
#=push+jan
Patch083: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-bz1219747-attach-kills.patch
# Force libncursesw over libncurses to match the includes (RH BZ 1270534).
#=push+jan
Patch084: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-fedora-libncursesw.patch
# Test clflushopt instruction decode (for RH BZ 1262471).
#=fedoratest
Patch085: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-opcodes-clflushopt-test.patch
# [SCL] Skip deprecated .gdb_index warning for Red Hat built files (BZ 953585).
#=push+jan
# NEEDS REBASE Patch087: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.6-buildid-locate-rpm-scl.patch
# Make the GDB quit processing non-abortable to cleanup everything properly.
#=fedora: It was useful only after gdb-6.8-attach-signalled-detach-stopped.patch .
# NEEDS REBASE Patch088: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-6.8-quit-never-aborts.patch
# [aarch64] Fix hardware watchpoints (RH BZ 1261564).
#=fedoratest
Patch089: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-rhbz1261564-aarch64-hw-watchpoint-test.patch
# Add messages suggesting more recent RHEL gdbserver (RH BZ 1321114).
#=fedora
# NEEDS REBASE Patch090: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-container-rh-pkg.patch
# New test for Python "Cannot locate object file for block" (for RH BZ 1325795).
#=fedoratest
Patch091: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-rhbz1325795-framefilters-test.patch
# [dts+el7] [x86*] Bundle linux_perf.h for libipt (RH BZ 1256513).
#=fedora
# NEEDS REBASE Patch092: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-linux_perf-bundle.patch
# Fix gdb-headless /usr/bin/ executables (BZ 1390251).
#
# Also, make /usr/bin/gdb.minimal be the default GDB used, if it's
# present.  For rationale, see:
#
#   https://fedoraproject.org/wiki/Changes/Minimal_GDB_in_buildroot
#=fedora
Patch093: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-libexec-add-index.patch
# New testcase for: Fix <tab>-completion crash (Gary Benson, RH BZ 1398387).
#=fedoratest
Patch094: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-rhbz1398387-tab-crash-test.patch
# Python patches of: http://sourceware.org/gdb/wiki/ProjectArcher
#=push
Patch095: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-archer.patch
# Revert upstream commit 469412dd9ccc4de5874fd3299b105833f36b34cd
# NEEDS REBASE Patch096: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-vla-intel-fix-print-char-array.patch
# [s390x] Backport arch12 instructions decoding (RH BZ 1553104).
# =fedoratest
Patch097: https://src.fedoraproject.org/rpms/gdb/raw/master/f/gdb-rhbz1553104-s390x-arch12-test.patch

# OM only patches
Patch500: gdb-12.1-readline-8.2.patch

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
%if %{with guile}
BuildRequires: pkgconfig(guile-3.0)
%endif
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

# --htmldir and --pdfdir are not used as they are used from %{gdb_build}.
if ! ../configure							\
	--prefix=%{_prefix}					\
	--libdir=%{_libdir}					\
	--sysconfdir=%{_sysconfdir}				\
	--mandir=%{_mandir}					\
	--infodir=%{_infodir}					\
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
	--with-python=%{__python}				\
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
%doc %{_mandir}/*/gcore.1*
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
%ifnarch riscv64
# GDB Server not ported yet on risc
# 22 March 2019
%{_bindir}/gdbserver
# GDB Server not ported yet on risc
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
%{_infodir}/gdb.info*
%{_infodir}/sframe-spec.info*
