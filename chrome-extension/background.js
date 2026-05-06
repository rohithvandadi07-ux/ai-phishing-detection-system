chrome.webNavigation.onBeforeNavigate.addListener(async (details) => {
    if (details.frameId !== 0) return; // main tab only

    const url = details.url;

    // skip chrome pages
    if (url.startsWith("chrome://") || url.startsWith("edge://")) return;

    try {
        const response = await fetch(
            `http://127.0.0.1:8000/predict?url=${encodeURIComponent(url)}`,
            { method: "POST" }
        );

        const data = await response.json();

        if (data.prediction === "malicious") {
            chrome.tabs.update(details.tabId, {
                url: chrome.runtime.getURL("blocked.html") + "?url=" + encodeURIComponent(url)
            });
        }

    } catch (err) {
        console.log("API error:", err);
    }
});