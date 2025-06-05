#!/usr/bin/env python3
"""
HONEY DUO WEALTH - System Monitor Dashboard
Real-time monitoring of AI family and system resources
"""

import psutil
import subprocess
import time
import json
from datetime import datetime

class SystemMonitor:
    def __init__(self):
        self.ai_models = {
            "CLAUDAE": "mistral:7b",
            "NYALA": "mixtral:8x7b", 
            "DEON": "llama2:13b"
        }
    
    def get_system_stats(self):
        """Get current system resource usage"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory": {
                "total": f"{psutil.virtual_memory().total / (1024**3):.1f}GB",
                "used": f"{psutil.virtual_memory().used / (1024**3):.1f}GB",
                "percent": psutil.virtual_memory().percent
            },
            "disk": {
                "total": f"{psutil.disk_usage('/').total / (1024**3):.1f}GB",
                "used": f"{psutil.disk_usage('/').used / (1024**3):.1f}GB",
                "percent": psutil.disk_usage('/').percent
            }
        }
    
    def check_storage_mount(self):
        """Check if 8TB storage is mounted"""
        try:
            storage = psutil.disk_usage('/mnt/honey_duo_storage')
            return {
                "mounted": True,
                "total": f"{storage.total / (1024**4):.1f}TB",
                "used": f"{storage.used / (1024**4):.1f}TB",
                "free": f"{storage.free / (1024**4):.1f}TB"
            }
        except:
            return {"mounted": False}
    
    def check_ai_models(self):
        """Check Ollama model status"""
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            models_output = result.stdout.lower()
            
            status = {}
            for name, model in self.ai_models.items():
                status[name] = {
                    "model": model,
                    "available": model.lower() in models_output,
                    "status": "Ready" if model.lower() in models_output else "Loading"
                }
            return status
        except:
            return {"error": "Cannot check Ollama status"}
    
    def get_gpu_stats(self):
        """Get GPU usage if available"""
        try:
            result = subprocess.run([
                "nvidia-smi", "--query-gpu=name,memory.used,memory.total,utilization.gpu",
                "--format=csv,noheader,nounits"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                gpu_data = result.stdout.strip().split(', ')
                return {
                    "name": gpu_data[0],
                    "memory_used": f"{gpu_data[1]}MB",
                    "memory_total": f"{gpu_data[2]}MB", 
                    "utilization": f"{gpu_data[3]}%"
                }
        except:
            pass
        return {"status": "Not available"}
    
    def display_dashboard(self):
        """Display real-time dashboard"""
        print("\033[2J\033[H")  # Clear screen
        print("🏠 HONEY DUO WEALTH - System Monitor")
        print("=" * 50)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # System Resources
        stats = self.get_system_stats()
        print("💻 System Resources:")
        print(f"   CPU: {stats['cpu_percent']:.1f}%")
        print(f"   RAM: {stats['memory']['used']}/{stats['memory']['total']} ({stats['memory']['percent']:.1f}%)")
        print(f"   Disk: {stats['disk']['used']}/{stats['disk']['total']} ({stats['disk']['percent']:.1f}%)")
        
        # GPU Status
        gpu = self.get_gpu_stats()
        print("\n🎮 GPU Status:")
        if "name" in gpu:
            print(f"   {gpu['name']}")
            print(f"   Memory: {gpu['memory_used']}/{gpu['memory_total']}")
            print(f"   Usage: {gpu['utilization']}")
        else:
            print(f"   {gpu['status']}")
        
        # Storage
        storage = self.check_storage_mount()
        print("\n💾 8TB Storage:")
        if storage["mounted"]:
            print(f"   Total: {storage['total']}")
            print(f"   Used: {storage['used']}")
            print(f"   Free: {storage['free']}")
        else:
            print("   ❌ Not mounted")
        
        # AI Family Status
        ai_status = self.check_ai_models()
        print("\n🤖 AI Family Status:")
        for name, info in ai_status.items():
            if name != "error":
                status_icon = "✅" if info["available"] else "⏳"
                print(f"   {status_icon} {name}: {info['status']} ({info['model']})")
        
        print(f"\n📊 Next update in 5 seconds... (Ctrl+C to exit)")
    
    def run_continuous(self):
        """Run continuous monitoring"""
        try:
            while True:
                self.display_dashboard()
                time.sleep(5)
        except KeyboardInterrupt:
            print("\n\n👋 Monitor stopped. AI family continues running.")

if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.run_continuous()