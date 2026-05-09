chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {

    // ---------------------------------------------------
    // RUN ONLY AFTER PAGE LOAD
    // ---------------------------------------------------

    if (changeInfo.status !== "complete" || !tab.url) {
        return;
    }

    // ---------------------------------------------------
    // IGNORE INTERNAL BROWSER PAGES
    // ---------------------------------------------------

    if (
        tab.url.startsWith("chrome://") ||
        tab.url.startsWith("chrome-extension://") ||
        tab.url.startsWith("edge://")
    ) {
        return;
    }

    // ---------------------------------------------------
    // WHITELIST DEVELOPMENT URLS
    // ---------------------------------------------------

    const safeUrls = [

        "http://localhost",
        "http://127.0.0.1",

        "http://localhost:8501",
        "http://127.0.0.1:8501",

        "https://ai-phishing-detection-system-y2dn.onrender.com"
    ];

    for (const safe of safeUrls) {

        if (tab.url.startsWith(safe)) {

            console.log("Whitelisted URL:", tab.url);

            return;
        }
    }

    try {

        // ---------------------------------------------------
        // API URL
        // ---------------------------------------------------

        const apiUrl =
            `https://ai-phishing-detection-system-y2dn.onrender.com/predict?url=${encodeURIComponent(tab.url)}`;

        // ---------------------------------------------------
        // SEND REQUEST
        // ---------------------------------------------------

        const response = await fetch(apiUrl, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            }
        });

        // ---------------------------------------------------
        // HANDLE FAILED RESPONSE
        // ---------------------------------------------------

        if (!response.ok) {

            console.error(
                "API Error:",
                response.status,
                response.statusText
            );

            return;
        }

        // ---------------------------------------------------
        // PARSE JSON
        // ---------------------------------------------------

        const data = await response.json();

        console.log("Checked URL:", tab.url);

        console.log("Prediction:", data);

        // ---------------------------------------------------
        // BLOCK MALICIOUS URL
        // ---------------------------------------------------

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