# 🛡️ AI Phishing Shield

> Next-generation AI-powered phishing intelligence and browser security platform.

AI Phishing Shield is an advanced phishing detection and threat intelligence platform designed to identify, analyze, explain, and block phishing attacks in real time.

Unlike traditional phishing detectors that rely primarily on blacklists and signature-based detection, AI Phishing Shield combines machine learning, semantic analysis, threat intelligence, reputation systems, and browser-native protection to detect both known and previously unseen phishing threats.

---

# 🚀 Vision

Build a modern phishing intelligence platform capable of:

* Real-time phishing prevention
* Brand impersonation detection
* Zero-day phishing detection
* Browser-native security protection
* Threat intelligence enrichment
* Explainable AI threat analysis
* Enterprise-ready browser security

---

# 🔥 Key Features

## ✅ Real-Time Browser Protection

The browser extension continuously monitors websites visited by the user and evaluates them in real time.

Features:

* Real-time URL monitoring
* Background scanning
* Automatic threat detection
* Browser-native phishing blocking
* Instant threat alerts

---

## ✅ Hybrid Threat Intelligence Engine

AI Phishing Shield combines multiple intelligence layers into a single risk assessment pipeline.

Current detection architecture:

```text
URL
 │
 ├── URL Intelligence
 ├── LightGBM Analysis
 ├── DistilBERT Semantic Analysis
 ├── WHOIS Intelligence
 ├── Reputation Engine
 ├── Redirect Intelligence
 ├── VirusTotal Verification
 ├── Typosquatting Detection
 └── Brand Impersonation Detection
 │
 ▼
 Hybrid Risk Fusion Engine
 │
 ▼
 Final Threat Decision
```

---

## ✅ Semantic Phishing Detection

DistilBERT-based semantic analysis detects:

* Phishing-related language patterns
* Credential harvesting indicators
* Obfuscated phishing URLs
* Authentication-related attacks
* Suspicious contextual structures

---

## ✅ Brand Impersonation Detection

Detects domains attempting to imitate trusted brands.

Examples:

```text
g00gle-login.com
paypa1-verification.net
micr0soft-auth.xyz
amaz0n-security-check.com
```

The system identifies:

* Typosquatting attacks
* Homograph attacks
* Brand impersonation attempts
* Credential theft campaigns

---

## ✅ Redirect Intelligence Engine

Analyzes redirect chains to identify:

* URL shorteners
* Redirect abuse
* Domain switching
* Multi-hop redirection attacks
* Suspicious destination changes

---

## ✅ WHOIS & Domain Intelligence

The platform evaluates:

* Domain age
* Registrar trustworthiness
* Registration anomalies
* Newly created domains
* Domain reputation signals

---

## ✅ VirusTotal Integration

Threat intelligence enrichment using VirusTotal:

* Malicious detections
* Suspicious detections
* Reputation verification
* Multi-engine validation

---

## ✅ Reputation Engine

Risk scoring based on:

* Suspicious keywords
* Entropy analysis
* Domain structure
* Authentication keywords
* TLD intelligence
* Historical threat indicators

---

## ✅ Explainable Threat Analysis

Instead of simply saying "malicious", the platform explains why.

Example:

```json
{
  "prediction": "malicious",
  "risk_level": "CRITICAL",
  "reasons": [
    "Possible Google typosquatting domain",
    "Contains login keyword",
    "Brand impersonation detected",
    "WHOIS lookup failed"
  ]
}
```

---

## ✅ Browser-Native Threat Blocking

When a threat is detected:

* Website access is blocked
* User is redirected to a warning page
* Risk score is displayed
* Threat explanations are shown
* Protection occurs before interaction

---

# 📊 Risk Scoring System

The platform calculates:

* Confidence Score
* Risk Score
* Risk Level
* Threat Indicators
* Detection Reasons

### Risk Levels

| Score  | Level    |
| ------ | -------- |
| 0-34   | SAFE     |
| 35-59  | MEDIUM   |
| 60-79  | HIGH     |
| 80-100 | CRITICAL |

---

# 🧠 Detection Pipeline

```text
Website Visit
      │
      ▼
URL Collection
      │
      ▼
Threat Intelligence Layer
      │
      ├── WHOIS Analysis
      ├── Reputation Analysis
      ├── Redirect Intelligence
      ├── VirusTotal Verification
      ├── Typosquatting Detection
      └── Semantic Analysis
      │
      ▼
Hybrid Risk Fusion Engine
      │
      ▼
Risk Score Calculation
      │
      ▼
Threat Classification
      │
      ├── SAFE
      ├── MEDIUM
      ├── HIGH
      └── CRITICAL
      │
      ▼
Browser Protection Action
```

---

# 🌐 System Architecture

```text
Browser
   │
   ▼
Chrome Extension
   │
   ▼
Background Scanner
   │
   ▼
Local Cache Engine
   │
   ▼
FastAPI Backend
   │
   ▼
Threat Intelligence Layer
   │
   ├── WHOIS Intelligence
   ├── Reputation Engine
   ├── Redirect Intelligence
   ├── VirusTotal
   ├── Typosquatting Detection
   └── Semantic Analysis
   │
   ▼
Hybrid Risk Fusion Engine
   │
   ▼
Threat Decision
   │
   ▼
Browser Protection
```

---

# 🧱 Technology Stack

| Technology        | Purpose             |
| ----------------- | ------------------- |
| Python            | Backend             |
| FastAPI           | Inference API       |
| JavaScript        | Browser Extension   |
| HTML/CSS          | Extension UI        |
| LightGBM          | URL Intelligence    |
| DistilBERT        | Semantic Analysis   |
| Docker            | Deployment          |
| SQLAlchemy        | Database ORM        |
| SQLite/PostgreSQL | Threat Storage      |
| VirusTotal API    | Threat Intelligence |

---

# 📂 Project Structure

```text
phishing-detector/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── schemas/
│   │   └── database/
│   │
│   ├── models/
│   ├── logs/
│   └── Dockerfile
│
├── chrome-extension/
│
├── README.md
├── requirements.txt
└── .env
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/rohithvandadi07-ux/ai-phishing-detection-system.git

cd ai-phishing-detection-system
```

---

## Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create `.env`

```env
VIRUSTOTAL_API_KEY=YOUR_API_KEY
DATABASE_URL=YOUR_DATABASE_URL
SECRET_KEY=YOUR_SECRET_KEY
```

---

## Run Backend

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

## Docker Deployment

Build:

```bash
docker build --no-cache -t phishing-api .
```

Run:

```bash
docker run --env-file .env -p 8080:8080 phishing-api
```

Backend:

```text
http://localhost:8080
```

---

## Load Browser Extension

1. Open Chrome
2. Navigate to:

```text
chrome://extensions
```

3. Enable Developer Mode
4. Click Load Unpacked
5. Select:

```text
chrome-extension/
```

---

# 📡 API Endpoints

| Method | Endpoint | Description  |
| ------ | -------- | ------------ |
| POST   | /predict | Scan URL     |
| GET    | /health  | Health Check |
| GET    | /        | Home Route   |

---

# 🧪 Example Test URLs

### Safe

```text
https://google.com
https://github.com
https://openai.com
https://microsoft.com
```

### Suspicious

```text
https://g00gle-login.com
https://paypa1-security.net
https://amaz0n-authentication.xyz
```

---

# 📈 Current Development Status

## Phase 1 — Core Detection Platform

Completed:

* FastAPI backend
* Hybrid risk engine
* LightGBM URL intelligence
* DistilBERT semantic analysis
* Risk scoring system
* Threat explanation engine

---

## Phase 2 — Browser Protection

Completed:

* Chrome extension
* Real-time scanning
* Automatic threat blocking
* Warning page system
* Browser badge indicators
* Local caching

---

## Phase 3 — Threat Intelligence

Completed:

* WHOIS intelligence
* Reputation engine
* VirusTotal integration
* Redirect intelligence
* Typosquatting detection
* Brand impersonation detection

---

# 🚀 Roadmap

## Phase 4 — Brand Intelligence

* Advanced impersonation detection
* Homograph attack detection
* Brand relationship analysis

---

## Phase 5 — Webpage Intelligence

* DOM analysis
* Login form analysis
* Credential harvesting detection
* Hidden element detection

---

## Phase 6 — Visual Intelligence

* Screenshot analysis
* Visual similarity detection
* Fake login page detection
* OCR-based phishing detection

---

## Phase 7 — Threat Graph

* Domain relationship mapping
* Infrastructure clustering
* Campaign detection
* Threat attribution

---

## Phase 8 — Platform Expansion

* Firefox extension
* Edge extension
* SaaS dashboard
* Team management
* Enterprise APIs

---

# 🎯 Mission

AI Phishing Shield aims to evolve beyond traditional phishing detection and become a complete phishing intelligence platform capable of identifying phishing campaigns, brand impersonation attacks, malicious infrastructure, and emerging threats before users become victims.

---

# 👨‍💻 Author

Rohith V

---

# ⚠️ Disclaimer

This software is intended for cybersecurity research, phishing analysis, browser security testing, and defensive security applications.

Always use responsibly and ethically.
