chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {

    if (changeInfo.status !== "complete" || !tab.url) {
        return;
    }

    if (
        tab.url.startsWith("chrome://") ||
        tab.url.startsWith("chrome-extension://") ||
        tab.url.startsWith("edge://")
    ) {
        return;
    }

    try {

        const apiUrl =
            `https://ai-phishing-detection-system-y2dn.onrender.com/predict?url=${encodeURIComponent(tab.url)}`;

        const response = await fetch(apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {

            console.error(
                "API Error:",
                response.status,
                response.statusText
            );

            return;
        }

        const data = await response.json();

        console.log("Checked URL:", tab.url);
        console.log("Prediction:", data);

        if (data.prediction === "malicious") {

            const blockedUrl =
                chrome.runtime.getURL(
                    "blocked.html?url=" +
                    encodeURIComponent(tab.url)
                );

            chrome.tabs.update(tabId, {
                url: blockedUrl
            });
        }

    } catch (error) {

        console.error(
            "Background scanner error:",
            error
        );
    }
});