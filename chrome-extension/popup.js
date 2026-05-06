const urlText = document.getElementById("url");
const resultDiv = document.getElementById("result");

// Get current tab URL
chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    const currentUrl = tabs[0].url;
    urlText.textContent = currentUrl;

    checkURL(currentUrl);
});

function checkURL(url) {
    fetch(`http://127.0.0.1:8000/predict?url=${encodeURIComponent(url)}`, {
        method: "POST"
    })
    .then(res => res.json())
    .then(data => displayResult(data))
    .catch(() => {
        resultDiv.innerHTML = "❌ API not reachable";
    });
}

function displayResult(data) {
    resultDiv.innerHTML = "";

    const div = document.createElement("div");

    if (data.prediction === "malicious") {
        div.classList.add("malicious");
        div.innerHTML = `
            ⚠️ Malicious URL <br>
            Confidence: ${data.confidence.toFixed(4)}<br>
            ${data.why_flagged.join("<br>")}
        `;
    } else {
        div.classList.add("safe");
        div.innerHTML = `
            ✅ Safe URL <br>
            Confidence: ${data.confidence.toFixed(4)}
        `;
    }

    resultDiv.appendChild(div);
}