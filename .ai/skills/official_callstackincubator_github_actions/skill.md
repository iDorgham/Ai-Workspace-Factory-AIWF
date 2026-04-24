---
name: github-actions
description: GitHub Actions workflow patterns for React Native iOS simulator and Android emulator cloud builds with downloadable artifacts. Use when setting up CI build pipelines or downloading GitHub Actions artifacts via gh CLI and GitHub API.
license: MIT
metadata:
  author: Callstack
  tags: github-actions, github, ci, react-native, ios, android, simulator, emulator, artifacts, gh-cli
---

# GitHub Actions Build Artifacts

## Overview

Reusable GitHub Actions patterns to build React Native apps for iOS simulators and Android emulators in the cloud, then publish artifacts retrievable via `gh` CLI or GitHub API.

## When to Apply

Use this skill when:
- Creating CI workflows that build React Native simulator/emulator artifacts.
- Uploading iOS simulator and Android emulator installables from PRs or manual dispatch runs.
- Replacing local-only mobile builds with downloadable CI artifacts.
- Needing stable artifact IDs/names for scripted retrieval with `gh` or REST API.

## Quick Reference

1. Add composite actions from [gha_ios_composite_action.md][gha-ios-composite-action] and [gha_android_composite_action.md][gha-android-composite-action].
2. Wire them into `.github/workflows/mobile-build.yml` from [gha_workflow_and_downloads.md][gha-workflow-and-downloads].
3. Upload with `actions/upload-artifact@v4` and capture `artifact-id` output.
4. Download with `gh run download` or `GET /repos/{owner}/{repo}/actions/artifacts/{artifact_id}/{archive_format}`.

## References

| File | Description |
|------|-------------|
| [gha_ios_composite_action.md][gha-ios-composite-action] | Composite `action.yml` for iOS simulator `.app.tar.gz` builds and artifact upload |
| [gha_android_composite_action.md][gha-android-composite-action] | Composite `action.yml` for Android emulator `.apk` builds and artifact upload |
| [gha_workflow_and_downloads.md][gha-workflow-and-downloads] | End-to-end workflow wiring plus `gh` and REST download commands |

## Problem -> Skill Mapping

| Problem | Start With |
|---------|------------|
| Need CI iOS simulator `.app.tar.gz` artifact | [gha_ios_composite_action.md][gha-ios-composite-action] |
| Need CI Android emulator `.apk` artifact | [gha_android_composite_action.md][gha-android-composite-action] |
| Need one workflow to trigger both platform jobs | [gha_workflow_and_downloads.md][gha-workflow-and-downloads] |
| Need scripted artifact download | [gha_workflow_and_downloads.md][gha-workflow-and-downloads] |

## Source Inspiration

- [callstackincubator/ios/action.yml](https://github.com/callstackincubator/ios/blob/main/action.yml)
- [callstackincubator/android/action.yml](https://github.com/callstackincubator/android/blob/main/action.yml)

[gha-ios-composite-action]: references/gha_ios_composite_action.md
[gha-android-composite-action]: references/gha_android_composite_action.md
[gha-workflow-and-downloads]: references/gha_workflow_and_downloads.md
