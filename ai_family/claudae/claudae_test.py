#!/usr/bin/env python3
"""
CLAUDAE - System Guardian Test
Basic communication with the AI family
"""

import subprocess
import json
from datetime import datetime

def ask_claudae(prompt):
    """Send prompt to CLAUDAE (Mistral 7B)"""
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral:7b", prompt],
            capture_output=True, text=True, timeout=30
        )
        return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Exception: {str(e)}"

def test_claudae():
    """Test CLAUDAE system guardian"""
    print("🤖 Testing CLAUDAE - System Guardian")
    print("=" * 35)
    
    prompt = """Hello CLAUDAE! You are the system guardian for HONEY DUO WEALTH, 
    protecting our family's financial future. Please provide a brief status report."""
    
    response = ask_claudae(prompt)
    print(f"CLAUDAE Response:\n{response}")
    
    # Log the interaction
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "member": "CLAUDAE", 
        "prompt": prompt,
        "response": response
    }
    
    with open("ai_family/claudae/test_log.json", "w") as f:
        json.dump(log_entry, f, indent=2)
    
    print(f"\n✅ Test logged to ai_family/claudae/test_log.json")

if __name__ == "__main__":
    test_claudae()# Test comment for CLAUDAE learning
# Fresh test comment at Thu Jun  5 03:43:28 AM PDT 2025
