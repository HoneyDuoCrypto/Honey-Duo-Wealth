#!/usr/bin/env python3
"""
CLAUDAE Memory System - Phase 2: Document Migration
==================================================

Phase 2: Intelligent document migration with CLAUDAE
- Preserves all original documents
- CLAUDAE analyzes and organizes content
- Creates structured memory system
- Sets up automated processing

Author: Claude (Lead)
Project: HONEY DUO WEALTH - AI Family Guardian System
Status: Phase 2 - DOCUMENT MIGRATION
"""

import os
import json
import time
import hashlib
import asyncio
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import requests

# Configure logging
def setup_logging(log_dir: Path):
    """Setup comprehensive logging system"""
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "claudae_migration.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - CLAUDAE-MIGRATION - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

@dataclass
class DocumentAnalysis:
    """CLAUDAE's analysis of a document"""
    file_path: str
    content_type: str
    importance_score: float
    key_topics: List[str]
    relationships: List[str]
    summary: str
    claudae_confidence: float
    processing_time: float

@dataclass
class MigrationResult:
    """Result of migrating a single document"""
    original_path: str
    migrated_path: str
    analysis: DocumentAnalysis
    success: bool
    error_message: Optional[str] = None

class CLAUDAEInterface:
    """Enhanced CLAUDAE interface for document migration"""
    
    def __init__(self):
        self.model = "mistral:7b"
        self.base_url = "http://localhost:11434"
        self.timeout = 120
        
    async def analyze_document(self, file_path: str, content: str) -> DocumentAnalysis:
        """Have CLAUDAE analyze a document for migration"""
        start_time = time.time()
        
        # Create context-aware prompt for CLAUDAE
        prompt = f"""
You are CLAUDAE, the System Guardian of the HONEY DUO WEALTH project.
Analyze this document for intelligent organization in our family wealth protection system.

DOCUMENT: {file_path}
CONTENT:
{content[:2000]}  # First 2000 characters for analysis

ANALYSIS REQUIRED:
1. Content Type: (blueprint/session/status/config/documentation)
2. Importance Score: (0.0-1.0, where 1.0 is critical for family wealth protection)
3. Key Topics: (3-5 main topics this document covers)
4. Relationships: (which other documents or systems this relates to)
5. Summary: (2-3 sentences describing what this document contains)

CONTEXT: This is part of building an AI family (CLAUDAE/NYALA/DEON) to protect family wealth.
Focus on the family-first philosophy and wealth protection aspects.

Respond in this exact JSON format:
{{
    "content_type": "...",
    "importance_score": 0.0,
    "key_topics": ["topic1", "topic2", "topic3"],
    "relationships": ["related_file1", "related_system1"],
    "summary": "Brief summary here.",
    "confidence": 0.0
}}
"""
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2,  # Low temperature for consistent analysis
                        "top_k": 40,
                        "top_p": 0.9
                    }
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                claudae_response = result.get('response', '')
                processing_time = time.time() - start_time
                
                # Parse CLAUDAE's response
                analysis_data = self._parse_claudae_response(claudae_response)
                
                return DocumentAnalysis(
                    file_path=file_path,
                    content_type=analysis_data.get('content_type', 'unknown'),
                    importance_score=analysis_data.get('importance_score', 0.5),
                    key_topics=analysis_data.get('key_topics', []),
                    relationships=analysis_data.get('relationships', []),
                    summary=analysis_data.get('summary', 'No summary available'),
                    claudae_confidence=analysis_data.get('confidence', 0.5),
                    processing_time=processing_time
                )
            else:
                # Fallback analysis if CLAUDAE is unavailable
                return self._fallback_analysis(file_path, content, time.time() - start_time)
                
        except Exception as e:
            logging.error(f"CLAUDAE analysis failed for {file_path}: {e}")
            return self._fallback_analysis(file_path, content, time.time() - start_time)
    
    def _parse_claudae_response(self, response: str) -> Dict[str, Any]:
        """Parse CLAUDAE's JSON response"""
        try:
            # Try to extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # If no JSON found, create basic analysis from text
                return self._extract_analysis_from_text(response)
                
        except json.JSONDecodeError:
            return self._extract_analysis_from_text(response)
    
    def _extract_analysis_from_text(self, response: str) -> Dict[str, Any]:
        """Extract analysis from CLAUDAE's text response if JSON parsing fails"""
        # Basic text analysis as fallback
        analysis = {
            "content_type": "documentation",
            "importance_score": 0.7,
            "key_topics": [],
            "relationships": [],
            "summary": response[:200] + "..." if len(response) > 200 else response,
            "confidence": 0.6
        }
        
        # Extract topics from response text
        if "blueprint" in response.lower():
            analysis["content_type"] = "blueprint"
            analysis["importance_score"] = 0.9
        elif "session" in response.lower():
            analysis["content_type"] = "session"
        elif "status" in response.lower():
            analysis["content_type"] = "status"
        
        return analysis
    
    def _fallback_analysis(self, file_path: str, content: str, processing_time: float) -> DocumentAnalysis:
        """Fallback analysis when CLAUDAE is unavailable"""
        # Basic file-based analysis
        content_type = "documentation"
        importance_score = 0.5
        
        if "blueprint" in file_path.lower():
            content_type = "blueprint"
            importance_score = 0.9
        elif "session" in file_path.lower():
            content_type = "session"
            importance_score = 0.8
        elif "status" in file_path.lower():
            content_type = "status"
            importance_score = 0.7
        
        return DocumentAnalysis(
            file_path=file_path,
            content_type=content_type,
            importance_score=importance_score,
            key_topics=["family_wealth", "ai_system"],
            relationships=["ai_family"],
            summary=f"Document from {file_path} - analyzed without CLAUDAE",
            claudae_confidence=0.3,
            processing_time=processing_time
        )

class CLAUDAEMigrationSystem:
    """Phase 2: Document migration with CLAUDAE intelligence"""
    
    def __init__(self, project_root: str = "/home/honey-duo-wealth/honey_duo_wealth"):
        self.project_root = Path(project_root)
        self.foundation_dir = self.project_root / "claudae_foundation"
        self.migration_dir = self.foundation_dir / "migration"
        self.memory_dir = self.project_root / "project_memory"
        
        # Create migration directory
        self.migration_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.logger = setup_logging(self.foundation_dir / "logs")
        
        # Initialize CLAUDAE
        self.claudae = CLAUDAEInterface()
        
        # Migration results
        self.migration_results: List[MigrationResult] = []
        
        self.logger.info("🎯 CLAUDAE Migration System initializing...")
        self.logger.info(f"Migration directory: {self.migration_dir}")
    
    async def run_document_migration(self) -> Dict[str, Any]:
        """Run complete document migration with CLAUDAE analysis"""
        self.logger.info("🔄 Starting CLAUDAE-powered document migration...")
        
        migration_report = {
            "start_time": datetime.now().isoformat(),
            "phase": "document_migration",
            "documents_found": 0,
            "documents_migrated": 0,
            "claudae_analyses": 0,
            "migration_results": [],
            "success": False
        }
        
        try:
            # Step 1: Discover all documents
            documents = self._discover_documents()
            migration_report["documents_found"] = len(documents)
            
            self.logger.info(f"📄 Found {len(documents)} documents to migrate")
            
            # Step 2: Create additional backup for Phase 2
            await self._create_phase2_backup()
            
            # Step 3: Migrate each document with CLAUDAE
            for doc_path in documents:
                try:
                    self.logger.info(f"🔍 Processing: {doc_path}")
                    
                    # Read document content
                    content = doc_path.read_text(encoding='utf-8')
                    
                    # Have CLAUDAE analyze the document
                    analysis = await self.claudae.analyze_document(str(doc_path), content)
                    migration_report["claudae_analyses"] += 1
                    
                    # Migrate the document
                    migration_result = await self._migrate_document(doc_path, content, analysis)
                    self.migration_results.append(migration_result)
                    migration_report["migration_results"].append(asdict(migration_result))
                    
                    if migration_result.success:
                        migration_report["documents_migrated"] += 1
                        self.logger.info(f"✅ Migrated: {doc_path.name}")
                    else:
                        self.logger.error(f"❌ Failed: {doc_path.name} - {migration_result.error_message}")
                    
                except Exception as e:
                    self.logger.error(f"❌ Error processing {doc_path}: {e}")
                    
                    # Create error result
                    error_result = MigrationResult(
                        original_path=str(doc_path),
                        migrated_path="",
                        analysis=DocumentAnalysis(
                            file_path=str(doc_path),
                            content_type="error",
                            importance_score=0.0,
                            key_topics=[],
                            relationships=[],
                            summary=f"Error processing: {str(e)}",
                            claudae_confidence=0.0,
                            processing_time=0.0
                        ),
                        success=False,
                        error_message=str(e)
                    )
                    self.migration_results.append(error_result)
                    migration_report["migration_results"].append(asdict(error_result))
            
            # Step 4: Create migration summary
            await self._create_migration_summary()
            
            migration_report["end_time"] = datetime.now().isoformat()
            migration_report["success"] = migration_report["documents_migrated"] > 0
            migration_report["success_rate"] = migration_report["documents_migrated"] / max(1, migration_report["documents_found"])
            
            # Save migration report
            report_file = self.migration_dir / "migration_report.json"
            with open(report_file, 'w') as f:
                json.dump(migration_report, f, indent=2)
            
            self.logger.info(f"🎯 Migration complete: {migration_report['documents_migrated']}/{migration_report['documents_found']} documents migrated")
            return migration_report
            
        except Exception as e:
            migration_report["error"] = str(e)
            migration_report["success"] = False
            self.logger.error(f"❌ Migration failed: {e}")
            return migration_report
    
    def _discover_documents(self) -> List[Path]:
        """Discover all documents for migration"""
        documents = []
        doc_patterns = ["*.md", "*.json", "*.yaml", "*.yml", "*.txt"]
        
        for pattern in doc_patterns:
            # Search in project_memory and main project directory
            for doc_path in self.project_root.rglob(pattern):
                # Skip files in foundation directory and venv
                if ("claudae_foundation" not in str(doc_path) and 
                    "venv" not in str(doc_path) and
                    ".git" not in str(doc_path) and
                    doc_path.is_file()):
                    documents.append(doc_path)
        
        return documents
    
    async def _create_phase2_backup(self):
        """Create additional backup before Phase 2 migration"""
        backup_dir = self.migration_dir / "phase2_backup"
        backup_dir.mkdir(exist_ok=True)
        
        # Copy all discovered documents
        for doc_path in self._discover_documents():
            try:
                # Create backup path preserving directory structure
                rel_path = doc_path.relative_to(self.project_root)
                backup_path = backup_dir / rel_path
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                
                shutil.copy2(doc_path, backup_path)
            except Exception as e:
                self.logger.warning(f"Failed to backup {doc_path}: {e}")
        
        self.logger.info(f"✅ Phase 2 backup created at {backup_dir}")
    
    async def _migrate_document(self, doc_path: Path, content: str, analysis: DocumentAnalysis) -> MigrationResult:
        """Migrate a single document with CLAUDAE's analysis"""
        try:
            # Create organized structure in migration directory
            category_dir = self.migration_dir / "organized_docs" / analysis.content_type
            category_dir.mkdir(parents=True, exist_ok=True)
            
            # Create migrated file with enhanced metadata
            migrated_path = category_dir / f"{doc_path.stem}_migrated{doc_path.suffix}"
            
            # Enhanced document with CLAUDAE analysis
            enhanced_content = self._create_enhanced_document(doc_path, content, analysis)
            
            # Write enhanced document
            migrated_path.write_text(enhanced_content, encoding='utf-8')
            
            return MigrationResult(
                original_path=str(doc_path),
                migrated_path=str(migrated_path),
                analysis=analysis,
                success=True
            )
            
        except Exception as e:
            return MigrationResult(
                original_path=str(doc_path),
                migrated_path="",
                analysis=analysis,
                success=False,
                error_message=str(e)
            )
    
    def _create_enhanced_document(self, doc_path: Path, content: str, analysis: DocumentAnalysis) -> str:
        """Create enhanced document with CLAUDAE analysis metadata"""
        
        # Create metadata header
        metadata = f"""<!-- CLAUDAE Analysis Metadata
File: {doc_path}
Content Type: {analysis.content_type}
Importance Score: {analysis.importance_score}
Key Topics: {', '.join(analysis.key_topics)}
Relationships: {', '.join(analysis.relationships)}
Summary: {analysis.summary}
CLAUDAE Confidence: {analysis.claudae_confidence}
Processing Time: {analysis.processing_time:.2f}s
Migration Date: {datetime.now().isoformat()}
-->

"""
        
        # Preserve original content exactly
        enhanced_content = metadata + content
        
        return enhanced_content
    
    async def _create_migration_summary(self):
        """Create comprehensive migration summary"""
        summary = {
            "migration_date": datetime.now().isoformat(),
            "total_documents": len(self.migration_results),
            "successful_migrations": sum(1 for r in self.migration_results if r.success),
            "failed_migrations": sum(1 for r in self.migration_results if not r.success),
            "content_type_breakdown": {},
            "importance_distribution": {},
            "claudae_performance": {}
        }
        
        # Analyze results
        for result in self.migration_results:
            if result.success:
                # Content type breakdown
                content_type = result.analysis.content_type
                summary["content_type_breakdown"][content_type] = summary["content_type_breakdown"].get(content_type, 0) + 1
                
                # Importance distribution
                importance = result.analysis.importance_score
                importance_range = f"{int(importance * 10)}/10"
                summary["importance_distribution"][importance_range] = summary["importance_distribution"].get(importance_range, 0) + 1
        
        # CLAUDAE performance
        if self.migration_results:
            avg_confidence = sum(r.analysis.claudae_confidence for r in self.migration_results) / len(self.migration_results)
            avg_processing_time = sum(r.analysis.processing_time for r in self.migration_results) / len(self.migration_results)
            
            summary["claudae_performance"] = {
                "average_confidence": round(avg_confidence, 3),
                "average_processing_time": round(avg_processing_time, 3),
                "total_processing_time": round(sum(r.analysis.processing_time for r in self.migration_results), 2)
            }
        
        # Save summary
        summary_file = self.migration_dir / "migration_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        self.logger.info("✅ Migration summary created")

# CLI Interface for Phase 2
async def main():
    """Main execution for Phase 2 migration"""
    print("🔄 CLAUDAE Memory System - Phase 2: Document Migration")
    print("=" * 60)
    print("Phase 2: Intelligent document migration with CLAUDAE")
    print("- Preserves all original documents")
    print("- CLAUDAE analyzes and organizes content")
    print("- Creates structured memory system")
    print("- Sets up automated processing")
    print()
    
    # Initialize migration system
    migration = CLAUDAEMigrationSystem()
    
    # Run migration
    print("🔄 Starting CLAUDAE-powered document migration...")
    print("This will take a few minutes as CLAUDAE analyzes each document...")
    print()
    
    migration_results = await migration.run_document_migration()
    
    if migration_results["success"]:
        print()
        print("🎉 PHASE 2 COMPLETE - DOCUMENT MIGRATION SUCCESSFUL")
        print("=" * 60)
        print(f"✅ Documents found: {migration_results['documents_found']}")
        print(f"✅ Documents migrated: {migration_results['documents_migrated']}")
        print(f"✅ CLAUDAE analyses: {migration_results['claudae_analyses']}")
        print(f"✅ Success rate: {migration_results.get('success_rate', 0):.1%}")
        print()
        print("📁 Migration results available at:")
        print("   - claudae_foundation/migration/migration_report.json")
        print("   - claudae_foundation/migration/migration_summary.json")
        print("   - claudae_foundation/migration/organized_docs/")
        print()
        print("✅ Ready for Phase 3: Automated Processing")
        
    else:
        print()
        print("❌ PHASE 2 FAILED - MIGRATION INCOMPLETE")
        print("Check logs for details:")
        print("   - claudae_foundation/logs/claudae_migration.log")
        print("   - claudae_foundation/migration/migration_report.json")
    
    return migration_results["success"]

if __name__ == "__main__":
    import sys
    success = asyncio.run(main())
    sys.exit(0 if success else 1)