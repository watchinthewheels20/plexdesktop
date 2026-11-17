# AGENTS.md — LoungeMedia Windows client

## Identity and scope
This repository is **LoungeMedia**, an independent Windows x64 Plex client forked from [Plezy](https://github.com/edde746/plezy) (GPL-3.0). Do not market it as Plezy or as an official Plex product. Keep Plezy copyright/GPL notices, attribution and source availability. Internal Dart package name `plezy` is deliberately unchanged to simplify upstream integration.

## Expected working relationship
The owner tests Windows installer builds and submits Feedback reviews with Issues, Feature requests, Questions and Feedback. Address every actionable item in one coherent batch. Work from latest main and current code rather than old chat assumptions. Use a review branch, test first, squash once to main, verify GitHub Actions and inspect actual installer artifacts before reporting success. Do not invent artifact URLs or claim unverified builds.

## Architecture
- Flutter/Dart UI in `lib/screens`, `lib/widgets`, `lib/navigation`, `lib/focus` and `lib/theme`. The `lib/media`, `lib/connection`, `lib/profiles`, `lib/mpv` and `lib/services` areas include authentication, media browsing and player internals.
- Preserve Plezy's Plex authentication, server discovery, direct playback/mpv, watch-state/resume, subtitles, secure token storage and native key handling. Avoid unrelated backend rewrites.
- The target is **Plex Web**, not Plex HTPC. The owner's 2026-11-17 screenshots specify a charcoal top bar and fixed pinned sidebar, golden highlights, horizontal media shelves, underline library tabs and horizontal Select User cards. Do not commit the user's private Plex images/profile artwork into the public repo.
- Desktop theme changes are gated to Windows wherever possible. Preserve the existing user-configurable appearance and Plex metadata/artwork editor. Retain profile switching/PIN authorization and server administrator checks.
- The Windows app should use its own name, icons, executable, installer GUID and release source, with no dependency on Plezy-operated auxiliary endpoints. Investigate tracker/OAuth integrations before publishing them in this fork.

## Tooling and release
- Upstream SDK pinned by `.github/workflows/build.yml`, Flutter 3.47.1. Check `CONTRIBUTING.md` and `.github/workflows/ci.yml` before implementation.
- Flutter validation: `dart format lib test` (as applicable), `flutter analyze`, `scripts/run_tests.sh`, plus relevant widget tests and Windows bundle smoke checks. Never silently ignore failing CI.
- Reuse `.github/workflows/build.yml` to generate the **Windows x64 Inno Setup installer** and portable .7z. Verify all required native files remain alongside the executable.
- Preserve per-user data and settings across upgrades of *LoungeMedia*. Keep its installation and updater identity separate from upstream Plezy.
- Never commit tokens, credentials, stream URLs or personal information, and never expose auth tokens in logs.
- Current version follows upstream's 2.26.x series. Do not make a major version jump without approval.

## Development workflow
1. Inspect `main`, this file, upstream changes, relevant implementation and tests.
2. Implement complete review with focused regression tests; maintain remote/gamepad navigation and focus.
3. Open PR, run all CI checks; ensure Windows build/installer succeeds and actual release assets are verified.
4. Merge via squash (one main commit) only when checks pass, then report changes, tests, commit/version, and direct installer link; identify blocked items.
