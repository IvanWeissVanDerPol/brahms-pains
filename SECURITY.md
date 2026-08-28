# Security

## Visibility

This repository is **private**. It contains:

- ~1.21 GB of medical PHI (MRI imaging, DICOM files, segmentation volumes)
- ~350 MB of third-party WhatsApp data (chat exports, voice note transcripts)
- ~1.1 GB of bulk voice notes (~8,200 files from multiple chats)
- Personal psychology research (CORE_PSYCHOLOGY/, HAT_*_ANALYSIS, INDEX.md)

The repo is intended as a **complete personal archive**. Visibility must remain **private**.

## Branch protection

`master` is protected:
- ✅ Requires pull request review before merging
- ✅ Requires linear history
- ✅ Includes administrators
- ❌ Disallows force pushes
- ❌ Disallows deletions

## Hardening checklist

- [x] Repo flipped to private (2026-08-28)
- [x] Branch protection on master
- [ ] GitHub PAT rotated
- [ ] Deploy keys rotated
- [ ] GitHub Apps with access reviewed

## Data classification

| Data type | Location | Severity |
|---|---|---|
| MRI imaging (DICOM) | `MEDICAL/MRI_2026-07-22_LUMBAR_PELVIS/` | � Critical PHI |
| DICOM attachments | `.hermes/desktop-attachments/*.dcm` | � Critical PHI |
| Third-party WhatsApp | `SOURCE_OF_TRUTH/wa_messages/` | � GDPR / data protection |
| Voice note transcripts | `SOURCE_OF_TRUTH/voice_note_transcripts/` | 🟠 Personal |
| Bulk voice notes | `media/audio/_wa_chat_*`, `_wa_lid_*`, `_w4b_unmapped/` | 🟡 Personal |
| Personal psychology | `CORE_PSYCHOLOGY/`, `docs/`, `INDEX.md`, `HAT_*` | 🟢 OK if private |

## Reporting

If you find PHI in a public repo or accidental disclosure:

1. **Stop work immediately.**
2. Flip the repo to private.
3. Open a GitHub support ticket to purge cached views.
4. Rotate all tokens/keys with access.
5. Use `git-filter-repo` to scrub from history (already installed locally).
6. Force-push the rewritten history.

See `~/.claude/skills/safe-credential-scrub/` and `~/.claude/skills/credential-incident-reporting/`.
