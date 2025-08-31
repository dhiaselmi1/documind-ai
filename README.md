

# 📄 DocuMind AI - Multi-Agent Document Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🤖 **Transform document analysis with collaborative AI agents**

DocuMind AI is an intelligent document analysis platform that automatically processes your documents using specialized AI agents. Upload any PDF, DOCX, or TXT file and watch as three collaborative agents work together to provide comprehensive insights, risk detection, and decision extraction.

## ✨ Features

🔍 **Multi-Agent Analysis**
- **Summary Agent**: Creates comprehensive document summaries with key topics
- **Red Flag Detector**: Identifies risks, legal issues, and compliance concerns  
- **Decision Extractor**: Finds decisions, action items, and deadlines

📄 **Multi-Format Support**
- PDF documents with text extraction
- Microsoft Word (DOCX) files
- Plain text (TXT) files

⚡ **Real-Time Processing**
- Concurrent agent execution
- Live progress tracking
- Instant results dashboard

📊 **Interactive Dashboard**
- Visual analytics and charts
- Risk level assessments
- Collaborative insights
- Export capabilities (JSON, TXT)

🚀 **Easy Deployment**
- Simple FastAPI backend
- Streamlit web interface
- Docker support ready
- No external dependencies for basic functionality

## 🎯 Use Cases

- **Legal Document Review**: Quickly identify risks and key decisions in contracts
- **Business Report Analysis**: Extract action items and strategic decisions
- **Compliance Checking**: Detect potential compliance issues and red flags
- **Meeting Minutes Processing**: Summarize discussions and extract action items
- **Research Paper Analysis**: Generate summaries and identify key findings

## 🏗️ Architecture

```
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
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/documind-ai.git
cd documind-ai
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

#### Option 1: Manual Start (Recommended for Development)

**Terminal 1 - Start Backend:**
```bash
cd backend
python main.py
```
✅ Backend API running at: `http://localhost:8000`  
📚 API Documentation: `http://localhost:8000/docs`

**Terminal 2 - Start Frontend:**
```bash
cd frontend
streamlit run app.py
```
✅ Web Interface: `http://localhost:8501`

#### Option 2: Docker (Coming Soon)
```bash
docker-compose up --build
```

## 📖 Usage Guide

### 1. Upload Document
- Navigate to the "📁 Upload & Analyze" page
- Drag and drop or select your document (PDF, DOCX, or TXT)
- Click "🚀 Upload & Analyze"

### 2. View Analysis
- Watch real-time progress as agents analyze your document
- Review comprehensive results from all three agents
- Explore collaborative insights and recommendations

### 3. Dashboard & History
- Use the "📊 Analysis Dashboard" for detailed visualizations
- Check "📈 History" to see all previously analyzed documents
- Export results in JSON or text format

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# File Upload Limits
MAX_FILE_SIZE=10485760  # 10MB in bytes
ALLOWED_EXTENSIONS=pdf,docx,txt

# Llama3 Configuration (Optional)
LLAMA_MODEL_PATH=./models/llama-3-8b-instruct.gguf
LLAMA_CONTEXT_SIZE=4096
```

### Llama3 Integration
The system works with keyword-based analysis by default. To enable Llama3:

1. Download a Llama3 model (GGUF format recommended)
2. Place in `./models/` directory
3. Update the `LLAMA_MODEL_PATH` in your `.env` file
4. Implement the `LlamaService` class in the agents

## 📊 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload` | Upload a document for analysis |
| `POST` | `/analyze/{document_id}` | Analyze uploaded document |
| `GET` | `/documents` | List all uploaded documents |
| `GET` | `/analysis/{document_id}` | Get analysis results |
| `GET` | `/health` | API health check |

### Example API Usage

```python
import requests

# Upload document
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/upload', files=files)
    document_id = response.json()['id']

# Analyze document
analysis = requests.post(f'http://localhost:8000/analyze/{document_id}')
results = analysis.json()

print(f"Summary: {results['summary']}")
print(f"Red Flags: {len(results['red_flags'])}")
print(f"Decisions: {len(results['decisions'])}")
```

## 🧪 Testing

Run the test suite:
```bash
pytest tests/ -v
```

Test specific components:
```bash
# Test agents
pytest tests/test_agents/ -v

# Test API endpoints
pytest tests/test_api/ -v
```

## 🔍 Project Structure

```
documind-ai/
├── backend/
│   ├── main.py                 # FastAPI application
│   └── agents/
│       ├── base.py            # Base agent class
│       ├── summary_agent.py   # Document summarization
│       ├── red_flag_agent.py  # Risk detection
│       ├── decision_agent.py  # Decision extraction
│       └── orchestrator.py    # Agent coordination
├── frontend/
│   └── app.py                 # Streamlit interface
├── tests/                     # Test suite
├── models/                    # AI model storage
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🛡️ Security & Privacy

- **Local Processing**: All document analysis happens locally
- **No Data Persistence**: Documents are stored in memory only
- **CORS Protection**: Configured for secure cross-origin requests
- **File Validation**: Strict file type and size validation

## 🔮 Roadmap

- [ ] **Enhanced AI Integration**: Full Llama3 local inference
- [ ] **Database Persistence**: Optional document storage with SQLite/PostgreSQL
- [ ] **Batch Processing**: Upload and analyze multiple documents
- [ ] **Custom Agents**: Framework for creating specialized analysis agents
- [ ] **Advanced Visualizations**: More detailed analytics and charts
- [ ] **API Authentication**: Secure API access with JWT tokens
- [ ] **Document Comparison**: Compare analyses across multiple documents
- [ ] **Export Templates**: Customizable report templates

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Open a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use type hints where possible
- Add docstrings to functions and classes
- Write tests for new features

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/dhiaselmi1/documind-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/dhiaselmi1/documind-ai/discussions)
- **Email**: mohameddhiaselmii@gmail.com

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** - Modern, fast web framework for building APIs
- **Streamlit** - Rapid web app development for data science
- **Llama3** - Advanced language model for text analysis
- **PyPDF2** - PDF text extraction
- **python-docx** - DOCX document processing
