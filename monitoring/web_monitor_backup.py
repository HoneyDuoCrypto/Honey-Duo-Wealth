#!/usr/bin/env python3
"""
Production-Ready System Monitor for HONEY DUO WEALTH
Scalable, optimized monitoring with data retention policies
"""

import streamlit as st
import psutil
import time
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import subprocess
import sys
import json
import sqlite3
from pathlib import Path
import threading
import queue

# Replace the page_link lines with:
with st.sidebar:
    st.markdown("### 📊 Navigation")
# Page config
st.set_page_config(
    page_title="HONEY DUO WEALTH Monitor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better design
st.markdown("""
<style>
    .main-header { 
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #0e1117;
        border: 1px solid #262730;
        border-radius: 8px;
        padding: 1rem;
    }
    .alert-box {
        background: #ff4b4b20;
        border-left: 4px solid #ff4b4b;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background: #00ff0020;
        border-left: 4px solid #00ff00;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class OptimizedMetricsTracker:
    def __init__(self):
        self.db_path = Path("monitoring/metrics.db")
        self.db_path.parent.mkdir(exist_ok=True)
        self.init_database()
        self.data_queue = queue.Queue()
        self.retention_hours = 168  # 1 week
        
    def init_database(self):
        """Initialize optimized database with indexes and retention"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                timestamp INTEGER PRIMARY KEY,
                cpu REAL,
                memory REAL,
                memory_gb REAL,
                disk REAL,
                gpu_util TEXT,
                training_status TEXT
            )
        ''')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON metrics(timestamp)')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS training_events (
                id INTEGER PRIMARY KEY,
                ai_name TEXT,
                event_type TEXT,
                timestamp INTEGER,
                cpu_peak REAL,
                memory_peak REAL,
                duration_sec INTEGER
            )
        ''')
        conn.commit()
        conn.close()
        
    def cleanup_old_data(self):
        """Remove data older than retention period"""
        cutoff = int((datetime.now() - timedelta(hours=self.retention_hours)).timestamp())
        conn = sqlite3.connect(self.db_path)
        conn.execute('DELETE FROM metrics WHERE timestamp < ?', (cutoff,))
        conn.execute('DELETE FROM training_events WHERE timestamp < ?', (cutoff,))
        conn.commit()
        conn.close()
        
    def log_metrics(self, metrics):
        """Efficiently log metrics"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            INSERT OR REPLACE INTO metrics VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            int(datetime.now().timestamp()),
            metrics['cpu'], metrics['memory'], metrics['memory_gb'],
            metrics['disk'], metrics['gpu'], metrics['training_status']
        ))
        conn.commit()
        conn.close()
        
    def get_recent_data(self, minutes=60):
        """Get recent data efficiently"""
        since = int((datetime.now() - timedelta(minutes=minutes)).timestamp())
        conn = sqlite3.connect(self.db_path)
        
        df = pd.read_sql_query('''
            SELECT timestamp, cpu, memory, memory_gb, training_status
            FROM metrics 
            WHERE timestamp > ? 
            ORDER BY timestamp DESC LIMIT 1000
        ''', conn, params=[since])
        
        conn.close()
        
        if not df.empty:
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
        return df

# Initialize tracker
@st.cache_resource
def get_tracker():
    return OptimizedMetricsTracker()

tracker = get_tracker()

# Efficient data fetching
@st.cache_data(ttl=10)  # Cache for 10 seconds
def get_system_metrics():
    """Get current system metrics"""
    return {
        'cpu': psutil.cpu_percent(interval=0.1),
        'memory': psutil.virtual_memory().percent,
        'memory_gb': psutil.virtual_memory().used / (1024**3),
        'disk': psutil.disk_usage('/').percent,
        'gpu': get_gpu_info(),
        'training_status': detect_training()
    }

@st.cache_data(ttl=30)
def get_gpu_info():
    """Get GPU information"""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5
        )
        return f"{result.stdout.strip()}%" if result.returncode == 0 else "N/A"
    except:
        return "N/A"

@st.cache_data(ttl=10)
def detect_training():
    """Detect active training processes"""
    try:
        for proc in psutil.process_iter(['name', 'cmdline']):
            cmdline = ' '.join(proc.info.get('cmdline', []))
            if any(word in cmdline.lower() for word in ['train', 'fine-tune', 'llm']):
                return f"Training: {proc.info['name']}"
    except:
        pass
    return "Idle"

@st.cache_data(ttl=60)
def get_training_stats():
    """Get training statistics with caching"""
    try:
        sys.path.append('.')
        from ai_family.llm_training_manager import LLMTrainingManager
        manager = LLMTrainingManager()
        return manager.get_model_status()
    except:
        return {"error": "Training manager unavailable"}

# Main Dashboard
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("🏠 HONEY DUO WEALTH - Production Monitor")
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar controls
with st.sidebar:
    st.header("⚙️ Controls")
    auto_refresh = st.toggle("Auto Refresh", True)
    refresh_rate = st.slider("Refresh (sec)", 1, 30, 5)
    show_charts = st.toggle("Show Charts", True)
    chart_timeframe = st.selectbox("Chart Range", ["1h", "6h", "24h"], index=0)

# Get current metrics
current_metrics = get_system_metrics()
tracker.log_metrics(current_metrics)

# Real-time metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    cpu_color = "🔴" if current_metrics['cpu'] > 80 else "🟡" if current_metrics['cpu'] > 60 else "🟢"
    st.metric("CPU Usage", f"{current_metrics['cpu']:.1f}%", 
              delta=f"{cpu_color}")

with col2:
    mem_color = "🔴" if current_metrics['memory'] > 85 else "🟡" if current_metrics['memory'] > 70 else "🟢"
    st.metric("Memory", f"{current_metrics['memory']:.1f}%", 
              delta=f"{current_metrics['memory_gb']:.1f}GB {mem_color}")

with col3:
    disk_color = "🔴" if current_metrics['disk'] > 90 else "🟡" if current_metrics['disk'] > 80 else "🟢"
    st.metric("Disk Usage", f"{current_metrics['disk']:.1f}%", 
              delta=f"{disk_color}")

with col4:
    st.metric("GPU", current_metrics['gpu'])

# Training status alert
if "Training" in current_metrics['training_status']:
    st.markdown(f"""
    <div class="alert-box">
        🔥 <strong>Active Training Detected:</strong> {current_metrics['training_status']}
    </div>
    """, unsafe_allow_html=True)

# Historical charts
if show_charts:
    st.subheader("📈 System Performance")
    
    timeframe_minutes = {"1h": 60, "6h": 360, "24h": 1440}[chart_timeframe]
    hist_data = tracker.get_recent_data(timeframe_minutes)
    
    if not hist_data.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=hist_data['datetime'], y=hist_data['cpu'], 
                                   name='CPU %', line_color='#ff6b6b'))
            fig.add_trace(go.Scatter(x=hist_data['datetime'], y=hist_data['memory'], 
                                   name='Memory %', line_color='#4ecdc4'))
            fig.update_layout(title="CPU & Memory Usage", height=300, 
                            template="plotly_dark", margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Training events overlay
            training_events = hist_data[hist_data['training_status'] != 'Idle']
            if not training_events.empty:
                fig = px.scatter(training_events, x='datetime', y='cpu', 
                               color='training_status', title="Training Activity",
                               template="plotly_dark")
                fig.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No training activity in timeframe")

# AI Family Status
st.subheader("🤖 AI Family Status")

# Check ollama status
try:
    subprocess.run(["ollama", "list"], capture_output=True, check=True, timeout=5)
    ollama_running = True
except:
    ollama_running = False

col1, col2, col3 = st.columns(3)

with col1:
    if ollama_running:
        st.markdown('<div class="success-box">✅ <strong>CLAUDAE</strong><br/>Mistral 7B - Online</div>', 
                   unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-box">❌ <strong>CLAUDAE</strong><br/>Offline</div>', 
                   unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">⏳ <strong>NYALA</strong><br/>Mixtral 8x7b - Ready</div>', 
               unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">⏳ <strong>DEON</strong><br/>Llama2 13B - Ready</div>', 
               unsafe_allow_html=True)

# Training Dashboard
st.subheader("🎓 Training Management")

training_stats = get_training_stats()
if "error" not in training_stats:
    for ai_name, stats in training_stats.items():
        with st.expander(f"{ai_name.upper()} - {stats.get('latest_version', 'No versions')}"):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Versions", stats.get("total_versions", 0))
            with col2:
                st.metric("Examples", stats.get("training_examples", 0))
            with col3:
                status = stats.get("production_status", "Unknown")
                color = {"Deployed": "🟢", "Training": "🟡", "Not Deployed": "⚪"}
                st.write(f"{color.get(status, '⚪')} {status}")
            with col4:
                if st.button(f"Manage {ai_name.upper()}", key=f"manage_{ai_name}"):
                    st.info(f"Training management for {ai_name} - Ready for implementation")

# Footer with cleanup
if st.button("🧹 Cleanup Old Data"):
    tracker.cleanup_old_data()
    st.success("Database cleaned successfully")

st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')} | "
          f"Data retention: {tracker.retention_hours}h")

# Auto refresh
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()