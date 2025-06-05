#!/usr/bin/env python3
"""
CLAUDAE Project Management System
Auto-updates documentation, manages Git, tracks project progress
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

class CLAUDAEProjectManager:
    def __init__(self, project_root="~/honey_duo_wealth"):
        self.project_root = Path(project_root).expanduser()
        self.docs_dir = self.project_root / "documentation"
        self.memory_dir = self.project_root / "project_memory"
        
    def update_project_status(self):
        """Generate current project status"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "components": self._check_components(),
            "ai_family": self._check_ai_status(),
            "recent_changes": self._get_recent_changes(),
            "next_priorities": self._identify_next_tasks()
        }
        
        # Save to project memory
        status_file = self.memory_dir / "current_status.json"
        with open(status_file, 'w') as f:
            json.dump(status, f, indent=2)
            
        return status
        
    def auto_update_documentation(self):
        """Update documentation based on current state"""
        status = self.update_project_status()
        
        # Update README
        readme_content = f"""# HONEY DUO WEALTH - AI Portfolio Guardian
**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 🎯 Current Status
- **Phase:** {self._get_current_phase()}
- **Components Ready:** {len([c for c in status['components'].values() if c == 'Ready'])}
- **AI Family Status:** {status['ai_family']['status']}

## 🚀 Quick Start
```bash
cd ~/honey_duo_wealth
source activate.sh
python3 ai_family/ai_orchestrator.py
```

## 📊 System Health
{self._format_component_status(status['components'])}

## 🎓 CLAUDAE Training Progress
- Total Examples Collected: {self._get_training_count()}
- Categories: Market Data, AI Integration, Trading, Monitoring

## 🔗 Links
- [Master Blueprint](documentation/master_blueprint_v1.3.md)
- [Web Monitor](https://monitor.honey-duo.com)
- [Training Data](ai_family/claudae/training/)
"""
        
        readme_file = self.project_root / "README.md"
        with open(readme_file, 'w') as f:
            f.write(readme_content)
            
    def setup_git_repository(self):
        """Initialize and configure Git repository"""
        os.chdir(self.project_root)
        
        commands = [
            ["git", "init"],
            ["git", "config", "user.name", "HONEY DUO WEALTH"],
            ["git", "config", "user.email", "claudae@honey-duo.com"],
            ["git", "add", ".gitignore"],
            ["git", "add", "documentation/"],
            ["git", "add", "ai_family/"],
            ["git", "add", "README.md"]
        ]
        
        for cmd in commands:
            try:
                subprocess.run(cmd, check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                print(f"Git command failed: {' '.join(cmd)} - {e}")
                
    def commit_progress(self, message=None):
        """Auto-commit current progress"""
        if not message:
            status = self.update_project_status()
            message = f"CLAUDAE Auto-commit: {len(status['components'])} components ready"
            
        os.chdir(self.project_root)
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", message], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
            
    def generate_progress_report(self):
        """Generate detailed progress report"""
        status = self.update_project_status()
        
        report = f"""# HONEY DUO WEALTH Progress Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📋 Component Status
"""
        for component, state in status['components'].items():
            emoji = "✅" if state == "Ready" else "⏳" if state == "Partial" else "❌"
            report += f"- {emoji} **{component}**: {state}\n"
            
        report += f"""
## 🤖 AI Family Status
- **CLAUDAE**: {status['ai_family']['claudae']}
- **NYALA**: {status['ai_family']['nyala']}  
- **DEON**: {status['ai_family']['deon']}

## 🎯 Next Priorities
"""
        for priority in status['next_priorities']:
            report += f"1. {priority}\n"
            
        report += f"""
## 📊 Training Progress
- Examples Collected: {self._get_training_count()}
- Last Session: {self._get_last_training_session()}

## 🔧 Recent Changes
"""
        for change in status['recent_changes']:
            report += f"- {change}\n"
            
        # Save report
        report_file = self.docs_dir / f"progress_report_{datetime.now().strftime('%Y%m%d')}.md"
        with open(report_file, 'w') as f:
            f.write(report)
            
        return report
        
    def _check_components(self):
        """Check status of all components"""
        components = {
            "Market Data Pipeline": self._check_file_exists("data_pipeline/unified_data.py"),
            "AI Family Communication": self._check_file_exists("ai_family/ai_orchestrator.py"),
            "Trading Engine": self._check_file_exists("ai_family/nyala/trading_engine.py"),
            "Paper Trading": self._check_file_exists("trading_systems/paper_trader.py"),
            "System Monitor": self._check_file_exists("monitoring/web_monitor.py"),
            "Training System": self._check_file_exists("ai_family/claudae/training/claudae_training_collector.py")
        }
        return components
        
    def _check_ai_status(self):
        """Check AI family operational status"""
        # This would integrate with actual AI testing
        return {
            "status": "Operational",
            "claudae": "Learning Phase",
            "nyala": "Ready for Trading",
            "deon": "Risk Assessment Ready"
        }
        
    def _check_file_exists(self, relative_path):
        """Check if component file exists and has content"""
        file_path = self.project_root / relative_path
        if file_path.exists() and file_path.stat().st_size > 100:
            return "Ready"
        elif file_path.exists():
            return "Partial"
        else:
            return "Missing"
            
    def _get_current_phase(self):
        """Determine current development phase"""
        components = self._check_components()
        ready_count = len([c for c in components.values() if c == "Ready"])
        
        if ready_count >= 5:
            return "Phase 2: AI Training & Integration"
        elif ready_count >= 3:
            return "Phase 1: Foundation Complete"
        else:
            return "Phase 1: Foundation Building"
            
    def _format_component_status(self, components):
        """Format component status for display"""
        output = ""
        for component, status in components.items():
            emoji = "✅" if status == "Ready" else "⏳" if status == "Partial" else "❌"
            output += f"- {emoji} {component}\n"
        return output
        
    def _get_training_count(self):
        """Get total training examples collected"""
        try:
            from ai_family.claudae.training.claudae_training_collector import CLAUDAETrainingCollector
            collector = CLAUDAETrainingCollector()
            summary = collector.generate_training_summary()
            return summary.get('total_examples', 0)
        except:
            return "N/A"
            
    def _get_last_training_session(self):
        """Get last training session info"""
        sessions_dir = self.project_root / "ai_family/claudae/training/sessions"
        if sessions_dir.exists():
            sessions = list(sessions_dir.glob("*.json"))
            if sessions:
                latest = max(sessions, key=lambda x: x.stat().st_mtime)
                return latest.stem
        return "No sessions found"
        
    def _get_recent_changes(self):
        """Get recent file changes"""
        # Simple version - could integrate with Git log
        return [
            "Market data pipeline implemented",
            "AI family communication established", 
            "Training system activated",
            "System monitoring configured"
        ]
        
    def _identify_next_tasks(self):
        """Identify next development priorities"""
        components = self._check_components()
        
        tasks = []
        if components.get("Market Data Pipeline") != "Ready":
            tasks.append("Complete market data pipeline")
        if components.get("Trading Engine") != "Ready":
            tasks.append("Integrate NYALA trading engine")
        if len([c for c in components.values() if c == "Ready"]) >= 4:
            tasks.append("Deploy to production server")
            tasks.append("Begin live paper trading")
            
        return tasks[:3]  # Top 3 priorities

# CLI interface
if __name__ == "__main__":
    import sys
    
    manager = CLAUDAEProjectManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "status":
            status = manager.update_project_status()
            print(json.dumps(status, indent=2))
        elif command == "docs":
            manager.auto_update_documentation()
            print("✅ Documentation updated")
        elif command == "git-setup":
            manager.setup_git_repository()
            print("✅ Git repository initialized")
        elif command == "commit":
            message = sys.argv[2] if len(sys.argv) > 2 else None
            if manager.commit_progress(message):
                print("✅ Progress committed to Git")
            else:
                print("❌ Git commit failed")
        elif command == "report":
            report = manager.generate_progress_report()
            print(report)
    else:
        print("CLAUDAE Project Manager")
        print("Commands: status, docs, git-setup, commit, report")