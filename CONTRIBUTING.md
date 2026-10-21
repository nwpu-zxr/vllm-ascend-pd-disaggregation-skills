# Contributing

Keep instructions scoped to a concrete engineering task and grounded in source or runtime evidence. Avoid turning a historical failure, model recipe or workaround into a universal rule.

- Maintain each complete skill package, including its references, scripts and interface metadata. Preserve standalone use and optional runtime integrations.
- Keep formal instructions in English. Do not include private endpoints, credentials, session transcripts, model outputs or tensor dumps.
- For compatibility changes, identify the relevant spec, layout, connector revision and runtime conditions. Separate static reasoning from hardware reproduction.
- When changing an executable helper, add or update a regression case for observable behavior. Tests must not require Torch or NPU hardware on the host.
- `references/official-docs.md`, `references/runtime-integration.md` and `references/skill-reuse.md` are intentionally copied into each package so it can be installed independently. Update all three copies together; validation detects drift.
- Keep the English and Chinese READMEs and catalogue descriptions consistent with the final capabilities. Do not mark a catalogue entry reproduced based on documentation checks or another source revision's result.

Run `python3 scripts/validate.py` before submission. Include the concrete problem, resulting behavior, validation performed and any remaining runtime uncertainty in the change description.
