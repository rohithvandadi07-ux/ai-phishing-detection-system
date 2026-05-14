chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {

    // ---------------------------------------------------
    // RUN ONLY AFTER FULL LOAD
    // ---------------------------------------------------

    if (changeInfo.status !== "complete" || !tab.url) {
        return;
    }

    // ---------------------------------------------------
    // IF ALREADY BLOCK PAGE
    // ---------------------------------------------------

    if (tab.url.includes("blocked.html")) {

        chrome.action.setBadgeText({

            text: "BAD",
            tabId: tabId
        });

        chrome.action.setBadgeBackgroundColor({

            color: "#dc2626",
            tabId: tabId
        });

        return;
    }

    // ---------------------------------------------------
    // IGNORE INTERNAL PAGES
    // ---------------------------------------------------

    if (
        tab.url.startsWith("chrome://") ||
        tab.url.startsWith("chrome-extension://") ||
        tab.url.startsWith("edge://")
    ) {
        return;
    }

    // ---------------------------------------------------
    // WHITELIST
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

            chrome.action.setBadgeText({

                text: "SAFE",
                tabId: tabId
            });

            chrome.action.setBadgeBackgroundColor({

                color: "#16a34a",
                tabId: tabId
            });

            return;
        }
    }

    try {

        console.log("Scanning:", tab.url);

        // ---------------------------------------------------
        // CACHE KEY
        // ---------------------------------------------------

        const cacheKey = `scan_${tab.url}`;

        // ---------------------------------------------------
        // CHECK CACHE
        // ---------------------------------------------------

        const cache =
            await chrome.storage.local.get([cacheKey]);

        // ---------------------------------------------------
        // CACHE HIT
        // ---------------------------------------------------

        if (cache[cacheKey]) {

            console.log("CACHE HIT");

            const data = cache[cacheKey];

            // SAFE CACHE

            if (data.prediction === "safe") {

                chrome.action.setBadgeText({

                    text: "SAFE",
                    tabId: tabId
                });

                chrome.action.setBadgeBackgroundColor({

                    color: "#16a34a",
                    tabId: tabId
                });

                return;
            }

            // MALICIOUS CACHE

            chrome.action.setBadgeText({

                text: "BAD",
                tabId: tabId
            });

            chrome.action.setBadgeBackgroundColor({

                color: "#dc2626",
                tabId: tabId
            });

            // BLOCK PAGE

            const blockedUrl =
                chrome.runtime.getURL(
                    `blocked.html?url=${encodeURIComponent(tab.url)}`
                    + `&risk=${encodeURIComponent(data.risk_level)}`
                    + `&score=${encodeURIComponent(data.risk_score)}`
                    + `&confidence=${encodeURIComponent(data.confidence)}`
                );

            await chrome.tabs.update(tabId, {

                url: blockedUrl
            });

            return;
        }

        // ---------------------------------------------------
        // CACHE MISS
        // ---------------------------------------------------

        console.log("CACHE MISS");

        // ---------------------------------------------------
        // API CALL
        // ---------------------------------------------------

        const apiUrl =
            `https://ai-phishing-detection-system-y2dn.onrender.com/predict?url=${encodeURIComponent(tab.url)}`;

        const response = await fetch(apiUrl, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            }
        });

        // ---------------------------------------------------
        // BACKEND ERROR
        // ---------------------------------------------------

        if (!response.ok) {

            throw new Error("Backend failed");
        }

        // ---------------------------------------------------
        // JSON RESPONSE
        // ---------------------------------------------------

        const data = await response.json();

        console.log("Backend Response:", data);

        // ---------------------------------------------------
        // SAVE CACHE
        // ---------------------------------------------------

        await chrome.storage.local.set({

            [cacheKey]: data
        });

        console.log("Saved to cache");

        // ---------------------------------------------------
        // SAVE HISTORY
        // ---------------------------------------------------

        const historyResult =
            await chrome.storage.local.get(["phishingHistory"]);

        const history =
            historyResult.phishingHistory || [];

        history.unshift({

            url: tab.url,

            score: data.risk_score,

            prediction: data.prediction,

            time: new Date().toLocaleString()
        });

        await chrome.storage.local.set({

            phishingHistory: history.slice(0, 20)
        });

        // ---------------------------------------------------
        // SAFE RESULT
        // ---------------------------------------------------

        if (data.prediction === "safe") {

            chrome.action.setBadgeText({

                text: "SAFE",
                tabId: tabId
            });

            chrome.action.setBadgeBackgroundColor({

                color: "#16a34a",
                tabId: tabId
            });

            return;
        }

        // ---------------------------------------------------
        // MALICIOUS RESULT
        // ---------------------------------------------------

        chrome.action.setBadgeText({

            text: "BAD",
            tabId: tabId
        });

        chrome.action.setBadgeBackgroundColor({

            color: "#dc2626",
            tabId: tabId
        });

        // ---------------------------------------------------
        // REDIRECT TO BLOCK PAGE
        // ---------------------------------------------------

        const blockedUrl =
            chrome.runtime.getURL(
                `blocked.html?url=${encodeURIComponent(tab.url)}`
                + `&risk=${encodeURIComponent(data.risk_level)}`
                + `&score=${encodeURIComponent(data.risk_score)}`
                + `&confidence=${encodeURIComponent(data.confidence)}`
            );

        await chrome.tabs.update(tabId, {

            url: blockedUrl
        });

    } catch (error) {

        console.error("Scanner Error:", error);

        chrome.action.setBadgeText({

            text: "ERR",
            tabId: tabId
        });

        chrome.action.setBadgeBackgroundColor({

            color: "#f59e0b",
            tabId: tabId
        });
    }
});