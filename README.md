# 🛡️ AI-Powered Real-Time Phishing Detection System

A real-time phishing detection and website blocking system built using **Machine Learning, FastAPI, Streamlit, and a Chrome Extension**.

This project automatically analyzes URLs, detects phishing behavior, and blocks malicious websites directly inside the browser.

---

# 🚀 Features

- 🧠 Machine Learning-based phishing detection using LightGBM
- ⚡ FastAPI backend for real-time inference
- 🌐 Chrome Extension for live URL monitoring
- 🚫 Automatic phishing website blocking
- 📊 Confidence score with phishing explanation
- 🖥️ Streamlit dashboard for manual URL testing
- 🔒 Safe-domain whitelist support
- 🧩 Modular project structure for future upgrades

---

# 🧱 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core backend |
| FastAPI | Real-time prediction API |
| LightGBM | ML phishing classifier |
| Scikit-learn | Feature scaling & preprocessing |
| Streamlit | Frontend testing dashboard |
| JavaScript | Chrome extension logic |
| HTML/CSS | Extension UI & blocker page |

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
```

---

## ⚠️ Suspicious URLs

```text
http://paypal-login-secure.xyz
http://verify-amazon-login.free
http://google.security-check-login.com
```

---

# ⚠️ Current Limitations

- Uses feature-based ML detection only
- Runs on local FastAPI server
- No cloud deployment yet
- No WHOIS or SSL verification currently
- No caching layer implemented

---

# 🚀 Future Roadmap

## Phase 2
- 🔥 Background automatic tab scanning
- ⚡ Real-time monitoring like antivirus

## Phase 3
- 🌐 VirusTotal API integration
- 🛡️ PhishTank integration

## Phase 4
- 🔒 SSL certificate analysis
- 🌍 WHOIS/domain-age analysis
- 🎯 Typosquatting detection

## Phase 5
- 🧠 DistilBERT-based URL analysis
- 🤖 Hybrid Deep Learning model

## Phase 6
- ☁️ Deploy FastAPI backend publicly
- 🌍 Publish Chrome Extension

---

# 👨‍💻 Author

## Rohith V

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
