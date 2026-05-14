# 🛡️ AI Phishing Shield

AI Phishing Shield is an AI-powered real-time browser security platform designed to detect, block, and analyze phishing and malicious websites directly inside the browser.

The platform combines:
- Real-time browser monitoring
- AI-driven phishing detection
- Intelligent threat scoring
- Automatic website blocking
- Local caching for instant repeat detection
- Threat telemetry and analytics

Built using:
- FastAPI
- Chrome Extension (Manifest V3)
- Machine Learning
- Deep Learning
- DistilBERT
- Random Forest
- LightGBM
- PostgreSQL
- Streamlit

---

# 🚀 Product Vision

AI Phishing Shield is being developed as a modern AI-powered browser cybersecurity platform capable of evolving into a full-scale browser protection and threat intelligence ecosystem.

The long-term goal is to provide:

- Real-time phishing protection
- Intelligent browser defense
- AI-based threat analysis
- Browser-native cyber protection
- Threat intelligence infrastructure
- Enterprise-grade web security

---

# 🔥 Current Core Features

# ✅ Real-Time Browser Protection

- Live website monitoring
- Real-time phishing detection
- Automatic malicious website blocking
- Browser-native protection engine

---

# ✅ Automatic Phishing Blocking

When a malicious website is detected:

- Website access is blocked instantly
- User is redirected to a warning screen
- Risk score and threat details are displayed

---

# ✅ Browser Badge Detection System

The extension provides instant visual indicators:

| Badge | Meaning |
|------|------|
| SAFE | Website is safe |
| BAD | Website is malicious |
| ERR | Backend/API issue |

---

# ✅ Intelligent Local Cache System

AI Phishing Shield includes a browser-side cache engine:

- First scan → backend analysis
- Repeated scan → instant cached detection
- Reduced backend requests
- Faster browsing experience
- Lower latency protection

---

# ✅ Threat History Dashboard

The popup dashboard stores:

- Recent malicious detections
- Threat scores
- Detection timestamps
- Historical phishing activity

---

# ✅ Risk Intelligence Engine

Current threat analysis includes:

- Suspicious keyword analysis
- URL structure analysis
- Entropy-based detection
- Suspicious TLD analysis
- Typosquatting indicators
- Risk score calculation
- Confidence scoring

---

# 🧠 Current Detection Pipeline

```text
URL
 ↓
Feature Extraction
 ↓
Threat Intelligence Analysis
 ↓
ML Risk Engine
 ↓
Risk Score Calculation
 ↓
Prediction Response
 ↓
Automatic Browser Blocking
```

---

# 🧠 Upcoming Hybrid AI Engine

The next-generation detection pipeline will combine:

```text
Manual URL Features
        +
Traditional Machine Learning
        +
DistilBERT Semantic Analysis
        +
Hybrid Risk Fusion
        =
Final Prediction
```

This hybrid AI architecture is designed to improve:

- Semantic phishing detection
- Zero-day phishing detection
- Obfuscated URL analysis
- AI-generated phishing detection
- Context-aware threat analysis

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
ML / Hybrid AI Engine
   ↓
Risk Analysis
   ↓
Automatic Blocking
```

---

# 🧱 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend & ML |
| FastAPI | Real-time inference API |
| JavaScript | Chrome extension |
| HTML/CSS | Browser UI |
| Random Forest | ML classification |
| LightGBM | Advanced boosting |
| DistilBERT | Semantic URL analysis |
| Streamlit | Threat analytics dashboard |
| PostgreSQL | Threat telemetry storage |
| Supabase | Managed cloud database |
| Docker | Containerized deployment |

---

# 🛡️ Browser Extension Features

## ✅ Real-Time URL Monitoring

The extension monitors tabs in real time and scans newly opened websites automatically.

---

## ✅ Full-Page Blocking UI

Malicious websites are replaced with a custom phishing warning page containing:

- Threat level
- Risk score
- Confidence score
- Website information
- Safety navigation controls

---

## ✅ Popup Threat Dashboard

The popup interface displays:

- Prediction result
- Risk level
- Confidence score
- Threat indicators
- Recent phishing history

---

## ✅ Local Threat Storage

Using:

```text
chrome.storage.local
```

the extension stores:

- Cached detections
- Threat history
- Recent phishing activity

---

# 📂 Project Structure

```text
ai-phishing-shield/
│
├── chrome-extension/
│   ├── manifest.json
│   ├── background.js
│   ├── popup.html
│   ├── popup.js
│   ├── blocked.html
│   ├── blocked.js
│   └── styles/
│
├── models/
│   ├── rf_model.pkl
│   ├── lgb_model.pkl
│   ├── distilbert/
│   └── scaler.pkl
│
├── utils/
│   ├── features.py
│   ├── intelligence.py
│   ├── explain.py
│   └── database.py
│
├── dashboard/
│   └── dashboard.py
│
├── assets/
│   ├── popup.png
│   ├── blocker.png
│   └── dashboard.png
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── README.md
└── .gitignore
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

Activate:

## Linux/macOS

```bash
source venv/bin/activate
```

## Windows

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
DATABASE_URL=YOUR_DATABASE_URL
```

---

# 5️⃣ Run Backend

## Local

```bash
uvicorn app:app --reload
```

---

## Docker

```bash
sudo docker build -t phishing-api .

sudo docker run --env-file .env -p 8080:8080 phishing-api
```

---

# 6️⃣ Load Chrome Extension

1. Open Chrome

2. Go to:

```text
chrome://extensions
```

3. Enable Developer Mode

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
https://microsoft.com
https://amazon.com
```

---

# ⚠️ Phishing Test URLs

```text
http://paypal-login-secure.xyz
http://gooogle-login.xyz
http://paypa1-secure-login.top
http://micr0soft-authentication.xyz
http://google.security-check-login.com
```

---

# 📸 Screenshots

## 🔹 Extension Popup

![Popup](assets/popup.png)

---

## 🔹 Full-Page Phishing Blocker

![Blocker](assets/blocker.png)

---

## 🔹 Threat Dashboard

![Dashboard](assets/dashboard.png)

---

# 📈 Current Product Status

# ✅ Completed

## Phase 1 — Core Detection Engine

- Real-time phishing detection
- FastAPI backend
- Browser extension integration
- ML risk engine

---

## Phase 2 — Browser Protection Layer

- Full-page phishing blocker
- Browser badge system
- Real-time tab monitoring
- Popup threat dashboard

---

## Phase 3 — Performance Optimization

- Local cache system
- Instant repeat detection
- Reduced backend requests
- Faster response pipeline

---

## Phase 4 — Threat Intelligence Layer

- Suspicious TLD analysis
- URL structure analysis
- Risk scoring engine
- Threat indicators

---

# 🚀 Upcoming Roadmap

# 🔜 Hybrid AI Engine

- DistilBERT integration
- Feature fusion architecture
- Hybrid risk scoring
- Semantic phishing detection

---

# 🔜 Advanced Browser Protection

- Cache expiry system
- Search-result threat warnings
- Live page-content analysis
- Fake login detection

---

# 🔜 Threat Intelligence Expansion

- WHOIS analysis
- SSL certificate analysis
- Domain reputation analysis
- Community threat reporting

---

# 🔜 Multi-Modal Detection

- Screenshot analysis
- Logo impersonation detection
- OCR-based phishing detection
- Visual similarity analysis

---

# 🔜 Enterprise Expansion

- Multi-browser support
- Threat telemetry platform
- Enterprise dashboard
- Organization-wide protection

---

# 🎯 Product Goal

AI Phishing Shield aims to evolve into:

```text
AI-powered browser security platform
```

capable of providing:

- Real-time phishing protection
- AI-driven threat analysis
- Browser-native cyber defense
- Intelligent phishing prevention
- Threat intelligence infrastructure

---

# 👨‍💻 Author

## Rohith V

---

# ⭐ Support

If you found this project useful:

- Give it a ⭐ on GitHub
- Share feedback
- Contribute improvements
