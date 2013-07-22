# Extract Mandriva Linux name and version
%define mdv_distro_version	%(perl -ne '/^([.\\w\\s]+) \\(.+\\).+/ and print $1' < /etc/release)

%define branch 7.5
%define linaro 2012.12

Summary:	A GNU source-level debugger for C, C++ and Fortran
Name:		gdb
Version:	%{branch}_%linaro
Release:	1
License:	GPLv3+
Group:		Development/Other
URL:		http://www.gnu.org/software/gdb/
# See also http://launchpad.net/gdb-linaro
Source0:	gdb-linaro-%branch-%linaro-1.tar.bz2
# Cleanup any leftover testsuite processes as it may stuck mock(1) builds.
#=push
Source2:	gdb-orphanripper.c

# Man page for gstack(1).
#=push
Source3:	gdb-gstack.man

# /etc/gdbinit (from Debian but with Fedora compliant location).
#=fedora
Source4:	gdbinit

# libstdc++ pretty printers from GCC SVN HEAD (4.5 experimental).
%define libstdcxxpython libstdc++-v3-python-r155978
Source5:	%{libstdcxxpython}.tar.bz2

# Work around out-of-date dejagnu that does not have KFAIL
#=drop: That dejagnu is too old to be supported.
Patch1: gdb-6.3-rh-dummykfail-20041202.patch

# Match the Fedora's version info.
#=fedora
Patch2: gdb-6.3-rh-testversion-20041202.patch

# Check that libunwind works - new test then fix
#=ia64
Patch3: gdb-6.3-rh-testlibunwind-20041202.patch

# Better parse 64-bit PPC system call prologues.
#=maybepush+ppc: Write new testcase.
Patch105: gdb-6.3-ppc64syscall-20040622.patch

# Include the pc's section when doing a symbol lookup so that the
# correct symbol is found.
#=maybepush: Write new testcase.
Patch111: gdb-6.3-ppc64displaysymbol-20041124.patch

# Fix upstream `set scheduler-locking step' vs. upstream PPC atomic seqs.
#=push+work: It is a bit difficult patch, a part is ppc specific.
Patch112: gdb-6.6-scheduler_locking-step-sw-watchpoints2.patch
# Make upstream `set scheduler-locking step' as default.
#=push+work: How much is scheduler-locking relevant after non-stop?
Patch260: gdb-6.6-scheduler_locking-step-is-default.patch

# Add a wrapper script to GDB that implements pstack using the
# --readnever option.
#=push+work: with gdbindex maybe --readnever should no longer be used.
Patch118: gdb-6.3-gstack-20050411.patch

# VSYSCALL and PIE
#=fedoratest
Patch122: gdb-6.3-test-pie-20050107.patch
#=push: May get obsoleted by Tom's unrelocated objfiles patch.
Patch389: gdb-archer-pie-addons.patch
#=push+work: Breakpoints disabling matching should not be based on address.
Patch394: gdb-archer-pie-addons-keep-disabled.patch

# Get selftest working with sep-debug-info
#=fedoratest
Patch125: gdb-6.3-test-self-20050110.patch

# Test support of multiple destructors just like multiple constructors
#=fedoratest
Patch133: gdb-6.3-test-dtorfix-20050121.patch

# Fix to support executable moving
#=fedoratest
Patch136: gdb-6.3-test-movedir-20050125.patch

# Fix gcore for threads
#=ia64
Patch140: gdb-6.3-gcore-thread-20050204.patch

# Test sibling threads to set threaded watchpoints for x86 and x86-64
#=fedoratest
Patch145: gdb-6.3-threaded-watchpoints2-20050225.patch

# Do not issue warning message about first page of storage for ia64 gcore
#=ia64
Patch153: gdb-6.3-ia64-gcore-page0-20050421.patch

# IA64 sigtramp prev register patch
#=ia64
Patch158: gdb-6.3-ia64-sigtramp-frame-20050708.patch

# IA64 gcore speed-up patch
#=ia64
Patch160: gdb-6.3-ia64-gcore-speedup-20050714.patch

# Notify observers that the inferior has been created
#=fedoratest
Patch161: gdb-6.3-inferior-notification-20050721.patch

# Fix ia64 info frame bug
#=ia64
Patch162: gdb-6.3-ia64-info-frame-fix-20050725.patch

# Verify printing of inherited members test
#=fedoratest
Patch163: gdb-6.3-inheritancetest-20050726.patch

# Add readnever option
#=push
Patch164: gdb-6.3-readnever-20050907.patch

# Fix ia64 gdb problem with user-specified SIGILL handling
#=ia64
Patch169: gdb-6.3-ia64-sigill-20051115.patch

# Fix debuginfo addresses resolving for --emit-relocs Linux kernels (BZ 203661).
#=push+work: There was some mail thread about it, this patch may be a hack.
Patch188: gdb-6.5-bz203661-emit-relocs.patch

# Support TLS symbols (+`errno' suggestion if no pthread is found) (BZ 185337).
#=push+work: It should be replaced by existing uncommitted Roland's glibc patch for TLS without libpthreads.
Patch194: gdb-6.5-bz185337-resolve-tls-without-debuginfo-v2.patch

# Fix TLS symbols resolving for shared libraries with a relative pathname.
# The testsuite needs `gdb-6.5-tls-of-separate-debuginfo.patch'.
#=fedoratest+work: One should recheck if it is really fixed upstream.
Patch196: gdb-6.5-sharedlibrary-path.patch

# Suggest fixing your target architecture for gdbserver(1) (BZ 190810).
# FIXME: It could be autodetected.
#=push+work: There are more such error cases that can happen.
Patch199: gdb-6.5-bz190810-gdbserver-arch-advice.patch

# Testcase for deadlocking on last address space byte; for corrupted backtraces.
#=fedoratest
Patch211: gdb-6.5-last-address-space-byte-test.patch

# Improved testsuite results by the testsuite provided by the courtesy of BEA.
#=fedoratest+work: For upstream it should be rewritten as a dejagnu test, the test of no "??" was useful.
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
#=fedoratest+ppc
Patch229: gdb-6.3-bz140532-ppc-unwinding-test.patch

# Testcase for exec() from threaded program (BZ 202689).
#=fedoratest
Patch231: gdb-6.3-bz202689-exec-from-pthread-test.patch

# Backported fixups post the source tarball.
#Xdrop: Just backports.
Patch232: gdb-upstream.patch

# Testcase for PPC Power6/DFP instructions disassembly (BZ 230000).
#=fedoratest+ppc
Patch234: gdb-6.6-bz230000-power6-disassembly-test.patch

# Temporary support for shared libraries >2GB on 64bit hosts. (BZ 231832)
#=push+work: Upstream should have backward compat. API: libc-alpha: <20070127104539.GA9444@.*>
Patch235: gdb-6.3-bz231832-obstack-2gb.patch

# Allow running `/usr/bin/gcore' with provided but inaccessible tty (BZ 229517).
#=fedoratest
Patch245: gdb-6.6-bz229517-gcore-without-terminal.patch

# Notify user of a child forked process being detached (BZ 235197).
#=push: This is more about discussion if/what should be printed.
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

# New locating of the matching binaries from the pure core file (build-id).
#=push
Patch274: gdb-6.6-buildid-locate.patch
# Fix loading of core files without build-ids but with build-ids in executables.
#=push
Patch659: gdb-6.6-buildid-locate-solib-missing-ids.patch
#=push
Patch353: gdb-6.6-buildid-locate-rpm.patch
#=push
Patch415: gdb-6.6-buildid-locate-core-as-arg.patch
# Workaround librpm BZ 643031 due to its unexpected exit() calls (BZ 642879).
#=push
Patch519: gdb-6.6-buildid-locate-rpm-librpm-workaround.patch

# Add kernel vDSO workaround (`no loadable ...') on RHEL-5 (kernel BZ 765875).
#=push
Patch276: gdb-6.6-bfd-vdso8k.patch

# Fix displaying of numeric char arrays as strings (BZ 224128).
#=fedoratest: But it is failing anyway, one should check the behavior more.
Patch282: gdb-6.7-charsign-test.patch

# Test PPC hiding of call-volatile parameter register.
#=fedoratest+ppc
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

# Support DW_TAG_interface_type the same way as DW_TAG_class_type (BZ 426600).
#=fedoratest
Patch294: gdb-6.7-bz426600-DW_TAG_interface_type-test.patch

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

# Fix PRPSINFO in the core files dumped by gcore (BZ 254229).
#=push
Patch329: gdb-6.8-bz254229-gcore-prpsinfo.patch

# Fix register assignments with no GDB stack frames (BZ 436037).
#=push+work: This fix is incorrect.
Patch330: gdb-6.8-bz436037-reg-no-longer-active.patch

# Make the GDB quit processing non-abortable to cleanup everything properly.
#=push: It was useful only after gdb-6.8-attach-signalled-detach-stopped.patch .
Patch331: gdb-6.8-quit-never-aborts.patch

# Test the watchpoints conditionals works.
#=fedoratest
Patch343: gdb-6.8-watchpoint-conditionals-test.patch

# Fix resolving of variables at locations lists in prelinked libs (BZ 466901).
#=fedoratest
Patch348: gdb-6.8-bz466901-backtrace-full-prelinked.patch

# The merged branch `archer-jankratochvil-fedora15' of:
# http://sourceware.org/gdb/wiki/ProjectArcher
#=push+work
Patch349: gdb-archer.patch

# Fix parsing elf64-i386 files for kdump PAE vmcore dumps (BZ 457187).
# - Turn on 64-bit BFD support, globally enable AC_SYS_LARGEFILE.
#=fedoratest
Patch360: gdb-6.8-bz457187-largefile-test.patch

# New test for step-resume breakpoint placed in multiple threads at once.
#=fedoratest
Patch381: gdb-simultaneous-step-resume-breakpoint-test.patch

# Fix GNU/Linux core open: Can't read pathname for load map: Input/output error.
# Fix regression of undisplayed missing shared libraries caused by a fix for.
#=push+work: It should be in glibc: libc-alpha: <20091004161706.GA27450@.*>
Patch382: gdb-core-open-vdso-warning.patch

# Fix syscall restarts for amd64->i386 biarch.
#=push
Patch391: gdb-x86_64-i386-syscall-restart.patch

# Fix stepping with OMP parallel Fortran sections (BZ 533176).
#=push+work: It requires some better DWARF annotations.
Patch392: gdb-bz533176-fortran-omp-step.patch

# Fix regression by python on ia64 due to stale current frame.
#=push
Patch397: gdb-follow-child-stale-parent.patch

# Workaround ccache making lineno non-zero for command-line definitions.
#=fedoratest: ccache is rarely used and it is even fixed now.
Patch403: gdb-ccache-workaround.patch

# Implement `info common' for Fortran.
#=push
Patch404: gdb-fortran-common-reduce.patch
#=push
Patch405: gdb-fortran-common.patch

# Testcase for "Do not make up line information" fix by Daniel Jacobowitz.
#=fedoratest
Patch407: gdb-lineno-makeup-test.patch

# Test power7 ppc disassembly.
#=fedoratest+ppc
Patch408: gdb-ppc-power7-test.patch

# Fix i386+x86_64 rwatch+awatch before run, regression against 6.8 (BZ 541866).
# Fix i386 rwatch+awatch before run (BZ 688788, on top of BZ 541866).
#=push+work: It should be fixed properly instead.
Patch417: gdb-bz541866-rwatch-before-run.patch

# Workaround non-stop moribund locations exploited by kernel utrace (BZ 590623).
#=push+work: Currently it is still not fully safe.
Patch459: gdb-moribund-utrace-workaround.patch

# Fix follow-exec for C++ programs (bugreported by Martin Stransky).
#=fedoratest
Patch470: gdb-archer-next-over-throw-cxx-exec.patch

# Backport DWARF-4 support (BZ 601887, Tom Tromey).
#=fedoratest
Patch475: gdb-bz601887-dwarf4-rh-test.patch

# [delayed-symfile] Test a backtrace regression on CFIs without DIE (BZ 614604).
#=fedoratest
Patch490: gdb-test-bt-cfi-without-die.patch

# Provide /usr/bin/gdb-add-index for rpm-build (Tom Tromey).
#=fedora: Re-check against the upstream version.
Patch491: gdb-gdb-add-index-script.patch

# Out of memory is just an error, not fatal (uninitialized VLS vars, BZ 568248).
#=drop+work: Inferior objects should be read in parts, then this patch gets obsoleted.
Patch496: gdb-bz568248-oom-is-error.patch

# Fix gcore writer for -Wl,-z,relro (PR corefiles/11804).
#=push: There is different patch on gdb-patches, waiting now for resolution in kernel.
Patch504: gdb-bz623749-gcore-relro.patch

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
#=push+work
Patch579: gdb-7.2.50-sparc-add-workaround-to-broken-debug-files.patch

# Fix dlopen of libpthread.so, patched glibc required (Gary Benson, BZ 669432).
#=push
Patch618: gdb-dlopen-stap-probe-1of7.patch
Patch717: gdb-dlopen-stap-probe-2of7.patch
Patch718: gdb-dlopen-stap-probe-3of7.patch
Patch719: gdb-dlopen-stap-probe-4of7.patch
Patch720: gdb-dlopen-stap-probe-5of7.patch
Patch721: gdb-dlopen-stap-probe-6of7.patch
Patch722: gdb-dlopen-stap-probe-7of7.patch
Patch619: gdb-dlopen-stap-probe-test.patch
Patch723: gdb-dlopen-stap-probe-test2.patch

# Work around PR libc/13097 "linux-vdso.so.1" warning message.
#=push
Patch627: gdb-glibc-vdso-workaround.patch

# Hack for proper PIE run of the testsuite.
#=fedoratest
Patch634: gdb-runtest-pie-override.patch

# Enable smaller %{_bindir}/gdb in future by no longer using -rdynamic.
#=push
Patch643: gdb-python-rdynamic.patch

# Print reasons for failed attach/spawn incl. SELinux deny_ptrace (BZ 786878).
#=push
Patch653: gdb-attach-fail-reasons-5of5.patch
#=fedora
Patch657: gdb-attach-fail-reasons-5of5configure.patch

# Workaround crashes from stale frame_info pointer (BZ 804256).
#=fedora
Patch661: gdb-stale-frame_info.patch

# Workaround PR libc/14166 for inferior calls of strstr.
#=push+work: But push it to glibc.
Patch690: gdb-glibc-strstr-workaround.patch

# Include testcase for `Unable to see a variable inside a module (XLF)' (BZ 823789).
#=fedoratest
#+ppc
Patch698: gdb-rhel5.9-testcase-xlf-var-inside-mod.patch

# Testcase for `Setting solib-absolute-prefix breaks vDSO' (BZ 818343).
#=fedoratest
Patch703: gdb-rhbz-818343-set-solib-absolute-prefix-testcase.patch

# Implement MiniDebugInfo F-18 Feature consumer (Alexander Larsson, BZ 834068).
#=fedora
Patch716: gdb-minidebuginfo.patch

# Fix crash printing classes (BZ 849357, Tom Tromey).
Patch726: gdb-print-class.patch

# Permit passing pointers as address number even for C++ methods (Keith Seitz).
Patch728: gdb-check-type.patch

# entry values: Fix resolving in inlined frames.
Patch729: gdb-entryval-inlined.patch

# Fix `GDB cannot access struct member whose offset is larger than 256MB'
# (RH BZ 795424).
Patch797: gdb-rhbz795424-bitpos-06of25.patch
Patch798: gdb-rhbz795424-bitpos-07of25.patch
Patch799: gdb-rhbz795424-bitpos-08of25.patch
Patch800: gdb-rhbz795424-bitpos-09of25.patch
Patch801: gdb-rhbz795424-bitpos-10of25.patch
Patch802: gdb-rhbz795424-bitpos-11of25.patch
Patch803: gdb-rhbz795424-bitpos-12of25.patch
Patch804: gdb-rhbz795424-bitpos-13of25.patch
Patch805: gdb-rhbz795424-bitpos-14of25.patch
Patch806: gdb-rhbz795424-bitpos-15of25.patch
Patch807: gdb-rhbz795424-bitpos-16of25.patch
Patch808: gdb-rhbz795424-bitpos-17of25.patch
Patch809: gdb-rhbz795424-bitpos-18of25.patch
Patch810: gdb-rhbz795424-bitpos-19of25.patch
Patch811: gdb-rhbz795424-bitpos-20of25.patch
Patch812: gdb-rhbz795424-bitpos-21of25.patch
Patch813: gdb-rhbz795424-bitpos-22of25.patch
Patch814: gdb-rhbz795424-bitpos-23of25.patch
Patch815: gdb-rhbz795424-bitpos-24of25.patch
Patch816: gdb-rhbz795424-bitpos-25of25.patch
Patch817: gdb-rhbz795424-bitpos-25of25-test.patch
Patch818: gdb-rhbz795424-bitpos-lazyvalue.patch

# Fix DW_OP_GNU_implicit_pointer offset bug (Tom Tromey).
Patch819: gdb-implicitpointer-offset.patch

Patch1000:	gdb-7.3.50.20110722-rpm5.patch

BuildRequires:	bison
Buildrequires:	cloog-devel
BuildRequires:	flex
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	expat-devel
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(rpm) >= 5.3
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	texinfo

%description
Gdb is a full featured, command driven debugger. Gdb allows you to
trace the execution of programs and examine their internal state at
any time.  Gdb works for C and C++ compiled with the GNU C compiler
gcc.

If you are going to develop C and/or C++ programs and use the GNU gcc
compiler, you may want to install gdb to help you debug your programs.

%prep
%setup -q -n gdb-linaro-%branch-%linaro-1 -a5

%patch2 -p1

%patch349 -p1
%patch232 -p1
%patch1 -p1
%patch3 -p1

%patch105 -p1
%patch111 -p1
%patch112 -p1
%patch118 -p1
%patch122 -p1
%patch125 -p1
%patch133 -p1
%patch136 -p1
%patch140 -p1
%patch145 -p1
%patch153 -p1
%patch158 -p1
%patch160 -p1
%patch161 -p1
%patch162 -p1
%patch163 -p1
%patch164 -p1
%patch169 -p1
%patch188 -p1
%patch194 -p1
%patch196 -p1
%patch199 -p1
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
%patch235 -p1
%patch245 -p1
%patch247 -p1
%patch254 -p1
%patch258 -p1
%patch260 -p1
%patch263 -p1
%patch271 -p1
%patch274 -p1
%patch659 -p1
%patch353 -p1
%patch276 -p1
%patch282 -p1
%patch284 -p1
%patch287 -p1
%patch289 -p1
%patch290 -p1
%patch294 -p1
%patch296 -p1
%patch298 -p1
%patch309 -p1
%patch311 -p1
%patch315 -p1
%patch317 -p1
%patch320 -p1
%patch329 -p1
%patch330 -p1
%patch331 -p1
%patch343 -p1
%patch348 -p1
%patch360 -p1
%patch381 -p1
%patch382 -p1
%patch391 -p1
%patch392 -p1
%patch397 -p1
%patch403 -p1
%patch404 -p1
%patch405 -p1
%patch389 -p1
%patch394 -p1
%patch407 -p1
%patch408 -p1
%patch417 -p1
%patch459 -p1
%patch470 -p1
%patch475 -p1
%patch415 -p1
%patch519 -p1
%patch490 -p1
%patch491 -p1
%patch496 -p1
%patch504 -p1
%patch526 -p1
%patch542 -p1
%patch547 -p1
%patch548 -p1
%patch579 -p1
%patch618 -p1
%patch717 -p1
%patch718 -p1
%patch719 -p1
%patch720 -p1
%patch721 -p1
%patch722 -p1
%patch723 -p1
%patch619 -p1
%patch627 -p1
%patch634 -p1
%patch643 -p1
%patch653 -p1
%patch657 -p1
%patch661 -p1
%patch690 -p1
%patch698 -p1
%patch703 -p1
%patch716 -p1
%patch726 -p1
%patch728 -p1
%patch729 -p1
%patch797 -p1
%patch798 -p1
%patch799 -p1
%patch800 -p1
%patch801 -p1
%patch802 -p1
%patch803 -p1
%patch804 -p1
%patch805 -p1
%patch806 -p1
%patch807 -p1
%patch808 -p1
%patch809 -p1
%patch810 -p1
%patch811 -p1
%patch812 -p1
%patch813 -p1
%patch814 -p1
%patch815 -p1
%patch816 -p1
%patch817 -p1
%patch818 -p1
%patch819 -p1

%patch1000 -p1 -b .rpm5~

cat > gdb/version.in << EOF
%{version}-%{release} (%{mdv_distro_version})
EOF

%build
%configure2_5x	--with-separate-debug-dir=%{_prefix}/lib/debug \
		--with-pythondir=%{_datadir}/gdb/python \
		--with-rpm \
		--with-expat \
		--disable-werror \
		--with-system-gdbinit=%{_sysconfdir}/gdbinit
%make
make info

%install
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/gdbinit.d
sed 's#%%{_sysconfdir}#%{_sysconfdir}#g' <%{SOURCE4} >%{buildroot}%{_sysconfdir}/gdbinit

# The above is broken, do this for now:
mkdir -p %{buildroot}%{_infodir}
cp `find . -name "*.info*"` %{buildroot}/%{_infodir}
rm -f %{buildroot}%{_infodir}/dir %{buildroot}%{_infodir}/dir.info* 
rm -f %{buildroot}%{_bindir}/{texindex,texi2dvi,makeinfo,install-info,info}

# These are part of binutils
rm -f %{buildroot}%{_infodir}/{bfd,standard,readline,history,info,texinfo}*
rm -fr %{buildroot}%{_includedir}
rm -fr %{buildroot}%{_libdir}/lib{bfd*,opcodes*,iberty*}

# Remove even more unpackaged files
rm -f %{buildroot}%{_libdir}/libmmalloc.a
rm -f %{buildroot}%{_infodir}/{configure,libiberty,rluserman}.info*
rm -rf %{buildroot}%{_datadir}/locale/
rm -f %{buildroot}%{_infodir}/annotate.info*

install -m644 %{SOURCE3} -D %{buildroot}%{_mandir}/man1/gstack.1

%files
%doc README gdb/NEWS
%{_bindir}/gdb
%{_bindir}/gdbserver
%{_bindir}/gstack
%ifarch %arm
%{_bindir}/run
%endif
%{_bindir}/gdb-add-index
%{_sysconfdir}/gdbinit
%{_sysconfdir}/gdbinit.d
%dir %{_datadir}/gdb
%{_datadir}/gdb/python
%{_datadir}/gdb/syscalls
%ifarch %{mips} %{arm}
%{_libdir}/lib*-mandriva-linux-gnu*-sim.a
%endif
%ifarch %{ix86} x86_64
%{_libdir}/libinproctrace.so
%endif
%{_mandir}/man1/gdb.1*
%ifarch %arm
%{_mandir}/man1/run.1*
%endif
%{_mandir}/man1/gdbserver.1*
%{_mandir}/man1/gstack.1*
%{_infodir}/gdb.info*
%{_infodir}/gdbint.info*
%{_infodir}/stabs.info*


%changelog
* Wed Jun 06 2012 Andrey Bondrov <abondrov@mandriva.org> 7.3.50.20110722-4
+ Revision: 802906
- Drop some legacy junk

* Sat Mar 17 2012 Per Ãyvind Karlsen <peroyvind@mandriva.org> 7.3.50.20110722-3
+ Revision: 785440
- debug packages has now '-debuginfo' as suffix, rather than '-debug'
- use pkgconfig() deps for buildrequires

* Tue Nov 29 2011 Per Ãyvind Karlsen <peroyvind@mandriva.org> 7.3.50.20110722-2
+ Revision: 735290
- enable P487

* Tue Nov 29 2011 Per Ãyvind Karlsen <peroyvind@mandriva.org> 7.3.50.20110722-1
+ Revision: 735285
- add gstack.1 man page
- remove legacy rpm stuff
- provide stub %%{_sysconfdir}/gdbinit (rhbz#651232)
- sync version & patches with gdb-7.3.50.20110722-11 from Fedora

  + Matthew Dawkins <mattydaw@mandriva.org>
    - added arm support
    - _gnu in arm is -gnueabi

* Sun May 08 2011 Funda Wang <fwang@mandriva.org> 7.1-5
+ Revision: 672383
- disable werror

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Sun Jan 09 2011 Per Ãyvind Karlsen <peroyvind@mandriva.org> 7.1-4mdv2011.0
+ Revision: 630736
- fix python 2.7 support (P1001)

* Sat Dec 04 2010 Per Ãyvind Karlsen <peroyvind@mandriva.org> 7.1-3mdv2011.0
+ Revision: 608927
- add versioned rpm-devel build requires
- port to rpm5 API (P1000)

* Sun Oct 31 2010 Funda Wang <fwang@mandriva.org> 7.1-2mdv2011.0
+ Revision: 590743
- rebuild for py2.7

* Fri Apr 16 2010 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 7.1-1mdv2010.1
+ Revision: 535538
- Updated gdb to version 7.1
- Sync Fedora patches with gdb-7.1-12.fc13
- Update buildid-locate-mandriva patch for new gdb.

* Fri Jan 15 2010 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 7.0.1-2mdv2010.1
+ Revision: 491836
- Make sure we always build with libexpat.

* Wed Jan 06 2010 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 7.0.1-1mdv2010.1
+ Revision: 486873
- Sync fedora patches with 7.0.1-19.fc12

  + Emmanuel Andry <eandry@mandriva.org>
    - New version 7.0.1
    - drop p232 (merged upstream)
    - BR libcloog-devel

* Fri Dec 18 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 7.0-1mdv2010.1
+ Revision: 479987
- Rediff fix-sim-build, buildid-locate-mandriva.
- Sync patches with Fedora gdb package (7.0-9.fc12).

  + Christophe Fergeau <cfergeau@mandriva.com>
    - upload gdb 7.0 tarball (still not building :-/)
    - readd patches I didn't mean to remove just yet
    - update to first 7.0 prerelease, still not working because of autoconf issues :(
    - rediff patches against new gdb tarball
      add gdb-6.6-buildid-locate-rpm.patch from fedora (they split gdb-6.6-buildid-locate.patch in 2 separate patches)
      comment out 2 patches that haven't been rediffed yet
    - fix patch comment to be in line with fedora .spec comment
    - pick attach-signalled patch from fedora to replace ours
    - drop no longer useful patch (after switch to gcc 4.4?)
    - Patch179 has been dropped from RedHat too
    - sync RedHat patches to latest version
    - remove no longer used patches
    - patch backporting upstream fixes is no longer necessary
    - drop patches that are no longer in fedora package
    - use 6.8.50 CVS snapshot instead of the old 6.8 release
    - fix Patch176 (depended on an ia64 patch)
    - Patch112 is needed by Patch141, readd it
    - remove obsolete patches
    - drop unused patches
    - fix cvs snapshot handling
    - delete dropped patches
    - drop ppc, ia64 and sparc patches

  + Olivier Blin <blino@mandriva.org>
    - add mips support (from Arnaud Patard)
    - fix a format error in sim-utils (from Arnaud Patard)

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 6.8-7mdv2010.0
+ Revision: 424577
- rebuild

* Mon Mar 23 2009 Paulo Andrade <pcpa@mandriva.com.br> 6.8-6mdv2009.1
+ Revision: 360759
- Correct #37755. See https://bugzilla.redhat.com/show_bug.cgi?id=453688#c3
  for more information. This basically allows 'valgrind --db-attach=yes' to
  work again, as this feature is missing since 2008.0. This patch is not
  fully correct as it depends on corrections in kernel code, but is enough
  to get gdb to stop at the proper moment memory corruption happened, and
  to allow checking contents of global and stack variables (of the current
  function, stack frame information is lost).

* Wed Jan 21 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 6.8-5mdv2009.1
+ Revision: 332266
- Really fix display of missing debug packages (#47170).

* Wed Jan 21 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 6.8-4mdv2009.1
+ Revision: 332195
- Fix display of missing debug packages (#47170).

* Tue Jan 20 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 6.8-3mdv2009.1
+ Revision: 332036
- Reset _default_patch_fuzz to 2 until patches are rediffed.
- Updated buildid-locate patch from Fedora (reported by Pixel).
- Redid buildid-locate-mandriva patch.
- Rediffed rpm5-compat patch.

  + Per Ãyvind Karlsen <peroyvind@mandriva.org>
    - add rpm5.org compatibility (P319)

* Sun Aug 24 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 6.8-2mdv2009.0
+ Revision: 275428
- Provide again gdbserver (#41257). For some unknown reason it was being
  removed on the spec, no explanation or changelog explaining this.

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - fix license

* Wed Jun 18 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 6.8-1mdv2009.0
+ Revision: 224207
- Add BuildRequires for librpm-devel
- Mandriva doesn't have debuginfo-install etc., quick adapt for
  buildid-locate patch from Fedora (we should stop to share/sync all
  patches...)
- Updated to version 6.8
- Removed already applied patches:
  gdb-6.6-makeinfoversion.patch
  gdb-6.6-do-not-crash-on-line-info-with-no-file.patch
- Sync fedora patches with their latest gdb package (gdb-6.8-10.fc10).

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 6.6-6mdv2009.0
+ Revision: 221044
- rebuild

* Mon Mar 31 2008 Pixel <pixel@mandriva.com> 6.6-5mdv2008.1
+ Revision: 191243
- fixes gdb crashing when using kdelibs-debug (#29755)
  (without this patch, kcrash/drkonqi fails with a weird error message)

  + Frederic Crozat <fcrozat@mandriva.com>
    - Patch235 (CVS): fix rebuild with latest makeinfo

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Mon Sep 10 2007 Adam Williamson <awilliamson@mandriva.org> 6.6-3mdv2008.0
+ Revision: 84260
- rediff patch234 (spaces vs. tabs...)
- better version of patch234
- add patch234 suggested by blino to fix a warning which breaks %%configure
- don't package COPYING and COPYING.LIB
- drop menu entries (#27065)
- Fedora license policy, correct license
- drop old (10.1) conditionals

  + Oden Eriksson <oeriksson@mandriva.com>
    - sync with gdb-6.6-1mdv2007.1.src.rpm


* Sun Jan 28 2007 Per Ãyvind Karlsen <pkarlsen@mandriva.com> 6.6-1mdv2007.0
+ Revision: 114460
- new release: 6.6
  sync with fedora
  fix prereq
- Import gdb

* Tue Sep 19 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 6.3-8mdv2007.0
- Rebuild

* Mon Jul 17 2006 Nicolas Lécureuil <neoclust@mandriva.org> 6.3-7mdv2007.0
- XDG

* Wed Oct 05 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 6.3-6mdk
- ppc64 fixes

* Mon Aug 01 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.3-5mdk
- add BuildRequires: bison

* Wed Jul 27 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 6.3-4mdk
- merge with RH 6.3.0.0-1.49

* Thu Jan 20 2005 Per Ãyvind Karlsen <peroyvind@linux-mandrake.com> 6.3-3mdk
- rebuild for new readline
- wipe out buildroot at the beginning of %%install

* Sun Nov 14 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.3-2mdk
- add BuildRequires: flex

* Wed Nov 10 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.3-1mdk
- 6.3

* Fri Aug 27 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.2-2mdk
- Improved i386 prologue analyzer from 6.2-branch (2004/07/08)

* Thu Aug 26 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.2-1mdk
- 6.2

* Sat Aug 14 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 6.1.1-2mdk
- Rebuild for new conversion table menu

* Sat Jul 31 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.1.1-1mdk
- package ppc-specific files
- 6.1.1

* Tue May 25 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.1-1mdk
- 6.1

