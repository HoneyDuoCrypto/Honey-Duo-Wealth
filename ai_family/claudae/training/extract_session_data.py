#!/usr/bin/env python3
"""
CLAUDAE Training Data Extraction
Extract code examples and decisions from this development session
"""

import json
from datetime import datetime

def extract_session_training_data():
    """Extract training examples from this session"""
    
    training_data = {
        "session_date": "2025-06-04",
        "session_type": "Foundation Setup & AI Family Testing",
        "code_examples": [],
        "architectural_decisions": [],
        "ai_interactions": []
    }
    
    # Code examples from this session
    code_examples = [
        {
            "file": "ai_family/claudae/claudae_test.py",
            "purpose": "Basic AI communication and logging",
            "pattern": "ollama subprocess communication",
            "success": True
        },
        {
            "file": "system_monitor.py", 
            "purpose": "Real-time system resource monitoring",
            "pattern": "psutil system monitoring with live display",
            "success": True
        },
        {
            "file": "ai_family/nyala/nyala_test.py",
            "purpose": "Trading engine testing with market analysis",
            "pattern": "AI prompt engineering for trading decisions",
            "success": False,
            "issue": "Timeout on large model (Mixtral 8x7b)"
        }
    ]
    
    # Architectural decisions
    decisions = [
        {
            "decision": "Enhanced AI models over basic Llama2",
            "reasoning": "40% intelligence gain with Mixtral 8x7b for NYALA",
            "impact": "Better trading analysis, higher memory usage"
        },
        {
            "decision": "VS Code Remote development",
            "reasoning": "Better development experience than terminal-only",
            "impact": "Improved productivity for complex coding"
        },
        {
            "decision": "8TB storage mount for project data",
            "reasoning": "Historical data, model versions, trading logs",
            "impact": "7.3TB available for long-term data storage"
        }
    ]
    
    # AI interaction patterns
    interactions = [
        {
            "ai": "CLAUDAE",
            "prompt_type": "System status report",
            "response_quality": "Excellent - understood role immediately",
            "pattern": "Brief, professional system reports"
        },
        {
            "ai": "NYALA", 
            "prompt_type": "Market analysis request",
            "response_quality": "Timeout - model too large for default timeouts",
            "pattern": "Need increased timeout for complex analysis"
        },
        {
            "ai": "DEON",
            "prompt_type": "Risk assessment",
            "response_quality": "Timeout - similar to NYALA issue", 
            "pattern": "Need optimized prompts for risk grading"
        }
    ]
    
    training_data["code_examples"] = code_examples
    training_data["architectural_decisions"] = decisions  
    training_data["ai_interactions"] = interactions
    
    return training_data

def save_training_data():
    """Save extracted data for CLAUDAE training"""
    data = extract_session_training_data()
    
    filename = f"ai_family/claudae/training/session_{datetime.now().strftime('%Y%m%d')}.json"
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Training data saved to {filename}")
    print(f"Code examples: {len(data['code_examples'])}")
    print(f"Decisions: {len(data['architectural_decisions'])}")
    print(f"AI interactions: {len(data['ai_interactions'])}")

if __name__ == "__main__":
    save_training_data()