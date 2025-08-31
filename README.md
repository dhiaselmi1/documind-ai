# 📄 DocuMind AI: Multi-Agent Document Intelligence Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-green)](https://fastapi.tiangolo.com/)
[![Frontend](https://img.shields.io/badge/Frontend-Streamlit-red)](https://streamlit.io/)

An intelligent document analysis platform that uses collaborative AI agents to automatically summarize, detect risks, and extract decisions from uploaded documents. Built with FastAPI, Streamlit, and designed for Llama3 integration.

---



## 🤖 Transform Document Analysis with Collaborative AI Agents

**DocuMind AI** is an intelligent document analysis platform that automatically processes your documents using specialized AI agents. Upload any PDF, DOCX, or TXT file and watch as three collaborative agents work together to provide comprehensive insights, risk detection, and decision extraction.

---

## ✨ Features

* **🔍 Multi-Agent Analysis**
    * **Summary Agent:** Creates comprehensive document summaries with key topics.
    * **Red Flag Detector:** Identifies risks, legal issues, and compliance concerns.
    * **Decision Extractor:** Finds decisions, action items, and deadlines.

* **📄 Multi-Format Support**
    * PDF documents with text extraction.
    * Microsoft Word (DOCX) files.
    * Plain text (TXT) files.

* **⚡ Real-Time Processing**
    * Concurrent agent execution.
    * Live progress tracking.
    * Instant results dashboard.

* **📊 Interactive Dashboard**
    * Visual analytics and charts.
    * Risk level assessments.
    * Collaborative insights.
    * Export capabilities (JSON, TXT).

* **🚀 Easy Deployment**
    * Simple FastAPI backend.
    * Streamlit web interface.
    * Docker support ready.
    * No external dependencies for basic functionality.

---

## 🎯 Use Cases

* **Legal Document Review:** Quickly identify risks and key decisions in contracts.
* **Business Report Analysis:** Extract action items and strategic decisions.
* **Compliance Checking:** Detect potential compliance issues and red flags.
* **Meeting Minutes Processing:** Summarize discussions and extract action items.
* **Research Paper Analysis:** Generate summaries and identify key findings.

---

## 🏗️ Architecture

┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│   Streamlit     │◄───────────────►│    FastAPI      │
│   Frontend      │                 │    Backend      │
│                 │                 │                 │
│ • File Upload   │                 │ • Text Extract  │
│ • Dashboard     │                 │ • Agent System  │
│ • Visualizations│                 │ • API Endpoints │
└─────────────────┘                 └─────────────────┘
                                            │
                                            ▼
                                    ┌─────────────────┐
                                    │ AI Agent System │
                                    │                 │
                                    │ ┌─────────────┐ │
                                    │ │Summary Agent│ │
                                    │ └─────────────┘ │
                                    │ ┌─────────────┐ │
                                    │ │Red Flag Det.│ │
                                    │ └─────────────┘ │
                                    │ ┌─────────────┐ │
                                    │ │Decision Ext.│ │
                                    │ └─────────────┘ │
                                    └─────────────────┘


---

## 🚀 Quick Start

### Prerequisites
* Python 3.8 or higher
* `pip` package manager

### Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/documind-ai.git](https://github.com/yourusername/documind-ai.git)
    cd documind-ai
    ```

2.  **Create and activate a virtual environment**
    ```bash
    # Create the environment
    python -m venv venv

    # Activate on Windows
    venv\Scripts\activate

    # Activate on macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

#### Option 1: Manual Start (Recommended for Development)

* **Terminal 1 - Start Backend:**
    ```bash
    cd backend
    python main.py
    ```
    ✅ **Backend API running at:** `http://localhost:8000`  
    📚 **API Documentation:** `http://localhost:8000/docs`

* **Terminal 2 - Start Frontend:**
    ```bash
    cd frontend
    streamlit run app.py
    ```
    ✅ **Web Interface:** `http://localhost:8501`
