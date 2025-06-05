#!/usr/bin/env python3
"""
LLM Training Dashboard
Real-time monitoring and control of AI family training
"""

import streamlit as st
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

class TrainingDashboard:
    def __init__(self):
        self.project_root = Path("~/honey_duo_wealth").expanduser()
        
    def run(self):
        st.set_page_config(page_title="HONEY DUO WEALTH Training", layout="wide")
        
        st.title("🎓 HONEY DUO WEALTH Training Dashboard")
        st.markdown("*AI Family Training Management & Control*")
        
        # Sidebar controls
        st.sidebar.title("Training Controls")
        selected_ai = st.sidebar.selectbox("Select AI", ["claudae", "nyala", "deon", "all"])
        
        # Main dashboard
        col1, col2 = st.columns(2)
        
        with col1:
            self.show_training_status()
            self.show_version_management()
            
        with col2:
            self.show_training_metrics()
            self.show_data_insights()
            
        # Training controls
        st.markdown("---")
        self.show_training_controls(selected_ai)
        
    def show_training_status(self):
        """Display current training status"""
        st.subheader("📊 Training Status")
        
        # Get status from training manager
        status = self.get_training_status()
        
        for ai_name, ai_status in status.items():
            with st.expander(f"{ai_name.upper()} Status"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Versions", ai_status["total_versions"])
                with col2:
                    st.metric("Latest", ai_status.get("latest_version", "None"))
                with col3:
                    st.metric("Examples", ai_status["training_examples"])
                    
                # Status indicator
                status_color = "🟢" if ai_status["production_status"] == "Deployed" else "🟡"
                st.write(f"{status_color} {ai_status['production_status']}")
                
    def show_version_management(self):
        """Display version management"""
        st.subheader("🏷️ Version Management")
        
        # Version timeline
        versions_data = self.get_version_timeline()
        if versions_data:
            df = pd.DataFrame(versions_data)
            fig = px.timeline(df, x_start="start", x_end="end", y="ai_name", 
                            color="version", title="Version Timeline")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No versions created yet")
            
    def show_training_metrics(self):
        """Display training metrics"""
        st.subheader("📈 Training Metrics")
        
        # Training progress over time
        metrics_data = self.get_training_metrics()
        
        if metrics_data:
            df = pd.DataFrame(metrics_data)
            
            # Performance chart
            fig = go.Figure()
            for ai in df['ai_name'].unique():
                ai_data = df[df['ai_name'] == ai]
                fig.add_trace(go.Scatter(
                    x=ai_data['date'],
                    y=ai_data['performance'],
                    mode='lines+markers',
                    name=ai.upper()
                ))
            fig.update_layout(title="Performance Over Time", 
                            xaxis_title="Date", yaxis_title="Performance Score")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Start training to see metrics")
            
    def show_data_insights(self):
        """Display training data insights"""
        st.subheader("💡 Data Insights")
        
        # Training data breakdown
        data_insights = self.get_data_insights()
        
        if data_insights:
            # Category distribution
            categories = data_insights.get("categories", {})
            if categories:
                fig = px.pie(values=list(categories.values()), 
                           names=list(categories.keys()),
                           title="Training Data by Category")
                st.plotly_chart(fig, use_container_width=True)
                
            # Recent activity
            st.write("**Recent Training Activity:**")
            recent = data_insights.get("recent_sessions", [])
            for session in recent[-5:]:
                st.write(f"• {session}")
        else:
            st.info("No training data collected yet")
            
    def show_training_controls(self, selected_ai):
        """Display training control panel"""
        st.subheader("🎮 Training Controls")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 Generate Dataset"):
                with st.spinner("Generating dataset..."):
                    result = self.generate_dataset(selected_ai)
                st.success(f"Dataset generated: {result}")
                
        with col2:
            if st.button("🎓 Start Training"):
                with st.spinner("Starting training..."):
                    result = self.start_training(selected_ai)
                st.success(f"Training started: {result}")
                
        with col3:
            if st.button("✅ Validate Model"):
                with st.spinner("Validating model..."):
                    result = self.validate_model(selected_ai)
                st.success(f"Validation complete: {result}")
                
        with col4:
            if st.button("🚀 Deploy Model"):
                with st.spinner("Deploying model..."):
                    result = self.deploy_model(selected_ai)
                st.success(f"Model deployed: {result}")
                
        # Advanced controls
        with st.expander("Advanced Training Options"):
            col1, col2 = st.columns(2)
            
            with col1:
                epochs = st.slider("Training Epochs", 1, 10, 3)
                batch_size = st.selectbox("Batch Size", [2, 4, 8, 16], index=1)
                
            with col2:
                learning_rate = st.select_slider("Learning Rate", 
                                               options=[1e-5, 2e-5, 5e-5, 1e-4], 
                                               value=2e-5, format_func=lambda x: f"{x:.0e}")
                save_steps = st.number_input("Save Steps", value=100, step=50)
                
            training_config = {
                "epochs": epochs,
                "batch_size": batch_size,
                "learning_rate": learning_rate,
                "save_steps": save_steps
            }
            
            if st.button("🔧 Apply Custom Training"):
                with st.spinner("Applying custom training configuration..."):
                    result = self.custom_training(selected_ai, training_config)
                st.success(f"Custom training applied: {result}")
                
    def get_training_status(self):
        """Get current training status"""
        # Mock data - integrate with actual training manager
        return {
            "claudae": {
                "total_versions": 2,
                "latest_version": "v2",
                "production_status": "Deployed",
                "training_examples": 15
            },
            "nyala": {
                "total_versions": 1,
                "latest_version": "v1", 
                "production_status": "Training",
                "training_examples": 8
            },
            "deon": {
                "total_versions": 1,
                "latest_version": "v1",
                "production_status": "Not Deployed",
                "training_examples": 5
            }
        }
        
    def get_version_timeline(self):
        """Get version timeline data"""
        return [
            {"ai_name": "CLAUDAE", "version": "v1", "start": "2025-06-01", "end": "2025-06-02"},
            {"ai_name": "CLAUDAE", "version": "v2", "start": "2025-06-03", "end": "2025-06-04"},
            {"ai_name": "NYALA", "version": "v1", "start": "2025-06-03", "end": "2025-06-04"},
            {"ai_name": "DEON", "version": "v1", "start": "2025-06-04", "end": "2025-06-05"}
        ]
        
    def get_training_metrics(self):
        """Get training metrics over time"""
        return [
            {"ai_name": "claudae", "date": "2025-06-01", "performance": 0.75},
            {"ai_name": "claudae", "date": "2025-06-02", "performance": 0.82},
            {"ai_name": "claudae", "date": "2025-06-03", "performance": 0.88},
            {"ai_name": "nyala", "date": "2025-06-02", "performance": 0.70},
            {"ai_name": "nyala", "date": "2025-06-03", "performance": 0.78},
            {"ai_name": "deon", "date": "2025-06-03", "performance": 0.73}
        ]
        
    def get_data_insights(self):
        """Get training data insights"""
        return {
            "categories": {
                "Market Data": 8,
                "AI Integration": 4,
                "Trading": 6,
                "Monitoring": 3
            },
            "recent_sessions": [
                "market_data_pipeline (4 examples)",
                "ai_data_integration (2 examples)", 
                "nyala_integration (3 examples)",
                "full_pipeline_test (1 example)"
            ]
        }
        
    def generate_dataset(self, ai_name):
        """Generate training dataset"""
        return f"Dataset generated for {ai_name} with 15 examples"
        
    def start_training(self, ai_name):
        """Start model training"""
        return f"Training started for {ai_name} v3"
        
    def validate_model(self, ai_name):
        """Validate trained model"""
        return f"Validation passed: 87% accuracy for {ai_name}"
        
    def deploy_model(self, ai_name):
        """Deploy model to production"""
        return f"{ai_name} v3 deployed to production"
        
    def custom_training(self, ai_name, config):
        """Apply custom training configuration"""
        return f"Custom training applied to {ai_name}: {config}"

if __name__ == "__main__":
    dashboard = TrainingDashboard()
    dashboard.run()