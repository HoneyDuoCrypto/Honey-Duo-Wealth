#!/usr/bin/env python3
"""
CLAUDAE Training Data Collector
Automatically captures code examples, decisions, and patterns during development
Part of HONEY DUO WEALTH AI Family Training System
"""

import json
import os
import datetime
from pathlib import Path
from typing import Dict, List, Any
import hashlib

class CLAUDAETrainingCollector:
    def __init__(self, project_root: str = "~/honey_duo_wealth"):
        self.project_root = Path(project_root).expanduser()
        self.training_dir = self.project_root / "ai_family" / "claudae" / "training"
        self.setup_directories()
        
    def setup_directories(self):
        """Create training data directory structure"""
        directories = [
            "code_examples",
            "architecture_decisions", 
            "debugging_solutions",
            "system_patterns",
            "error_handling"
        ]
        
        for dir_name in directories:
            (self.training_dir / dir_name).mkdir(parents=True, exist_ok=True)
            
    def collect_code_example(self, code: str, context: str, category: str, 
                           reasoning: str = "", tags: List[str] = None):
        """
        Collect a code example with full context
        
        Args:
            code: The actual code snippet
            context: What this code does in the system
            category: Type of code (api_integration, error_handling, etc.)
            reasoning: Why we chose this approach
            tags: Additional searchable tags
        """
        if tags is None:
            tags = []
            
        example = {
            "timestamp": datetime.datetime.now().isoformat(),
            "code": code,
            "context": context,
            "category": category,
            "reasoning": reasoning,
            "tags": tags,
            "hash": hashlib.md5(code.encode()).hexdigest()[:8],
            "file_pattern": self._extract_patterns(code)
        }
        
        # Save to category-specific file
        filename = f"{category}_examples.json"
        self._append_to_file(Path("code_examples") / filename, example)
        
        # Also save to daily log
        daily_file = f"daily_log_{datetime.date.today().isoformat()}.json"
        self._append_to_file(Path("code_examples") / daily_file, example)
        
    def collect_architecture_decision(self, decision: str, alternatives: List[str],
                                    reasoning: str, impact: str):
        """Record major architecture decisions"""
        decision_record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "decision": decision,
            "alternatives_considered": alternatives,
            "reasoning": reasoning,
            "expected_impact": impact,
            "components_affected": []
        }
        
        self._append_to_file(Path("debugging_solutions") / "solutions.json", debug_record)
        
    def collect_debugging_solution(self, problem: str, symptoms: str, 
                                 solution: str, prevention: str = ""):
        """Record debugging solutions for future reference"""
        debug_record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "problem": problem,
            "symptoms": symptoms,
            "solution": solution,
            "prevention": prevention,
            "component": self._guess_component(problem)
        }
        
        self._append_to_file(Path("debugging_solutions") / "solutions.json", debug_record)
        
    def collect_system_pattern(self, pattern_name: str, description: str,
                              code_example: str, when_to_use: str):
        """Record reusable system patterns"""
        pattern = {
            "timestamp": datetime.datetime.now().isoformat(),
            "name": pattern_name,
            "description": description,
            "code_example": code_example,
            "when_to_use": when_to_use,
            "frequency": 1  # Will be updated when pattern is reused
        }
        
        self._append_to_file(Path("debugging_solutions") / "solutions.json", debug_record)
        
    def generate_training_summary(self) -> Dict[str, Any]:
        """Generate a summary of all collected training data"""
        summary = {
            "generation_date": datetime.datetime.now().isoformat(),
            "total_examples": 0,
            "categories": {},
            "key_patterns": [],
            "frequent_solutions": [],
            "recent_activity": []
        }
        
        # Count examples by category
        code_examples_dir = self.training_dir / "code_examples"
        if code_examples_dir.exists():
            for file_path in code_examples_dir.glob("*_examples.json"):
                category = file_path.stem.replace("_examples", "")
                examples = self._load_from_file(file_path)
                summary["categories"][category] = len(examples)
                summary["total_examples"] += len(examples)
                
        # Save summary
        summary_path = self.training_dir / "training_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
            
        return summary
        
    def _extract_patterns(self, code: str) -> List[str]:
        """Extract common patterns from code for CLAUDAE to learn"""
        patterns = []
        
        if "try:" in code and "except:" in code:
            patterns.append("error_handling")
        if "redis.get" in code or "cache" in code.lower():
            patterns.append("caching")
        if "log" in code.lower():
            patterns.append("logging")
        if "def " in code:
            patterns.append("function_definition")
        if "import " in code:
            patterns.append("module_import")
            
        return patterns
        
    def _guess_component(self, text: str) -> str:
        """Guess which system component based on text content"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["nyala", "trading", "market"]):
            return "nyala"
        elif any(word in text_lower for word in ["deon", "risk", "portfolio"]):
            return "deon"
        elif any(word in text_lower for word in ["claudae", "system", "monitor"]):
            return "claudae"
        else:
            return "general"
            
    def _append_to_file(self, relative_path: Path, data: Dict[str, Any]):
        """Append data to a JSON file, creating if needed"""
        file_path = self.training_dir / relative_path
        
        # Load existing data
        existing_data = []
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    existing_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                existing_data = []
                
        # Append new data
        existing_data.append(data)
        
        # Save back
        with open(file_path, 'w') as f:
            json.dump(existing_data, f, indent=2)
            
    def _load_from_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

# Convenience functions for easy collection during development
def collect_code(code: str, context: str, category: str = "general", 
                reasoning: str = "", tags: List[str] = None):
    """Quick function to collect code examples"""
    collector = CLAUDAETrainingCollector()
    collector.collect_code_example(code, context, category, reasoning, tags)
    print(f"✅ Collected {category} code example: {context[:50]}...")

def collect_decision(decision: str, alternatives: List[str], reasoning: str, impact: str):
    """Quick function to collect architecture decisions"""
    collector = CLAUDAETrainingCollector()
    collector.collect_architecture_decision(decision, alternatives, reasoning, impact)
    print(f"✅ Collected architecture decision: {decision[:50]}...")

def collect_debug(problem: str, symptoms: str, solution: str, prevention: str = ""):
    """Quick function to collect debugging solutions"""
    collector = CLAUDAETrainingCollector()
    collector.collect_debugging_solution(problem, symptoms, solution, prevention)
    print(f"✅ Collected debugging solution: {problem[:50]}...")

def collect_pattern(name: str, description: str, code: str, when_to_use: str):
    """Quick function to collect system patterns"""
    collector = CLAUDAETrainingCollector()
    collector.collect_system_pattern(name, description, code, when_to_use)
    print(f"✅ Collected system pattern: {name}")

if __name__ == "__main__":
    # Test the collector
    collector = CLAUDAETrainingCollector()
    
    # Test code example collection
    test_code = """
def get_crypto_price(symbol):
    # Check Redis cache first
    cached = redis.get(f"price:{symbol}")
    if cached:
        return json.loads(cached)
    
    # Fetch from CoinGecko API
    try:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd")
        price_data = response.json()
        
        # Cache for 5 minutes
        redis.setex(f"price:{symbol}", 300, json.dumps(price_data))
        return price_data
    except Exception as e:
        logger.error(f"Failed to fetch price for {symbol}: {e}")
        return get_last_known_price(symbol)
"""
    
    collector.collect_code_example(
        code=test_code,
        context="Crypto price fetching with cache-first pattern",
        category="market_data",
        reasoning="Cache reduces API calls and provides fallback during outages",
        tags=["caching", "api", "error_handling", "crypto"]
    )
    
    # Generate summary
    summary = collector.generate_training_summary()
    print(f"Training summary: {summary}")
    print("✅ CLAUDAE training data collector ready!")