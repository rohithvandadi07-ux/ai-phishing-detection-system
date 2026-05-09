chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {

    // Run only when page fully loads
    if (changeInfo.status !== "complete" || !tab.url) {
        return;
    }

    // Ignore browser internal pages
    if (
        tab.url.startsWith("chrome://") ||
        tab.url.startsWith("chrome-extension://") ||
        tab.url.startsWith("edge://") ||
        tab.url.startsWith("about:") ||
        tab.url.startsWith("file://")
    ) {
        return;
    }

    try {

        console.log("Scanning URL:", tab.url);

        // Cloud backend API
        const apiUrl =
            "https://ai-phishing-detection-system-y2dn.onrender.com/predict?url=" +
            encodeURIComponent(tab.url);

        // Send request to backend
        const response = await fetch(apiUrl, {
            method: "POST"
        });

        // Handle Render sleeping / failed responses
        if (!response.ok) {

            console.error(
                "Backend API error:",
                response.status,
                response.statusText
            );

            return;
        }

        // Parse JSON response
        const data = await response.json();

        console.log("Prediction Result:", data);

        // Block malicious websites
        if (data.prediction === "malicious") {

            console.log("Malicious website detected!");

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