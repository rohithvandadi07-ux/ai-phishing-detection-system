# 🛡️ AI Phishing Shield

AI Phishing Shield is an AI-powered browser cybersecurity platform designed to detect, analyze, score, and block phishing and malicious websites in real time.

The platform combines:

* Real-time browser monitoring
* Hybrid AI phishing detection
* Semantic URL analysis
* Threat intelligence engines
* Browser-native protection
* Automated risk scoring
* Full-page phishing blocking
* Cloud-based telemetry
* Modular AI microservices

AI Phishing Shield is being developed as a startup-grade cybersecurity product focused on modern browser protection against phishing, scam, spoofing, malicious redirects, and zero-day URL threats.

---

# 🚀 Vision

AI Phishing Shield aims to evolve into a:

```text
Next-generation AI-powered browser security platform
```

capable of providing:

* Real-time phishing prevention
* AI-driven browser protection
* Zero-day phishing detection
* Semantic threat analysis
* Browser-native cyber defense
* Enterprise threat intelligence
* Cloud-based telemetry infrastructure

---

# 🔥 Current Product Capabilities

## ✅ Real-Time URL Scanning

The browser extension monitors websites in real time and automatically scans newly opened URLs.

Features:

* Instant URL scanning
* Background tab monitoring
* Real-time prediction engine
* Browser-native protection

---

## ✅ Hybrid AI Detection Engine

The platform uses a multi-layer hybrid AI architecture.

Current detection stack:

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
Risk Fusion Engine
        =
Final Prediction
```

---

## ✅ Semantic Phishing Detection

DistilBERT-based semantic analysis is used to detect:

* Obfuscated phishing URLs
* AI-generated phishing links
* Brand impersonation
* Contextual phishing structures
* Suspicious semantic patterns

---

## ✅ Browser-Native Phishing Blocking

When a malicious website is detected:

* Access is blocked automatically
* User is redirected to a phishing warning page
* Risk level and threat score are displayed
* Confidence score is shown

---

## ✅ Intelligent Risk Scoring System

AI Phishing Shield calculates:

* Threat confidence
* Risk score
* Risk level
* Detection indicators
* Threat explanations

Risk Levels:

| Risk Score | Level    |
| ---------- | -------- |
| 0–34       | SAFE     |
| 35–59      | MEDIUM   |
| 60–79      | HIGH     |
| 80–100     | CRITICAL |

---

## ✅ Threat Intelligence Layer

Current threat analysis includes:

* Suspicious keyword analysis
* Entropy analysis
* URL structure analysis
* Suspicious TLD analysis
* Typosquatting detection
* WHOIS intelligence
* Reputation analysis
* Domain intelligence
* VirusTotal scanning
* PhishTank verification

---

## ✅ Browser Badge Detection System

The extension provides real-time visual indicators.

| Badge | Meaning              |
| ----- | -------------------- |
| SAFE  | Website is safe      |
| BAD   | Website is malicious |
| ERR   | Backend/API issue    |

---

## ✅ Intelligent Cache Engine

AI Phishing Shield includes a local caching system.

Benefits:

* Faster repeat detection
* Reduced backend requests
* Lower latency
* Improved performance
* Instant cached predictions

---

## ✅ Detection History Dashboard

The extension dashboard stores:

* Recent detections
* Threat scores
* Detection timestamps
* Historical phishing activity
* Cached threat intelligence

---

# 🧠 Current AI Detection Pipeline

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

| Technology    | Purpose                       |
| ------------- | ----------------------------- |
| Python        | Backend & AI                  |
| FastAPI       | Real-time inference API       |
| JavaScript    | Browser extension             |
| HTML/CSS      | Extension UI                  |
| Random Forest | ML classification             |
| LightGBM      | Boosting engine               |
| DistilBERT    | Semantic phishing analysis    |
| PostgreSQL    | Threat telemetry database     |
| Supabase      | Cloud database infrastructure |
| Docker        | Containerized deployment      |
| Streamlit     | Analytics dashboard           |
| SQLAlchemy    | ORM/database layer            |

---

# 📂 Current Project Structure

```text
phishing-detector/
│
├── app/
│   ├── core/
│   ├── database/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── chrome-extension/
├── models/
├── logs/
├── assets/
├── Dockerfile
├── requirements.txt
├── frontend.py
├── dashboard.py
├── render.yaml
├── runtime.txt
├── README.md
└── .env
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
DATABASE_URL=YOUR_SUPABASE_DATABASE_URL
```

Example:

```env
DATABASE_URL=postgresql://postgres.xxxxx:[PASSWORD]@aws-1-ap-south-1.pooler.supabase.com:6543/postgres
```

---

## 5️⃣ Run Backend

### Local Development

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

## 6️⃣ Docker Deployment

### Build Docker Image

```bash
sudo docker build --no-cache -t phishing-api .
```

### Run Docker Container

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

## 7️⃣ Load Chrome Extension

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

## ✅ Safe URLs

```text
https://google.com
https://github.com
https://amazon.com
https://microsoft.com
```

---

## ⚠️ Test Phishing URLs

```text
http://paypal-login-secure.xyz
http://gooogle-login.xyz
http://paypa1-verification.top
http://micr0soft-authentication.xyz
http://google.security-check-login.com
```

---

# 📡 API Endpoints

## GET /

Health home route.

---

## GET /health

Returns backend health status.

---

## POST /predict

Scans URL for phishing detection.

Example Request:

```json
{
  "url": "http://paypal-login-secure.xyz"
}
```

---

# 📸 Product Screenshots

## 🔹 Browser Popup

![Popup](assets/popup.png)

---

## 🔹 Phishing Block Page

![Blocker](assets/blocker.png)

---

## 🔹 Threat Dashboard

![Dashboard](assets/dashboard.png)

---

# 📈 Current Development Status

## ✅ Completed

### Phase 1 — Core AI Backend

* FastAPI backend
* Modular architecture
* Hybrid AI engine
* Semantic AI integration
* Risk scoring system

---

### Phase 2 — Browser Protection Layer

* Chrome extension
* Real-time scanning
* Browser blocking
* Badge detection system
* Popup dashboard

---

### Phase 3 — Threat Intelligence

* WHOIS analysis
* Reputation engine
* Domain intelligence
* VirusTotal integration
* PhishTank integration

---

### Phase 4 — Infrastructure

* Docker deployment
* Supabase integration
* Cloud database support
* Logging system
* Cache engine

---

# 🚀 Upcoming Roadmap

## 🔜 AI Improvements

* CNN phishing detection
* Transformer fine-tuning
* Zero-day adaptive learning
* Ensemble optimization

---

## 🔜 Browser Security Expansion

* Fake login page detection
* DOM analysis
* OCR phishing analysis
* Search-result warnings

---

## 🔜 Threat Intelligence Expansion

* SSL certificate intelligence
* DNS intelligence
* Community threat feeds
* Threat telemetry platform

---

## 🔜 SaaS Infrastructure

* User authentication
* API key system
* Usage analytics
* Subscription plans
* Multi-user dashboard

---

## 🔜 Enterprise Platform

* Organization-wide protection
* Threat analytics portal
* Multi-browser support
* Enterprise telemetry

---

# 🎯 Product Goal

AI Phishing Shield is being built as a:

```text
Production-grade AI browser cybersecurity platform
```

focused on:

* Real-time phishing prevention
* Browser-native cyber defense
* AI-powered threat intelligence
* Hybrid phishing detection
* Modern web security

---

# 👨‍💻 Author

## Rohith V

---

# ⭐ Support

If you found this project useful:

* Star the repository
* Share feedback
* Suggest improvements
* Contribute to development
