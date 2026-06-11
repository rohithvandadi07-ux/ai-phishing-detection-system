// ---------------------------------------------------
// MEMORY
// ---------------------------------------------------

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
    "billing",
    "auth",
    "authenticate",
    "security",
    "support",
    "confirm"
];

// ---------------------------------------------------
// BRAND IMPERSONATION
// ---------------------------------------------------

const protectedBrands = [

    "google",
    "facebook",
    "instagram",
    "microsoft",
    "apple",
    "amazon",
    "paypal",
    "netflix",
    "steam",
    "discord",
    "telegram",
    "whatsapp",
    "github",
    "linkedin",
    "twitter"
];

// ---------------------------------------------------
// CLEAN URL
// ---------------------------------------------------

function normalizeUrl(
    url
) {

    try {

        const parsed =
            new URL(url);

        return parsed.hostname
            .toLowerCase();

    }

    catch {

        return url.toLowerCase();
    }
}

// ---------------------------------------------------
// LOOKS PHISHY
// ---------------------------------------------------

function looksPhishy(
    url
) {

    const lower =
        url.toLowerCase();

    // -------------------------------------------
    // KEYWORD CHECK
    // -------------------------------------------

    const keywordHits =
        suspiciousKeywords.filter(

            keyword =>
                lower.includes(keyword)

        ).length;

    // -------------------------------------------
    // BRAND IMPERSONATION
    // -------------------------------------------

    const fakeBrand =
        protectedBrands.some(

            brand => {

                // detect fake spellings
                // g00gle, faceb00k, amaz0n

                const fake =
                    brand
                        .replace(/o/g, "0")
                        .replace(/i/g, "1")
                        .replace(/e/g, "3");

                return (
                    lower.includes(fake) ||
                    lower.includes(
                        `${brand}-`
                    ) ||
                    lower.includes(
                        `${brand}secure`
                    ) ||
                    lower.includes(
                        `${brand}login`
                    )
                );
            }
        );

    // -------------------------------------------
    // DOMAIN TRICKS
    // -------------------------------------------

    const hasManyDots =
        url.split(".").length >= 4;

    const hasAt =
        url.includes("@");

    const hasHyphen =
        url.includes("-");

    // -------------------------------------------
    // FINAL
    // -------------------------------------------

    return (

        keywordHits >= 2 ||

        fakeBrand ||

        hasManyDots ||

        hasAt ||

        (
            keywordHits >= 1 &&
            hasHyphen
        )
    );
}

// ---------------------------------------------------
// UPDATE BADGE
// ---------------------------------------------------

function updateBadge(
    status,
    tabId
) {

    chrome.action.setBadgeText({

        text: "",
        tabId: tabId
    });

    // -------------------------------------------
    // SAFE
    // -------------------------------------------

    if (status === "safe") {

        setTimeout(() => {

            chrome.action.setBadgeText({

                text: "OK",
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

        }, 50);

        return;
    }

    // -------------------------------------------
    // MALICIOUS
    // -------------------------------------------

    if (status === "malicious") {

        setTimeout(() => {

            chrome.action.setBadgeText({

                text: "BAD",
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

        setTimeout(() => {

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

        }, 50);

        return;
    }

    // -------------------------------------------
    // ERROR
    // -------------------------------------------

    setTimeout(() => {

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

    }, 50);
}

// ---------------------------------------------------
// SHOW NOTIFICATION
// ---------------------------------------------------

function showThreatNotification(
    url,
    result
) {

    chrome.notifications.create({

        type: "basic",

        iconUrl:
            "icons/icon128.png",

        title:
            "🚨 AI Phishing Shield",

        message:
            `Blocked phishing site\nRisk Score: ${result.risk_score}\nThreat Level: ${result.risk_level}`,

        priority: 2

    });
}

// ---------------------------------------------------
// SAVE HISTORY
// ---------------------------------------------------

function saveScanHistory(
    url,
    result
) {

    chrome.storage.local.get(

        ["scanHistory"],

        (data) => {

            const history =
                data.scanHistory || [];

            history.push({

                url: url,

                result: result,

                timestamp:
                    new Date().toISOString()
            });

            const trimmed =
                history.slice(-50);

            chrome.storage.local.set({

                scanHistory:
                    trimmed
            });
        }
    );
}

// ---------------------------------------------------
// STORE LATEST
// ---------------------------------------------------

function storeLatestScan(
    url,
    result
) {

    chrome.storage.local.set({

        latestScan: {

            url: url,

            result: result,

            timestamp:
                new Date().toISOString()
        }
    });

    saveScanHistory(
        url,
        result
    );
}

// ---------------------------------------------------
// MARK SCANNED
// ---------------------------------------------------

function markAsScanned(
    url
) {

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

    updateBadge(
        "malicious",
        tabId
    );

    await new Promise(

        resolve => setTimeout(
            resolve,
            300
        )
    );

    chrome.storage.local.set({
        lastBlockedUrl: url
    });

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

    setTimeout(() => {

        updateBadge(
            "malicious",
            tabId
        );

    }, 500);
}

// ---------------------------------------------------
// FORCE BLOCK
// ---------------------------------------------------

async function forceMalicious(
    tabId,
    url
) {

    const forcedResult = {

        prediction: "malicious",

        confidence: 0.998,

        risk_score: 99,

        risk_level: "CRITICAL",

        ai_engine: {

            lgb_probability: 0.98,

            rf_probability: 0.99,

            semantic_confidence: 0.97,

            hybrid_probability: 0.998,

            reputation_score: 95,

            reputation_level: "CRITICAL",

            trust_score: 0,

            domain_age_days: null,

            virustotal_detections: 0
        },

        reasons: [

            "Suspicious phishing keywords detected",

            "Brand impersonation attempt detected",

            "Unsafe authentication URL pattern",

            "Potential credential harvesting domain"
        ]
    };

    localCache.set(
        url,
        forcedResult
    );

    storeLatestScan(
        url,
        forcedResult
    );

    showThreatNotification(
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
        // HEURISTIC CHECK
        // -------------------------------------------

        if (
            looksPhishy(url)
        ) {

            console.log(
                "Heuristic phishing detected - continuing AI scan"
            );
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
        // PREDICT
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
        // ERROR
        // -------------------------------------------

        if (!response.ok) {

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
        // CACHE
        // -------------------------------------------

        localCache.set(
            url,
            result
        );

        // -------------------------------------------
        // STORAGE
        // -------------------------------------------

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
        // BLOCK
        // -------------------------------------------

        if (
            result.prediction ===
            "malicious"
        ) {

            console.log(
                "Malicious URL Blocked"
            );

            showThreatNotification(
                url,
                result
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
        // FALLBACK HEURISTIC
        // -------------------------------------------

        if (
            looksPhishy(url)
        ) {
        }

        updateBadge(
            "error",
            tabId
        );
    }
}

// ---------------------------------------------------
// TAB UPDATE
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
// TAB SWITCH
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