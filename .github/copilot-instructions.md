# Copilot Instructions

## CTF Writeup Structure

All writeups live at `Writeups/<challenge name>/README.md`.
Always follow the template at `TEMPLATE.md` when creating or editing writeups.

### Required fields in metadata block
- **CTF:** event name and year
- **Category:** challenge category
- **Tags:** comma-separated

### Optional fields
- **Difficulty:** Easy · Medium · Hard
- **Author:**
- **Date:** Month YYYY or YYYY

### Required sections in order
1. Objective
2. Overview
3. Analysis
4. Solution
5. Conclusion — must end with `Flag: \`PREFIX{...}\``

### Rules
- Do not add "(Migrated from Docs)" or any suffix to the challenge title
- Do not reorder sections
- Mitigation is optional — uncomment from template only if relevant
- Challenge name casing follows the official challenge name exactly, do not correct it

### When editing existing writeups
- Preserve the author's original wording and analysis
- Only fix formatting to match the template (section order, metadata fields)
- Do not rewrite, summarize, or rephrase any existing content
- Do not add content that wasn't there unless it is critically important