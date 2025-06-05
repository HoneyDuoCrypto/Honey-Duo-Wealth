#!/usr/bin/env python3
"""
Fast AI Configuration - Optimized for trading speed
"""

import ollama
import time
from concurrent.futures import ThreadPoolExecutor

class FastAIFamily:
    def __init__(self):
        # Use smaller, faster models for real-time trading
        self.models = {
            'claudae': {
                'primary': 'mistral:7b',
                'backup': 'phi:2.7b',  # Ultra-fast backup
                'timeout': 10
            },
            'nyala': {
                'primary': 'mistral:7b',  # Replace Mixtral for speed
                'backup': 'neural-chat:7b',
                'timeout': 15
            },
            'deon': {
                'primary': 'llama2:7b',  # Smaller version
                'backup': 'phi:2.7b',
                'timeout': 10
            }
        }
        
        # Pre-load models
        self.preload_models()
        
    def preload_models(self):
        """Keep models warm in memory"""
        print("⚡ Pre-loading AI models for fast response...")
        
        for ai_name, config in self.models.items():
            try:
                # Load primary model
                ollama.chat(
                    model=config['primary'],
                    messages=[{'role': 'user', 'content': 'Initialize'}],
                    keep_alive='24h'
                )
                print(f"✅ {ai_name}: {config['primary']} loaded")
            except:
                print(f"❌ {ai_name}: Failed to load {config['primary']}")
    
    def quick_decision(self, market_data):
        """Ultra-fast trading decision (<5 seconds total)"""
        with ThreadPoolExecutor(max_workers=3) as executor:
            # Parallel AI queries
            futures = {
                'nyala': executor.submit(self._quick_analysis, 'nyala', market_data),
                'deon': executor.submit(self._quick_risk, 'deon', market_data)
            }
            
            results = {}
            for name, future in futures.items():
                try:
                    results[name] = future.result(timeout=5)
                except:
                    results[name] = {'decision': 'HOLD', 'reason': 'timeout'}
            
            return results
    
    def _quick_analysis(self, ai_name, data):
        """Fast market analysis"""
        prompt = f"QUICK: BUY/SELL/HOLD for {data['symbol']} at ${data['price']}? (10 words max)"
        
        response = ollama.chat(
            model=self.models[ai_name]['primary'],
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.1, 'num_predict': 50}
        )
        
        return {
            'decision': response['message']['content'],
            'model': self.models[ai_name]['primary']
        }
    
    def _quick_risk(self, ai_name, data):
        """Fast risk check"""
        prompt = f"Risk level LOW/MEDIUM/HIGH for {data['symbol']}? (5 words max)"
        
        response = ollama.chat(
            model=self.models[ai_name]['primary'],
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.1, 'num_predict': 30}
        )
        
        return {
            'risk': response['message']['content'],
            'model': self.models[ai_name]['primary']
        }


if __name__ == "__main__":
    # Test fast configuration
    fast_ai = FastAIFamily()
    
    # Test data
    test_market = {
        'symbol': 'BTC-USD',
        'price': 95420.50,
        'change': 2.3
    }
    
    print("\n⚡ Testing fast decision...")
    start = time.time()
    decision = fast_ai.quick_decision(test_market)
    elapsed = time.time() - start
    
    print(f"\n✅ Decision in {elapsed:.2f} seconds:")
    print(decision)