document.addEventListener("DOMContentLoaded", async () => {
    const resultDiv = document.getElementById("result");

    try {
        // Get current active tab
        const [tab] = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        const currentUrl = tab.url;

        resultDiv.innerHTML = `
            <p><strong>Scanning URL:</strong></p>
            <p>${currentUrl}</p>
            <p>Checking with AI engine...</p>
        `;

        // Call FastAPI backend
        const response = await fetch(
            `http://localhost:8080/predict?url=${encodeURIComponent(currentUrl)}`
        );

        const data = await response.json();

        // Display result
        resultDiv.innerHTML = `
            <h2>${data.prediction.toUpperCase()}</h2>
            <p><strong>Risk Level:</strong> ${data.risk_level}</p>
            <p><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(2)}%</p>
            <p><strong>Risk Score:</strong> ${data.risk_score}</p>
            <hr>
            <h3>Reasons:</h3>
            <ul>
                ${data.reasons.map(reason => `<li>${reason}</li>`).join("")}
            </ul>
        `;

        // Color coding
        if (data.prediction === "malicious") {
            resultDiv.style.color = "red";
        } else {
            resultDiv.style.color = "lime";
        }

    } catch (error) {
        console.error(error);

        resultDiv.innerHTML = `
            <h2>ERROR</h2>
            <p>Could not connect to backend.</p>
        `;

        resultDiv.style.color = "orange";
    }
});