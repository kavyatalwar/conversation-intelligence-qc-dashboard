import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pipeline import get_processed_data
import statsmodels

st.set_page_config(page_title="Convin QC Conversation Intelligence", layout="wide")

@st.cache_data
def load_cached_data():
    return get_processed_data()

df_calls = load_cached_data()

st.title("🎙️ Automated Conversation Intelligence Platform")
st.markdown("### 🛠️ 7 QC Tools - Data Visualization Audit Framework")

# Global Analytical Filters (Sidebar Navigation)
st.sidebar.header("📁 Navigation & Filters")
selected_agents = st.sidebar.multiselect("Select Agents", options=df_calls['agent_name'].unique(), default=df_calls['agent_name'].unique())
selected_type = st.sidebar.multiselect("Call Type Filter", options=df_calls['call_type'].unique(), default=df_calls['call_type'].unique())

filtered_df = df_calls[(df_calls['agent_name'].isin(selected_agents)) & (df_calls['call_type'].isin(selected_type))]

# Multi-Page Tabs aligned to QC Strategy
tab1, tab2, tab3, tab4 = st.tabs(["📊 Statistical Control Center", "📈 Correlation & Pareto Analysis", "🔀 Individual Call Deep-Dive","🏆 Agent Performance Leaderboard"])

# --- TAB 1: CONTROL CHART (STATISTICAL PROCESS CONTROL) ---
with tab1:
    st.markdown("#### 1. Control Chart (Shewhart Chart) — Daily Process Stability")
    st.markdown("> *QC Tool Objective: Track daily quality stability. Points violating control limits indicate operational anomalies.*")
    
    # Aggregate data by date
    daily_stats = filtered_df.groupby('date')['quality_score'].agg(['mean', 'std']).reset_index()
    
    # Establish statistical control boundaries (Process Mean +/- 1.5 Standard Deviation for sample variance)
    grand_mean = filtered_df['quality_score'].mean()
    ucl = grand_mean + (1.5 * filtered_df['quality_score'].std())
    lcl = grand_mean - (1.5 * filtered_df['quality_score'].std())
    
    fig_control = go.Figure()
    
    # Plot active daily averages
    fig_control.add_trace(go.Scatter(x=daily_stats['date'], y=daily_stats['mean'], mode='lines+markers', name='Daily Avg Quality', line=dict(color='#636EFA', width=3)))
    # Center Line (CL)
    fig_control.add_trace(go.Scatter(x=daily_stats['date'], y=[grand_mean]*len(daily_stats), mode='lines', name='Center Line (Mean)', line=dict(color='green', dash='dash')))
    # Upper Control Limit (UCL)
    fig_control.add_trace(go.Scatter(x=daily_stats['date'], y=[ucl]*len(daily_stats), mode='lines', name='UCL (Upper Limit)', line=dict(color='red', width=1.5)))
    # Lower Control Limit (LCL)
    fig_control.add_trace(go.Scatter(x=daily_stats['date'], y=[lcl]*len(daily_stats), mode='lines', name='LCL (Lower Limit)', line=dict(color='red', width=1.5)))
    
    fig_control.update_layout(yaxis_title="Quality Score (%)", xaxis_title="Timeline Date", hovermode="x unified")
    st.plotly_chart(fig_control, use_container_width=True)

# --- TAB 2: CORRELATION (SCATTER) & PARETO ANALYSIS ---
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 2. Scatter Diagram — Factor Correlation")
        st.markdown("> *QC Tool Objective: Isolate mathematical dependencies between conversational dynamics and customer sentiment.*")
        
        fig_scatter = px.scatter(
            filtered_df, 
            x='talk_ratio', 
            y='sentiment_score', 
            color='agent_name',
            trendline="ols",
            title="Correlation: Talk-to-Listen Ratio vs. Customer Sentiment Score",
            labels={'talk_ratio': 'Agent Talk Ratio (Normalized)', 'sentiment_score': 'Customer Sentiment polarity'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with col2:
        st.markdown("#### 3. Pareto Chart — The 80/20 Defect Rule")
        st.markdown("> *QC Tool Objective: Identify the vital few sources of error. Isolating the top categories resolves 80% of system defects.*")
        
        # Define a "Defect" as any call scoring under a passing quality threshold of 65%
        defect_df = filtered_df[filtered_df['quality_score'] < 65.0]
        
        if not defect_df.empty:
            pareto_data = defect_df.groupby('agent_name').size().reset_index(name='count')
            pareto_data = pareto_data.sort_values(by='count', ascending=False)
            pareto_data['cumulative_percentage'] = (pareto_data['count'].cumsum() / pareto_data['count'].sum()) * 100
            
            fig_pareto = go.Figure()
            # Bar chart for absolute defect frequency counts
            fig_pareto.add_trace(go.Bar(x=pareto_data['agent_name'], y=pareto_data['count'], name='Defect Count', yaxis='y1', marker_color='#EF553B'))
            # Line plot tracing cumulative impact percentage progression
            fig_pareto.add_trace(go.Scatter(x=pareto_data['agent_name'], y=pareto_data['cumulative_percentage'], name='Cumulative %', yaxis='y2', mode='lines+markers', line=dict(color='#00CC96', width=3)))
            
            fig_pareto.update_layout(
                title="Pareto Distribution: Defect Contribution Metrics By Agent Profile",
                yaxis=dict(title="Number of Low-Quality Calls (Defects)"),
                yaxis2=dict(title="Cumulative Percentage (%)", overlaying='y', side='right', range=[0, 105]),
                showlegend=True
            )
            st.plotly_chart(fig_pareto, use_container_width=True)
        else:
            st.success("Zero system anomalies logged! All active operations are clearing the target 65% Quality threshold.")

# --- TAB 3: DRILL DOWN ARC ANALYSIS ---
with tab3:
    st.markdown("#### 4. Run Chart Timeline Exploration")
    target_call = st.selectbox("Select Call Instance to View Details", options=filtered_df['call_id'].unique())
    call_row = filtered_df[filtered_df['call_id'] == target_call].iloc[0]
    
    fig_arc = px.line(
        y=call_row['individual_customer_scores'], 
        markers=True,
        labels={'x': "Conversation Turn Index", 'y': "Polarity Score (-1 to +1)"}, 
        title=f"Utterance-by-Utterance Customer Sentiment Arc for {target_call}"
    )
    st.plotly_chart(fig_arc, use_container_width=True)
    
    st.markdown("**Raw Audited Transcript Data:**")
    st.text_area("Transcript Reader Box", value=call_row['full_transcript'], height=200)

# --- PAGE 4: AGENT PERFORMANCE LEADERBOARD ---
with tab4:
    st.markdown("#### Multi-Dimensional Quality Assurance Assessment Profile") 
    agent_summary = filtered_df.groupby('agent_name').agg({
        'quality_score': 'mean',
        'script_adherence': 'mean',
        'talk_ratio': 'mean',
        'sentiment_score': 'mean'
    }).reset_index()
    
    selected_leader = st.selectbox("Select Target Agent for Spider Evaluation", options=agent_summary['agent_name'].unique())
    agent_data = agent_summary[agent_summary['agent_name'] == selected_leader].iloc[0]
    
    # Structuring clean Plotly Graph Objects Radar Profile
    fig_radar = go.Figure() 
    fig_radar.add_trace(go.Scatterpolar(
          r=[agent_data['quality_score']/100, agent_data['script_adherence'], agent_data['talk_ratio'], (agent_data['sentiment_score']+1)/2],
          theta=['Overall Quality Score', 'Script Adherence Rule', 'Talk-to-Listen Efficiency', 'Normalized Sentiment Balance'],
          fill='toself',
          name=selected_leader
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), title=f"Operational Radar Framework Mapping: {selected_leader}") 
    st.plotly_chart(fig_radar, use_container_width=True)