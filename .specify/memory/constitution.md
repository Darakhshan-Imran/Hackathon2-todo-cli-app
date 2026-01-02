<!--
  ============================================================================
  SYNC IMPACT REPORT
  ============================================================================
  Version Change: N/A (template) → 1.0.0 (initial constitution)

  Modified Principles: N/A (new document)

  Added Sections:
  - Core Principles (13 principles as specified)
  - Reusable Intelligence Requirements (Subagents + Agent Skills)
  - Technology Stack
  - Phase Evolution Roadmap
  - Governance

  Removed Sections: N/A

  Templates Requiring Updates:
  - ✅ plan-template.md - Compatible (Constitution Check section exists)
  - ✅ spec-template.md - Compatible (Requirements section aligns)
  - ✅ tasks-template.md - Compatible (Phase structure aligns)

  Follow-up TODOs: None
  ============================================================================
-->

# Todo System Constitution

## Purpose

Define permanent architectural, behavioral, and governance rules for a multi-phase evolving Todo system, starting from a Python CLI app and evolving into a cloud-native, AI-powered distributed system.

## Core Principles

### I. Spec-Driven Development Only

All development MUST follow Spec-Driven Development (SDD) methodology. No "vibe coding" or ad-hoc implementation is permitted.

- Every feature MUST have a specification before implementation begins
- Specifications MUST be reviewed and approved before coding
- Implementation MUST trace back to specification requirements
- Deviations from spec require explicit amendment and re-approval

### II. Reusable Intelligence Architecture

Claude Code MUST operate using reusable intelligence via Subagents and Agent Skills.

- All AI-assisted operations MUST use defined Subagents
- Agent Skills MUST be designed for reuse across all project phases
- Intelligence components MUST be documented and versioned
- No ad-hoc AI prompts in production workflows

### III. Cloud-Native Blueprints

Cloud-Native Blueprints MUST be defined via Agent Skills, even if not implemented in Phase 1.

- Infrastructure patterns MUST be declared as Agent Skills
- Cloud deployment configurations MUST be version-controlled
- Migration paths from CLI to cloud MUST be documented
- Serverless, container, and orchestration patterns MUST be pre-defined

### IV. Python Standards

Python version MUST be 3.13 or higher. Use `uv` as the package and environment manager.

- All code MUST be compatible with Python 3.13+
- `uv` is the ONLY permitted package manager
- Virtual environments MUST be managed via `uv`
- Dependencies MUST be declared in `pyproject.toml`
- Lock files MUST be committed to version control

### V. Clean Code Architecture

Follow clean code principles and maintain a readable project structure.

- Code MUST be self-documenting with clear naming conventions
- Functions MUST do one thing and do it well
- Modules MUST have single responsibility
- Directory structure MUST reflect domain boundaries
- No circular dependencies permitted

### VI. Phase 1 Storage Constraint

Phase 1 MUST store data in memory only—no files, no database.

- All todo items MUST persist only for session duration
- No file I/O for data persistence in Phase 1
- No database connections in Phase 1
- Data structures MUST be designed for future persistence migration

### VII. Language Standards

English is the default language. Urdu language support MUST be planned for chatbot interaction in future phases.

- All code, comments, and documentation MUST be in English
- User-facing messages in Phase 1 MUST be in English
- Internationalization (i18n) architecture MUST be planned
- Urdu chatbot integration is a declared future capability

### VIII. Voice Command Declaration

Voice command support MUST be declared in the constitution but NOT implemented in Phase 1.

- Voice interface is a declared future capability
- API boundaries MUST accommodate future voice input
- Command structure MUST be voice-friendly (clear, unambiguous)
- No voice-related dependencies in Phase 1

### IX. Modular Extensibility

All logic MUST be modular and future-extensible.

- Business logic MUST be separate from I/O handling
- Features MUST be pluggable without core changes
- Interfaces MUST be stable; implementations may vary
- Extension points MUST be documented

### X. Security-First Mindset

Security-first mindset MUST be followed even in CLI phase.

- Input validation MUST occur at all entry points
- No sensitive data in logs or error messages
- Command injection prevention is mandatory
- Authentication/authorization patterns MUST be planned (even if not enforced in Phase 1)

### XI. Test-First Development

Test-Driven Development (TDD) is MANDATORY for all feature implementation.

- Tests MUST be written before implementation code
- Tests MUST fail before implementation begins
- Red-Green-Refactor cycle MUST be strictly followed
- Minimum 80% code coverage required

### XII. Observability

All operations MUST be observable and debuggable.

- Structured logging MUST be implemented
- Error states MUST be clearly reported
- CLI output MUST support both human-readable and JSON formats
- Debug mode MUST expose internal state

### XIII. Simplicity (YAGNI)

Start simple. Do not build features that are not immediately needed.

- Implement the simplest solution that satisfies requirements
- No speculative features or over-engineering
- Complexity MUST be justified in writing
- Prefer deletion over deprecation

## Reusable Intelligence Requirements

### Subagents

The following Subagents MUST be defined and available:

| Subagent | Purpose | Phase |
|----------|---------|-------|
| Domain Logic Agent | Execute todo business logic operations | 1+ |
| Spec Validation Agent | Validate specifications against constitution | 1+ |
| Code Quality Agent | Enforce clean code standards | 1+ |
| Test Generation Agent | Generate test cases from specifications | 1+ |
| Cloud Mapping Agent | Map features to cloud-native patterns | 2+ |
| i18n Agent | Handle internationalization concerns | 3+ |

### Agent Skills

The following Agent Skills MUST be defined and reusable:

| Skill | Description | Phase Available |
|-------|-------------|-----------------|
| `todo.domain` | Todo CRUD operations, priority, tags, due dates | 1+ |
| `todo.validate` | Input validation and business rule enforcement | 1+ |
| `spec.validate` | Specification conformance checking | 1+ |
| `code.structure` | Clean Python project structure enforcement | 1+ |
| `code.quality` | Code quality and style checking | 1+ |
| `cloud.blueprint` | Cloud-native architecture patterns | Declared (impl 2+) |
| `cloud.deploy` | Deployment configuration generation | Declared (impl 2+) |
| `i18n.urdu` | Urdu language support for chatbot | Declared (impl 3+) |
| `voice.command` | Voice command parsing and routing | Declared (impl 4+) |

## Technology Stack

### Phase 1 (Current)

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Language | Python 3.13+ | Modern features, type hints, performance |
| Package Manager | uv | Fast, reliable, lockfile support |
| Interface | CLI (argparse/click) | Simple, testable, scriptable |
| Storage | In-memory (dict/dataclass) | Phase constraint |
| Testing | pytest | Industry standard, excellent fixtures |
| Linting | ruff | Fast, comprehensive, replaces multiple tools |
| Type Checking | mypy | Static type verification |

### Future Phases (Declared)

| Phase | Additions | Notes |
|-------|-----------|-------|
| 2 | SQLite/PostgreSQL, REST API | Persistence layer |
| 3 | FastAPI, i18n, Urdu chatbot | Web interface, localization |
| 4 | Voice SDK, Cloud deployment | Voice commands, production infrastructure |

## Phase Evolution Roadmap

```
Phase 1: CLI + In-Memory (CURRENT)
    ↓
Phase 2: CLI + Persistence + API
    ↓
Phase 3: Web UI + Chatbot (EN/UR)
    ↓
Phase 4: Voice + Cloud-Native
```

Each phase MUST:
- Maintain backward compatibility with previous phase CLI
- Pass all existing tests before adding new features
- Update specifications before implementation
- Document migration path from previous phase

## Governance

### Amendment Process

1. Proposed amendments MUST be documented with rationale
2. Amendments MUST be reviewed against existing principles
3. Breaking changes require MAJOR version bump
4. All amendments MUST include migration guidance

### Versioning Policy

- **MAJOR**: Backward-incompatible principle changes or removals
- **MINOR**: New principles, sections, or material expansions
- **PATCH**: Clarifications, typos, non-semantic refinements

### Compliance

- All pull requests MUST verify constitution compliance
- Complexity additions MUST be justified in PR description
- Constitution Check in plan.md MUST pass before implementation
- Violations block merge until resolved or constitution amended

### Authoritative Documents

| Document | Location | Purpose |
|----------|----------|---------|
| Constitution | `.specify/memory/constitution.md` | Permanent rules (this file) |
| Specifications | `specs/<feature>/spec.md` | Feature requirements |
| Plans | `specs/<feature>/plan.md` | Implementation design |
| Tasks | `specs/<feature>/tasks.md` | Executable work items |
| ADRs | `history/adr/` | Architectural decisions |
| PHRs | `history/prompts/` | Prompt history records |

**Version**: 1.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01
