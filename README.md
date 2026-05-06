# 🚀 Real-Time Phishing Detection System

A machine learning-powered phishing detection system with a Chrome extension that **automatically detects and blocks malicious URLs in real-time**.

---

## 🔥 Features

* 🧠 ML-based phishing detection (LightGBM)
* ⚡ FastAPI backend for real-time predictions
* 🌐 Chrome Extension for live URL monitoring
* 🚫 Automatic phishing website blocking
* 📊 Confidence score + explanation
* 🖥️ Streamlit UI for manual testing

---

## 🧱 Tech Stack

* Python
* FastAPI
* LightGBM
* Scikit-learn
* Streamlit
* JavaScript (Chrome Extension)

---

## 🧠 System Architecture

```
Browser → Chrome Extension → FastAPI → ML Model → Response → Block Page
```

---

## 📸 Demo

### 🔹 Safe URL

* Shows "Safe URL"
* Confidence score = 1.0

### 🔹 Malicious URL

* Detects phishing patterns
* Blocks page automatically
* Displays warning screen

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/your-username/ai-phishing-detection-system.git
cd ai-phishing-detection-system
```

---

### 2. Install dependencies

```
pip install -r requirements.txt
```

---

### 3. Run FastAPI server

```
python3 -m uvicorn app:app --reload
```

---

### 4. Run Streamlit (optional)

```
streamlit run frontend.py
```

---

### 5. Load Chrome Extension

* Go to `chrome://extensions`
* Enable **Developer Mode**
* Click **Load unpacked**
* Select `chrome-extension/` folder

---

## ⚠️ Current Limitations

* Uses basic feature-based model (25 features)
* Works with local API (127.0.0.1)
* No caching yet

---

## 🚀 Future Improvements

* 🔥 Deploy API (global usage)
* 🧠 Add DistilBERT / Deep Learning model
* ⚡ Add caching for faster detection
* 🛡️ Advanced phishing detection (WHOIS, SSL)
* 🌍 Publish Chrome Extension

---

## 👨‍💻 Author

Rohith V

---

## ⭐ If you like this project, give it a star!
