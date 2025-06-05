#!/usr/bin/env python3
"""
AI Family Orchestrator - Manages CLAUDAE, NYALA, and DEON
Fixes timeout issues and coordinates AI family communication
"""

import ollama
import json
import time
from datetime import datetime
from pathlib import Path

class AIFamilyOrchestrator:
    def __init__(self):
        self.models = {
            'claudae': {'name': 'mistral:7b', 'timeout': 120, 'role': 'System Guardian'},
            'nyala': {'name': 'mixtral:8x7b', 'timeout': 300, 'role': 'Trading Engine'},  # 5 min timeout
            'deon': {'name': 'llama2:13b', 'timeout': 180, 'role': 'Risk Grader'}  # 3 min timeout
        }
        self.log_dir = Path('/home/honey-duo-wealth/honey_duo_wealth/ai_family/logs')
        self.log_dir.mkdir(exist_ok=True)
        
    def test_model(self, ai_name, prompt=None):
        """Test individual AI model with proper timeout"""
        model_info = self.models[ai_name]
        
        if not prompt:
            prompt = f"You are {ai_name.upper()}, the {model_info['role']} for HONEY DUO WEALTH. Confirm your role and readiness."
        
        print(f"\n🤖 Testing {ai_name.upper()} ({model_info['name']})...")
        print(f"⏱️  Timeout: {model_info['timeout']} seconds")
        
        try:
            start_time = time.time()
            
            response = ollama.chat(
                model=model_info['name'],
                messages=[{'role': 'user', 'content': prompt}],
                options={
                    'timeout': model_info['timeout'],
                    'num_predict': 512,  # Limit response length for testing
                    'temperature': 0.7
                }
            )
            
            elapsed = time.time() - start_time
            
            result = {
                'ai': ai_name,
                'status': 'success',
                'response': response['message']['content'],
                'elapsed_time': f"{elapsed:.2f}s",
                'timestamp': datetime.now().isoformat()
            }
            
            # Log success
            self._log_interaction(ai_name, result)
            
            print(f"✅ {ai_name.upper()} responded in {elapsed:.2f}s")
            print(f"📝 Response: {result['response'][:200]}...")
            
            return result
            
        except Exception as e:
            elapsed = time.time() - start_time
            result = {
                'ai': ai_name,
                'status': 'error',
                'error': str(e),
                'elapsed_time': f"{elapsed:.2f}s",
                'timestamp': datetime.now().isoformat()
            }
            
            # Log error
            self._log_interaction(ai_name, result)
            
            print(f"❌ {ai_name.upper()} error after {elapsed:.2f}s: {str(e)}")
            return result
    
    def coordinate_decision(self, market_data):
        """Coordinate all three AIs for a trading decision"""
        print("\n🏠 HONEY DUO WEALTH - AI Family Coordination")
        print("=" * 50)
        
        decisions = {}
        
        # 1. NYALA analyzes market
        nyala_prompt = f"""As NYALA, the Trading Engine, analyze this market data:
        {json.dumps(market_data, indent=2)}
        
        Provide: 
        1. Trade recommendation (BUY/SELL/HOLD)
        2. Confidence level (0-100%)
        3. Technical reasoning
        4. Target entry/exit points"""
        
        decisions['nyala'] = self.test_model('nyala', nyala_prompt)
        
        # 2. DEON validates risk
        if decisions['nyala']['status'] == 'success':
            deon_prompt = f"""As DEON, the Risk Grader, evaluate NYALA's recommendation:
            {decisions['nyala']['response']}
            
            Provide:
            1. Risk score (0-100, lower is safer)
            2. Position size recommendation
            3. Stop loss level
            4. Approval (YES/NO) with reasoning"""
            
            decisions['deon'] = self.test_model('deon', deon_prompt)
        
        # 3. CLAUDAE oversees execution
        if all(d['status'] == 'success' for d in decisions.values()):
            claudae_prompt = f"""As CLAUDAE, the System Guardian, review the family decision:
            
            NYALA's Analysis: {decisions['nyala']['response'][:300]}...
            DEON's Risk Assessment: {decisions['deon']['response'][:300]}...
            
            Provide final execution decision and any system alerts."""
            
            decisions['claudae'] = self.test_model('claudae', claudae_prompt)
        
        return decisions
    
    def _log_interaction(self, ai_name, result):
        """Log AI interactions for training data"""
        log_file = self.log_dir / f"{ai_name}_interactions.jsonl"
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(result) + '\n')
    
    def health_check(self):
        """Check all AI models are responding"""
        print("\n🏥 HONEY DUO WEALTH - AI Family Health Check")
        print("=" * 50)
        
        results = {}
        for ai_name in self.models:
            results[ai_name] = self.test_model(ai_name)
            time.sleep(2)  # Avoid overwhelming system
        
        # Summary
        print("\n📊 Health Check Summary:")
        for ai_name, result in results.items():
            status_icon = "✅" if result['status'] == 'success' else "❌"
            print(f"{status_icon} {ai_name.upper()}: {result['status']} ({result['elapsed_time']})")
        
        return results


if __name__ == "__main__":
    orchestrator = AIFamilyOrchestrator()
    
    # Run health check
    orchestrator.health_check()
    
    # Test coordinated decision
    print("\n" + "="*50)
    print("Testing Coordinated Decision Making...")
    
    sample_market_data = {
        "symbol": "BTC-USD",
        "price": 95420.50,
        "change_24h": 2.3,
        "rsi": 45,
        "volume": 28500000000,
        "sentiment": "neutral"
    }
    
    decisions = orchestrator.coordinate_decision(sample_market_data)