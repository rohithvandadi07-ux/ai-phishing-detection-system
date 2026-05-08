chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {

    // Run only when page fully loads
    if (changeInfo.status !== "complete" || !tab.url) {
        return;
    }

    // Ignore Chrome internal pages
    if (
        tab.url.startsWith("chrome://") ||
        tab.url.startsWith("chrome-extension://") ||
        tab.url.startsWith("edge://")
    ) {
        return;
    }

    try {

        // Send URL to FastAPI backend
        const response = await fetch(
            `http://127.0.0.1:8000/predict?url=${encodeURIComponent(tab.url)}`,
            {
                method: "POST"
            }
        );

        const data = await response.json();

        console.log("Checked URL:", tab.url);
        console.log("Prediction:", data);

        // 🚨 Block malicious websites
        if (data.prediction === "malicious") {

            const blockedUrl =
                chrome.runtime.getURL(
                    "blocked.html?url=" + encodeURIComponent(tab.url)
                );

            chrome.tabs.update(tabId, {
                url: blockedUrl
            });
        }

    } catch (error) {

        console.error("Background scanner error:", error);
    }
});