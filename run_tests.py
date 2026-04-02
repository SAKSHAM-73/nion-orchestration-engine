"""
Run all test cases and save outputs.
"""

import json
import os
from orchestrator import process

TEST_CASES = {
    "sample": {
        "message_id": "MSG-001",
        "source": "email",
        "sender": {"name": "Sarah Chen", "role": "Product Manager"},
        "content": "The customer demo went great! They loved it but asked if we could add real-time notifications and a dashboard export feature. They're willing to pay 20% more and need it in the same timeline. Can we make this work?",
        "project": "PRJ-ALPHA"
    },
    "MSG-101": {
        "message_id": "MSG-101",
        "source": "slack",
        "sender": {"name": "John Doe", "role": "Engineering Manager"},
        "content": "What's the status of the authentication feature?",
        "project": "PRJ-BETA"
    },
    "MSG-102": {
        "message_id": "MSG-102",
        "source": "email",
        "sender": {"name": "Sarah Chen", "role": "Product Manager"},
        "content": "Can we add SSO integration before the December release?",
        "project": "PRJ-ALPHA"
    },
    "MSG-103": {
        "message_id": "MSG-103",
        "source": "email",
        "sender": {"name": "Mike Johnson", "role": "VP Engineering"},
        "content": "Should we prioritize security fixes or the new dashboard?",
        "project": "PRJ-GAMMA"
    },
    "MSG-104": {
        "message_id": "MSG-104",
        "source": "meeting",
        "sender": {"name": "System", "role": "Meeting Bot"},
        "content": "Dev: I'm blocked on API integration, staging is down. QA: Found 3 critical bugs in payment flow. Designer: Mobile mockups ready by Thursday. Tech Lead: We might need to refactor the auth module.",
        "project": "PRJ-ALPHA"
    },
    "MSG-105": {
        "message_id": "MSG-105",
        "source": "email",
        "sender": {"name": "Lisa Wong", "role": "Customer Success Manager"},
        "content": "The client is asking why feature X promised for Q3 is still not delivered. They're threatening to escalate to legal. What happened?",
        "project": "PRJ-DELTA"
    },
    "MSG-106": {
        "message_id": "MSG-106",
        "source": "slack",
        "sender": {"name": "Random User", "role": "Unknown"},
        "content": "We need to speed things up",
        "project": None
    },
}

os.makedirs("outputs", exist_ok=True)

for name, msg in TEST_CASES.items():
    result = process(msg)
    fname  = f"outputs/{name}.txt"
    with open(fname, "w") as f:
        f.write(result)
    print(f"✓ {name} → {fname}")
    print(result)
    print()
