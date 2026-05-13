document.addEventListener("DOMContentLoaded", async () => {

    const resultDiv = document.getElementById("result");

    const historyDiv = document.getElementById("history");

    try {

        // ---------------------------------------------------
        // GET ACTIVE TAB
        // ---------------------------------------------------

        const [tab] = await chrome.tabs.query({

            active: true,
            currentWindow: true
        });

        const currentUrl = tab.url;

        // ---------------------------------------------------
        // HANDLE BLOCKED PAGE URL
        // ---------------------------------------------------

        let originalUrl = currentUrl;

        if (currentUrl.includes("blocked.html")) {

            const params =
                new URL(currentUrl).searchParams;

            originalUrl = params.get("url");
        }

        // ---------------------------------------------------
        // GET CACHED RESULT
        // ---------------------------------------------------

        const cacheKey = `scan_${originalUrl}`;

        const result =
            await chrome.storage.local.get([cacheKey]);

        const data = result[cacheKey];

        // ---------------------------------------------------
        // NO DATA
        // ---------------------------------------------------

        if (!data) {

            resultDiv.innerHTML = `
                <h2 class="warning">NO DATA</h2>
                <p>No scan result found.</p>
            `;

            return;
        }

        // ---------------------------------------------------
        // SHOW RESULT
        // ---------------------------------------------------

        resultDiv.innerHTML = `
            <h2 class="${data.prediction === "malicious"
                ? "danger"
                : "safe"}">

                ${data.prediction.toUpperCase()}

            </h2>

            <p><strong>URL:</strong></p>

            <p>${originalUrl}</p>

            <p><strong>Risk Level:</strong>
                ${data.risk_level}
            </p>

            <p><strong>Confidence:</strong>
                ${(data.confidence * 100).toFixed(2)}%
            </p>

            <p><strong>Risk Score:</strong>
                ${data.risk_score}
            </p>

            <hr>

            <h3>Reasons:</h3>

            <ul>
                ${data.reasons.map(
                    reason => `<li>${reason}</li>`
                ).join("")}
            </ul>
        `;

        // ---------------------------------------------------
        // LOAD HISTORY
        // ---------------------------------------------------

        chrome.storage.local.get(
            ["phishingHistory"],
            (historyResult) => {

                const history =
                    historyResult.phishingHistory || [];

                if (history.length === 0) {

                    historyDiv.innerHTML = `
                        <p class="warning">
                            No threats detected yet.
                        </p>
                    `;

                    return;
                }

                historyDiv.innerHTML = "";

                history.slice(0, 5).forEach((item) => {

                    const div =
                        document.createElement("div");

                    div.className = "history-item";

                    div.innerHTML = `
                        <div class="history-url">
                            ${item.url}
                        </div>

                        <div class="history-risk">
                            Risk Score: ${item.score}
                        </div>

                        <div class="history-time">
                            ${item.time}
                        </div>
                    `;

                    historyDiv.appendChild(div);
                });
            }
        );

    } catch (error) {

        console.error(error);

        resultDiv.innerHTML = `
            <h2 class="warning">ERROR</h2>

            <p>Popup failed to load.</p>
        `;
    }
});