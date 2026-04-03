# Nion Orchestration Engine

A simplified implementation of Nion's three-tier AI orchestration architecture.

## Architecture

```
L1 ORCHESTRATOR
  Ingests message, reasons about intent, builds execution plan.
  Visibility: L2 domain coordinators + Cross-Cutting agents only.

    L2 COORDINATOR (TRACKING_EXECUTION)
      Visibility: own L3 agents + Cross-Cutting agents.
        L3: action_item_extraction, action_item_validation, action_item_tracking
        L3: risk_extraction, risk_tracking
        L3: issue_extraction, issue_tracking
        L3: decision_extraction, decision_tracking

    L2 COORDINATOR (COMMUNICATION_COLLABORATION)
      Visibility: own L3 agents + Cross-Cutting agents.
        L3: qna, report_generation, message_delivery, meeting_attendance

    L2 COORDINATOR (LEARNING_IMPROVEMENT)
      Visibility: own L3 agents + Cross-Cutting agents.
        L3: instruction_led_learning

    Cross-Cutting (visible to L1 and all L2 domains):
        L3: knowledge_retrieval
        L3: evaluation
```

## Requirements

- Python 3.9 or later (uses `list[...]` type hints — no third-party packages required)

## Setup

```bash
git clone https://github.com/SAKSHAM-73/nion-orchestration-engine.git
cd nion-orchestration-engine
```

No virtual environment or pip install needed — the engine is pure Python stdlib.

## Usage

### From a JSON file

```bash
python orchestrator.py input.json
```

### From stdin

```bash
echo '{"message_id":"MSG-001","source":"email","sender":{"name":"Sarah Chen","role":"Product Manager"},"content":"Can we make this work?","project":"PRJ-ALPHA"}' | python orchestrator.py
```

### Run all test cases

```bash
python run_tests.py
```

Outputs are written to `outputs/` directory.

### Programmatic use

```python
from orchestrator import process

msg = {
    "message_id": "MSG-001",
    "source": "email",
    "sender": {"name": "Sarah Chen", "role": "Product Manager"},
    "content": "The customer demo went great! ...",
    "project": "PRJ-ALPHA"
}

print(process(msg))
```

## Input Format

```json
{
  "message_id": "MSG-001",
  "source": "email",              // email | slack | meeting
  "sender": {
    "name": "Sarah Chen",
    "role": "Product Manager"
  },
  "content": "...",
  "project": "PRJ-ALPHA"          // null if unknown
}
```

## Output Format

```
==============================================================================
NION ORCHESTRATION MAP
==============================================================================
Message: <id>
From: <name> (<role>)
Project: <project>

==============================================================================
L1 PLAN
==============================================================================
[TASK-001] -> L3:knowledge_retrieval (Cross-Cutting)
  Purpose: Retrieve project context and stakeholder details

[TASK-002] -> L2:TRACKING_EXECUTION
  Purpose: Extract action items from message content

...

==============================================================================
L2/L3 EXECUTION
==============================================================================

[TASK-001] L3:knowledge_retrieval (Cross-Cutting)
  Status: COMPLETED
  Output:
    * Project: PRJ-ALPHA
    * ...

[TASK-002] L2:TRACKING_EXECUTION
  +-> [TASK-002-A] L3:action_item_extraction
        Status: COMPLETED
        Output:
          * AI-001: "Add real-time notifications feature"
          *       Owner: ? | Due: ? | Flags: [MISSING_OWNER, MISSING_DUE_DATE]

==============================================================================
```

## Test Cases

| ID      | Scenario                     | Project   |
|---------|------------------------------|-----------|
| MSG-001 | Customer feature request     | PRJ-ALPHA |
| MSG-101 | Simple status question       | PRJ-BETA  |
| MSG-102 | Feasibility question (SSO)   | PRJ-ALPHA |
| MSG-103 | Decision/prioritization      | PRJ-GAMMA |
| MSG-104 | Meeting transcript           | PRJ-ALPHA |
| MSG-105 | Urgent legal escalation      | PRJ-DELTA |
| MSG-106 | Ambiguous / no project       | null      |

## Assumptions & Design Decisions

- **L3 outputs are simulated** with realistic placeholder data as permitted by the task spec ("dummy placeholders can be generated randomly").
- **Intent detection** uses keyword scanning on message content to keep the L1 plan minimal and relevant — only agents needed for the message are scheduled.
- **Visibility is enforced architecturally**: `L1Orchestrator` only references `L2:<DOMAIN>` or cross-cutting agents. `L2Coordinator.resolve_l3()` maps purposes to domain-specific L3 agents — L1 has no knowledge of these.
- **Dependency tracking** is explicit: each task records `depends_on` IDs, visible in the L1 PLAN section.
- No third-party packages — pure Python 3.9+ stdlib only.

## Key Design Decisions

**Visibility enforcement:** L1 only schedules tasks targeting `L2:<DOMAIN>` or
`L3:<cross-cutting-agent>`. It never directly references a domain-specific L3 agent.
L2 resolves which L3 agent to invoke based on task purpose — L1 has no knowledge of
individual L3 agents within a domain.

**Intent detection:** L1 scans message content for keyword signals to decide which
extraction tasks to add to the plan (action items, risks, issues, decisions). This keeps
the plan minimal and relevant rather than always running every possible agent.

**Dependency tracking:** Each task records `depends_on` IDs so the execution order and
data flow are explicit in the plan output.

**L3 agent outputs:** Each agent produces structured bullet-point output with realistic
placeholder values (`?`, `PENDING`, `MISSING_*` flags) when information is absent from
the message, matching real-world PM system behavior.
