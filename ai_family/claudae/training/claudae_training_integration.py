#!/usr/bin/env python3
"""
CLAUDAE Training Integration
Seamlessly integrates training data collection into development workflow
"""

import os
import sys
import json
from pathlib import Path
import subprocess
from datetime import datetime
from .claudae_training_collector import CLAUDAETrainingCollector

class CLAUDAETrainingIntegration:
    def __init__(self):
        self.collector = CLAUDAETrainingCollector()
        self.session_log = []
        
    def start_session(self, session_name: str):
        """Start a new development session"""
        self.session_name = session_name
        self.session_start = datetime.now()
        print(f"🎯 CLAUDAE Training Session: {session_name}")
        print("All code and decisions will be collected for training")
        
    def quick_collect(self, code: str, description: str, category: str = "development"):
        """Quick collection during active development"""
        self.collector.collect_code_example(
            code=code,
            context=f"Session: {self.session_name} - {description}",
            category=category,
            reasoning="Active development pattern",
            tags=[self.session_name, "active_dev"]
        )
        
        self.session_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "code",
            "description": description,
            "category": category
        })
        
    def collect_file_creation(self, filepath: str, purpose: str, key_patterns: list = None):
        """Collect when we create new files"""
        if key_patterns is None:
            key_patterns = []
            
        try:
            with open(filepath, 'r') as f:
                code = f.read()
                
            self.collector.collect_code_example(
                code=code,
                context=f"File creation: {filepath} - {purpose}",
                category="file_creation",
                reasoning=f"Created for: {purpose}",
                tags=["file_creation"] + key_patterns
            )
            
            print(f"✅ Collected file creation: {Path(filepath).name}")
            
        except Exception as e:
            print(f"❌ Failed to collect {filepath}: {e}")
            
    def collect_problem_solution(self, problem: str, solution_code: str, explanation: str):
        """Collect problem-solving patterns"""
        self.collector.collect_debugging_solution(
            problem=problem,
            symptoms="Development challenge encountered",
            solution=f"{explanation}\n\nCode:\n{solution_code}",
            prevention="Pattern learned for future reference"
        )
        
        print(f"✅ Collected problem solution: {problem[:50]}...")
        
    def collect_architecture_choice(self, choice: str, alternatives: list, reasoning: str):
        """Collect architectural decisions made during development"""
        self.collector.collect_architecture_decision(
            decision=choice,
            alternatives=alternatives,
            reasoning=reasoning,
            impact="Will influence future development patterns"
        )
        
        print(f"✅ Collected architecture choice: {choice[:50]}...")
        
    def end_session(self):
        """End session and generate summary"""
        duration = datetime.now() - self.session_start
        
        session_summary = {
            "session_name": self.session_name,
            "duration_minutes": int(duration.total_seconds() / 60),
            "items_collected": len(self.session_log),
            "categories": list(set(item.get("category", "unknown") for item in self.session_log)),
            "timestamp": datetime.now().isoformat()
        }
        
        # Save session log
        session_file = self.collector.training_dir / "sessions" / f"{self.session_name}_{datetime.now().strftime('%Y%m%d')}.json"
        session_file.parent.mkdir(exist_ok=True)
        
        with open(session_file, 'w') as f:
            json.dump({
                "summary": session_summary,
                "log": self.session_log
            }, f, indent=2)
            
        print(f"\n🎓 Session Complete: {self.session_name}")
        print(f"   Duration: {duration}")
        print(f"   Items collected: {len(self.session_log)}")
        print(f"   Categories: {', '.join(session_summary['categories'])}")
        
        # Generate overall training summary
        summary = self.collector.generate_training_summary()
        print(f"   Total training examples: {summary['total_examples']}")

# Development helper functions for easy integration
def train_start(session_name: str):
    """Start training collection session"""
    global training_session
    training_session = CLAUDAETrainingIntegration()
    training_session.start_session(session_name)
    
def train_code(code: str, description: str, category: str = "development"):
    """Quick code collection"""
    if 'training_session' in globals():
        training_session.quick_collect(code, description, category)
    else:
        print("❌ No training session active. Run train_start() first.")
        
def train_file(filepath: str, purpose: str, patterns: list = None):
    """Collect file creation"""
    if 'training_session' in globals():
        training_session.collect_file_creation(filepath, purpose, patterns)
    else:
        print("❌ No training session active. Run train_start() first.")
        
def train_solution(problem: str, code: str, explanation: str):
    """Collect problem solution"""
    if 'training_session' in globals():
        training_session.collect_problem_solution(problem, code, explanation)
    else:
        print("❌ No training session active. Run train_start() first.")
        
def train_decision(choice: str, alternatives: list, reasoning: str):
    """Collect architecture decision"""
    if 'training_session' in globals():
        training_session.collect_architecture_choice(choice, alternatives, reasoning)
    else:
        print("❌ No training session active. Run train_start() first.")
        
def train_end():
    """End training session"""
    if 'training_session' in globals():
        training_session.end_session()
        del globals()['training_session']
    else:
        print("❌ No training session active.")

# Auto-import into development environment
def setup_training_environment():
    """Add training functions to Python environment"""
    training_code = """
# CLAUDAE Training Integration
from ai_family.claudae.training.claudae_training_integration import *

# Quick reference:
# train_start("session_name") - Start collecting
# train_code(code, "description") - Collect code
# train_file("path/file.py", "purpose") - Collect file
# train_solution("problem", code, "explanation") - Collect solution
# train_decision("choice", ["alt1", "alt2"], "reasoning") - Collect decision
# train_end() - End session and summarize
    """
    
    startup_file = Path.home() / ".pythonrc"
    with open(startup_file, 'a') as f:
        f.write(training_code)
        
    print("✅ Training functions added to Python environment")
    print("Use train_start('session_name') to begin collecting training data")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup_training_environment()
    else:
        # Interactive setup
        print("🎯 CLAUDAE Training Integration Setup")
        print("\nThis will help CLAUDAE learn from our development process.")
        print("\nExample workflow:")
        print("1. train_start('market_data_pipeline')")
        print("2. # Write some code")
        print("3. train_code(code, 'Crypto price fetching logic')")
        print("4. train_file('market_collector.py', 'Real-time data collection')")
        print("5. train_end()")
        print("\nReady to train CLAUDAE as we build! 🚀")