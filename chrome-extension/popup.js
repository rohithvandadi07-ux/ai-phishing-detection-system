document.addEventListener("DOMContentLoaded", async () => {

    const resultDiv =
        document.getElementById("result");

    const historyDiv =
        document.getElementById("history");

    try {

        // ---------------------------------------------------
        // GET ACTIVE TAB
        // ---------------------------------------------------

        const tabs = await chrome.tabs.query({

            active: true,
            currentWindow: true
        });

        if (!tabs || tabs.length === 0) {

            resultDiv.innerHTML = `
                <h2 class="warning">ERROR</h2>
                <p>No active tab found.</p>
            `;

            return;
        }

        const tab = tabs[0];

        if (!tab.url) {

            resultDiv.innerHTML = `
                <h2 class="warning">ERROR</h2>
                <p>No URL found.</p>
            `;

            return;
        }

        // ---------------------------------------------------
        // HANDLE BLOCKED PAGE
        // ---------------------------------------------------

        let originalUrl = tab.url;

        if (originalUrl.includes("blocked.html")) {

            const params =
                new URL(originalUrl).searchParams;

            originalUrl =
                params.get("url") || originalUrl;
        }

        // ---------------------------------------------------
        // CACHE KEY
        // ---------------------------------------------------

        const cacheKey =
            `scan_${originalUrl}`;

        // ---------------------------------------------------
        // GET CACHE
        // ---------------------------------------------------

        chrome.storage.local.get(

            [cacheKey],

            (result) => {

                try {

                    const data =
                        result[cacheKey];

                    console.log(
                        "Popup Cache:",
                        data
                    );

                    // ---------------------------------------------------
                    // NO DATA
                    // ---------------------------------------------------

                    if (!data) {

                        resultDiv.innerHTML = `
                            <h2 class="warning">
                                NO DATA
                            </h2>

                            <p>
                                No cached scan found.
                            </p>
                        `;

                        return;
                    }

                    // ---------------------------------------------------
                    // SAFE REASONS
                    // ---------------------------------------------------

                    let reasonsHtml =
                        "<li>No reasons available</li>";

                    if (
                        data.reasons &&
                        Array.isArray(data.reasons)
                    ) {

                        reasonsHtml =
                            data.reasons
                                .map(reason =>
                                    `<li>${reason}</li>`
                                )
                                .join("");
                    }

                    // ---------------------------------------------------
                    // SHOW RESULT
                    // ---------------------------------------------------

                    resultDiv.innerHTML = `

                        <h2 class="${
                            data.prediction === "malicious"
                                ? "danger"
                                : "safe"
                        }">

                            ${String(
                                data.prediction || "unknown"
                            ).toUpperCase()}

                        </h2>

                        <p>
                            <strong>URL:</strong>
                        </p>

                        <p>
                            ${originalUrl}
                        </p>

                        <p>
                            <strong>Risk Level:</strong>
                            ${data.risk_level || "UNKNOWN"}
                        </p>

                        <p>
                            <strong>Confidence:</strong>
                            ${(
                                (data.confidence || 0) * 100
                            ).toFixed(2)}%
                        </p>

                        <p>
                            <strong>Risk Score:</strong>
                            ${data.risk_score || 0}
                        </p>

                        <hr>

                        <h3>Reasons:</h3>

                        <ul>
                            ${reasonsHtml}
                        </ul>
                    `;

                } catch (popupError) {

                    console.error(
                        "Popup Render Error:",
                        popupError
                    );

                    resultDiv.innerHTML = `
                        <h2 class="warning">
                            ERROR
                        </h2>

                        <p>
                            Failed to render popup.
                        </p>
                    `;
                }
            }
        );

        // ---------------------------------------------------
        // LOAD HISTORY
        // ---------------------------------------------------

        chrome.storage.local.get(

            ["phishingHistory"],

            (historyResult) => {

                try {

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

                    history
                        .slice(0, 5)
                        .forEach((item) => {

                            const div =
                                document.createElement("div");

                            div.className =
                                "history-item";

                            div.innerHTML = `

                                <div class="history-url">
                                    ${item.url || "Unknown URL"}
                                </div>

                                <div class="history-risk">
                                    Risk Score:
                                    ${item.score || 0}
                                </div>

                                <div class="history-time">
                                    ${item.time || "Unknown"}
                                </div>
                            `;

                            historyDiv.appendChild(div);
                        });

                } catch (historyError) {

                    console.error(
                        "History Error:",
                        historyError
                    );

                    historyDiv.innerHTML = `
                        <p class="warning">
                            Failed to load history.
                        </p>
                    `;
                }
            }
        );

    } catch (error) {

        console.error(
            "Popup Fatal Error:",
            error
        );

        resultDiv.innerHTML = `
            <h2 class="warning">ERROR</h2>

            <p>
                Popup failed to load.
            </p>
        `;
    }
});