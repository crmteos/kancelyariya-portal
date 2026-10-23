# AGENTS.md — Deterministic Context Control for Kancelyariya Portal

## 1. Algorithmic Constraints (Replacement of Anthropomorphic Roles)

- Work exclusively within the typology and relational JSON structure of `chancery_manifest.json`.
- Any newly created data files, passports, or modules must be registered in the manifest.
- Before completing any task, run the validator `python check_and_update.py` and verify absence of errors.
- No anthropomorphic role assignments (e.g., "assistant", "manager", "coordinator") are permitted in system prompts or file outputs.
- All operations must conform to the strict data formats defined in `chancery_manifest.json.osint_passport_schema`.

## 2. Strict Output Schemas (No Chat Preamble/Postamble)

- When generating, updating, or returning data, return **exclusively valid JSON** conforming to the defined schema.
- **Forbidden**: Any conversational introductory or concluding text when outputting JSON structures or logs.
- Output format must be pure JSON only, no markdown-wrapped text, no preambles, no summaries.

## 3. Context Budgeting & Synchronization (Minimize Context Drift)

- **Before starting any new task**, the AI coder must read only these three files:
  1. `PROJECT_STATE.md`
  2. `chancery_manifest.json`
  3. `AI_CONTEXT_GATEWAY.md`
- Do not load stale chats or logged files without direct need, to avoid context drift (Context Drift).
- Maintain file modification timestamps in sync with `AI_CONTEXT_GATEWAY.md` Last Report section.

## 4. Technical Stack & Inter-AI Protocol Compliance

- Preserve **$0 budget**: pure HTML5, Tailwind CSS via CDN, Vanilla JS (ES6).
- **No server backends or paid APIs** are permitted.
- Adhere to **Inter-AI Protocol**: after each execution, update `AI_CONTEXT_GATEWAY.md` (
  "Last Report" and "Config Slices" sections).
- All project-internal communications must route through `AI_CONTEXT_GATEWAY.md` for context synchronization.

## 5. Mandatory Post-Task Procedure

After completing any task or file update:

1. Run `python check_and_update.py` — verify no errors exit.
2. Update `AI_CONTEXT_GATEWAY.md`:
   - "Last Report" section: record task completion, files modified, validation result.
   - "Config Slices" section: extract and display relevant JSON slices (regions_register.json, passport schemas, manifest configs).
3. Update `PROJECT_STATE.md` to record the task completion status.