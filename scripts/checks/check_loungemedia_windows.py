#!/usr/bin/env python3
"""Guard the independent Windows x64 installer and release workflow.

The upstream guards pin Plezy's ARM64/MSIX Store and WinSparkle contracts.
Those are intentionally not shipped by this Windows x64 fork. Preserve a
meaningful build/installer security check rather than bypassing validation.
"""
from pathlib import Path
import re
import sys

from workflow_yaml import job_block

ROOT = Path(__file__).resolve().parents[2]
workflow = (ROOT / ".github/workflows/build.yml").read_text(encoding="utf-8")
installer = (ROOT / "windows/build-installer.ps1").read_text(encoding="utf-8")
cmake = (ROOT / "windows/CMakeLists.txt").read_text(encoding="utf-8")
native = (ROOT / "windows/runner/main.cpp").read_text(encoding="utf-8")
errors = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


build = job_block(workflow, "build-windows")
package = job_block(workflow, "package-windows")
publish = job_block(workflow, "publish-windows")
trusted = job_block(workflow, "validate-trusted-ref")

check(bool(build and package and publish and trusted), "Windows build, package, publish and trust jobs must exist")
check("refs/heads/main" in trusted, "release builds must only run from main")
check(re.search(r"(?m)^  push:\n    branches:\n      - main$", workflow) is not None, "main pushes must trigger release workflow")
check("needs: validate-trusted-ref" in build, "Windows builds must depend on the trusted-main gate")
check("runs-on: ${{ matrix.runner }}" in build, "Windows build must use the trusted runner matrix")
check("runner: windows-latest" in build and "- arch: x64" in build, "Windows x64 runner missing")
check("- arch: arm64" not in build, "Windows-only fork must not build ARM64")
check("flutter pub get --enforce-lockfile --no-example" in build, "dependencies must use the enforced lockfile")
check("flutter build windows --release" in build, "Windows release compilation missing")
check("Install patched Flutter engine (DComp)" in build, "upstream patched engine must be installed")
check("native_cache_path: build/windows/x64/_deps" in build, "Windows native cache missing")
check("hashFiles('windows/CMakeLists.txt', 'mpv-build.lock.json')" in build, "libmpv cache must be lock-file keyed")
check("loungemedia.exe" in build and "libmpv-2.dll" in build and "flutter_windows.dll" in build,
      "build must verify executable and essential native libraries")
check("name: windows-${{ matrix.arch }}-build" in build, "Windows build artifact upload missing")
check("needs: build-windows" in package, "packaging must depend on a successful Windows build")
check('name: windows-x64-build' in package, "packaging must download the compiled x64 build")
check(r'.\windows\build-installer.ps1 -X64BuildDir "build-x64"' in package,
      "installer must be built from the downloaded x64 bundle")
check("Build Store package (MSIX)" not in package, "fork cannot ship upstream's Store identity")
check('name: windows-installer' in package and 'name: windows-x64-portable' in package,
      "installer and portable must both be uploaded")
check("loungemedia-windows-installer.exe" in package and "loungemedia-windows-x64-portable.7z" in package,
      "packaging must use fork-specific filenames")
check("needs: package-windows" in publish and "if: ${{ github.event_name == 'push' }}" in publish,
      "publishing must depend on main-branch packaging only")
check("permissions:\n      contents: write" in publish, "publication must have explicit contents write")
check('test -s dist/installer/loungemedia-windows-installer.exe' in publish,
      "publishing must verify nonempty installer")
check('test -s dist/portable/loungemedia-windows-x64-portable.7z' in publish,
      "publishing must verify nonempty portable")
check("gh release create" in publish, "verified artifacts must be released")
check("gh release create" not in build and "gh release create" not in package,
      "only the publication job can create a release")
check('set(BINARY_NAME "loungemedia")' in cmake, "Windows binary name must be independent")
check('L"com.watchinthewheels20.LoungeMedia.SingleInstance"' in native,
      "single instance mutex must be separate from Plezy")
check('L"LoungeMedia"' in native, "native window title must be independent")

guid = "d3bba1a1-199d-4edd-9d1e-7161bfe975a4"
check(installer.count(guid) == 1, "new Inno AppId GUID must have one source")
for required in (
    '#define Name "LoungeMedia"',
    '#define ExeName "loungemedia.exe"',
    "AppId={{$AppGuid}",
    "OutputBaseFilename=loungemedia-windows-installer",
    "PrivilegesRequired=lowest",
    "PrivilegesRequiredOverridesAllowed=commandline",
    "{param:ELEVATED|0}",
    "ShellExec('runas'",
    "{param:NORUN|0}",
):
    check(required in installer, f"installer missing: {required}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    sys.exit(1)
print("LoungeMedia Windows x64 installer and release guard passed")
