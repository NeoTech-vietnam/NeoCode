# Windows setup

This guide sets up Python and a C/C++ compiler for this repository, including
AddressSanitizer and UndefinedBehaviorSanitizer (ASan/UBSan).

## 1. Check existing tools

Open PowerShell and run:

```powershell
python --version
git --version
Get-Command python, git, gcc, clang -ErrorAction SilentlyContinue
```

Python 3 and Git were already installed on this machine. The repository's Python
scripts use the standard library; no pip packages or virtual environment are needed.

If either tool is missing, install it from [Python](https://www.python.org/downloads/windows/)
or [Git for Windows](https://git-scm.com/download/win). Enable Python's PATH option
in its installer, then reopen the terminal.

## 2. Install or update MSYS2

Install [MSYS2](https://www.msys2.org/) at the default location, `C:\msys64`,
if it is not already installed. This machine already had MSYS2.

Open the MSYS2 shell and update it:

```bash
pacman -Syu
```

If the core update asks to close MSYS2, accept, reopen the MSYS2 shell, and run
the update again. Close other MSYS2 shells before the core update.

```bash
pacman -Syu
```

## 3. Install Clang64

In the MSYS2 shell:

```bash
pacman -S --needed mingw-w64-clang-x86_64-clang
```

This installs the compiler and its required C/C++ libraries, linker and sanitizer
runtime. See the [official package page](https://packages.msys2.org/packages/mingw-w64-clang-x86_64-clang).

The compiler executables should be:

```text
C:\msys64\clang64\bin\clang.exe
C:\msys64\clang64\bin\clang++.exe
```

## 4. Select the compiler

Run these commands in PowerShell under your normal Windows account:

```powershell
[Environment]::SetEnvironmentVariable('CC', 'C:\msys64\clang64\bin\clang.exe', 'User')
[Environment]::SetEnvironmentVariable('CXX', 'C:\msys64\clang64\bin\clang++.exe', 'User')
```

These user-level settings also apply to other tools that honor `CC` and `CXX`.
Restart Nimbalyst and open a new terminal to inherit them. To use the compiler
immediately in the current PowerShell session, also run:

```powershell
$env:CC = 'C:\msys64\clang64\bin\clang.exe'
$env:CXX = 'C:\msys64\clang64\bin\clang++.exe'
& $env:CC --version
& $env:CXX --version
```

The build script gives `CC`/`CXX` priority over compilers on PATH. Explicitly
selecting Clang64 matters on this machine because standalone LLVM at
`C:\Program Files\LLVM\bin` can compile ordinary samples but failed the repo's
sanitizer probe. MinGW GCC 6.3 is also installed, but cannot run these sanitizer checks.
Adding Clang64 to PATH is not required by the repo when `CC`/`CXX` are set.

## 5. Verify the setup

In PowerShell, from the repository root:

```powershell
Set-Location H:\Learning\leetcode-practice
python tools/selftest.py
```

Expect `Self-test passed`, including sanitizer cases for heap-buffer overflow and
use-after-free. If the output says sanitizer cases were skipped, sanitizer setup
is not yet verified. The full log is saved at `build/selftest.log`.
Self-test uses temporary samples and does not edit practice solutions.

For normal practice:

```powershell
python tools/build_test.py
python tools/build_test.py --sanitize
```

The compiler header should show `C:\msys64\clang64\bin\clang.exe` or
`clang++.exe`. With no problem directories yet, the build command reports
`No problems found`; use self-test to verify the toolchain in that case.

## Troubleshooting from this installation

### Default mirror returns HTTP 403 or database signatures fail

The default `mirror.msys2.org` endpoint returned HTTP 403 during setup, and some
downloaded databases were empty. Switching to the official `repo.msys2.org`
endpoint and forcing a database refresh resolved the download problem.

To reproduce that workaround without changing the permanent MSYS2 configuration,
run this in the MSYS2 shell:

```bash
cp /etc/pacman.conf /tmp/leetcode-pacman.conf
sed -i 's|Include = /etc/pacman.d/mirrorlist.mingw|Server = https://repo.msys2.org/mingw/$repo/|' /tmp/leetcode-pacman.conf
sed -i 's|Include = /etc/pacman.d/mirrorlist.msys|Server = https://repo.msys2.org/msys/$arch/|' /tmp/leetcode-pacman.conf
pacman --config /tmp/leetcode-pacman.conf -Syyu
```

If the core update closes the shell, reopen it and repeat the last command.
Then install Clang64 with the same temporary configuration:

```bash
pacman --config /tmp/leetcode-pacman.conf -S --needed mingw-w64-clang-x86_64-clang
```

Keep signature verification enabled. If signature errors persist after a fresh
download, consult the [MSYS2 update guide](https://www.msys2.org/docs/updating/).

### Pacman stalls at checking available disk space

During this installation, pacman stalled before starting the package transaction.
Windows reported 13.76 GiB free on C:, while the packages required about 1.08 GiB
installed space. After stopping that pre-transaction process, setup was retried
with `CheckSpace` commented out in the temporary configuration only:

```bash
sed -i 's/^CheckSpace$/# CheckSpace/' /tmp/leetcode-pacman.conf
pacman --config /tmp/leetcode-pacman.conf -Su --needed mingw-w64-clang-x86_64-clang
```

Use this workaround only after checking current free space and confirming the
previous pacman process has stopped before package changes began. Do not stop
pacman while it is installing or upgrading packages. Remove a leftover
`/var/lib/pacman/db.lck` only after confirming no pacman process is running.
Package signature and integrity checks remain enabled with this workaround.

## Verified installation

On 2026-11-07, this machine was verified with Python 3.12.0 and MSYS2 Clang64
23.1.5. The tooling self-test passed, including ASan detection of heap-buffer
overflow and use-after-free. The C++20 compiler also passed the build script's
compile-and-run sanitizer probe. Future package versions may differ.
