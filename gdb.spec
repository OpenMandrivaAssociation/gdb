%define name	gdb
%define version	6.8
%define release	%mkrel 1
#define cvsdate	20040708

# Extract Mandriva Linux name and version
%define mdv_distro_version	%(perl -ne '/^([.\\w\\s]+) \\(.+\\).+/ and print $1' < /etc/release)

Summary:	A GNU source-level debugger for C, C++ and Fortran
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+ and LGPLv2+
Group:		Development/Other
URL:		http://www.gnu.org/software/gdb/
Source:		gdb-%{version}%{?cvsdate:-%{cvsdate}}.tar.bz2

# Fixes a warning (which is treated as an error) in tekhex.c, breaking
# configure. Fix by blino. - AdamW 2007/09
Patch0: gdb-6.6-tekhex_warning_fix.patch

# Fix sim build
Patch1:		gdb-5.2.1-fix-sim-build.patch
Patch2:		gdb-6.3-system-readline.patch
Patch3:		gdb-6.0-tracepoint.patch

##
# Red Hat patches
##

# Work around out-of-date dejagnu that does not have KFAIL
Patch11: gdb-6.3-rh-dummykfail-20041202.patch

# Match Red Hat's version info
Patch12: gdb-6.3-rh-testversion-20041202.patch

# Check that libunwind works - new test then fix
Patch13: gdb-6.3-rh-testlibunwind-20041202.patch
Patch14: gdb-6.3-rh-testlibunwind1fix-20041202.patch

# Recognize i386 signal trampolines before CFI.  Ensures that signal
# frames are identified as signal frames.
Patch101: gdb-6.3-sigx86-20040621.patch

# Use convert_from_func_ptr_addr on the solib breakpoint address;
# simplifies and makes more consistent the logic.
Patch104: gdb-6.3-ppcdotsolib-20041022.patch

# Better parse 64-bit PPC system call prologues.
Patch105: gdb-6.3-ppc64syscall-20040622.patch

# Stop a backtrace when a zero PC is encountered.
Patch106: gdb-6.3-framepczero-20040927.patch

# Include the pc's section when doing a symbol lookup so that the
# correct symbol is found.
Patch111: gdb-6.3-ppc64displaysymbol-20041124.patch

# Fix upstream `set scheduler-locking step' vs. upstream PPC atomic seqs.
Patch112: gdb-6.6-scheduler_locking-step-sw-watchpoints2.patch
# Make upstream `set scheduler-locking step' as default.
Patch260: gdb-6.6-scheduler_locking-step-is-default.patch

# Continue removing breakpoints even when failure occurs.
Patch117: gdb-6.3-removebp-20041130.patch

# Add a wrapper script to GDB that implements pstack using the
# --readnever option.
Patch118: gdb-6.3-gstack-20050411.patch

# Fix to ensure types are visible
Patch120: gdb-6.3-type-fix-20041213.patch

# VSYSCALL and PIE
Patch124: gdb-6.3-pie-20050110.patch

# Get selftest working with sep-debug-info
Patch125: gdb-6.3-test-self-20050110.patch

# Fix for non-threaded watchpoints.
Patch128: gdb-6.3-nonthreaded-wp-20050117.patch

# Fix to support executable moving
Patch136: gdb-6.3-test-movedir-20050125.patch

# Tolerate DW_AT_type referencing <0>.
Patch139: gdb-6.3-dwattype0-20050201.patch

# Fix gcore for threads
Patch140: gdb-6.3-gcore-thread-20050204.patch

# Fix stepping over thread exit
Patch141: gdb-6.6-step-thread-exit.patch
Patch259: gdb-6.3-step-thread-exit-20050211-test.patch

# Prevent gdb from being pushed into background
Patch142: gdb-6.3-terminal-fix-20050214.patch

# Fix unexpected compiler warning messages.
Patch147: gdb-6.3-warnings-20050317.patch

# Fix printing of inherited members
Patch148: gdb-6.3-inheritance-20050324.patch

# Print a warning when the separate debug info's CRC doesn't match.
Patch150: gdb-6.3-test-sepcrc-20050402.patch
Patch151: gdb-6.3-sepcrc-20050402.patch

# Do not issue warning message about first page of storage for ia64 gcore
Patch153: gdb-6.3-ia64-gcore-page0-20050421.patch

# Security errata for bfd overflow and untrusted .gdbinit
Patch157: gdb-6.3-security-errata-20050610.patch

# IA64 sigtramp prev register patch
Patch158: gdb-6.3-ia64-sigtramp-frame-20050708.patch

# IA64 gcore speed-up patch
Patch160: gdb-6.3-ia64-gcore-speedup-20050714.patch

# Notify observers that the inferior has been created
Patch161: gdb-6.3-inferior-notification-20050721.patch

# Fix ia64 info frame bug
Patch162: gdb-6.3-ia64-info-frame-fix-20050725.patch

# Verify printing of inherited members test
Patch163: gdb-6.3-inheritancetest-20050726.patch

# Add readnever option
Patch164: gdb-6.3-readnever-20050907.patch

# Fix frame pointer for ia64 sigtramp frame
Patch166: gdb-6.3-ia64-sigtramp-fp-20050926.patch

# Fix ia64 gdb problem with user-specified SIGILL handling
Patch169: gdb-6.3-ia64-sigill-20051115.patch

# Allow option to continue backtracing past a zero pc value
Patch170: gdb-6.3-bt-past-zero-20051201.patch

# Use bigger numbers than int.
Patch176: gdb-6.3-large-core-20051206.patch

# Hard-code executable names in gstack, such that it can run with a
# corrupted or missing PATH.
Patch177: gdb-6.3-gstack-without-path-20060414.patch

# Do not let errors related with debug registers break thread debugging.
Patch178: gdb-6.3-catch-debug-registers-error-20060527.patch

# Cope with waitpid modifying status even when returning zero, as on
# ia32el.
Patch179: gdb-6.3-ia32el-fix-waitpid-20060615.patch

# Testcase for corrupted or missing location list information (BZ 196439).
Patch187: gdb-6.5-bz196439-valgrind-memcheck-compat-test.patch

# Fix debuginfo addresses resolving for --emit-relocs Linux kernels (BZ 203661).
Patch188: gdb-6.5-bz203661-emit-relocs.patch

# Security patch: avoid stack overflows in dwarf expression computation.
# CVE-2006-4146
Patch190: gdb-6.5-dwarf-stack-overflow.patch

# Support TLS symbols (+`errno' suggestion if no pthread is found) (BZ 185337).
Patch194: gdb-6.5-bz185337-resolve-tls-without-debuginfo-v2.patch

# Fix TLS symbols resolving for objects with separate .debug file (-debuginfo).
Patch195: gdb-6.5-tls-of-separate-debuginfo.patch

# Fix TLS symbols resolving for shared libraries with a relative pathname.
# The testsuite needs `gdb-6.5-tls-of-separate-debuginfo.patch'.
Patch196: gdb-6.5-sharedlibrary-path.patch

# Suggest fixing your target architecture for gdbserver(1) (BZ 190810).
# FIXME: It could be autodetected.
Patch199: gdb-6.5-bz190810-gdbserver-arch-advice.patch

# Fix dereferencing registers for 32bit inferiors on 64bit hosts (BZ 181390).
Patch200: gdb-6.5-bz181390-memory-address-width.patch

# Fix `gcore' command for 32bit inferiors on 64bit hosts.
Patch201: gdb-6.5-gcore-i386-on-amd64.patch

# Testcase for deadlocking on last address space byte; for corrupted backtraces.
Patch211: gdb-6.5-last-address-space-byte-test.patch

# Improved testsuite results by the testsuite provided by the courtesy of BEA.
Patch208: gdb-6.5-BEA-testsuite.patch

# Fix readline segfault on excessively long hand-typed lines.
Patch209: gdb-6.5-readline-long-line-crash.patch
Patch213: gdb-6.5-readline-long-line-crash-test.patch

# Fix bogus 0x0 unwind of the thread's topmost function clone(3) (BZ 216711).
Patch214: gdb-6.5-bz216711-clone-is-outermost.patch

# Try to reduce sideeffects of skipping ppc .so libs trampolines (BZ 218379).
Patch215: gdb-6.5-bz218379-ppc-solib-trampoline-fix.patch
Patch216: gdb-6.5-bz218379-ppc-solib-trampoline-test.patch

# Fix lockup on trampoline vs. its function lookup; unreproducible (BZ 218379).
Patch217: gdb-6.5-bz218379-solib-trampoline-lookup-lock-fix.patch

# Find symbols properly at their original (included) file (BZ 109921).
Patch225: gdb-6.5-bz109921-DW_AT_decl_file-test.patch

# Update PPC unwinding patches to their upstream variants (BZ 140532).
Patch229: gdb-6.3-bz140532-ppc-unwinding-test.patch

# Testcase for exec() from threaded program (BZ 202689).
Patch231: gdb-6.3-bz202689-exec-from-pthread-test.patch

# Backported post gdb-6.8 release fixups.
Patch232: gdb-6.8-upstream.patch

# Testcase for PPC Power6/DFP instructions disassembly (BZ 230000).
Patch234: gdb-6.6-bz230000-power6-disassembly-test.patch

# Temporary support for shared libraries >2GB on 64bit hosts (BZ 231832).
Patch235: gdb-6.3-bz231832-obstack-2gb.patch

# Fix prelink(8) testcase for non-root $PATH missing `/usr/sbin' (BZ 225783).
Patch240: gdb-6.6-bz225783-prelink-path.patch

# Fix debugging GDB itself - the compiled in source files paths (BZ 225783).
Patch241: gdb-6.6-bz225783-gdb-debuginfo-paths.patch

# Allow running `/usr/bin/gcore' with provided but inaccessible tty (BZ 229517).
Patch245: gdb-6.6-bz229517-gcore-without-terminal.patch

# Notify user of a child forked process being detached (BZ 235197).
Patch247: gdb-6.6-bz235197-fork-detach-info.patch

# New testcase for gcore of 32bit inferiors on 64bit hosts.
Patch249: gdb-6.6-gcore32-test.patch

# Avoid too long timeouts on failing cases of "annota1.exp annota3.exp".
Patch254: gdb-6.6-testsuite-timeouts.patch

# Fix attaching to stopped processes (BZ 219118, 233852).
# Fix attaching during a pending signal being delivered.
Patch256: gdb-6.7-bz233852-attach-signalled-fix.patch
Patch275: gdb-6.7-bz233852-attach-signalled-test.patch

# Support for stepping over PPC atomic instruction sequences (BZ 237572).
Patch258: gdb-6.6-bz237572-ppc-atomic-sequence-test.patch

# Link with libreadline provided by the operating system.
Patch261: gdb-6.6-readline-system.patch

# Test kernel VDSO decoding while attaching to an i386 process.
Patch263: gdb-6.3-attach-see-vdso-test.patch

# Do not hang on exit of a thread group leader (BZ 247354).
Patch265: gdb-6.6-bz247354-leader-exit-fix.patch
Patch266: gdb-6.6-bz247354-leader-exit-test.patch

# New locating of the matching binaries from the pure core file (build-id).
Patch274: gdb-6.6-buildid-locate.patch
# Mandriva doesn't have debuginfo-install etc., adapt
Patch276: gdb-6.8-buildid-locate-mandriva.patch

# Fixed the kernel i386-on-x86_64 VDSO loading (producing `Lowest section in').
Patch277: gdb-6.6-vdso-i386-on-amd64-warning.patch

# Fix hardware watchpoints after inferior forks-off some process.
# Threaded `set follow-fork-mode child' still not fixed there, glibc fixes reqd.
# `set detach-on-fork off' not fixed there in general - it already assert-fails.
Patch280: gdb-6.6-multifork-debugreg.patch

# Fix displaying of numeric char arrays as strings (BZ 224128).
Patch282: gdb-6.7-charsign-test.patch

# Fix rereading of the main executable on its change.
Patch283: gdb-6.7-reread-exec_bfd.patch

# Test PPC hiding of call-volatile parameter register.
Patch284: gdb-6.7-ppc-clobbered-registers-O2-test.patch

# Testsuite fixes for more stable/comparable results.
Patch287: gdb-6.7-testsuite-stable-results.patch

# Test ia64 memory leaks of the code using libunwind.
Patch289: gdb-6.5-ia64-libunwind-leak-test.patch

# Test hiding unexpected breakpoints on intentional step commands.
Patch290: gdb-6.5-missed-trap-on-step-test.patch

# Support DW_TAG_interface_type the same way as DW_TAG_class_type (BZ 426600).
Patch293: gdb-6.7-bz426600-DW_TAG_interface_type-fix.patch
Patch294: gdb-6.7-bz426600-DW_TAG_interface_type-test.patch

# Test gcore memory and time requirements for large inferiors.
Patch296: gdb-6.5-gcore-buffer-limit-test.patch

# Test debugging statically linked threaded inferiors (BZ 239652).
#  - It requires recent glibc to work in this case properly.
Patch298: gdb-6.6-threads-static-test.patch

# Fix false `(no debugging symbols found)' on `-readnever' runs.
Patch301: gdb-6.6-buildid-readnever-silent.patch

# Fix #include <asm/ptrace.h> on kernel-headers-2.6.25-0.40.rc1.git2.fc9.x86_64.
Patch304: gdb-6.7-kernel-headers-compat.patch

# Fix/implement the Fortran dynamic arrays support (BZ 377541).
Patch305: gdb-6.8-bz377541-fortran-dynamic-arrays.patch

# Backport fix of a segfault + PIE regression since 6.7.1 on PIE executables.
Patch306: gdb-6.8-watchpoint-inaccessible-memory.patch

# Test GCORE for shmid 0 shared memory mappings.
Patch309: gdb-6.3-mapping-zero-inode-test.patch

# Test a crash on `focus cmd', `focus prev' commands.
Patch311: gdb-6.3-focus-cmd-prev-test.patch

# Test crash on a sw watchpoint condition getting out of the scope.
Patch314: gdb-6.3-watchpoint-cond-gone-test.patch

# Test various forms of threads tracking across exec() (BZ 442765).
Patch315: gdb-6.8-bz442765-threaded-exec-test.patch

# Enable program counter for processing PTID to PC (sparc/sparc64)
Patch316: gdb-6.8-sparc-fix.patch

# Silence memcpy check which returns false positive (sparc64)
Patch317: gdb-6.8-sparc64-silence-memcpy-check.patch

# Fix memory trashing on binaries from GCC Ada (workaround GCC PR 35998).
Patch318: gdb-6.8-gcc35998-ada-memory-trash.patch

Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires(post):	info-install
Requires(preun):	info-install
BuildRequires:	ncurses-devel readline-devel texinfo flex bison

%description
Gdb is a full featured, command driven debugger. Gdb allows you to
trace the execution of programs and examine their internal state at
any time.  Gdb works for C and C++ compiled with the GNU C compiler
gcc.

If you are going to develop C and/or C++ programs and use the GNU gcc
compiler, you may want to install gdb to help you debug your programs.

%prep
%setup -q
%patch232 -p1
%patch0 -p1
%patch1 -p1 -b .sim-fixes
#%patch2 -p1 -b .system-readline
#%patch3 -p1 -b .tracepoint
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

%patch101 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch111 -p1
%patch112 -p1
%patch117 -p1
%patch118 -p1
%patch120 -p1
%patch125 -p1
%patch128 -p1
%patch136 -p1
%patch139 -p1
%patch140 -p1
%patch141 -p1
%patch259 -p1
%patch142 -p1
%patch147 -p1
%patch148 -p1
%patch150 -p1
%patch151 -p1
%patch153 -p1
%patch157 -p1
%patch158 -p1
%patch160 -p1
%patch161 -p1
%patch162 -p1
%patch163 -p1
%patch164 -p1
%patch166 -p1
%patch169 -p1
%patch170 -p1
%patch176 -p1
%patch177 -p1
%patch178 -p1
%patch179 -p1
%patch187 -p1
%patch188 -p1
%patch190 -p1
%patch194 -p1
%patch195 -p1
%patch196 -p1
%patch199 -p1
%patch200 -p1
%patch201 -p1
%patch208 -p1
%patch209 -p1
%patch211 -p1
%patch213 -p1
%patch214 -p1
%patch215 -p1
%patch216 -p1
%patch217 -p1
%patch225 -p1
%patch229 -p1
%patch231 -p1
%patch234 -p1
%patch235 -p1
%patch240 -p1
%patch241 -p1
%patch245 -p1
%patch247 -p1
%patch249 -p1
%patch254 -p1
%patch256 -p1
%patch258 -p1
%patch260 -p1
%patch261 -p1
%patch263 -p1
%patch265 -p1
%patch266 -p1
%patch274 -p1
%patch275 -p1
%patch276 -p1
%patch277 -p1
%patch280 -p1
%patch282 -p1
%patch283 -p1
%patch284 -p1
%patch287 -p1
%patch289 -p1
%patch290 -p1
%patch293 -p1
%patch294 -p1
%patch296 -p1
%patch298 -p1
%patch301 -p1
%patch304 -p1
%patch305 -p1
%patch306 -p1
%patch309 -p1
%patch311 -p1
%patch314 -p1
%patch315 -p1
%patch316 -p1
%patch317 -p1
%patch318 -p1
%patch124 -p1

rm -rf ./gdb/gdbserver

cat > gdb/version.in << EOF
%{version}-%{release} (%{mdv_distro_version})
EOF

%build
%configure2_5x --with-separate-debug-dir=%{_prefix}/lib/debug
%make
make info

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# The above is broken, do this for now:
mkdir -p $RPM_BUILD_ROOT/%{_infodir}
cp `find . -name "*.info*"` $RPM_BUILD_ROOT/%{_infodir}
rm -f $RPM_BUILD_ROOT%{_infodir}/dir $RPM_BUILD_ROOT%{_infodir}/dir.info* 
rm -f $RPM_BUILD_ROOT%{_bindir}/{texindex,texi2dvi,makeinfo,install-info,info}

# These are part of binutils
rm -f $RPM_BUILD_ROOT%{_infodir}/{bfd,standard,readline,history,info,texinfo}*
rm -fr $RPM_BUILD_ROOT%{_includedir}
rm -fr $RPM_BUILD_ROOT%{_libdir}/lib{bfd*,opcodes*,iberty*}

# Remove even more unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/libmmalloc.a
rm -f $RPM_BUILD_ROOT%{_infodir}/{configure,libiberty,rluserman}.info*
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/
rm -f $RPM_BUILD_ROOT%{_infodir}/annotate.info*

%clean
rm -fr $RPM_BUILD_ROOT

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
%defattr(-,root,root)
%doc README gdb/NEWS
%{_bindir}/gdb
%{_bindir}/gdbtui
%{_bindir}/gstack
%ifarch ppc ppc64
%{_bindir}/run
%{_mandir}/man1/run.1*
%endif
%{_mandir}/man1/gdb.1*
%{_mandir}/man1/gdbtui.1*
%{_infodir}/gdb.info*
%{_infodir}/gdbint.info*
%{_infodir}/stabs.info*

