async function checkURL() {

    const [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true
    });

    const url = tab.url;

    document.getElementById("url").innerText = url;

    try {

        const response = await fetch(
            `http://127.0.0.1:8000/predict?url=${encodeURIComponent(url)}`,
            {
                method: "POST"
            }
        );

        const data = await response.json();

        const resultDiv = document.getElementById("result");

        const riskLevel = data.risk_level || "UNKNOWN";
        const riskScore = data.risk_score || 0;
        const confidence = (data.confidence * 100).toFixed(2);

        let color = "#22c55e";

        if (riskLevel === "MEDIUM") color = "#f59e0b";
        if (riskLevel === "HIGH") color = "#ef4444";
        if (riskLevel === "CRITICAL") color = "#dc2626";

        let reasonsHTML = "";

        if (data.reasons && data.reasons.length > 0) {

            reasonsHTML = `
                <div class="reasons">
                    <h4>Threat Indicators</h4>
                    <ul>
                        ${data.reasons.map(r => `<li>${r}</li>`).join("")}
                    </ul>
                </div>
            `;
        }

        resultDiv.innerHTML = `
            <div class="card">

                <h2 style="color:${color}">
                    ${data.prediction === "malicious"
                        ? "⚠️ Malicious Website"
                        : "✅ Safe Website"}
                </h2>

                <div class="score-box">

                    <div class="score">
                        <span>Threat Score</span>
                        <strong>${riskScore}/100</strong>
                    </div>

                    <div class="score">
                        <span>Risk Level</span>
                        <strong style="color:${color}">
                            ${riskLevel}
                        </strong>
                    </div>

                </div>

                <p>
                    Confidence:
                    <strong>${confidence}%</strong>
                </p>

                ${reasonsHTML}

            </div>
        `;

    } catch (err) {

        document.getElementById("result").innerHTML = `
            <div class="card">
                <h2 style="color:red;">Backend Offline</h2>
                <p>Make sure FastAPI server is running.</p>
            </div>
        `;
    }
}

checkURL();