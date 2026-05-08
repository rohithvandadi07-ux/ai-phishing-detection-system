# 🛡️ AI-Powered Real-Time Phishing Detection System

A real-time phishing detection and automatic website blocking system built using **Machine Learning, FastAPI, Streamlit, and a Chrome Extension**.

This project analyzes URLs in real-time, detects phishing behavior, calculates threat levels, and automatically blocks malicious websites directly inside the browser.

---

# 🚀 Features

* 🧠 Machine Learning-based phishing detection using LightGBM
* ⚡ FastAPI backend for real-time inference
* 🌐 Chrome Extension for live URL monitoring
* 🚫 Automatic phishing website blocking
* 📊 Confidence score with phishing explanation
* 🖥️ Streamlit dashboard for manual URL testing
* 🔒 Safe-domain whitelist support
* 🧩 Modular architecture for future AI upgrades
* 🛡️ Typosquatting detection
* 🎯 Brand impersonation detection
* 🌍 Suspicious TLD detection
* ⚠️ Real-time phishing warning system

---

# 🛡️ AI Threat Intelligence

The extension now includes advanced phishing intelligence techniques similar to real-world browser security systems.

## ✅ Detection Capabilities

* Detects fake brand impersonation
* Detects suspicious phishing domains
* Detects typo-based attacks
* Detects dangerous phishing TLDs
* Blocks malicious pages automatically

---

## 🔥 Example Detections

```text
http://paypal-login-secure.xyz
http://gooogle-login.xyz
http://paypa1-secure-login.top
http://micr0soft-authentication.xyz
```

---

# 🧱 Tech Stack

| Technology   | Purpose                         |
| ------------ | ------------------------------- |
| Python       | Core backend                    |
| FastAPI      | Real-time prediction API        |
| LightGBM     | ML phishing classifier          |
| Scikit-learn | Feature scaling & preprocessing |
| Streamlit    | Frontend testing dashboard      |
| JavaScript   | Chrome extension logic          |
| HTML/CSS     | Extension UI & blocker page     |

---

# 🧠 System Architecture

```text
Browser
   ↓
Chrome Extension
   ↓
FastAPI Backend
   ↓
Feature Extraction
   ↓
Threat Intelligence Engine
   ↓
LightGBM Model
   ↓
Prediction Response
   ↓
Popup Warning / Auto Block
```

---

# 📂 Project Structure

```text
ai-phishing-detection-system/
│
├── chrome-extension/
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   ├── content.js
│   ├── blocked.html
│   └── blocked.js
│
├── models/
│   ├── lgb_model_small.pkl
│   └── scaler.pkl
│
├── utils/
│   ├── features.py
│   └── explain.py
│
├── assets/
│   ├── popup.png
│   ├── blocker.png
│   └── dashboard.png
│
├── app.py
├── frontend.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 📸 Screenshots

## 🔹 Chrome Extension Popup

![Popup](assets/popup.png)

---

## 🔹 Automatic Phishing Blocker

![Blocker](assets/blocker.png)

---

## 🔹 Streamlit Dashboard

![Dashboard](assets/dashboard.png)

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/rohithvandadi07-ux/ai-phishing-detection-system.git
cd ai-phishing-detection-system
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Run FastAPI Backend

```bash
python3 -m uvicorn app:app --reload
```

FastAPI will start on:

```text
http://127.0.0.1:8000
```

---

## 4️⃣ Run Streamlit Dashboard (Optional)

```bash
streamlit run frontend.py
```

Streamlit dashboard:

```text
http://localhost:8501
```

---

## 5️⃣ Load Chrome Extension

1. Open Chrome
2. Go to:

```text
chrome://extensions
```

3. Enable **Developer Mode**
4. Click **Load unpacked**
5. Select the `chrome-extension/` folder

---

# 🧪 Example URLs for Testing

## ✅ Safe URLs

```text
https://google.com
https://github.com
https://microsoft.com
https://amazon.com
```

---

## ⚠️ Suspicious URLs

```text
http://paypal-login-secure.xyz
http://verify-amazon-login.free
http://google.security-check-login.com
http://gooogle-login.xyz
http://paypa1-secure-login.top
http://micr0soft-authentication.xyz
```

---

# ⚠️ Current Limitations

* Uses feature-based ML detection currently
* Runs on local FastAPI backend
* No cloud deployment yet
* WHOIS analysis not added yet
* SSL verification not added yet
* No threat intelligence feeds yet
* No caching layer implemented

---

# 🚀 Future Roadmap

## ✅ Phase 1 — Core Detection System

* ML phishing detection
* FastAPI backend
* Streamlit dashboard
* Chrome extension popup

---

## ✅ Phase 2 — Automatic Blocking Engine

* Real-time website monitoring
* Automatic phishing page blocking
* Custom phishing warning screen

---

## ✅ Phase 3 — AI Threat Intelligence

* Brand impersonation detection
* Typosquatting detection
* Suspicious TLD analysis

---

## 🔜 Phase 4 — Advanced Risk Engine

* Threat score calculation
* Risk severity levels
* Intelligent blocking rules

---

## 🔜 Phase 5 — External Threat Intelligence

* VirusTotal API integration
* PhishTank integration
* URL reputation analysis

---

## 🔜 Phase 6 — Domain Intelligence

* SSL certificate analysis
* WHOIS/domain-age analysis
* Registrar intelligence

---

## 🔜 Phase 7 — Deep Learning Upgrade

* DistilBERT URL analysis
* Hybrid ML + DL model
* Zero-day phishing detection

---

## 🔜 Phase 8 — Performance Optimization

* Caching system
* Faster inference
* Async scanning engine

---

## 🔜 Phase 9 — Cloud Deployment

* Deploy FastAPI publicly
* Remote inference server
* Global accessibility

---

## 🔜 Phase 10 — Browser Extension Release

* Chrome Web Store deployment
* Auto updates
* Extension packaging

---

## 🔜 Phase 11 — Enterprise Security Dashboard

* Threat analytics
* Detection logs
* Security reports
* Admin monitoring panel

---

## 🔜 Phase 12 — Startup-Grade Security Platform

* Multi-browser support
* Real-time telemetry
* AI behavioral detection
* Enterprise SaaS platform

---

# 👨‍💻 Author

## Rohith V

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
