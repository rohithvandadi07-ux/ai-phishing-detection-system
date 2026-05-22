const recentlyScanned = new Set();

const localCache = new Map();

// ---------------------------------------------------
// API CONFIG
// ---------------------------------------------------

const API_BASE_URL =
    "http://localhost:8080";

const API_KEY =
    "2727253faaca7b371e5954da68df3971ec2679a317eaf8f6c3986ea77e1770c8";

// ---------------------------------------------------
// MARK URL AS SCANNED
// ---------------------------------------------------

function markAsScanned(url) {

    recentlyScanned.add(url);

    setTimeout(() => {

        recentlyScanned.delete(url);

    }, 15000);
}

// ---------------------------------------------------
// UPDATE BADGE
// ---------------------------------------------------

function updateBadge(status, tabId) {

    if (status === "safe") {

        chrome.action.setBadgeText({
            text: "SAFE",
            tabId
        });

        chrome.action.setBadgeBackgroundColor({
            color: "#16a34a",
            tabId
        });
    }

    else if (status === "malicious") {

        chrome.action.setBadgeText({
            text: "BAD",
            tabId
        });

        chrome.action.setBadgeBackgroundColor({
            color: "#dc2626",
            tabId
        });
    }

    else if (status === "scanning") {

        chrome.action.setBadgeText({
            text: "...",
            tabId
        });

        chrome.action.setBadgeBackgroundColor({
            color: "#2563eb",
            tabId
        });
    }

    else {

        chrome.action.setBadgeText({
            text: "ERR",
            tabId
        });

        chrome.action.setBadgeBackgroundColor({
            color: "#f59e0b",
            tabId
        });
    }
}

// ---------------------------------------------------
// STORE SCAN RESULT
// ---------------------------------------------------

function storeLatestScan(url, result) {

    chrome.storage.local.set({

        latestScan: {

            url,
            result,

            timestamp:
                new Date().toISOString()
        }
    });
}

// ---------------------------------------------------
// BLOCK PAGE
// ---------------------------------------------------

async function redirectToBlockPage(
    tabId,
    url,
    result
) {

    const blockPage =

        chrome.runtime.getURL(

            `blocker.html` +
            `?url=${encodeURIComponent(url)}` +
            `&risk=${result.risk_score}` +
            `&level=${result.risk_level}` +
            `&confidence=${result.confidence}`
        );

    await chrome.tabs.update(tabId, {

        url: blockPage
    });
}

// ---------------------------------------------------
// MAIN SCAN ENGINE
// ---------------------------------------------------

async function scanUrl(tabId, url) {

    try {

        // -------------------------------------------
        // CACHE
        // -------------------------------------------

        if (localCache.has(url)) {

            const cachedResult =
                localCache.get(url);

            console.log(
                "Using cached result:",
                cachedResult
            );

            updateBadge(
                cachedResult.prediction,
                tabId
            );

            storeLatestScan(
                url,
                cachedResult
            );

            if (
                cachedResult.prediction ===
                "malicious"
            ) {

                await redirectToBlockPage(
                    tabId,
                    url,
                    cachedResult
                );
            }

            return;
        }

        // -------------------------------------------
        // BADGE
        // -------------------------------------------

        updateBadge(
            "scanning",
            tabId
        );

        console.log(
            "Scanning:",
            url
        );

        // -------------------------------------------
        // HEALTH CHECK
        // -------------------------------------------

        const health =
            await fetch(
                `${API_BASE_URL}/health`
            );

        if (!health.ok) {

            throw new Error(
                "Backend Offline"
            );
        }

        // -------------------------------------------
        // PREDICTION REQUEST
        // -------------------------------------------

        const response =
            await fetch(

                `${API_BASE_URL}/predict`,

                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "X-API-Key":
                            API_KEY
                    },

                    body: JSON.stringify({

                        url: url
                    })
                }
            );

        if (!response.ok) {

            console.error(
                "Prediction API Failed:",
                response.status
            );

            throw new Error(
                "Prediction API Failed"
            );
        }

        const result =
            await response.json();

        console.log(
            "Prediction Result:",
            result
        );

        // -------------------------------------------
        // SAVE
        // -------------------------------------------

        localCache.set(
            url,
            result
        );

        storeLatestScan(
            url,
            result
        );

        // -------------------------------------------
        // BADGE
        // -------------------------------------------

        updateBadge(
            result.prediction,
            tabId
        );

        // -------------------------------------------
        // BLOCK PHISHING
        // -------------------------------------------

        if (
            result.prediction ===
            "malicious"
        ) {

            await redirectToBlockPage(
                tabId,
                url,
                result
            );
        }
    }

    catch (error) {

        console.error(
            "Scanner Error:",
            error
        );

        updateBadge(
            "error",
            tabId
        );
    }
}

// ---------------------------------------------------
// TAB LISTENER
// ---------------------------------------------------

chrome.tabs.onUpdated.addListener(

    async (
        tabId,
        changeInfo,
        tab
    ) => {

        if (

            changeInfo.status !==
            "complete" ||

            !tab.url

        ) {

            return;
        }

        // -------------------------------------------
        // IGNORE INTERNAL
        // -------------------------------------------

        if (

            tab.url.startsWith("chrome://") ||
            tab.url.startsWith("chrome-extension://") ||
            tab.url.startsWith("edge://") ||
            tab.url.startsWith("about:")

        ) {

            return;
        }

        // -------------------------------------------
        // IGNORE EXTENSION PAGES
        // -------------------------------------------

        if (

            tab.url.includes("blocker.html") ||
            tab.url.includes("popup.html") ||
            tab.url.includes("scanning.html")

        ) {

            return;
        }

        // -------------------------------------------
        // PREVENT LOOPS
        // -------------------------------------------

        if (
            recentlyScanned.has(tab.url)
        ) {

            return;
        }

        // -------------------------------------------
        // LOCALHOST WHITELIST
        // -------------------------------------------

        if (

            tab.url.startsWith("http://localhost") ||
            tab.url.startsWith("http://127.0.0.1")

        ) {

            updateBadge(
                "safe",
                tabId
            );

            return;
        }

        markAsScanned(
            tab.url
        );

        await scanUrl(
            tabId,
            tab.url
        );
    }
);

console.log(
    "AI Phishing Shield Loaded"
);