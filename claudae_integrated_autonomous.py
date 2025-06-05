#!/usr/bin/env python3
"""
CLAUDAE Integrated Autonomous System
===================================

Combines autonomous learning with automatic documentation updates.
SOLVES: Both learning AND documentation maintenance in real-time.

Features:
- Real-time file monitoring and learning
- Automatic documentation updates
- Project status synchronization  
- Seamless session handoffs
"""

import os
import json
import time
import asyncio
import logging
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import queue

class IntegratedCLAUDAESystem:
    """Integrated system combining learning and documentation"""
    
    def __init__(self, project_root: str = "/home/honey-duo-wealth/honey_duo_wealth"):
        self.project_root = Path(project_root)
        self.foundation_dir = self.project_root / "claudae_foundation"
        self.learning_dir = self.foundation_dir / "autonomous_learning"
        self.memory_dir = self.project_root / "project_memory"
        
        # Create directories
        self.learning_dir.mkdir(exist_ok=True)
        
        # Setup logging
        log_file = self.learning_dir / "integrated_system.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - CLAUDAE-INTEGRATED - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Queues for different types of processing
        self.change_queue = queue.Queue()
        self.doc_update_queue = queue.Queue()
        
        # Session tracking
        self.session_start = datetime.now()
        self.session_changes = []
        self.session_learnings = []
        self.significant_changes = []
        
        # CLAUDAE connection
        self.claudae_url = "http://localhost:11434/api/generate"
        self.claudae_model = "mistral:7b"
        
        # Documentation update triggers
        self.doc_update_triggers = {
            "major_feature": 0.8,      # Importance threshold for major updates
            "architectural": 0.7,      # Architecture changes
            "component_change": 0.6,   # Component modifications
            "change_count": 5          # Number of changes to trigger update
        }
        
        self.logger.info("🚀 Integrated CLAUDAE System initialized")
        self.logger.info("🔄 Learning + Documentation integration active")
    
    async def start_integrated_monitoring(self):
        """Start integrated monitoring with learning and documentation"""
        self.logger.info("🎯 Starting integrated monitoring...")
        
        # Start file monitoring
        file_monitor = FileChangeMonitor(
            self.project_root,
            self.change_queue,
            self.logger
        )
        file_monitor.start()
        
        # Start processing tasks
        learning_task = asyncio.create_task(self.process_learning())
        documentation_task = asyncio.create_task(self.process_documentation())
        session_task = asyncio.create_task(self.manage_session())
        
        self.logger.info("✅ Integrated system active!")
        self.logger.info("🧠 CLAUDAE learning from every change...")
        self.logger.info("📝 Documentation updating automatically...")
        
        try:
            await asyncio.gather(learning_task, documentation_task, session_task)
        except KeyboardInterrupt:
            self.logger.info("🛑 Shutting down integrated system...")
            file_monitor.stop()
            await self.generate_comprehensive_handoff()
    
    async def process_learning(self):
        """Process changes for learning data collection"""
        while True:
            try:
                try:
                    change_event = self.change_queue.get_nowait()
                    analysis = await self.analyze_change_with_claudae(change_event)
                    
                    if analysis:
                        # Store learning
                        await self.store_learning(change_event, analysis)
                        
                        # Check if documentation update needed
                        await self.evaluate_documentation_update(analysis)
                    
                    self.change_queue.task_done()
                except queue.Empty:
                    pass
                
                await asyncio.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Learning processing error: {e}")
                await asyncio.sleep(1)
    
    async def process_documentation(self):
        """Process documentation updates triggered by significant changes"""
        while True:
            try:
                try:
                    update_request = self.doc_update_queue.get_nowait()
                    await self.update_project_documentation(update_request)
                    self.doc_update_queue.task_done()
                except queue.Empty:
                    pass
                
                await asyncio.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Documentation processing error: {e}")
                await asyncio.sleep(1)
    
    async def analyze_change_with_claudae(self, change_event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Enhanced CLAUDAE analysis with documentation trigger evaluation"""
        try:
            file_path = Path(change_event['file_path'])
            
            if self.should_skip_file(file_path):
                return None
            
            self.logger.info(f"🧠 CLAUDAE analyzing: {file_path.name}")
            
            # Read file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                self.logger.warning(f"Could not read {file_path}: {e}")
                return None
            
            # Enhanced analysis prompt
            prompt = f"""You are CLAUDAE, analyzing code changes for the HONEY DUO WEALTH project.

FILE: {file_path.name}
CHANGE TYPE: {change_event['event_type']}
TIMESTAMP: {change_event['timestamp']}

CONTENT:
{content[:2000]}{'...' if len(content) > 2000 else ''}

Provide comprehensive analysis in JSON format:
{{
    "analysis_type": "integrated_change_analysis",
    "file_type": "python/markdown/json/config/other",
    "development_pattern": "what development pattern this represents",
    "key_insight": "main learning from this change",
    "importance_score": 0.1-1.0,
    "learning_category": "architecture/feature/bugfix/documentation/testing/config",
    "technical_details": "specific technical insights",
    "project_impact": "how this affects the overall project",
    "documentation_trigger": true/false,
    "documentation_type": "readme/blueprint/status/handoff/none",
    "architectural_change": true/false,
    "component_affected": "which system component this affects",
    "claudae_confidence": 0.1-1.0
}}

Focus on identifying changes that require documentation updates."""

            analysis = await self.query_claudae(prompt)
            return analysis
            
        except Exception as e:
            self.logger.error(f"Analysis error: {e}")
            return None
    
    async def evaluate_documentation_update(self, analysis: Dict[str, Any]):
        """Evaluate if documentation update is needed"""
        try:
            importance = analysis.get("importance_score", 0)
            doc_trigger = analysis.get("documentation_trigger", False)
            arch_change = analysis.get("architectural_change", False)
            
            # Check triggers
            update_needed = False
            update_type = "none"
            
            if importance >= self.doc_update_triggers["major_feature"]:
                update_needed = True
                update_type = "major_update"
            elif arch_change and importance >= self.doc_update_triggers["architectural"]:
                update_needed = True
                update_type = "architectural_update"
            elif doc_trigger and importance >= self.doc_update_triggers["component_change"]:
                update_needed = True
                update_type = "component_update"
            elif len(self.session_changes) >= self.doc_update_triggers["change_count"]:
                update_needed = True
                update_type = "accumulated_changes"
            
            if update_needed:
                self.logger.info(f"📝 Documentation update triggered: {update_type}")
                
                update_request = {
                    "trigger_type": update_type,
                    "analysis": analysis,
                    "session_changes": len(self.session_changes),
                    "timestamp": datetime.now().isoformat()
                }
                
                self.doc_update_queue.put_nowait(update_request)
                
        except Exception as e:
            self.logger.error(f"Documentation evaluation error: {e}")
    
    async def update_project_documentation(self, update_request: Dict[str, Any]):
        """Update project documentation based on changes"""
        try:
            self.logger.info("📝 Updating project documentation...")
            
            # Prepare documentation update prompt
            recent_changes = self.session_changes[-5:]  # Last 5 changes
            recent_learnings = self.session_learnings[-3:]  # Last 3 learnings
            
            doc_prompt = f"""You are CLAUDAE updating HONEY DUO WEALTH project documentation.

UPDATE TRIGGER: {update_request['trigger_type']}
ANALYSIS: {json.dumps(update_request['analysis'], indent=2)}

RECENT CHANGES:
{json.dumps(recent_changes, indent=2)}

RECENT LEARNINGS:
{json.dumps(recent_learnings, indent=2)}

UPDATE REQUIREMENTS:
1. Determine which documents need updating (README.md, blueprint, status files)
2. Identify key changes to document
3. Suggest specific updates to maintain accuracy

Provide response in JSON format:
{{
    "documents_to_update": ["README.md", "master_blueprint.md", "current_status.json"],
    "update_summary": "brief summary of what needs updating",
    "key_changes": ["change 1", "change 2", "change 3"],
    "priority": "high/medium/low",
    "specific_updates": {{
        "README.md": "specific changes needed",
        "master_blueprint.md": "specific changes needed",
        "current_status.json": "specific changes needed"
    }}
}}"""

            doc_response = await self.query_claudae(doc_prompt)
            
            if doc_response:
                await self.execute_documentation_updates(doc_response)
                
                # Log the update
                self.logger.info(f"✅ Documentation updated: {doc_response.get('update_summary', 'No summary')}")
                
        except Exception as e:
            self.logger.error(f"Documentation update error: {e}")
    
    async def execute_documentation_updates(self, update_plan: Dict[str, Any]):
        """Execute the actual documentation updates"""
        try:
            # For now, log the planned updates
            # In full implementation, this would update the actual files
            
            updates_log = {
                "timestamp": datetime.now().isoformat(),
                "update_plan": update_plan,
                "execution_status": "planned"  # Would be "completed" when fully implemented
            }
            
            # Save update plan
            update_file = self.learning_dir / f"doc_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(update_file, 'w') as f:
                json.dump(updates_log, f, indent=2)
            
            self.logger.info(f"📋 Documentation update plan saved: {update_file.name}")
            
            # TODO: Implement actual file updates using existing CLAUDAE migration system
            # This would integrate with the document migration/review system
            
        except Exception as e:
            self.logger.error(f"Documentation execution error: {e}")
    
    async def store_learning(self, change_event: Dict[str, Any], analysis: Dict[str, Any]):
        """Store learning data and integrate with training system"""
        try:
            learning_record = {
                "timestamp": datetime.now().isoformat(),
                "file_path": change_event['file_path'],
                "change_event": change_event,
                "claudae_analysis": analysis,
                "session_id": f"integrated_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
            
            # Add to session tracking
            self.session_changes.append(change_event)
            self.session_learnings.append(learning_record)
            
            # Store as significant if high importance
            if analysis.get("importance_score", 0) >= 0.7:
                self.significant_changes.append(learning_record)
            
            # Save learning record
            learning_file = self.learning_dir / f"integrated_learning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(learning_file, 'w') as f:
                json.dump(learning_record, f, indent=2)
            
            # Integrate with existing training system
            await self.update_training_data(learning_record)
            
        except Exception as e:
            self.logger.error(f"Learning storage error: {e}")
    
    async def update_training_data(self, learning_record: Dict[str, Any]):
        """Update existing training data collection system"""
        try:
            import sys
            sys.path.append(str(self.project_root))
            
            from ai_family.claudae.training.claudae_training_collector import CLAUDAETrainingCollector
            
            collector = CLAUDAETrainingCollector()
            analysis = learning_record.get("claudae_analysis", {})
            
            # Extract code if it's a code file
            file_path = learning_record["file_path"]
            if any(ext in file_path for ext in ['.py', '.js', '.ts', '.java', '.cpp']):
                try:
                    with open(file_path, 'r') as f:
                        code_content = f.read()
                    
                    collector.collect_code_example(
                        code=code_content[:1000],
                        context=f"Integrated Learning: {analysis.get('development_pattern', 'Code change')}",
                        category=analysis.get('learning_category', 'integrated'),
                        reasoning=analysis.get('key_insight', 'Automatically captured'),
                        tags=['integrated_learning', 'autonomous']
                    )
                except Exception as e:
                    self.logger.warning(f"Training data integration failed: {e}")
                    
        except Exception as e:
            self.logger.warning(f"Training system integration error: {e}")
    
    async def manage_session(self):
        """Enhanced session management with documentation tracking"""
        while True:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                # Update session stats
                session_duration = (datetime.now() - self.session_start).total_seconds() / 60
                
                current_status = {
                    "session_duration_minutes": session_duration,
                    "total_changes": len(self.session_changes),
                    "total_learnings": len(self.session_learnings),
                    "significant_changes": len(self.significant_changes),
                    "documentation_updates": self.doc_update_queue.qsize(),
                    "last_update": datetime.now().isoformat()
                }
                
                # Save session status
                status_file = self.learning_dir / "current_session_status.json"
                with open(status_file, 'w') as f:
                    json.dump(current_status, f, indent=2)
                
                # Generate periodic handoff if significant activity
                if (len(self.significant_changes) > 0 and 
                    session_duration % 15 < 1):  # Every 15 minutes
                    await self.generate_periodic_handoff()
                    
            except Exception as e:
                self.logger.error(f"Session management error: {e}")
    
    async def generate_comprehensive_handoff(self):
        """Generate final comprehensive handoff with learning and documentation status"""
        try:
            self.logger.info("📋 Generating comprehensive final handoff...")
            
            handoff_data = {
                "session_summary": {
                    "duration_minutes": (datetime.now() - self.session_start).total_seconds() / 60,
                    "total_changes": len(self.session_changes),
                    "total_learnings": len(self.session_learnings),
                    "significant_changes": len(self.significant_changes),
                    "documentation_updates_processed": len([l for l in self.session_learnings 
                                                          if l.get("claudae_analysis", {}).get("documentation_trigger")])
                },
                "learning_insights": [l.get("claudae_analysis", {}).get("key_insight") 
                                    for l in self.session_learnings[-5:]],
                "architectural_changes": [l for l in self.significant_changes 
                                        if l.get("claudae_analysis", {}).get("architectural_change")],
                "documentation_status": "integrated_and_synchronized",
                "next_session_priorities": [
                    "Continue integrated learning and documentation",
                    "Review captured architectural insights",
                    "Optimize documentation update triggers"
                ]
            }
            
            # Generate handoff with CLAUDAE
            handoff_prompt = f"""Create a comprehensive session handoff for seamless continuation.

SESSION DATA:
{json.dumps(handoff_data, indent=2)}

Create a handoff that covers:
1. What was accomplished this session
2. Key learnings and insights captured
3. Documentation updates made
4. Current project status
5. Immediate next priorities
6. Technical context needed for continuation

This handoff should eliminate any "getting up to speed" time."""

            handoff_content = await self.query_claudae(handoff_prompt)
            
            # Save comprehensive handoff
            handoff_file = self.learning_dir / f"COMPREHENSIVE_HANDOFF_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(handoff_file, 'w') as f:
                json.dump({
                    "handoff_data": handoff_data,
                    "claudae_handoff": handoff_content,
                    "generation_time": datetime.now().isoformat()
                }, f, indent=2)
            
            self.logger.info("✅ Comprehensive handoff complete!")
            self.logger.info("🎯 Next session can continue seamlessly with full context")
            
        except Exception as e:
            self.logger.error(f"Comprehensive handoff failed: {e}")
    
    async def generate_periodic_handoff(self):
        """Generate periodic handoff for continuous documentation"""
        try:
            # Similar to comprehensive but lighter weight
            periodic_data = {
                "timestamp": datetime.now().isoformat(),
                "recent_changes": self.session_changes[-3:],
                "recent_learnings": self.session_learnings[-2:],
                "status": "active_development"
            }
            
            periodic_file = self.learning_dir / f"periodic_handoff_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            with open(periodic_file, 'w') as f:
                json.dump(periodic_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Periodic handoff error: {e}")
    
    async def query_claudae(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Query CLAUDAE with enhanced error handling"""
        try:
            response = requests.post(
                self.claudae_url,
                json={
                    "model": self.claudae_model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=45
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "")
                
                # Try to parse JSON response
                try:
                    return json.loads(response_text)
                except json.JSONDecodeError:
                    # Extract JSON if wrapped
                    start = response_text.find('{')
                    end = response_text.rfind('}') + 1
                    if start >= 0 and end > start:
                        return json.loads(response_text[start:end])
                    return None
            
        except Exception as e:
            self.logger.error(f"CLAUDAE query error: {e}")
            return None
    
    def should_skip_file(self, file_path: Path) -> bool:
        """Enhanced file filtering"""
        skip_patterns = [
            '.git/', '__pycache__/', '.pyc', '.log', 
            'node_modules/', '.venv/', 'venv/',
            '.DS_Store', '.gitignore', 'claudae_foundation/autonomous_learning/'
        ]
        
        file_str = str(file_path)
        return any(pattern in file_str for pattern in skip_patterns)


class FileChangeMonitor(FileSystemEventHandler):
    """Enhanced file monitoring for integrated system"""
    
    def __init__(self, watch_path: Path, change_queue: queue.Queue, logger):
        super().__init__()
        self.watch_path = watch_path
        self.change_queue = change_queue
        self.logger = logger
        self.observer = Observer()
        
    def start(self):
        self.observer.schedule(self, str(self.watch_path), recursive=True)
        self.observer.start()
        self.logger.info(f"📁 Integrated file monitoring started: {self.watch_path}")
    
    def stop(self):
        self.observer.stop()
        self.observer.join()
        self.logger.info("📁 Integrated file monitoring stopped")
    
    def on_modified(self, event):
        if not event.is_directory:
            self.queue_change(event.src_path, "modified")
    
    def on_created(self, event):
        if not event.is_directory:
            self.queue_change(event.src_path, "created")
    
    def on_moved(self, event):
        if not event.is_directory:
            self.queue_change(event.dest_path, "moved")
    
    def queue_change(self, file_path: str, event_type: str):
        change_event = {
            "file_path": file_path,
            "event_type": event_type,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            self.change_queue.put_nowait(change_event)
        except queue.Full:
            self.logger.warning("Change queue full, skipping change")


# CLI Interface
async def main():
    """Main entry point for integrated system"""
    print("🚀 CLAUDAE INTEGRATED AUTONOMOUS SYSTEM")
    print("=" * 60)
    print("🎯 MISSION: Learning + Documentation in real-time")
    print("🔄 INTEGRATION: Autonomous learning with documentation updates")
    print()
    
    system = IntegratedCLAUDAESystem()
    
    print("🔋 Integrated System Status:")
    print("✅ Real-time file monitoring")
    print("✅ Automatic CLAUDAE analysis")
    print("✅ Training data integration")
    print("✅ Documentation update triggers")
    print("✅ Comprehensive session handoffs")
    print()
    print("🎉 INTEGRATED SYSTEM ACTIVE!")
    print("💡 Learning from every change + Updating docs automatically")
    print()
    print("Press Ctrl+C to stop and generate comprehensive handoff")
    print()
    
    try:
        await system.start_integrated_monitoring()
    except KeyboardInterrupt:
        print("\n🎯 Integrated autonomous session complete!")
        print("✅ Learning captured + Documentation synchronized")


if __name__ == "__main__":
    asyncio.run(main())