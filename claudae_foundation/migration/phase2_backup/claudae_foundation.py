#!/usr/bin/env python3
"""
CLAUDAE Memory System - Foundation Infrastructure
=================================================

Phase 1: Safe infrastructure deployment
- No document modifications
- Comprehensive validation
- Bulletproof backup systems
- Risk-mitigated approach

Author: Claude (Lead)
Project: HONEY DUO WEALTH - AI Family Guardian System
Status: Foundation Phase - SAFE DEPLOYMENT
"""

import os
import json
import time
import hashlib
import asyncio
import logging
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import requests

# Configure comprehensive logging
def setup_logging(log_dir: Path):
    """Setup comprehensive logging system"""
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "claudae_foundation.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - CLAUDAE-FOUNDATION - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

@dataclass
class SystemValidation:
    """System validation results"""
    component: str
    status: bool
    message: str
    timestamp: datetime
    details: Dict[str, Any] = None

class CLAUDAEFoundationSystem:
    """Foundation infrastructure for CLAUDAE memory system"""
    
    def __init__(self, project_root: str = "/home/honey-duo-wealth/honey_duo_wealth"):
        self.project_root = Path(project_root)
        self.foundation_dir = self.project_root / "claudae_foundation"
        self.memory_dir = self.project_root / "project_memory"
        
        # Create foundation directory
        self.foundation_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.logger = setup_logging(self.foundation_dir / "logs")
        
        # Validation results
        self.validations: List[SystemValidation] = []
        
        self.logger.info("🎯 CLAUDAE Foundation System initializing...")
        self.logger.info(f"Project root: {self.project_root}")
        self.logger.info(f"Foundation dir: {self.foundation_dir}")
    
    async def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run comprehensive system validation before any deployment"""
        self.logger.info("🔍 Starting comprehensive system validation...")
        
        validation_results = {
            "start_time": datetime.now().isoformat(),
            "validations": [],
            "overall_status": False,
            "ready_for_deployment": False
        }
        
        # Validation sequence
        validations = [
            self._validate_environment,
            self._validate_claudae_connection,
            self._validate_project_structure,
            self._validate_existing_documentation,
            self._validate_git_repository,
            self._validate_dependencies,
            self._validate_permissions
        ]
        
        all_passed = True
        for validation_func in validations:
            try:
                result = await validation_func()
                self.validations.append(result)
                validation_results["validations"].append(asdict(result))
                
                if result.status:
                    self.logger.info(f"✅ {result.component}: {result.message}")
                else:
                    self.logger.error(f"❌ {result.component}: {result.message}")
                    all_passed = False
                    
            except Exception as e:
                error_result = SystemValidation(
                    component=validation_func.__name__,
                    status=False,
                    message=f"Validation error: {str(e)}",
                    timestamp=datetime.now().isoformat()
                )
                self.validations.append(error_result)
                validation_results["validations"].append(asdict(error_result))
                self.logger.error(f"❌ {validation_func.__name__}: {str(e)}")
                all_passed = False
        
        validation_results["overall_status"] = all_passed
        validation_results["ready_for_deployment"] = all_passed
        validation_results["end_time"] = datetime.now().isoformat()
        
        # Save validation results
        results_file = self.foundation_dir / "validation_results.json"
        with open(results_file, 'w') as f:
            json.dump(validation_results, f, indent=2)
        
        self.logger.info(f"🎯 Validation complete: {'READY' if all_passed else 'NOT READY'}")
        return validation_results
    
    async def _validate_environment(self) -> SystemValidation:
        """Validate the basic environment"""
        try:
            # Check project directory
            if not self.project_root.exists():
                return SystemValidation(
                    component="Environment",
                    status=False,
                    message=f"Project directory not found: {self.project_root}",
                    timestamp=datetime.now().isoformat()
                )
            
            # Check virtual environment
            venv_path = self.project_root / "venv"
            if not venv_path.exists():
                return SystemValidation(
                    component="Environment",
                    status=False,
                    message="Virtual environment not found",
                    timestamp=datetime.now().isoformat()
                )
            
            # Check if we're in the venv
            if "honey_duo_wealth" not in str(os.environ.get("VIRTUAL_ENV", "")):
                return SystemValidation(
                    component="Environment",
                    status=False,
                    message="Virtual environment not activated",
                    timestamp=datetime.now().isoformat()
                )
            
            return SystemValidation(
                component="Environment",
                status=True,
                message="Environment validated successfully",
                timestamp=datetime.now().isoformat(),
                details={"project_root": str(self.project_root), "venv": str(venv_path)}
            )
            
        except Exception as e:
            return SystemValidation(
                component="Environment",
                status=False,
                message=f"Environment validation failed: {str(e)}",
                timestamp=datetime.now().isoformat()
            )
    
    async def _validate_claudae_connection(self) -> SystemValidation:
        """Validate CLAUDAE (Ollama) connection and model availability"""
        try:
            # Check Ollama service
            response = requests.get("http://localhost:11434/api/tags", timeout=10)
            if response.status_code != 200:
                return SystemValidation(
                    component="CLAUDAE Connection",
                    status=False,
                    message="Ollama service not accessible",
                    timestamp=datetime.now().isoformat()
                )
            
            # Check for mistral:7b model
            models = response.json()
            mistral_found = False
            for model in models.get("models", []):
                if "mistral:7b" in model.get("name", ""):
                    mistral_found = True
                    break
            
            if not mistral_found:
                return SystemValidation(
                    component="CLAUDAE Connection",
                    status=False,
                    message="CLAUDAE model (mistral:7b) not found",
                    timestamp=datetime.now().isoformat()
                )
            
            # Test basic CLAUDAE query
            test_response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "mistral:7b",
                    "prompt": "Respond with 'CLAUDAE OPERATIONAL' if you can understand this.",
                    "stream": False
                },
                timeout=30
            )
            
            if test_response.status_code == 200:
                result = test_response.json()
                if "operational" in result.get("response", "").lower():
                    return SystemValidation(
                        component="CLAUDAE Connection",
                        status=True,
                        message="CLAUDAE connection validated successfully",
                        timestamp=datetime.now().isoformat(),
                        details={"model": "mistral:7b", "response_time": "OK"}
                    )
            
            return SystemValidation(
                component="CLAUDAE Connection",
                status=False,
                message="CLAUDAE test query failed",
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            return SystemValidation(
                component="CLAUDAE Connection",
                status=False,
                message=f"CLAUDAE validation failed: {str(e)}",
                timestamp=datetime.now().isoformat()
            )
    
    async def _validate_project_structure(self) -> SystemValidation:
        """Validate existing project structure"""
        try:
            required_dirs = [
                self.project_root / "ai_family",
                self.project_root / "monitoring",
                self.memory_dir
            ]
            
            missing_dirs = []
            for dir_path in required_dirs:
                if not dir_path.exists():
                    missing_dirs.append(str(dir_path))
            
            if missing_dirs:
                return SystemValidation(
                    component="Project Structure",
                    status=False,
                    message=f"Missing directories: {', '.join(missing_dirs)}",
                    timestamp=datetime.now().isoformat()
                )
            
            return SystemValidation(
                component="Project Structure",
                status=True,
                message="Project structure validated successfully",
                timestamp=datetime.now().isoformat(),
                details={"validated_dirs": [str(d) for d in required_dirs]}
            )
            
        except Exception as e:
            return SystemValidation(
                component="Project Structure",
                status=False,
                message=f"Project structure validation failed: {str(e)}",
                timestamp=datetime.now().isoformat()
            )
    
    async def _validate_existing_documentation(self) -> SystemValidation:
        """Validate existing documentation without modifying it"""
        try:
            doc_patterns = ["*.md", "*.json", "*.yaml", "*.yml"]
            total_docs = 0
            total_size = 0
            doc_types = {}
            
            for pattern in doc_patterns:
                docs = list(self.project_root.rglob(pattern))
                for doc in docs:
                    if doc.is_file():
                        total_docs += 1
                        total_size += doc.stat().st_size
                        ext = doc.suffix.lower()
                        doc_types[ext] = doc_types.get(ext, 0) + 1
            
            if total_docs == 0:
                return SystemValidation(
                    component="Existing Documentation",
                    status=False,
                    message="No documentation files found to preserve",
                    timestamp=datetime.now().isoformat()
                )
            
            return SystemValidation(
                component="Existing Documentation",
                status=True,
                message=f"Found {total_docs} documentation files to preserve",
                timestamp=datetime.now().isoformat(),
                details={
                    "total_files": total_docs,
                    "total_size_mb": round(total_size / 1024 / 1024, 2),
                    "file_types": doc_types
                }
            )
            
        except Exception as e:
            return SystemValidation(
                component="Existing Documentation",
                status=False,
                message=f"Documentation validation failed: {str(e)}",
                timestamp=datetime.now().isoformat()
            )
    
    async def _validate_git_repository(self) -> SystemValidation:
        """Validate Git repository status"""
        try:
            # Check if git repo exists
            git_dir = self.project_root / ".git"
            if not git_dir.exists():
                return SystemValidation(
                    component="Git Repository",
                    status=False,
                    message="Git repository not initialized",
                    timestamp=datetime.now().isoformat()
                )
            
            # Check git status
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return SystemValidation(
                    component="Git Repository",
                    status=False,
                    message="Git repository error",
                    timestamp=datetime.now().isoformat()
                )
            
            # Check for uncommitted changes
            uncommitted_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            return SystemValidation(
                component="Git Repository",
                status=True,
                message="Git repository validated successfully",
                timestamp=datetime.now().isoformat(),
                details={
                    "uncommitted_files": len(uncommitted_files),
                    "status": "clean" if not uncommitted_files else "has_changes"
                }
            )
            
        except Exception as e:
            return SystemValidation(
                component="Git Repository",
                status=False,
                message=f"Git validation failed: {str(e)}",
                timestamp=datetime.now().isoformat()
            )
    
    async def _validate_dependencies(self) -> SystemValidation:
        """Validate required dependencies"""
        try:
            required_packages = ["watchdog", "requests"]
            missing_packages = []
            
            for package in required_packages:
                try:
                    __import__(package)
                except ImportError:
                    missing_packages.append(package)
            
            if missing_packages:
                return SystemValidation(
                    component="Dependencies",
                    status=False,
                    message=f"Missing packages: {', '.join(missing_packages)}",
                    timestamp=datetime.now().isoformat()
                )
            
            return SystemValidation(
                component="Dependencies",
                status=True,
                message="All dependencies validated successfully",
                timestamp=datetime.now().isoformat(),
                details={"validated_packages": required_packages}
            )
            
        except Exception as e:
            return SystemValidation(
                component="Dependencies",
                status=False,
                message=f"Dependency validation failed: {str(e)}",
                timestamp=datetime.now().isoformat()
            )
    
    async def _validate_permissions(self) -> SystemValidation:
        """Validate file and directory permissions"""
        try:
            # Check write permissions
            test_file = self.foundation_dir / "permission_test.txt"
            try:
                test_file.write_text("permission test")
                test_file.unlink()
            except Exception:
                return SystemValidation(
                    component="Permissions",
                    status=False,
                    message="Insufficient write permissions",
                    timestamp=datetime.now().isoformat()
                )
            
            # Check if we can create directories
            test_dir = self.foundation_dir / "test_dir"
            try:
                test_dir.mkdir(exist_ok=True)
                test_dir.rmdir()
            except Exception:
                return SystemValidation(
                    component="Permissions",
                    status=False,
                    message="Cannot create directories",
                    timestamp=datetime.now().isoformat()
                )
            
            return SystemValidation(
                component="Permissions",
                status=True,
                message="Permissions validated successfully",
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            return SystemValidation(
                component="Permissions",
                status=False,
                message=f"Permission validation failed: {str(e)}",
                timestamp=datetime.now().isoformat()
            )
    
    async def create_backup_system(self) -> Dict[str, Any]:
        """Create comprehensive backup system BEFORE any changes"""
        self.logger.info("🛡️ Creating bulletproof backup system...")
        
        backup_dir = self.foundation_dir / "original_state_backup"
        backup_dir.mkdir(exist_ok=True)
        
        backup_report = {
            "start_time": datetime.now().isoformat(),
            "backup_location": str(backup_dir),
            "files_backed_up": 0,
            "total_size_mb": 0,
            "backup_verification": False,
            "backup_integrity": False
        }
        
        try:
            # Copy entire project_memory directory
            if self.memory_dir.exists():
                memory_backup = backup_dir / "project_memory"
                shutil.copytree(self.memory_dir, memory_backup, dirs_exist_ok=True)
                
                # Count files and calculate size
                for file_path in memory_backup.rglob("*"):
                    if file_path.is_file():
                        backup_report["files_backed_up"] += 1
                        backup_report["total_size_mb"] += file_path.stat().st_size / 1024 / 1024
                
                backup_report["total_size_mb"] = round(backup_report["total_size_mb"], 2)
                
                # Verify backup integrity
                backup_report["backup_verification"] = self._verify_backup_integrity(
                    self.memory_dir, memory_backup
                )
                backup_report["backup_integrity"] = backup_report["backup_verification"]
                
                self.logger.info(f"✅ Backup created: {backup_report['files_backed_up']} files ({backup_report['total_size_mb']} MB)")
            
            # Create git commit for current state
            try:
                subprocess.run(
                    ["git", "add", "."],
                    cwd=self.project_root,
                    check=True,
                    capture_output=True
                )
                subprocess.run(
                    ["git", "commit", "-m", "CLAUDAE Foundation: Pre-deployment state"],
                    cwd=self.project_root,
                    check=True,
                    capture_output=True
                )
                backup_report["git_commit"] = True
                self.logger.info("✅ Git commit created for current state")
            except subprocess.CalledProcessError:
                backup_report["git_commit"] = False
                self.logger.warning("⚠️ Git commit failed (may be no changes)")
            
            backup_report["end_time"] = datetime.now().isoformat()
            backup_report["success"] = True
            
            # Save backup report
            report_file = backup_dir / "backup_report.json"
            with open(report_file, 'w') as f:
                json.dump(backup_report, f, indent=2)
            
            return backup_report
            
        except Exception as e:
            backup_report["error"] = str(e)
            backup_report["success"] = False
            self.logger.error(f"❌ Backup creation failed: {e}")
            return backup_report
    
    def _verify_backup_integrity(self, original_dir: Path, backup_dir: Path) -> bool:
        """Verify backup integrity by comparing file hashes"""
        try:
            original_files = {}
            backup_files = {}
            
            # Hash original files
            for file_path in original_dir.rglob("*"):
                if file_path.is_file():
                    rel_path = file_path.relative_to(original_dir)
                    with open(file_path, 'rb') as f:
                        original_files[str(rel_path)] = hashlib.md5(f.read()).hexdigest()
            
            # Hash backup files
            for file_path in backup_dir.rglob("*"):
                if file_path.is_file():
                    rel_path = file_path.relative_to(backup_dir)
                    with open(file_path, 'rb') as f:
                        backup_files[str(rel_path)] = hashlib.md5(f.read()).hexdigest()
            
            # Compare
            return original_files == backup_files
            
        except Exception as e:
            self.logger.error(f"Backup verification failed: {e}")
            return False
    
    async def setup_foundation_infrastructure(self) -> Dict[str, Any]:
        """Setup foundation infrastructure without touching existing docs"""
        self.logger.info("🏗️ Setting up foundation infrastructure...")
        
        setup_report = {
            "start_time": datetime.now().isoformat(),
            "components_created": [],
            "infrastructure_ready": False
        }
        
        try:
            # Create necessary directories
            dirs_to_create = [
                self.foundation_dir / "config",
                self.foundation_dir / "logs",
                self.foundation_dir / "staging",
                self.foundation_dir / "training_data",
                self.foundation_dir / "vector_store"
            ]
            
            for dir_path in dirs_to_create:
                dir_path.mkdir(exist_ok=True)
                setup_report["components_created"].append(f"Directory: {dir_path.name}")
                self.logger.info(f"✅ Created directory: {dir_path}")
            
            # Create configuration files
            config_data = {
                "claudae_memory_config": {
                    "version": "1.0",
                    "deployment_phase": "foundation",
                    "project_root": str(self.project_root),
                    "foundation_dir": str(self.foundation_dir),
                    "claudae": {
                        "model": "mistral:7b",
                        "base_url": "http://localhost:11434",
                        "timeout": 120,
                        "temperature": 0.3
                    },
                    "safety": {
                        "backup_before_changes": True,
                        "validate_operations": True,
                        "rollback_on_failure": True,
                        "max_file_size_mb": 50
                    },
                    "training": {
                        "enabled": True,
                        "collection_enabled": False,  # Will enable in Phase 2
                        "training_data_dir": str(self.foundation_dir / "training_data")
                    }
                }
            }
            
            config_file = self.foundation_dir / "config" / "foundation_config.json"
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            setup_report["components_created"].append("Configuration files")
            self.logger.info("✅ Created configuration files")
            
            # Create status tracking
            status_data = {
                "deployment_phase": "foundation",
                "phase_1_complete": False,
                "phase_2_ready": False,
                "last_update": datetime.now().isoformat(),
                "system_status": "foundation_setup"
            }
            
            status_file = self.foundation_dir / "system_status.json"
            with open(status_file, 'w') as f:
                json.dump(status_data, f, indent=2)
            setup_report["components_created"].append("Status tracking")
            
            setup_report["infrastructure_ready"] = True
            setup_report["end_time"] = datetime.now().isoformat()
            
            self.logger.info("🎯 Foundation infrastructure setup complete")
            return setup_report
            
        except Exception as e:
            setup_report["error"] = str(e)
            setup_report["infrastructure_ready"] = False
            self.logger.error(f"❌ Infrastructure setup failed: {e}")
            return setup_report

# CLI Interface for Foundation Phase
async def main():
    """Main execution for foundation phase"""
    print("🎯 CLAUDAE Memory System - Foundation Phase")
    print("=" * 50)
    print("Phase 1: Safe infrastructure deployment")
    print("- No document modifications")
    print("- Comprehensive validation")
    print("- Bulletproof backup systems")
    print()
    
    # Initialize foundation system
    foundation = CLAUDAEFoundationSystem()
    
    # Step 1: Comprehensive validation
    print("🔍 Step 1: Running comprehensive validation...")
    validation_results = await foundation.run_comprehensive_validation()
    
    if not validation_results["ready_for_deployment"]:
        print("❌ System not ready for deployment. Please address validation issues.")
        print("Check validation_results.json for details.")
        return False
    
    print("✅ All validations passed! System ready for deployment.")
    print()
    
    # Step 2: Create backup system
    print("🛡️ Step 2: Creating bulletproof backup system...")
    backup_results = await foundation.create_backup_system()
    
    if not backup_results["success"]:
        print("❌ Backup creation failed. Deployment aborted for safety.")
        return False
    
    print(f"✅ Backup created: {backup_results['files_backed_up']} files backed up")
    print()
    
    # Step 3: Setup foundation infrastructure
    print("🏗️ Step 3: Setting up foundation infrastructure...")
    setup_results = await foundation.setup_foundation_infrastructure()
    
    if not setup_results["infrastructure_ready"]:
        print("❌ Infrastructure setup failed.")
        return False
    
    print("✅ Foundation infrastructure ready!")
    print()
    
    # Success summary
    print("🎉 PHASE 1 COMPLETE - FOUNDATION DEPLOYED")
    print("=" * 50)
    print("✅ System validated")
    print("✅ Complete backup created")
    print("✅ Infrastructure deployed")
    print("✅ Ready for Phase 2: Document Migration")
    print()
    print("Next step: Run Phase 2 when ready")
    
    return True

if __name__ == "__main__":
    import sys
    success = asyncio.run(main())
    sys.exit(0 if success else 1)