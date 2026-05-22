# 🛡️ AI Phishing Shield

> AI-powered real-time browser phishing detection and prevention platform.

AI Phishing Shield is a production-grade cybersecurity platform designed to detect, analyze, score, and block phishing and malicious websites in real time using hybrid Artificial Intelligence and browser-native protection systems.

The platform combines:

- Hybrid AI phishing detection
- Semantic URL intelligence
- Real-time browser monitoring
- Threat intelligence engines
- Browser-native phishing blocking
- Risk scoring systems
- Cloud telemetry
- AI microservices
- Threat history analytics

---

# 🚀 Vision

AI Phishing Shield aims to become a:

```text
Next-generation AI-powered browser cybersecurity platform
```

capable of delivering:

- Real-time phishing prevention
- Zero-day phishing detection
- Browser-native cyber defense
- AI-powered threat intelligence
- Enterprise browser protection
- Cloud-based security telemetry
- Multi-browser phishing defense

---

# 🔥 Core Product Features

# ✅ Real-Time URL Scanning

The browser extension continuously monitors URLs opened by the user and scans them in real time.

### Features

- Instant URL scanning
- Background tab monitoring
- Real-time prediction engine
- Browser-native phishing protection
- Intelligent phishing blocking

---

# ✅ Hybrid AI Detection Engine

AI Phishing Shield uses a layered hybrid AI architecture.

## Current Detection Stack

```text
Manual Feature Extraction
        +
Random Forest
        +
LightGBM
        +
DistilBERT Semantic AI
        +
Threat Intelligence
        +
Fusion Risk Engine
        =
Final Prediction
```

---

# ✅ Semantic Phishing Detection

DistilBERT semantic analysis detects:

- Obfuscated phishing URLs
- AI-generated phishing links
- Brand impersonation
- Contextual phishing structures
- Suspicious semantic patterns
- Semantic phishing indicators

---

# ✅ Browser-Native Phishing Blocking

When a malicious website is detected:

- Website access is blocked
- User is redirected to a warning page
- Threat explanations are shown
- Risk score is displayed
- Confidence score is displayed

---

# ✅ Intelligent Risk Scoring System

The platform calculates:

- Threat confidence
- Risk score
- Risk level
- Threat explanations
- Detection indicators

## Risk Levels

| Risk Score | Level |
|---|---|
| 0–34 | SAFE |
| 35–59 | MEDIUM |
| 60–79 | HIGH |
| 80–100 | CRITICAL |

---

# ✅ Threat Intelligence Layer

Current intelligence features include:

- Suspicious keyword analysis
- Entropy analysis
- URL structure analysis
- Suspicious TLD analysis
- Typosquatting detection
- WHOIS intelligence
- Domain intelligence
- Reputation analysis
- VirusTotal scanning
- PhishTank verification

---

# ✅ Browser Badge Detection System

The extension provides real-time badge indicators.

| Badge | Meaning |
|---|---|
| SAFE | Website is safe |
| BAD | Website is malicious |
| ERR | Backend/API issue |

---

# ✅ Intelligent Cache Engine

AI Phishing Shield includes local threat caching.

## Benefits

- Faster repeated scans
- Lower latency
- Reduced backend requests
- Better extension performance
- Instant cached predictions

---

# ✅ Detection History Dashboard

The dashboard stores:

- Threat history
- Scan timestamps
- Threat confidence
- Risk scores
- Historical phishing activity
- Cached threat intelligence

---

# 🧠 AI Detection Pipeline

```text
URL
 ↓
Feature Extraction
 ↓
Threat Intelligence
 ↓
Hybrid AI Models
 ↓
Semantic Analysis
 ↓
Fusion Risk Engine
 ↓
Risk Score Calculation
 ↓
Prediction Response
 ↓
Automatic Browser Blocking
```

---

# 🌐 System Architecture

```text
Browser
   ↓
Chrome Extension
   ↓
Background Scanner
   ↓
Local Cache Engine
   ↓
FastAPI Backend
   ↓
Threat Intelligence Layer
   ↓
Hybrid AI Engine
   ↓
Risk Fusion System
   ↓
Final Prediction
   ↓
Automatic Website Blocking
```

---

# 🧱 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend & AI |
| FastAPI | Real-time inference API |
| JavaScript | Browser extension |
| HTML/CSS | Extension UI |
| Random Forest | ML classification |
| LightGBM | Boosting engine |
| DistilBERT | Semantic phishing analysis |
| PostgreSQL | Threat telemetry database |
| Supabase | Cloud database infrastructure |
| Docker | Containerized deployment |
| SQLAlchemy | ORM/database layer |
| Streamlit | Threat analytics dashboard |

---

# 📂 Current Project Structure

```text
phishing-detector/
│
├── app/
│   ├── auth/
│   ├── core/
│   ├── database/
│   ├── middleware/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── chrome-extension/
│
├── models/
├── logs/
├── assets/
│
├── Dockerfile
├── requirements.txt
├── dashboard.py
├── frontend.py
├── render.yaml
├── runtime.txt
├── README.md
└── .env
```

---

# ⚙️ Installation & Setup

# 1️⃣ Clone Repository

```bash
git clone https://github.com/rohithvandadi07-ux/ai-phishing-detection-system.git

cd ai-phishing-detection-system
```

---

# 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
```

## Activate Environment

### Linux/macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

# 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 4️⃣ Configure Environment Variables

Create `.env`

```env
DATABASE_URL=YOUR_SUPABASE_DATABASE_URL

SECRET_KEY=YOUR_SECRET_KEY

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

VIRUSTOTAL_API_KEY=YOUR_VT_KEY

PHISHTANK_API_KEY=YOUR_PHISHTANK_KEY
```

---

# 5️⃣ Run Backend Locally

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

# 6️⃣ Docker Deployment

## Build Docker Image

```bash
sudo docker build --no-cache -t phishing-api .
```

## Run Docker Container

```bash
sudo docker run --env-file .env -p 8080:8080 phishing-api
```

Backend:

```text
http://localhost:8080
```

Swagger Docs:

```text
http://localhost:8080/docs
```

---

# 7️⃣ Load Chrome Extension

1. Open Chrome

2. Navigate to:

```text
chrome://extensions
```

3. Enable:

```text
Developer Mode
```

4. Click:

```text
Load unpacked
```

5. Select:

```text
chrome-extension/
```

---

# 🧪 Example URLs

# ✅ Safe URLs

```text
https://google.com
https://github.com
https://amazon.com
https://microsoft.com
```

---

# ⚠️ Test Phishing URLs

```text
http://paypal-login-secure.xyz
http://gooogle-login.xyz
http://paypa1-verification.top
http://micr0soft-authentication.xyz
http://google.security-check-login.com
```

---

# 📡 API Endpoints

# Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register user |
| POST | `/auth/login` | Login user |

---

# Prediction APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/predict` | Scan URL |
| GET | `/health` | Health check |
| GET | `/` | Home route |

---

# User APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/user/me` | Current user profile |
| GET | `/user/history` | Scan history |
| GET | `/user/usage` | Usage analytics |

---

# Example Prediction Request

```json
{
  "url": "http://paypal-login-secure.xyz"
}
```

---

# 📸 Product Screenshots

# 🔹 Browser Popup

![Popup](assets/popup.png)

---

# 🔹 Phishing Block Page

![Blocker](assets/blocker.png)

---

# 🔹 Threat Dashboard

![Dashboard](assets/dashboard.png)

---

# 📈 Current Development Status

# ✅ Phase 1 — Core AI Backend

Completed:

- FastAPI backend
- Modular architecture
- JWT authentication
- API key system
- Hybrid AI engine
- Semantic AI integration
- Risk scoring system
- Threat intelligence integration

---

# ✅ Phase 2 — Browser Protection Layer

Completed:

- Chrome extension
- Real-time scanning
- Browser phishing blocking
- Badge detection system
- Popup dashboard
- Local cache engine

---

# ✅ Phase 3 — Threat Intelligence

Completed:

- WHOIS analysis
- Reputation engine
- Domain intelligence
- VirusTotal integration
- PhishTank integration

---

# ✅ Phase 4 — Infrastructure

Completed:

- Docker deployment
- Supabase integration
- PostgreSQL telemetry
- Logging system
- Authentication system
- Protected APIs

---

# 🚀 Upcoming Roadmap

# 🔜 AI Improvements

- CNN phishing detection
- Transformer fine-tuning
- Adaptive learning systems
- Ensemble optimization
- Zero-day phishing learning

---

# 🔜 Browser Security Expansion

- Fake login page detection
- DOM analysis
- OCR phishing analysis
- Search-result phishing warnings
- Screenshot threat analysis

---

# 🔜 Threat Intelligence Expansion

- SSL intelligence
- DNS intelligence
- Community threat feeds
- Telemetry analytics
- Threat sharing infrastructure

---

# 🔜 SaaS Infrastructure

- Subscription plans
- Usage analytics
- API monetization
- Multi-user dashboard
- Team management

---

# 🔜 Enterprise Platform

- Organization-wide protection
- Threat analytics portal
- Enterprise telemetry
- Multi-browser support
- Centralized policy management

---

# 🎯 Product Goal

AI Phishing Shield is being developed as a:

```text
Production-grade AI browser cybersecurity platform
```

focused on:

- Real-time phishing prevention
- Browser-native cyber defense
- Hybrid AI phishing detection
- AI-powered threat intelligence
- Modern web protection

---

# 👨‍💻 Author

## Rohith V


---

# ⭐ Support

If you found this project useful:

- Star the repository
- Share feedback
- Suggest improvements
- Contribute to development

---

# ⚠️ Disclaimer

AI Phishing Shield is intended for:

- Educational purposes
- Cybersecurity research
- Browser security experimentation
- Threat analysis learning

Always use responsibly and ethically.
