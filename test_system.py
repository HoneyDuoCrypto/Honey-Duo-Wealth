#!/usr/bin/env python3
"""
HONEY DUO WEALTH System Test Suite
Tests all components and generates status reports
"""

import sys
import os
import traceback
from datetime import datetime
import json

class SystemTester:
    def __init__(self):
        self.results = {}
        self.start_time = datetime.now()
        
    def test_imports(self):
        """Test all component imports"""
        tests = {
            "data_pipeline": ["unified_data", "market_collector", "stock_collector"],
            "ai_family": ["data_bridge", "trading_workflow"],
            "trading_systems": ["paper_trader"],
            "monitoring": ["honey_duo_monitor"]
        }
        
        results = {}
        for module_group, modules in tests.items():
            sys.path.append(module_group)
            for module in modules:
                try:
                    __import__(module)
                    results[f"{module_group}.{module}"] = "✅ PASS"
                except Exception as e:
                    results[f"{module_group}.{module}"] = f"❌ FAIL: {e}"
                    
        return results
        
    def test_ai_family(self):
        """Test AI family communication"""
        try:
            sys.path.append('ai_family')
            from ai_orchestrator import test_all_models
            ai_results = test_all_models()
            return {"ai_family_communication": "✅ PASS", "details": ai_results}
        except Exception as e:
            return {"ai_family_communication": f"❌ FAIL: {e}"}
            
    def test_data_pipeline(self):
        """Test market data collection"""
        try:
            sys.path.append('data_pipeline')
            from unified_data import UnifiedDataInterface
            interface = UnifiedDataInterface()
            # Mock test without actual API calls
            return {"data_pipeline": "✅ PASS - Structure valid"}
        except Exception as e:
            return {"data_pipeline": f"❌ FAIL: {e}"}
            
    def test_training_system(self):
        """Test CLAUDAE training collection"""
        try:
            from ai_family.claudae.training.claudae_training_collector import CLAUDAETrainingCollector
            collector = CLAUDAETrainingCollector()
            summary = collector.generate_training_summary()
            return {
                "training_system": "✅ PASS",
                "examples_collected": summary.get('total_examples', 0)
            }
        except Exception as e:
            return {"training_system": f"❌ FAIL: {e}"}
            
    def run_full_test(self):
        """Run complete system test"""
        print("🧪 HONEY DUO WEALTH System Test")
        print("=" * 50)
        
        # Component imports
        print("\n📦 Testing Component Imports:")
        import_results = self.test_imports()
        for component, result in import_results.items():
            print(f"  {component}: {result}")
            
        # AI Family
        print("\n🤖 Testing AI Family:")
        ai_results = self.test_ai_family()
        for test, result in ai_results.items():
            print(f"  {test}: {result}")
            
        # Data Pipeline
        print("\n📊 Testing Data Pipeline:")
        data_results = self.test_data_pipeline()
        for test, result in data_results.items():
            print(f"  {test}: {result}")
            
        # Training System
        print("\n🎓 Testing Training System:")
        training_results = self.test_training_system()
        for test, result in training_results.items():
            print(f"  {test}: {result}")
            
        # Summary
        total_tests = len(import_results) + len(ai_results) + len(data_results) + len(training_results)
        passed_tests = sum(1 for results in [import_results, ai_results, data_results, training_results] 
                          for result in results.values() if "✅" in str(result))
        
        print(f"\n📈 Test Summary: {passed_tests}/{total_tests} passed")
        print(f"⏱️ Test Duration: {datetime.now() - self.start_time}")
        
        return {
            "imports": import_results,
            "ai_family": ai_results,
            "data_pipeline": data_results,
            "training": training_results,
            "summary": {"passed": passed_tests, "total": total_tests}
        }

if __name__ == "__main__":
    tester = SystemTester()
    results = tester.run_full_test()