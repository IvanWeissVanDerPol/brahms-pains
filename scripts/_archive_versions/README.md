# Archived Script Versions

This folder contains older versions of scripts that have been superseded by newer iterations. Each archived script was a working draft at the time but the final non-versioned `.py` file in the parent `scripts/` directory is the canonical, maintained version.

## Contents

| Prefix | Latest in scripts/ | Archived here |
|--------|-------------------:|--------------:|
| `apply_vnt_renames` | `apply_vnt_renames.py` | 7 versions |
| `rename_untiered_remaining` | `rename_untiered_remaining.py` | 4 versions |
| `build_vnt_mapping` | `build_vnt_mapping.py` | 3 versions |
| `generate_profile_stubs` | `generate_profile_stubs.py` | 1 version |
| `analyze_transcripts` | `analyze_transcripts.py` | 1 version |
| `match_vcard_chats` | `match_vcard_chats.py` | 1 version |

## Why Archived (not deleted)?

1. **Audit trail**: Documentation of what approaches were tried during cleanup
2. **Regression safety**: If a feature breaks, we can check if older versions had it
3. **Migration reference**: For future scripts that need to do similar work

## When to Remove

These scripts can be safely deleted once:
- The canonical scripts have been running in production for 6+ months
- All references to `_v2`, `_v3` etc. in cron jobs have been updated

## Cleanup Date

Archived: 2026-07-27 during repo cleanup pass.