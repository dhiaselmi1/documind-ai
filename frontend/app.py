# ===============================
# frontend/app.py
# ===============================

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List
import time
import json

# Page configuration
st.set_page_config(
    page_title="Document Intelligence Workspace",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        padding: 1rem 0;
        border-bottom: 2px solid #f0f2f6;
        margin-bottom: 2rem;
    }
    .agent-card {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e6e6e6;
        margin: 0.5rem 0;
    }
    .red-flag {
        background-color: #ffebee;
        padding: 0.5rem;
        border-left: 4px solid #f44336;
        margin: 0.5rem 0;
    }
    .decision-item {
        background-color: #e8f5e8;
        padding: 0.5rem;
        border-left: 4px solid #4caf50;
        margin: 0.5rem 0;
    }
    .summary-box {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main Streamlit application."""

    # Header
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("📄 Document Intelligence Workspace")
    st.markdown("*Upload documents and let AI agents collaboratively analyze them*")
    st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("🔧 Controls")

        # Check API status
        api_status = check_api_status()
        if api_status:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Disconnected")
            st.info("Make sure the FastAPI backend is running on port 8000")
            return

        st.markdown("---")

        # Navigation
        page = st.selectbox(
            "Navigate to:",
            ["📁 Upload & Analyze", "📊 Analysis Dashboard", "📈 History"]
        )

    # Main content based on selected page
    if page == "📁 Upload & Analyze":
        upload_and_analyze_page()
    elif page == "📊 Analysis Dashboard":
        analysis_dashboard_page()
    elif page == "📈 History":
        history_page()


def check_api_status() -> bool:
    """Check if the FastAPI backend is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def upload_and_analyze_page():
    """Document upload and analysis page."""

    st.header("📁 Document Upload & Analysis")

    # File upload
    uploaded_file = st.file_uploader(
        "Choose a document",
        type=['pdf', 'docx', 'txt'],
        help="Upload PDF, DOCX, or TXT files for analysis"
    )

    if uploaded_file is not None:
        # Display file info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("File Name", uploaded_file.name)
        with col2:
            st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
        with col3:
            st.metric("File Type", uploaded_file.type)

        # Upload button
        if st.button("🚀 Upload & Analyze", type="primary", use_container_width=True):
            analyze_document(uploaded_file)


def analyze_document(uploaded_file):
    """Upload and analyze the document."""

    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        # Step 1: Upload document
        status_text.text("📤 Uploading document...")
        progress_bar.progress(20)

        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        upload_response = requests.post(f"{API_BASE_URL}/upload", files=files)

        if upload_response.status_code != 200:
            st.error(f"Upload failed: {upload_response.text}")
            return

        document_info = upload_response.json()
        document_id = document_info["id"]

        # Step 2: Start analysis
        status_text.text("🤖 Running agent analysis...")
        progress_bar.progress(40)

        analysis_response = requests.post(f"{API_BASE_URL}/analyze/{document_id}")

        if analysis_response.status_code != 200:
            st.error(f"Analysis failed: {analysis_response.text}")
            return

        progress_bar.progress(100)
        status_text.text("✅ Analysis completed!")

        # Store results in session state
        st.session_state.current_analysis = analysis_response.json()
        st.session_state.current_document = document_info

        time.sleep(1)  # Brief pause for user feedback
        st.rerun()

    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")

    # Display results if available
    if "current_analysis" in st.session_state:
        display_analysis_results()


def display_analysis_results():
    """Display the analysis results."""

    if "current_analysis" not in st.session_state:
        return

    analysis = st.session_state.current_analysis
    document = st.session_state.current_document

    st.markdown("---")
    st.header("📊 Analysis Results")

    # Document info
    with st.expander("📄 Document Information", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Filename:** {document['filename']}")
            st.write(f"**File Type:** {document['file_type']}")
        with col2:
            stats = analysis.get('statistics', {})
            st.write(f"**Word Count:** {stats.get('word_count', 'N/A')}")
            st.write(f"**Character Count:** {stats.get('document_length', 'N/A')}")

    # Agent Results
    col1, col2, col3 = st.columns(3)

    # Summary Agent Results
    with col1:
        st.markdown('<div class="agent-card">', unsafe_allow_html=True)
        st.subheader("📝 Summary Agent")
        st.markdown('<div class="summary-box">', unsafe_allow_html=True)
        st.write(analysis.get("summary", "No summary available"))
        st.markdown('</div>', unsafe_allow_html=True)

        # Key topics
        key_topics = analysis.get('statistics', {}).get('key_topics', [])
        if key_topics:
            st.write("**Key Topics:**")
            for topic in key_topics:
                st.badge(topic)
        st.markdown('</div>', unsafe_allow_html=True)

    # Red Flag Agent Results
    with col2:
        st.markdown('<div class="agent-card">', unsafe_allow_html=True)
        st.subheader("🚨 Red Flag Detector")

        red_flags = analysis.get("red_flags", [])
        if red_flags:
            st.write(f"**Found {len(red_flags)} potential issues:**")
            for flag in red_flags:
                st.markdown(f'<div class="red-flag">{flag}</div>', unsafe_allow_html=True)
        else:
            st.success("✅ No red flags detected")
        st.markdown('</div>', unsafe_allow_html=True)

    # Decision Agent Results
    with col3:
        st.markdown('<div class="agent-card">', unsafe_allow_html=True)
        st.subheader("⚖️ Decision Extractor")

        decisions = analysis.get("decisions", [])
        if decisions:
            st.write(f"**Found {len(decisions)} decisions/actions:**")
            for decision in decisions:
                st.markdown(f'<div class="decision-item">{decision}</div>', unsafe_allow_html=True)
        else:
            st.info("ℹ️ No decisions or action items found")
        st.markdown('</div>', unsafe_allow_html=True)

    # Collaborative Insights
    if "collaborative_insights" in analysis:
        insights = analysis["collaborative_insights"]

        st.markdown("---")
        st.header("🔬 Collaborative Insights")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            risk_color = {"Low": "green", "Medium": "orange", "High": "red"}[insights["risk_level"]]
            st.metric("Risk Level", insights["risk_level"])
        with col2:
            st.metric("Urgency", insights["urgency"])
        with col3:
            st.metric("Complexity", insights["complexity"])
        with col4:
            st.metric("Confidence", f"{insights['confidence_score']:.1%}")

        # Recommendations
        st.subheader("💡 Recommendations")
        if insights["requires_attention"]:
            st.warning("⚠️ This document requires immediate attention due to identified red flags.")

        if insights["has_action_items"]:
            st.info("📋 This document contains action items that need to be tracked.")

        if not insights["requires_attention"] and not insights["has_action_items"]:
            st.success("✅ This document appears to be informational with no immediate actions required.")


def analysis_dashboard_page():
    """Analysis dashboard with visualizations."""

    st.header("📊 Analysis Dashboard")

    if "current_analysis" not in st.session_state:
        st.info("📥 Upload and analyze a document first to see dashboard.")
        return

    analysis = st.session_state.current_analysis
    stats = analysis.get('statistics', {})

    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Word Count", stats.get('word_count', 0))
    with col2:
        st.metric("Red Flags", stats.get('total_red_flags', 0))
    with col3:
        st.metric("Decisions", stats.get('total_decisions', 0))
    with col4:
        insights = analysis.get('collaborative_insights', {})
        st.metric("Risk Level", insights.get('risk_level', 'Unknown'))

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        # Red flags breakdown
        red_flags = analysis.get("red_flags", [])
        if red_flags:
            st.subheader("🚨 Red Flags Analysis")

            # Categorize red flags for visualization
            categories = {"Legal": 0, "Financial": 0, "Operational": 0, "Other": 0}

            for flag in red_flags:
                flag_lower = flag.lower()
                if any(word in flag_lower for word in ["legal", "lawsuit", "compliance", "violation"]):
                    categories["Legal"] += 1
                elif any(word in flag_lower for word in ["financial", "money", "cost", "budget", "debt"]):
                    categories["Financial"] += 1
                elif any(word in flag_lower for word in ["operational", "process", "system", "deadline"]):
                    categories["Operational"] += 1
                else:
                    categories["Other"] += 1

            fig = px.pie(
                values=list(categories.values()),
                names=list(categories.keys()),
                title="Red Flags by Category"
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Key topics
        key_topics = stats.get('key_topics', [])
        if key_topics:
            st.subheader("🔑 Key Topics")

            # Create a simple bar chart of topics
            topic_data = pd.DataFrame({
                'Topic': key_topics,
                'Relevance': [len(topic) for topic in key_topics]  # Simple relevance score
            })

            fig = px.bar(
                topic_data,
                x='Relevance',
                y='Topic',
                orientation='h',
                title="Document Topics"
            )
            st.plotly_chart(fig, use_container_width=True)


def history_page():
    """Analysis history page."""

    st.header("📈 Analysis History")

    try:
        # Get documents from API
        response = requests.get(f"{API_BASE_URL}/documents")
        if response.status_code == 200:
            documents = response.json()

            if documents:
                st.write(f"**Total Documents Analyzed:** {len(documents)}")

                # Create a table of documents
                doc_data = []
                for doc in documents:
                    doc_data.append({
                        "Filename": doc["filename"],
                        "File Type": doc["file_type"],
                        "Word Count": len(doc["content"].split()),
                        "ID": doc["id"][:8] + "..."
                    })

                df = pd.DataFrame(doc_data)
                st.dataframe(df, use_container_width=True)

                # File type distribution
                file_types = [doc["file_type"] for doc in documents]
                type_counts = pd.Series(file_types).value_counts()

                fig = px.pie(
                    values=type_counts.values,
                    names=type_counts.index,
                    title="Document Types Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.info("📭 No documents have been analyzed yet.")
        else:
            st.error("Failed to fetch document history.")

    except Exception as e:
        st.error(f"Error loading history: {str(e)}")


# Utility functions
def format_analysis_results(analysis: Dict[str, Any]) -> str:
    """Format analysis results for display."""

    summary = analysis.get("summary", "No summary available")
    red_flags = analysis.get("red_flags", [])
    decisions = analysis.get("decisions", [])

    formatted = f"""
    ## Summary
    {summary}

    ## Red Flags ({len(red_flags)})
    """

    for i, flag in enumerate(red_flags, 1):
        formatted += f"{i}. {flag}\n"

    formatted += f"\n## Decisions & Actions ({len(decisions)})\n"

    for i, decision in enumerate(decisions, 1):
        formatted += f"{i}. {decision}\n"

    return formatted


def export_analysis_results(analysis: Dict[str, Any], filename: str):
    """Export analysis results to various formats."""

    # JSON export
    json_data = json.dumps(analysis, indent=2)
    st.download_button(
        label="📥 Download JSON",
        data=json_data,
        file_name=f"{filename}_analysis.json",
        mime="application/json"
    )

    # Text export
    text_data = format_analysis_results(analysis)
    st.download_button(
        label="📥 Download Report",
        data=text_data,
        file_name=f"{filename}_report.txt",
        mime="text/plain"
    )


# Run the app
if __name__ == "__main__":
    main()