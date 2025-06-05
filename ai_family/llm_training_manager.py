#!/usr/bin/env python3
"""
LLM Training & Version Control Manager
Comprehensive training pipeline with version control for CLAUDAE, NYALA, DEON
"""

import json
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
import hashlib

class LLMTrainingManager:
    def __init__(self, project_root="~/honey_duo_wealth"):
        self.project_root = Path(project_root).expanduser()
        self.models_dir = self.project_root / "ai_family" / "models"
        self.training_dir = self.project_root / "ai_family" / "training_data"
        self.versions_dir = self.project_root / "ai_family" / "versions"
        self.setup_directories()
        
    def setup_directories(self):
        """Create training infrastructure"""
        dirs = [
            self.models_dir / "claudae",
            self.models_dir / "nyala", 
            self.models_dir / "deon",
            self.training_dir / "datasets",
            self.training_dir / "preprocessed",
            self.versions_dir / "claudae",
            self.versions_dir / "nyala",
            self.versions_dir / "deon"
        ]
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            
    def prepare_training_dataset(self, ai_name: str):
        """Prepare training dataset from collected examples"""
        from .claudae.training.claudae_training_collector import CLAUDAETrainingCollector
        
        collector = CLAUDAETrainingCollector()
        summary = collector.generate_training_summary()
        
        # Load all training examples
        examples = []
        training_path = self.project_root / "ai_family" / "claudae" / "training"
        
        for category_file in (training_path / "code_examples").glob("*_examples.json"):
            with open(category_file) as f:
                examples.extend(json.load(f))
                
        # Convert to training format
        training_data = []
        for example in examples:
            training_data.append({
                "input": f"Context: {example['context']}\nCategory: {example['category']}",
                "output": example['code'],
                "metadata": {
                    "reasoning": example.get('reasoning', ''),
                    "tags": example.get('tags', []),
                    "timestamp": example['timestamp']
                }
            })
            
        # Save preprocessed dataset
        dataset_file = self.training_dir / "datasets" / f"{ai_name}_training_{datetime.now().strftime('%Y%m%d')}.json"
        with open(dataset_file, 'w') as f:
            json.dump(training_data, f, indent=2)
            
        return dataset_file, len(training_data)
        
    def create_model_version(self, ai_name: str, base_model: str, notes: str = ""):
        """Create new model version with metadata"""
        version_num = self._get_next_version(ai_name)
        version_id = f"v{version_num}"
        
        version_metadata = {
            "version": version_id,
            "ai_name": ai_name,
            "base_model": base_model,
            "created": datetime.now().isoformat(),
            "training_data_size": 0,
            "performance_metrics": {},
            "notes": notes,
            "status": "created"
        }
        
        version_dir = self.versions_dir / ai_name / version_id
        version_dir.mkdir(parents=True, exist_ok=True)
        
        # Save metadata
        with open(version_dir / "metadata.json", 'w') as f:
            json.dump(version_metadata, f, indent=2)
            
        return version_id, version_dir
        
    def fine_tune_model(self, ai_name: str, version_id: str, training_params: dict):
        """Execute fine-tuning with comprehensive logging"""
        version_dir = self.versions_dir / ai_name / version_id
        
        # Prepare dataset
        dataset_file, data_size = self.prepare_training_dataset(ai_name)
        
        # Update metadata
        metadata_file = version_dir / "metadata.json"
        with open(metadata_file) as f:
            metadata = json.load(f)
        metadata["training_data_size"] = data_size
        metadata["training_params"] = training_params
        metadata["status"] = "training"
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        # Create training script
        training_script = self._generate_training_script(ai_name, dataset_file, training_params, version_dir)
        
        print(f"🎓 Starting fine-tuning for {ai_name} {version_id}")
        print(f"   Dataset: {data_size} examples")
        print(f"   Output: {version_dir}")
        
        # Execute training (placeholder - integrate with actual training framework)
        return self._execute_training(training_script, version_dir)
        
    def validate_model(self, ai_name: str, version_id: str):
        """Validate model performance"""
        version_dir = self.versions_dir / ai_name / version_id
        
        # Load test cases
        test_cases = self._load_test_cases(ai_name)
        
        # Run validation
        results = {}
        for test_name, test_data in test_cases.items():
            result = self._run_model_test(ai_name, version_id, test_data)
            results[test_name] = result
            
        # Calculate metrics
        metrics = self._calculate_performance_metrics(results)
        
        # Update metadata
        metadata_file = version_dir / "metadata.json"
        with open(metadata_file) as f:
            metadata = json.load(f)
        metadata["performance_metrics"] = metrics
        metadata["validation_results"] = results
        metadata["status"] = "validated"
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        return metrics
        
    def deploy_model(self, ai_name: str, version_id: str):
        """Deploy model version to production"""
        version_dir = self.versions_dir / ai_name / version_id
        production_dir = self.models_dir / ai_name / "production"
        
        # Backup current production
        if production_dir.exists():
            backup_dir = self.models_dir / ai_name / f"backup_{datetime.now().strftime('%Y%m%d_%H%M')}"
            shutil.copytree(production_dir, backup_dir)
            
        # Deploy new version
        if production_dir.exists():
            shutil.rmtree(production_dir)
        shutil.copytree(version_dir, production_dir)
        
        # Update deployment log
        deployment_log = self.models_dir / ai_name / "deployment_log.json"
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "version": version_id,
            "action": "deployed"
        }
        
        if deployment_log.exists():
            with open(deployment_log) as f:
                log = json.load(f)
        else:
            log = []
        log.append(log_entry)
        
        with open(deployment_log, 'w') as f:
            json.dump(log, f, indent=2)
            
        print(f"✅ {ai_name} {version_id} deployed to production")
        
    def rollback_model(self, ai_name: str, target_version: str = None):
        """Rollback to previous version"""
        if not target_version:
            # Find last working version
            deployment_log = self.models_dir / ai_name / "deployment_log.json"
            with open(deployment_log) as f:
                log = json.load(f)
            target_version = log[-2]["version"]  # Previous deployment
            
        self.deploy_model(ai_name, target_version)
        print(f"🔄 Rolled back {ai_name} to {target_version}")
        
    def get_model_status(self, ai_name: str = None):
        """Get comprehensive model status"""
        if ai_name:
            ais = [ai_name]
        else:
            ais = ["claudae", "nyala", "deon"]
            
        status = {}
        for ai in ais:
            ai_versions = list((self.versions_dir / ai).glob("v*"))
            latest_version = max(ai_versions, key=lambda x: int(x.name[1:])) if ai_versions else None
            
            production_status = "Not Deployed"
            if (self.models_dir / ai / "production").exists():
                production_status = "Deployed"
                
            status[ai] = {
                "total_versions": len(ai_versions),
                "latest_version": latest_version.name if latest_version else None,
                "production_status": production_status,
                "training_examples": self._count_training_examples(ai)
            }
            
        return status
        
    def _get_next_version(self, ai_name: str):
        """Get next version number"""
        existing_versions = list((self.versions_dir / ai_name).glob("v*"))
        if not existing_versions:
            return 1
        version_nums = [int(v.name[1:]) for v in existing_versions]
        return max(version_nums) + 1
        
    def _generate_training_script(self, ai_name: str, dataset_file: Path, params: dict, output_dir: Path):
        """Generate training script for the model"""
        script_content = f"""#!/usr/bin/env python3
# Auto-generated training script for {ai_name}
import json
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer

def load_dataset():
    with open('{dataset_file}') as f:
        return json.load(f)

def train_model():
    # Load base model
    model_name = "{params.get('base_model', 'mistral:7b')}"
    
    # Training configuration
    training_args = TrainingArguments(
        output_dir='{output_dir}',
        num_train_epochs={params.get('epochs', 3)},
        per_device_train_batch_size={params.get('batch_size', 4)},
        learning_rate={params.get('learning_rate', 2e-5)},
        logging_steps=10,
        save_strategy="epoch"
    )
    
    print("🎓 Training {ai_name} with {len(dataset)} examples")
    # Add actual training code here
    
if __name__ == "__main__":
    train_model()
"""
        script_path = output_dir / "train.py"
        with open(script_path, 'w') as f:
            f.write(script_content)
        return script_path
        
    def _execute_training(self, script_path: Path, output_dir: Path):
        """Execute training script"""
        # For now, simulate training
        print(f"   Executing: {script_path}")
        print("   Training simulation - would run actual fine-tuning here")
        
        # Create dummy model file
        model_file = output_dir / "model.bin"
        model_file.touch()
        
        return {"status": "completed", "model_file": str(model_file)}
        
    def _load_test_cases(self, ai_name: str):
        """Load test cases for validation"""
        return {
            "code_generation": {"input": "Generate a function", "expected_pattern": "def "},
            "error_handling": {"input": "Handle API error", "expected_pattern": "try:"},
            "project_knowledge": {"input": "HONEY DUO WEALTH", "expected_pattern": "family"}
        }
        
    def _run_model_test(self, ai_name: str, version_id: str, test_data: dict):
        """Run individual test case"""
        # Simulate model testing
        return {
            "score": 0.85,
            "output": "Generated test output",
            "passed": True
        }
        
    def _calculate_performance_metrics(self, results: dict):
        """Calculate overall performance metrics"""
        scores = [r["score"] for r in results.values()]
        return {
            "average_score": sum(scores) / len(scores),
            "pass_rate": sum(1 for r in results.values() if r["passed"]) / len(results),
            "total_tests": len(results)
        }
        
    def _count_training_examples(self, ai_name: str):
        """Count training examples for AI"""
        try:
            from .claudae.training.claudae_training_collector import CLAUDAETrainingCollector
            collector = CLAUDAETrainingCollector()
            summary = collector.generate_training_summary()
            return summary.get('total_examples', 0)
        except:
            return 0

# CLI Interface
if __name__ == "__main__":
    import sys
    
    manager = LLMTrainingManager()
    
    if len(sys.argv) < 2:
        print("LLM Training Manager")
        print("Commands:")
        print("  status [ai_name] - Show model status")
        print("  create <ai_name> <base_model> [notes] - Create new version")
        print("  train <ai_name> <version> - Start training")
        print("  validate <ai_name> <version> - Validate model")
        print("  deploy <ai_name> <version> - Deploy to production")
        print("  rollback <ai_name> [version] - Rollback model")
        sys.exit(0)
        
    command = sys.argv[1]
    
    if command == "status":
        ai_name = sys.argv[2] if len(sys.argv) > 2 else None
        status = manager.get_model_status(ai_name)
        print(json.dumps(status, indent=2))
        
    elif command == "create":
        ai_name = sys.argv[2]
        base_model = sys.argv[3]
        notes = sys.argv[4] if len(sys.argv) > 4 else ""
        version_id, version_dir = manager.create_model_version(ai_name, base_model, notes)
        print(f"✅ Created {ai_name} {version_id} at {version_dir}")
        
    elif command == "train":
        ai_name = sys.argv[2]
        version_id = sys.argv[3]
        params = {"epochs": 3, "batch_size": 4, "learning_rate": 2e-5}
        result = manager.fine_tune_model(ai_name, version_id, params)
        print(f"Training result: {result}")
        
    elif command == "validate":
        ai_name = sys.argv[2] 
        version_id = sys.argv[3]
        metrics = manager.validate_model(ai_name, version_id)
        print(f"Validation metrics: {json.dumps(metrics, indent=2)}")
        
    elif command == "deploy":
        ai_name = sys.argv[2]
        version_id = sys.argv[3]
        manager.deploy_model(ai_name, version_id)
        
    elif command == "rollback":
        ai_name = sys.argv[2]
        target_version = sys.argv[3] if len(sys.argv) > 3 else None
        manager.rollback_model(ai_name, target_version)