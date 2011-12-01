# Extract Mandriva Linux name and version
%define mdv_distro_version	%(perl -ne '/^([.\\w\\s]+) \\(.+\\).+/ and print $1' < /etc/release)

Summary:	A GNU source-level debugger for C, C++ and Fortran
Name:		gdb
Version:	7.3.50.20110722
Release:	2
License:	GPLv3+
Group:		Development/Other
URL:		http://www.gnu.org/software/gdb/
Source0:	gdb-%{version}%{?cvsdate:.%{cvsdate}}.tar.bz2
# Cleanup any leftover testsuite processes as it may stuck mock(1) builds.
#=push
Source2: gdb-orphanripper.c

# Man page for gstack(1).
#=push
Source3: gdb-gstack.man

# /etc/gdbinit (from Debian but with Fedora compliant location).
#=fedora
Source4: gdbinit

# libstdc++ pretty printers from GCC SVN HEAD (4.5 experimental).
%define libstdcxxpython libstdc++-v3-python-r155978
Source5: %{libstdcxxpython}.tar.bz2

# Fix sim build
Patch1:		gdb-fix-sim-build.patch

##
# Red Hat patches
##

# Work around out-of-date dejagnu that does not have KFAIL
#=drop: That dejagnu is too old to be supported.
Patch11: gdb-6.3-rh-dummykfail-20041202.patch

# Match the Fedora's version info.
#=fedora
Patch12: gdb-6.3-rh-testversion-20041202.patch

# Check that libunwind works - new test then fix
#=ia64
Patch13: gdb-6.3-rh-testlibunwind-20041202.patch

# Use convert_from_func_ptr_addr on the solib breakpoint address;
# simplifies and makes more consistent the logic.
#=maybepush+ppc: Write new testcase.
Patch104: gdb-6.3-ppcdotsolib-20041022.patch

# Better parse 64-bit PPC system call prologues.
#=maybepush+ppc: Write new testcase.
Patch105: gdb-6.3-ppc64syscall-20040622.patch

# Include the pc's section when doing a symbol lookup so that the
# correct symbol is found.
#=maybepush: Write new testcase.
Patch111: gdb-6.3-ppc64displaysymbol-20041124.patch

# Fix upstream `set scheduler-locking step' vs. upstream PPC atomic seqs.
#=maybepush+work: It is a bit difficult patch, a part is ppc specific.
Patch112: gdb-6.6-scheduler_locking-step-sw-watchpoints2.patch
# Make upstream `set scheduler-locking step' as default.
#=maybepush+work: How much is scheduler-locking relevant after non-stop?
Patch260: gdb-6.6-scheduler_locking-step-is-default.patch

# Add a wrapper script to GDB that implements pstack using the
# --readnever option.
#=push+work: with gdbindex maybe --readnever should no longer be used.
Patch118: gdb-6.3-gstack-20050411.patch

# VSYSCALL and PIE
#=fedoratest
Patch122: gdb-6.3-test-pie-20050107.patch
#=maybepush: May get obsoleted by Tom's unrelocated objfiles patch.
Patch389: gdb-archer-pie-addons.patch
#=push+work: Breakpoints disabling matching should not be based on address.
Patch394: gdb-archer-pie-addons-keep-disabled.patch

# Get selftest working with sep-debug-info
#=maybepush
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

# Stop while intentionally stepping and the thread exit is met.
#=push
Patch141: gdb-6.6-step-thread-exit.patch
#=push
Patch259: gdb-6.3-step-thread-exit-20050211-test.patch

# Test sibling threads to set threaded watchpoints for x86 and x86-64
#=fedoratest
Patch145: gdb-6.3-threaded-watchpoints2-20050225.patch

# Do not issue warning message about first page of storage for ia64 gcore
#=ia64
Patch153: gdb-6.3-ia64-gcore-page0-20050421.patch

# Security errata for untrusted .gdbinit
#=push
Patch157: gdb-6.3-security-errata-20050610.patch

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
#=fedoratest
Patch214: gdb-6.5-bz216711-clone-is-outermost.patch

# Test sideeffects of skipping ppc .so libs trampolines (BZ 218379).
#=fedoratest
Patch216: gdb-6.5-bz218379-ppc-solib-trampoline-test.patch

# Fix lockup on trampoline vs. its function lookup; unreproducible (BZ 218379).
#=push
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
#=push
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
#=push
Patch353: gdb-6.6-buildid-locate-rpm.patch
#=push
Patch415: gdb-6.6-buildid-locate-core-as-arg.patch
# Workaround librpm BZ 643031 due to its unexpected exit() calls (BZ 642879).
#=push
Patch519: gdb-6.6-buildid-locate-rpm-librpm-workaround.patch

# Fix displaying of numeric char arrays as strings (BZ 224128).
#=fedoratest: But it is failing anyway, one should check the behavior more.
Patch282: gdb-6.7-charsign-test.patch

# Test PPC hiding of call-volatile parameter register.
#=fedoratest+ppc
Patch284: gdb-6.7-ppc-clobbered-registers-O2-test.patch

# Testsuite fixes for more stable/comparable results.
#=push
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

# Create a single binary `gdb' autodetecting --tui by its argv[0].
#=push+work: IIRC Tom told argv[0] should not be used by GNU programs, also drop libgdb.a.
Patch326: gdb-6.8-tui-singlebinary.patch

# Fix PRPSINFO in the core files dumped by gcore (BZ 254229).
#=push
Patch329: gdb-6.8-bz254229-gcore-prpsinfo.patch

# Fix register assignments with no GDB stack frames (BZ 436037).
#=push+work: This fix is incorrect.
Patch330: gdb-6.8-bz436037-reg-no-longer-active.patch

# Make the GDB quit processing non-abortable to cleanup everything properly.
#=push: Useful only after gdb-6.8-attach-signalled-detach-stopped.patch .
Patch331: gdb-6.8-quit-never-aborts.patch

# Fix attaching to stopped processes and/or pending signals.
#=push+work
Patch337: gdb-6.8-attach-signalled-detach-stopped.patch

# Test the watchpoints conditionals works.
#=fedoratest
Patch343: gdb-6.8-watchpoint-conditionals-test.patch

# Fix resolving of variables at locations lists in prelinked libs (BZ 466901).
#=fedoratest
Patch348: gdb-6.8-bz466901-backtrace-full-prelinked.patch

# The merged branch `archer-jankratochvil-fedora15' of:
# http://sourceware.org/gdb/wiki/ProjectArcher
#=push
#archer-jankratochvil-vla
#=push
#archer-jankratochvil-watchpoint3
#=push
#archer-jankratochvil-ifunc
Patch349: gdb-archer.patch

# Fix parsing elf64-i386 files for kdump PAE vmcore dumps (BZ 457187).
# - Turn on 64-bit BFD support, globally enable AC_SYS_LARGEFILE.
#=fedoratest
Patch360: gdb-6.8-bz457187-largefile-test.patch

# New test for step-resume breakpoint placed in multiple threads at once.
#=fedoratest
Patch381: gdb-simultaneous-step-resume-breakpoint-test.patch

# Fix GNU/Linux core open: Can't read pathname for load map: Input/output error.
#=push+work: It should be in glibc: libc-alpha: <20091004161706.GA27450@.*>
Patch382: gdb-core-open-vdso-warning.patch

# Fix syscall restarts for amd64->i386 biarch.
#=push
Patch391: gdb-x86_64-i386-syscall-restart.patch

# Fix stepping with OMP parallel Fortran sections (BZ 533176).
#=push+work: It requires some better DWARF annotations.
Patch392: gdb-bz533176-fortran-omp-step.patch

# Use gfortran44 when running the testsuite on RHEL-5.
#=fedoratest
Patch393: gdb-rhel5-gcc44.patch

# Disable warning messages new for gdb-6.8+ for RHEL-5 backward compatibility.
# Workaround RHEL-5 kernels for detaching SIGSTOPped processes (BZ 498595).
#=fedoratest
Patch335: gdb-rhel5-compat.patch

# Fix regression by python on ia64 due to stale current frame.
#=push
Patch397: gdb-follow-child-stale-parent.patch

# Workaround ccache making lineno non-zero for command-line definitions.
#=drop: ccache is rarely used and it is even fixed now.
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

# Revert: Add -Wunused-function to compile flags.
#=drop
Patch412: gdb-unused-revert.patch

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

# Print 2D C++ vectors as matrices (BZ 562763, sourceware10659, Chris Moller).
#=push+work: There are some outstanding issues, check the mails.
Patch486: gdb-bz562763-pretty-print-2d-vectors.patch
#=push+work: There are some outstanding issues, check the mails.
Patch487: gdb-bz562763-pretty-print-2d-vectors-libstdcxx.patch

# [delayed-symfile] Test a backtrace regression on CFIs without DIE (BZ 614604).
#=fedoratest
Patch490: gdb-test-bt-cfi-without-die.patch

# Provide /usr/bin/gdb-add-index for rpm-build (Tom Tromey).
#=drop: Re-check against the upstream version.
Patch491: gdb-gdb-add-index-script.patch

# Out of memory is just an error, not fatal (uninitialized VLS vars, BZ 568248).
#=drop+work: Inferior objects should be read in parts, then this patch gets obsoleted.
Patch496: gdb-bz568248-oom-is-error.patch

# Fix gcore writer for -Wl,-z,relro (PR corefiles/11804).
#=push: There is different patch on gdb-patches, waiting now for resolution in kernel.
Patch504: gdb-bz623749-gcore-relro.patch

# Fix lost siginfo_t in linux-nat (BZ 592031).
#=push
Patch510: gdb-bz592031-siginfo-lost-4of5.patch
#=push
Patch511: gdb-bz592031-siginfo-lost-5of5.patch

# Verify GDB Python built-in function gdb.solib_address exists (BZ # 634108).
#=fedoratest
Patch526: gdb-bz634108-solib_address.patch

# New test gdb.arch/x86_64-pid0-core.exp for kernel PID 0 cores (BZ 611435).
#=fedoratest
Patch542: gdb-test-pid0-core.patch

# [archer-tromey-delayed-symfile] New test gdb.dwarf2/dw2-aranges.exp.
# =fedoratest
Patch547: gdb-test-dw2-aranges.patch

# [archer-keiths-expr-cumulative+upstream] Import C++ testcases.
# =fedoratest
Patch548: gdb-test-expr-cumulative-archer.patch

# Workaround gcc-4.6 stdarg false prologue end (GDB PR 12435 + GCC PR 47471).
# =push
Patch556: gdb-gcc46-stdarg-prologue.patch

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
Patch579: gdb-7.2.50-sparc-add-workaround-to-broken-debug-files.patch

# Improve GDB performance on inferior dlopen calls (Gary Benson, BZ 698001).
Patch617: gdb-dlopen-skip_inline_frames-perf.patch

# Fix dlopen of libpthread.so, patched glibc required (Gary Benson, BZ 669432).
Patch618: gdb-dlopen-stap-probe.patch
Patch619: gdb-dlopen-stap-probe-test.patch

# Work around PR libc/13097 "linux-vdso.so.1" warning message.
Patch627: gdb-glibc-vdso-workaround.patch

# [TUI] Fix stepi on stripped code.
Patch628: gdb-tui-strip-stepi.patch

# [vla] Fix VLA arrays displayed in `bt full' (BZ 738482).
Patch629: gdb-vla-frame-set.patch

# Fix DW_OP_GNU_implicit_pointer for DWARF32 v3+ on 64-bit arches.
Patch630: gdb-implptr-64bit-1of2.patch
Patch631: gdb-implptr-64bit-2of2.patch

# Fix internal error on some optimized-out values.
Patch632: gdb-optimized-out-internal-error.patch

# Hack for proper PIE run of the testsuite.
Patch634: gdb-runtest-pie-override.patch

Patch1000: gdb-7.3.50.20110722-rpm5.patch

Requires(post):	info-install
Requires(preun):	info-install
BuildRequires:	bison
Buildrequires:	cloog-ppl-devel
BuildRequires:	flex
BuildRequires:	ncurses-devel
BuildRequires:	libexpat-devel
BuildRequires:	libpython-devel
BuildRequires:	librpm-devel >= 1:5.3
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
%setup -q -n %{name}-%{version}%{?cvsdate:.%{cvsdate}} -a5
%patch1 -p1

%patch12 -p1

%patch232 -p1
%patch349 -p1
%patch11 -p1
%patch13 -p1

%patch104 -p1
%patch105 -p1
%patch111 -p1
%patch112 -p1
%patch118 -p1
%patch122 -p1
%patch125 -p1
%patch133 -p1
%patch136 -p1
%patch140 -p1
%patch141 -p1
%patch259 -p1
%patch145 -p1
%patch153 -p1
%patch157 -p1
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
%patch353 -p1
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
%patch326 -p1
%patch329 -p1
%patch330 -p1
%patch331 -p1
%patch337 -p1
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
%patch412 -p1
%patch417 -p1
%patch459 -p1
%patch470 -p1
%patch475 -p1
%patch486 -p1
%patch415 -p1
%patch519 -p1
%patch490 -p1
%patch491 -p1
%patch496 -p1
%patch504 -p1
%patch510 -p1
%patch511 -p1
%patch526 -p1
%patch542 -p1
%patch547 -p1
%patch548 -p1
%patch556 -p1
%patch579 -p1
%patch617 -p1
%patch618 -p1
%patch619 -p1
%patch627 -p1
%patch628 -p1
%patch629 -p1
%patch630 -p1
%patch631 -p1
%patch632 -p1
%patch634 -p1

%patch393 -p1
%patch335 -p1
%patch487 -p1

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

%post
%{_install_info gdb.info}
%{_install_info gdbint.info}
%{_install_info stabs.info}

%preun
if [ $1 = 0 ]; then
%{_remove_install_info gdb.info}
%{_remove_install_info gdbint.info}
%{_remove_install_info stabs.info}
fi

%files
%doc README gdb/NEWS
%{_bindir}/gdb
%{_bindir}/gdbserver
%{_bindir}/gdbtui
%{_bindir}/gstack
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
%{_mandir}/man1/gdbserver.1*
%{_mandir}/man1/gdbtui.1*
%{_mandir}/man1/gstack.1*
%{_infodir}/gdb.info*
%{_infodir}/gdbint.info*
%{_infodir}/stabs.info*
