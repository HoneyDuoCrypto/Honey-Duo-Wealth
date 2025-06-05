#!/usr/bin/env python3
"""
NYALA - Trading Engine Test
Market analysis and trade recommendations
"""

import subprocess
import json
from datetime import datetime

def ask_nyala(prompt):
    """Send prompt to NYALA (Mixtral 8x7b)"""
    try:
        result = subprocess.run(
            ["ollama", "run", "mixtral:8x7b", prompt],
            capture_output=True, text=True, timeout=60
        )
        return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Exception: {str(e)}"

def test_nyala():
    """Test NYALA trading engine"""
    print("📊 Testing NYALA - Trading Engine")
    print("=" * 33)
    
    prompt = """Hello NYALA! You are the trading engine for HONEY DUO WEALTH.
    Analyze Bitcoin (BTC) for a potential trade recommendation.
    Consider: market sentiment, technical indicators, risk factors.
    Provide: BUY/SELL/HOLD recommendation with confidence level."""
    
    response = ask_nyala(prompt)
    print(f"NYALA Response:\n{response}")
    
    # Log the interaction
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "member": "NYALA",
        "analysis_target": "Bitcoin (BTC)",
        "prompt": prompt,
        "response": response
    }
    
    with open("ai_family/nyala/test_log.json", "w") as f:
        json.dump(log_entry, f, indent=2)
    
    print(f"\n✅ Test logged to ai_family/nyala/test_log.json")

if __name__ == "__main__":
    test_nyala()