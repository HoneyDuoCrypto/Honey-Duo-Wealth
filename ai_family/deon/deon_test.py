#!/usr/bin/env python3
"""
DEON - Risk Grader Test
Risk assessment and validation
"""

import subprocess
import json
from datetime import datetime

def ask_deon(prompt):
    """Send prompt to DEON (Llama2 13B)"""
    try:
        result = subprocess.run(
            ["ollama", "run", "llama2:13b", prompt],
            capture_output=True, text=True, timeout=45
        )
        return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Exception: {str(e)}"

def test_deon():
    """Test DEON risk grader"""
    print("🛡️ Testing DEON - Risk Grader")
    print("=" * 29)
    
    prompt = """Hello DEON! You are the risk grader for HONEY DUO WEALTH.
    Assess this trade: BUY Bitcoin at $43,000, position size $200.
    Provide: Risk score (1-10), family safety assessment, APPROVE/REJECT."""
    
    response = ask_deon(prompt)
    print(f"DEON Response:\n{response}")
    
    # Log the interaction
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "member": "DEON",
        "assessment_type": "Trade Risk Analysis",
        "prompt": prompt,
        "response": response
    }
    
    with open("ai_family/deon/test_log.json", "w") as f:
        json.dump(log_entry, f, indent=2)
    
    print(f"\n✅ Test logged to ai_family/deon/test_log.json")

if __name__ == "__main__":
    test_deon()