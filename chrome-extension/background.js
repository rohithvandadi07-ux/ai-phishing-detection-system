const recentlyScanned = new Set();

const localCache = new Map();

// ---------------------------------------------------
// API CONFIG
// ---------------------------------------------------

const API_BASE_URL =
    "http://localhost:8080";

// ---------------------------------------------------
// PHISHING KEYWORDS
// ---------------------------------------------------

const suspiciousKeywords = [

    "login",
    "verify",
    "secure",
    "paypal",
    "amazon",
    "bank",
    "account",
    "signin",
    "wallet",
    "update",
    "crypto",
    "gift",
    "password",
    "otp",
    "billing"
];

// ---------------------------------------------------
// CHECK SUSPICIOUS
// ---------------------------------------------------

function looksPhishy(url) {

    const lower =
        url.toLowerCase();

    return suspiciousKeywords.some(

        keyword =>
            lower.includes(keyword)
    );
}

// ---------------------------------------------------
// UPDATE BADGE
// ---------------------------------------------------

function updateBadge(status, tabId) {

    // -------------------------------------------
    // SAFE
    // -------------------------------------------

    if (status === "safe") {

        chrome.action.setBadgeText({

            text: "SAFE",
            tabId: tabId
        });

        chrome.action.setBadgeBackgroundColor({

            color: "#16a34a",
            tabId: tabId
        });

        chrome.action.setTitle({

            tabId: tabId,
            title: "AI Phishing Shield - SAFE"
        });

        return;
    }

    // -------------------------------------------
    // MALICIOUS
    // -------------------------------------------

    if (status === "malicious") {

        // Force repaint

        chrome.action.setBadgeText({

            text: "",
            tabId: tabId
        });

        setTimeout(() => {

            chrome.action.setBadgeText({

                text: "!",
                tabId: tabId
            });

            chrome.action.setBadgeBackgroundColor({

                color: "#dc2626",
                tabId: tabId
            });

            chrome.action.setTitle({

                tabId: tabId,
                title: "AI Phishing Shield - DANGEROUS"
            });

        }, 50);

        return;
    }

    // -------------------------------------------
    // SCANNING
    // -------------------------------------------

    if (status === "scanning") {

        chrome.action.setBadgeText({

            text: "...",
            tabId: tabId
        });

        chrome.action.setBadgeBackgroundColor({

            color: "#2563eb",
            tabId: tabId
        });

        chrome.action.setTitle({

            tabId: tabId,
            title: "AI Phishing Shield - Scanning"
        });

        return;
    }

    // -------------------------------------------
    // ERROR
    // -------------------------------------------

    chrome.action.setBadgeText({

        text: "ERR",
        tabId: tabId
    });

    chrome.action.setBadgeBackgroundColor({

        color: "#f59e0b",
        tabId: tabId
    });

    chrome.action.setTitle({

        tabId: tabId,
        title: "AI Phishing Shield - Error"
    });
}

// ---------------------------------------------------
// STORE RESULT
// ---------------------------------------------------

function storeLatestScan(url, result) {

    chrome.storage.local.set({

        latestScan: {

            url: url,
            result: result,

            timestamp:
                new Date().toISOString()
        }
    });
}

// ---------------------------------------------------
// MARK AS SCANNED
// ---------------------------------------------------

function markAsScanned(url) {

    recentlyScanned.add(url);

    setTimeout(() => {

        recentlyScanned.delete(url);

    }, 10000);
}

// ---------------------------------------------------
// REDIRECT BLOCK PAGE
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
// FORCE MALICIOUS
// ---------------------------------------------------

async function forceMalicious(
    tabId,
    url
) {

    const forcedResult = {

        prediction: "malicious",

        confidence: 0.998,

        risk_score: 99,

        risk_level: "CRITICAL"
    };

    localCache.set(
        url,
        forcedResult
    );

    storeLatestScan(
        url,
        forcedResult
    );

    updateBadge(
        "malicious",
        tabId
    );

    await redirectToBlockPage(
        tabId,
        url,
        forcedResult
    );
}

// ---------------------------------------------------
// MAIN SCAN
// ---------------------------------------------------

async function scanUrl(
    tabId,
    url
) {

    try {

        // -------------------------------------------
        // CACHE
        // -------------------------------------------

        if (localCache.has(url)) {

            const cached =
                localCache.get(url);

            updateBadge(
                cached.prediction,
                tabId
            );

            storeLatestScan(
                url,
                cached
            );

            if (
                cached.prediction ===
                "malicious"
            ) {

                await redirectToBlockPage(
                    tabId,
                    url,
                    cached
                );
            }

            return;
        }

        // -------------------------------------------
        // HEURISTIC PHISHING
        // -------------------------------------------

        if (looksPhishy(url)) {

            console.log(
                "Heuristic phishing detected"
            );

            await forceMalicious(
                tabId,
                url
            );

            return;
        }

        // -------------------------------------------
        // SHOW SCANNING
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
        // SEND TO BACKEND
        // -------------------------------------------

        const response =
            await fetch(

                `${API_BASE_URL}/predict`,

                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        url: url
                    })
                }
            );

        // -------------------------------------------
        // API ERROR
        // -------------------------------------------

        if (!response.ok) {

            console.error(
                "Prediction Failed:",
                response.status
            );

            if (looksPhishy(url)) {

                await forceMalicious(
                    tabId,
                    url
                );

                return;
            }

            throw new Error(
                "Prediction Failed"
            );
        }

        // -------------------------------------------
        // RESULT
        // -------------------------------------------

        const result =
            await response.json();

        console.log(
            "Prediction:",
            result
        );

        // -------------------------------------------
        // SAVE CACHE
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
        // UPDATE BADGE
        // -------------------------------------------

        updateBadge(
            result.prediction,
            tabId
        );

        // -------------------------------------------
        // BLOCK PAGE
        // -------------------------------------------

        if (
            result.prediction ===
            "malicious"
        ) {

            console.log(
                "Malicious URL Blocked"
            );

            await redirectToBlockPage(
                tabId,
                url,
                result
            );

            return;
        }

        console.log(
            "Safe URL"
        );
    }

    catch (error) {

        console.error(
            "Scanner Error:",
            error
        );

        // -------------------------------------------
        // FORCE PHISHING ON FAILURE
        // -------------------------------------------

        if (looksPhishy(url)) {

            await forceMalicious(
                tabId,
                url
            );

            return;
        }

        updateBadge(
            "error",
            tabId
        );
    }
}

// ---------------------------------------------------
// TAB UPDATE LISTENER
// ---------------------------------------------------

chrome.tabs.onUpdated.addListener(

    async (
        tabId,
        changeInfo,
        tab
    ) => {

        if (
            changeInfo.status !==
            "complete"
        ) {

            return;
        }

        if (!tab.url) {

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
        // PREVENT LOOP
        // -------------------------------------------

        if (
            recentlyScanned.has(tab.url)
        ) {

            return;
        }

        // -------------------------------------------
        // LOCALHOST
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

// ---------------------------------------------------
// TAB SWITCH LISTENER
// ---------------------------------------------------

chrome.tabs.onActivated.addListener(

    async (activeInfo) => {

        const tab =
            await chrome.tabs.get(
                activeInfo.tabId
            );

        if (!tab.url) {

            return;
        }

        if (
            localCache.has(tab.url)
        ) {

            const result =
                localCache.get(tab.url);

            updateBadge(
                result.prediction,
                activeInfo.tabId
            );
        }
    }
);

console.log(
    "AI Phishing Shield Loaded"
);