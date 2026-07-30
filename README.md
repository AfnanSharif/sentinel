# 🏢 SENTINEL — Enterprise Support Agent & SLA Pipeline

![Sentinel Banner](docs/assets/banner.svg)


**Sentinel** is an enterprise-grade AI customer support engine built using OpenAI, FAISS vector stores, and Azure ML pipelines. It automates ticket sentiment classification, priority routing, SLA response management, and resolution retrieval.

---

## 📖 Table of Contents
1. [What is Sentinel?](#-what-is-sentinel)
2. [Industrial Use Cases](#-industrial-use-cases)
3. [Performance SLA Targets](#-performance-sla-targets)
4. [File & Directory Layout](#-file--directory-layout)
5. [Getting Started & Installation](#-getting-started--installation)
6. [Core Support Pipeline](#-core-support-pipeline)
7. [Unit Testing Suite](#-unit-testing-suite)

---

## 💡 What is Sentinel?

Sentinel is designed for enterprise scaling.
- **Sentiment & Priority NLP Engine**: Automatically parses support tickets to classify category (Billing, Tech, Quality) and detect customer frustration levels.
- **Top-K Resolution Retrieval**: Searches historic resolution guides using FAISS Vector Stores to find the best fixes.
- **SLA-Compliant Auto Responses**: Uses GPT-4 to draft professional, context-grounded support emails, starting with apologetic remarks for negative customer sentiments.

---

## 🎯 Industrial Use Cases

- **Enterprise SLA Enforcement**: Automate ticket response drafts, ensuring critical bug tickets (High Priority) receive resolution outlines within minutes.
- **Retail & E-commerce Operations**: Route shipping queries to carrier support and handle double-billing issues with Stripe integration templates.
- **Corporate Customer Relations**: Gauge customer happiness scores and track sentiment trends over time.

---

## 📈 Performance SLA Targets

| Metric | Target SLA | Engine Strategy |
|:---|:---|:---|
| **Response Latency** | < 2.0s | OpenAI Streaming + FAISS Cached Hits |
| **Priority Accuracy**| > 95% | Classification heuristics + GPT-4 Guardrails |
| **Sentiment Tracking**| Real-time | Sentiment analyzer |

---

## 📐 System Pipeline Flow

```
   [Incoming Support Request]
               │
               ▼
   [NLP Sentiment Analyzer] ──(Extract score/priority)──> [SLA Priority Router]
               │                                                  │
               └───────────────────────┬──────────────────────────┘
                                       ▼
                       [FAISS Vector Store Lookup]
                                       │
                              (Retrieve Top-K Context)
                                       ▼
                          [GPT-4 Prompt Grounding]
                                       │
                                       ▼
                         [SLA-Compliant Support Email]
```

---

## 📂 File & Directory Layout

All directories are located directly at the project root:
```
sentinel/
├── config/             # OpenAI and API parameters
│   ├── __init__.py
│   └── openai_config.py
├── nlp/                # Sentiment and classification routines
│   ├── __init__.py
│   ├── sentiment_analyzer.py
│   └── ticket_classifier.py
├── rag/                # FAISS indexing and grounding engine
│   ├── __init__.py
│   └── rag_engine.py
├── ui/                 # Plotly dashboards and layouts
│   ├── __init__.py
│   ├── dashboard.py
│   ├── styles.py
│   └── ticket_view.py
├── utils/              # Loguru structured logger utilities
│   ├── __init__.py
│   └── logger.py
├── scripts/            # FAISS builder scripts
│   ├── __init__.py
│   └── build_vector_db.py
├── tests/              # Test suites
│   ├── __init__.py
│   └── test_sentiment.py
├── .env.example        # Environment variable template
├── .gitignore          # Git exclusion lists
├── requirements.txt    # Pinned packages
├── README.md           # This document
└── main.py             # Entry application
```

---

## 🛠️ Getting Started & Installation

### 📋 Prerequisites
- Python 3.10.4 or higher
- Active OpenAI API credentials.

### 🐧 Linux / 🍏 macOS Installation
```bash
# 1. Navigate to directory
cd /home/afnan/Desktop/Projects/sentinel

# 2. Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Copy configuration template and input keys
cp .env.example .env

# 5. Populate FAISS Vector Database with resolution guides
python scripts/build_vector_db.py

# 6. Launch Streamlit UI
streamlit run main.py
```

### 🪟 Windows Setup
```powershell
# 1. Navigate to directory
cd C:\Path\To\sentinel

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# 3. Install packages
pip install -r requirements.txt

# 4. Copy config template
copy .env.example .env

# 5. Seed FAISS
python scripts/build_vector_db.py

# 6. Start Web Interface
streamlit run main.py
```

---

## 🧪 Unit Testing Suite
Verify sentiment scoring and ticket classification:
```bash
pytest tests/
```
