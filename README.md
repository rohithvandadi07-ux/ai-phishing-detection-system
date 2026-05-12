# 🛡️ AI Phishing Shield

An AI-powered real-time phishing detection and automatic website blocking platform built using:

- Machine Learning
- Deep Learning
- FastAPI
- Chrome Extension
- Streamlit
- PostgreSQL
- Threat Intelligence Techniques

AI Phishing Shield detects phishing URLs in real time, calculates threat severity, blocks malicious websites automatically, and provides centralized threat analytics through an enterprise-style monitoring dashboard.

---

# 🚀 Product Vision

AI Phishing Shield is designed as a modern browser-security and phishing-protection platform capable of evolving into a full SaaS cybersecurity solution.

The system combines:

- Real-time browser protection
- AI-driven phishing detection
- Threat intelligence analysis
- Centralized telemetry logging
- Enterprise monitoring dashboards

---

# 🔥 Core Features

## ✅ Real-Time Phishing Detection

- Live URL scanning
- AI-powered phishing prediction
- Real-time browser protection
- Automatic phishing website blocking

---

## ✅ Hybrid AI Detection Engine

The platform combines:

- DistilBERT embeddings
- Manual URL feature engineering
- 1D CNN detection
- Random Forest classification
- LightGBM boosting

to create a hybrid phishing-detection pipeline.

---

## ✅ Threat Intelligence Engine

Includes:

- Brand impersonation detection
- Typosquatting detection
- Suspicious TLD analysis
- Risk scoring engine
- Intelligent phishing indicators

---

## ✅ Enterprise Threat Dashboard

Interactive Streamlit dashboard with:

- Threat analytics
- Detection logs
- Risk severity monitoring
- KPI metrics
- Timeline analytics
- Search & filtering
- Centralized telemetry visualization

---

## ✅ Cloud Logging Architecture

Threat detections are stored in:

- Supabase PostgreSQL

Enabling:

- Centralized logging
- Cloud telemetry
- Scalable analytics
- Multi-device support

---

# 🧠 AI Detection Pipeline

```text
URL
 ↓
Feature Extraction
 ↓
DistilBERT Embeddings
 ↓
1D CNN + Random Forest + LightGBM
 ↓
Threat Intelligence Engine
 ↓
Risk Score Calculation
 ↓
Prediction Response
 ↓
Automatic Blocking
```

---

# 🌐 System Architecture

```text
Browser
   ↓
Chrome Extension
   ↓
FastAPI Backend API
   ↓
Hybrid AI Detection Engine
   ↓
Threat Intelligence Layer
   ↓
Supabase PostgreSQL
   ↓
Enterprise Dashboard
```

---

# 🧱 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend & ML |
| FastAPI | Real-time inference API |
| DistilBERT | Semantic URL analysis |
| 1D CNN | Deep learning detection |
| Random Forest | ML classification |
| LightGBM | Advanced boosting classifier |
| Streamlit | Analytics dashboard |
| PostgreSQL | Cloud threat logging |
| Supabase | Managed cloud database |
| JavaScript | Chrome extension |
| HTML/CSS | Extension UI |

---

# 🛡️ Threat Intelligence Capabilities

## ✅ Detection Techniques

- Brand impersonation detection
- Typosquatting detection
- Suspicious TLD analysis
- Keyword-based phishing indicators
- URL structure analysis
- Risk severity calculation
- Threat confidence scoring

---

# 🚫 Automatic Blocking Engine

The Chrome extension:

- Monitors websites in real time
- Sends URLs to FastAPI backend
- Detects malicious websites
- Automatically blocks phishing pages
- Displays phishing warning screen

---

# 📊 Enterprise Dashboard Features

## Dashboard Includes

- Threat analytics
- KPI metrics
- Risk distribution charts
- Detection timeline graphs
- Detection logs
- Search & filtering
- Recent threat feed
- PostgreSQL telemetry integration

---

# 📂 Project Structure

```text
ai-phishing-detection-system/
│
├── chrome-extension/
│   ├── manifest.json
│   ├── background.js
│   ├── popup.html
│   ├── popup.js
│   ├── blocked.html
│   ├── blocked.js
│   └── icons/
│
├── models/
│   ├── lgb_model.pkl
│   ├── rf_model.pkl
│   ├── cnn_model.h5
│   ├── scaler.pkl
│   └── tokenizer/
│
├── utils/
│   ├── features.py
│   ├── explain.py
│   ├── database.py
│   └── intelligence.py
│
├── logs/
│   └── detections.db
│
├── assets/
│   ├── popup.png
│   ├── blocker.png
│   └── dashboard.png
│
├── app.py
├── dashboard.py
├── requirements.txt
├── README.md
├── .env
└── .gitignore
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/rohithvandadi07-ux/ai-phishing-detection-system.git

cd ai-phishing-detection-system
```

---

## 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
```

Activate:

### Linux/macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create `.env`

```env
DATABASE_URL=YOUR_SUPABASE_POSTGRESQL_URL
```

---

## 5️⃣ Run FastAPI Backend

```bash
uvicorn app:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

## 6️⃣ Run Dashboard

```bash
streamlit run dashboard.py
```

Dashboard:

```text
http://localhost:8501
```

---

## 7️⃣ Load Chrome Extension

1. Open Chrome
2. Go to:

```text
chrome://extensions
```

3. Enable Developer Mode
4. Click Load unpacked
5. Select:

```text
chrome-extension/
```

---

# 🧪 Example URLs For Testing

## ✅ Safe URLs

```text
https://google.com
https://github.com
https://microsoft.com
https://amazon.com
```

---

## ⚠️ Phishing URLs

```text
http://paypal-login-secure.xyz
http://gooogle-login.xyz
http://paypa1-secure-login.top
http://micr0soft-authentication.xyz
http://google.security-check-login.com
```

---

# 📸 Screenshots

## 🔹 Chrome Extension Popup

![Popup](assets/popup.png)

---

## 🔹 Automatic Phishing Blocker

![Blocker](assets/blocker.png)

---

## 🔹 Enterprise Dashboard

![Dashboard](assets/dashboard.png)

---

# 📈 Current Product Status

## ✅ Completed

### Phase 1 — Core Detection System

- ML phishing detection
- FastAPI backend
- Streamlit dashboard
- Chrome extension popup

---

### Phase 2 — Automatic Blocking Engine

- Real-time monitoring
- Automatic phishing blocking
- Custom warning screen

---

### Phase 3 — AI Threat Intelligence

- Brand impersonation detection
- Typosquatting detection
- Suspicious TLD analysis

---

### Phase 4 — Advanced Risk Engine

- Threat score calculation
- Risk severity levels
- Intelligent phishing indicators

---

### Phase 11 — Enterprise Dashboard (Partial)

- Threat analytics
- Detection logs
- KPI monitoring
- PostgreSQL telemetry
- Dashboard analytics

---

# 🚀 Upcoming Roadmap

## 🔜 Phase 5 — External Threat Intelligence

- VirusTotal API integration
- PhishTank integration
- Reputation scoring

---

## 🔜 Phase 6 — Domain Intelligence

- WHOIS analysis
- SSL certificate analysis
- Registrar intelligence
- Domain age analysis

---

## 🔜 Phase 7 — Deep Learning Upgrade

- DistilBERT fine-tuning
- Zero-day phishing detection
- Advanced semantic analysis

---

## 🔜 Phase 8 — Performance Optimization

- Redis caching
- Async scanning engine
- Faster inference pipeline

---

## 🔜 Phase 9 — Cloud Deployment

- Dockerization
- Google Cloud Run deployment
- Production API hosting

---

## 🔜 Phase 10 — Browser Extension Release

- Chrome Web Store release
- Auto updates
- Extension packaging

---

## 🔜 Phase 12 — Startup-Grade Security Platform

- Multi-browser support
- Real-time telemetry
- AI behavioral detection
- Enterprise SaaS architecture

---

# 🎯 Product Goal

AI Phishing Shield aims to evolve into:

```text
AI-powered browser cybersecurity platform
```

capable of providing:

- Real-time phishing protection
- Threat intelligence
- Enterprise telemetry
- Browser security analytics
- AI-driven cyber defense

---

# 👨‍💻 Author

## Rohith V


---

# ⭐ Support

If you found this project useful:

- Give it a ⭐ on GitHub
- Share feedback
- Contribute improvements

---
