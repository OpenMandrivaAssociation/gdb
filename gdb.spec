# RH 6.3.0.0-1.49
%define name	gdb
%define version	6.6
%define release	%mkrel 4
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
# Fix sim build
Patch1:		gdb-5.2.1-fix-sim-build.patch
Patch2:		gdb-6.3-system-readline.patch
Patch3:		gdb-6.0-tracepoint.patch

##
# Red Hat patches
##

Patch10: gdb-6.3-rh-changelogs-20041202.patch

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

# Pass the pc's section into the symbol search code; stops the lookup
# finding a symbol from the wrong section.
Patch108: gdb-6.3-ppc64section-20041026.patch

# Include the pc's section when doing a symbol lookup so that the
# correct symbol is found.
Patch111: gdb-6.3-ppc64displaysymbol-20041124.patch

# Fix stepping in threads
Patch112: gdb-6.3-thread-step-20041207.patch

# Threaded watchpoint support
Patch113: gdb-6.3-threaded-watchpoints-20041213.patch

# Fix to expose multiple constructors to end-user
Patch115: gdb-6.3-constructor-20041216.patch

# Fix to display base constructors from list and breakpoint commands
Patch116: gdb-6.3-linespec-20041213.patch

# Continue removing breakpoints even when failure occurs.
Patch117: gdb-6.3-removebp-20041130.patch

# Add a wrapper script to GDB that implements pstack using the
# --readnever option.
Patch118: gdb-6.3-gstack-20050411.patch

# Fix for caching thread lwps for linux
Patch119: gdb-6.3-lwp-cache-20041216.patch

# Fix to ensure types are visible
Patch120: gdb-6.3-type-fix-20041213.patch

# VSYSCALL and PIE
Patch122: gdb-6.3-test-pie-20050107.patch
Patch124: gdb-6.3-pie-20050110.patch

# Get selftest working with sep-debug-info
Patch125: gdb-6.3-test-self-20050110.patch

# Fix for non-threaded watchpoints.
Patch128: gdb-6.3-nonthreaded-wp-20050117.patch

# Add PPC .symbols to min-symtable.
Patch130: gdb-6.3-ctorline-20050120.patch

# Fix to support multiple destructors just like multiple constructors
Patch133: gdb-6.3-test-dtorfix-20050121.patch
Patch134: gdb-6.3-dtorfix-20050121.patch

# Fix to support executable moving
Patch136: gdb-6.3-test-movedir-20050125.patch

# Fix to support unwinding syscalls in ia64 corefiles
# Patch138: gdb-6.3-ia64-corefile-fix-20050127.patch

# Tolerate DW_AT_type referencing <0>.
Patch139: gdb-6.3-dwattype0-20050201.patch

# Fix gcore for threads
Patch140: gdb-6.3-gcore-thread-20050204.patch

# Fix stepping over thread exit
Patch141: gdb-6.3-step-thread-exit-20050211.patch

# Prevent gdb from being pushed into background
Patch142: gdb-6.3-terminal-fix-20050214.patch

# Allow sibling threads to set threaded watchpoints for x86 and x86-64
Patch145: gdb-6.3-threaded-watchpoints2-20050225.patch

# Fix unexpected compiler warning messages.
Patch147: gdb-6.3-warnings-20050317.patch

# Fix printing of inherited members
Patch148: gdb-6.3-inheritance-20050324.patch

# Add vsyscall page support for ia64.
Patch149: gdb-6.3-ia64-vsyscall-20050330.patch

# Print a warning when the separate debug info's CRC doesn't match.
Patch150: gdb-6.3-test-sepcrc-20050402.patch
Patch151: gdb-6.3-sepcrc-20050402.patch

# Do not issue warning message about first page of storage for ia64 gcore
Patch153: gdb-6.3-ia64-gcore-page0-20050421.patch

# Security errata for bfd overflow and untrusted .gdbinit
Patch157: gdb-6.3-security-errata-20050610.patch

# IA64 sigtramp prev register patch
Patch158: gdb-6.3-ia64-sigtramp-frame-20050708.patch

# IA64 sigaltstack patch
Patch159: gdb-6.3-ia64-sigaltstack-20050711.patch

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

# Remove extraneous xfree
Patch165: gdb-6.3-xfree-20050922.patch

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

# Bugfix segv on the source display by ^X 1 (fixes Patch130, BZ 200048).
Patch181: gdb-6.5-bz200048-find_line_pc-segv.patch

# Bugfix object names completion (fixes Patch116, BZ 193763).
Patch185: gdb-6.3-bz193763-object-name-completion.patch

# Testcase for corrupted or missing location list information (BZ 196439).
Patch187: gdb-6.5-bz196439-valgrind-memcheck-compat-test.patch

# Fix debuginfo addresses resolving for --emit-relocs Linux kernels (BZ 203661).
Patch188: gdb-6.5-bz203661-emit-relocs.patch

# Security patch: avoid stack overflows in dwarf expression computation.
# CVE-2006-4146
Patch190: gdb-6.5-dwarf-stack-overflow.patch

# Fix gdb printf command argument using "%p" (BZ 205551).
Patch191: gdb-6.5-bz205551-printf-p.patch

# Fix attach to stopped process, supersede `gdb-6.3-attach-stop-20051011.patch'.
# Fix attachment also to a threaded stopped process (BZ 219118).
Patch193: gdb-6.5-attach-stop.patch

# Support TLS symbols (+`errno' suggestion if no pthread is found) (BZ 185337).
# FIXME: Still to be updated.
Patch194: gdb-6.5-bz185337-resolve-tls-without-debuginfo-v2.patch

# Fix TLS symbols resolving for objects with separate .debug file (-debuginfo).
Patch195: gdb-6.5-tls-of-separate-debuginfo.patch

# Fix TLS symbols resolving for shared libraries with a relative pathname.
# The testsuite needs `gdb-6.5-tls-of-separate-debuginfo.patch'.
Patch196: gdb-6.5-sharedlibrary-path.patch

# Support IPv6 for gdbserver (BZ 198365).
Patch197: gdb-6.5-bz198365-IPv6.patch

# Suggest fixing your target architecture for gdbserver(1) (BZ 190810).
# FIXME: It could be autodetected.
Patch199: gdb-6.5-bz190810-gdbserver-arch-advice.patch

# Fix dereferencing registers for 32bit inferiors on 64bit hosts (BZ 181390).
Patch200: gdb-6.5-bz181390-memory-address-width.patch

# Fix `gcore' command for 32bit inferiors on 64bit hosts.
Patch201: gdb-6.5-gcore-i386-on-amd64.patch

# Testcase for deadlocking on last address space byte; for corrupted backtraces.
Patch211: gdb-6.5-last-address-space-byte-test.patch

# Fix "??" resolving of symbols from (non-prelinked) debuginfo packages.
Patch206: gdb-6.5-relativedebug.patch

# Fix "??" resolving of symbols from overlapping functions (nanosleep(3)).
Patch207: gdb-6.5-symbols-overlap.patch

# Improved testsuite results by the testsuite provided by the courtesy of BEA.
Patch208: gdb-6.5-BEA-testsuite.patch

# Fix readline segfault on excessively long hand-typed lines.
Patch209: gdb-6.5-readline-long-line-crash.patch
Patch213: gdb-6.5-readline-long-line-crash-test.patch

# Fix readline history for input mode commands like `command' (BZ 215816).
Patch212: gdb-6.5-bz215816-readline-from-callback.patch
Patch219: gdb-6.5-bz215816-readline-from-callback-test.patch

# Fix bogus 0x0 unwind of the thread's topmost function clone(3) (BZ 216711).
Patch214: gdb-6.5-bz216711-clone-is-outermost.patch

# Try to reduce sideeffects of skipping ppc .so libs trampolines (BZ 218379).
Patch215: gdb-6.5-bz218379-ppc-solib-trampoline-fix.patch
Patch216: gdb-6.5-bz218379-ppc-solib-trampoline-test.patch

# Fix lockup on trampoline vs. its function lookup; unreproducible (BZ 218379).
Patch217: gdb-6.5-bz218379-solib-trampoline-lookup-lock-fix.patch

# Fix unwinding crash on older gcj(1) code (extended CFI support) (BZ 165025).
Patch221: gdb-6.5-bz165025-DW_CFA_GNU_negative_offset_extended-fix.patch
Patch222: gdb-6.5-bz165025-DW_CFA_GNU_negative_offset_extended-test.patch

# Find symbols properly at their original (included) file (BZ 109921).
Patch224: gdb-6.5-bz109921-DW_AT_decl_file-fix.patch
Patch225: gdb-6.5-bz109921-DW_AT_decl_file-test.patch

# Fix unwinding of non-CFI (w/o debuginfo) PPC code by recent GCC (BZ 140532).
Patch226: gdb-6.3-bz140532-ppcnoncfi-skip_prologue-PIC.patch
# Fix unwinding of non-debug (.eh_frame) PPC code, Andreas Schwab (BZ 140532).
Patch227: gdb-6.5-bz140532-ppc-eh_frame-regnum.patch
# Fix unwinding of debug (.debug_frame) PPC code, workaround GCC (BZ 140532).
Patch228: gdb-6.5-bz140532-ppc-debug_frame-return_address.patch
Patch229: gdb-6.5-bz140532-ppc-debug_frame-return_address-test.patch

# Fix missing testsuite .log output of testcases using get_compiler_info().
Patch230: gdb-6.5-testsuite-log.patch

# Testcase for exec() from threaded program (BZ 202689).
Patch231: gdb-6.3-bz202689-exec-from-pthread-test.patch

# Backported post gdb-6.6 release ia64 unwinding fixups.
Patch232: gdb-6.6-ia64-kernel-unwind.patch
Patch233: gdb-6.6-ia64-pc-unwind.patch

# Fixes a warning (which is treated as an error) in tekhex.c, breaking
# configure. Fix by blino. - AdamW 2007/09
Patch234: gdb-6.6-tekhex_warning_fix.patch
# (fc) 6.6-4mdv fix build with latest makeinfo (CVS)
Patch235: gdb-6.6-makeinfoversion.patch

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
%patch1 -p1 -b .sim-fixes
#%patch2 -p1 -b .system-readline
#%patch3 -p1 -b .tracepoint
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

%patch101 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch108 -p1
%patch111 -p1
%patch112 -p1
%patch113 -p1
%patch115 -p1
%patch116 -p1
%patch117 -p1
%patch118 -p1
%patch119 -p1
%patch120 -p1
%patch122 -p1
%patch124 -p1
%patch125 -p1
%patch128 -p1
%patch130 -p1
%patch133 -p1
%patch134 -p1
%patch136 -p1
%patch139 -p1
%patch140 -p1
%patch141 -p1
%patch142 -p1
%patch145 -p1
%patch147 -p1
%patch148 -p1
%patch149 -p1
%patch150 -p1
%patch151 -p1
%patch153 -p1
%patch157 -p1
%patch158 -p1
%patch159 -p1
%patch160 -p1
%patch161 -p1
%patch162 -p1
%patch163 -p1
%patch164 -p1
%patch165 -p1
%patch166 -p1
%patch169 -p1
%patch170 -p1
%patch176 -p1
%patch177 -p1
%patch178 -p1
%patch179 -p1
%patch181 -p1
%patch185 -p1
%patch187 -p1
%patch188 -p1
%patch190 -p1
%patch191 -p1
%patch193 -p1
%patch194 -p1
%patch195 -p1
%patch196 -p1
#%patch197 -p1
%patch199 -p1
%patch200 -p1
%patch201 -p1
%patch206 -p1
%patch207 -p1
%patch208 -p1
%patch209 -p1
%patch211 -p1
%patch212 -p1
%patch213 -p1
%patch214 -p1
%patch215 -p1
%patch216 -p1
%patch217 -p1
%patch219 -p1
%patch221 -p1
%patch222 -p1
%patch224 -p1
%patch225 -p1
%patch226 -p1
%patch227 -p1
%patch228 -p1
%patch229 -p1
%patch230 -p1
%patch231 -p1
%patch232 -p1
%patch233 -p1
%patch234 -p1
%patch235 -p1 -b .makeinfo

rm -rf ./gdb/gdbserver

cat > gdb/version.in << EOF
%{version}-%{release} (%{mdv_distro_version})
EOF

%define __libtoolize :
autoreconf
cd bfd
autoreconf
cd -
cd libiberty
autoreconf
cd -


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

