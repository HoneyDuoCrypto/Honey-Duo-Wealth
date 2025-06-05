#!/usr/bin/env python3
"""
HONEY DUO WEALTH - Simple Monitoring Dashboard
System health and training monitoring with historical data
"""

import streamlit as st
import psutil
import subprocess
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
from pathlib import Path
import time

st.set_page_config(
    page_title="HONEY DUO WEALTH Monitor",
    page_icon="🏠",
    layout="wide"
)

def get_system_metrics():
    return {
        'cpu': psutil.cpu_percent(interval=0.1),
        'memory': psutil.virtual_memory().percent,
        'memory_gb': psutil.virtual_memory().used / (1024**3),
        'disk': psutil.disk_usage('/').percent,
        'storage': get_storage_info(),
        'ollama': check_ollama()
    }

def get_storage_info():
    """Get detailed storage information"""
    storage = {}
    
    # Main partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            storage[partition.mountpoint] = {
                'total': usage.total / (1024**3),  # GB
                'used': usage.used / (1024**3),
                'free': usage.free / (1024**3),
                'percent': (usage.used / usage.total) * 100,
                'fstype': partition.fstype
            }
        except:
            continue
    
    return storage

def check_ollama():
    try:
        subprocess.run(["ollama", "list"], capture_output=True, check=True, timeout=3)
        return "🟢 Online"
    except:
        return "🔴 Offline"

def get_training_status():
    try:
        import sys
        sys.path.append('.')
        from ai_family.llm_training_manager import LLMTrainingManager
        manager = LLMTrainingManager()
        return manager.get_model_status()
    except:
        return {}

def log_metrics(metrics):
    """Log current metrics to database"""
    db_path = Path("monitoring/metrics.db")
    db_path.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    
    # Drop and recreate table with correct schema
    conn.execute('DROP TABLE IF EXISTS metrics')
    conn.execute('''
        CREATE TABLE metrics (
            timestamp INTEGER PRIMARY KEY,
            cpu REAL,
            memory REAL,
            memory_gb REAL,
            disk REAL
        )
    ''')
    
    conn.execute('''
        INSERT INTO metrics VALUES (?, ?, ?, ?, ?)
    ''', (
        int(datetime.now().timestamp()),
        metrics['cpu'], metrics['memory'], metrics['memory_gb'], metrics['disk']
    ))
    conn.commit()
    conn.close()

def get_historical_data(hours=24):
    """Get historical metrics from database"""
    db_path = Path("monitoring/metrics.db")
    if not db_path.exists():
        return pd.DataFrame()
        
    since = int((datetime.now() - timedelta(hours=hours)).timestamp())
    conn = sqlite3.connect(db_path)
    
    try:
        df = pd.read_sql_query('''
            SELECT timestamp, cpu, memory, memory_gb
            FROM metrics 
            WHERE timestamp > ? 
            ORDER BY timestamp DESC LIMIT 500
        ''', conn, params=[since])
        
        if not df.empty:
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
        return df
    except:
        return pd.DataFrame()
    finally:
        conn.close()

# Header
st.title("🏠 HONEY DUO WEALTH")
st.markdown("**System & Training Monitor**")

# Get and log current metrics
current_metrics = get_system_metrics()
log_metrics(current_metrics)

# System Health
col1, col2, col3, col4 = st.columns(4)

with col1:
    color = "🔴" if current_metrics['cpu'] > 80 else "🟡" if current_metrics['cpu'] > 60 else "🟢"
    st.metric("CPU", f"{current_metrics['cpu']:.0f}%", delta=color)

with col2:
    color = "🔴" if current_metrics['memory'] > 85 else "🟡" if current_metrics['memory'] > 70 else "🟢"
    st.metric("Memory", f"{current_metrics['memory']:.0f}%", 
              delta=f"{current_metrics['memory_gb']:.1f}GB {color}")

with col3:
    color = "🔴" if current_metrics['disk'] > 90 else "🟡" if current_metrics['disk'] > 80 else "🟢"
    st.metric("Disk", f"{current_metrics['disk']:.0f}%", delta=color)

with col4:
    st.metric("AI Models", current_metrics['ollama'])

# Storage Breakdown
st.markdown("---")
st.subheader("💾 Storage Allocation")

storage_info = current_metrics['storage']
cols = st.columns(len(storage_info))

for i, (mount, info) in enumerate(storage_info.items()):
    with cols[i]:
        color = "🔴" if info['percent'] > 90 else "🟡" if info['percent'] > 80 else "🟢"
        st.metric(
            f"{mount}", 
            f"{info['percent']:.0f}%",
            delta=f"{info['free']:.0f}GB free {color}"
        )
        st.caption(f"{info['total']:.0f}GB total ({info['fstype']})")

st.markdown("---")

# Historical Charts
st.subheader("📈 Historical Usage")

timeframe = st.selectbox("Timeframe", ["6h", "24h", "48h"], index=1)
hours = {"6h": 6, "24h": 24, "48h": 48}[timeframe]

hist_data = get_historical_data(hours)

if not hist_data.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist_data['datetime'], y=hist_data['cpu'], 
                               name='CPU %', line_color='#ff6b6b'))
        fig.add_trace(go.Scatter(x=hist_data['datetime'], y=hist_data['memory'], 
                               name='Memory %', line_color='#4ecdc4'))
        fig.update_layout(title="CPU & Memory %", height=300, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist_data['datetime'], y=hist_data['memory_gb'], 
                               name='Memory GB', line_color='#45b7d1'))
        fig.update_layout(title="Memory Usage (GB)", height=300, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("📊 Collecting historical data...")

st.markdown("---")

# Training Status
st.subheader("🎓 AI Training Status")

training_stats = get_training_status()

col1, col2, col3 = st.columns(3)

for i, ai in enumerate(['claudae', 'nyala', 'deon']):
    with [col1, col2, col3][i]:
        stats = training_stats.get(ai, {})
        status = stats.get('production_status', 'Not Ready')
        examples = stats.get('training_examples', 0)
        version = stats.get('latest_version', 'None')
        
        if status == "Deployed":
            st.success(f"✅ **{ai.upper()}**")
        elif status == "Training":
            st.warning(f"🟡 **{ai.upper()}**")
        else:
            st.info(f"⚪ **{ai.upper()}**")
            
        st.caption(f"v{version} | {examples} examples")

# Footer
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')} | Auto-refresh: 30s")

# Auto refresh
time.sleep(30)
st.rerun()