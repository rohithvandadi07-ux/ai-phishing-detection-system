const recentlyScanned =
    new Set();

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
// MAIN LISTENER
// ---------------------------------------------------

chrome.tabs.onUpdated.addListener(

    async (tabId, changeInfo, tab) => {

        // ---------------------------------------------------
        // FULL PAGE LOAD ONLY
        // ---------------------------------------------------

        if (

            changeInfo.status !== "complete" ||
            !tab.url

        ) {

            return;
        }

        // ---------------------------------------------------
        // IGNORE INTERNAL PAGES
        // ---------------------------------------------------

        if (

            tab.url.startsWith("chrome://") ||
            tab.url.startsWith("chrome-extension://") ||
            tab.url.startsWith("edge://") ||
            tab.url.startsWith("about:")

        ) {

            return;
        }

        // ---------------------------------------------------
        // IGNORE EXTENSION PAGES
        // ---------------------------------------------------

        if (

            tab.url.includes("blocked.html") ||
            tab.url.includes("scanning.html")

        ) {

            return;
        }

        // ---------------------------------------------------
        // PREVENT SAFE REDIRECT LOOP
        // ---------------------------------------------------

        if (
            recentlyScanned.has(tab.url)
        ) {

            console.log(
                "Skipping recently scanned URL:",
                tab.url
            );

            chrome.action.setBadgeText({

                text: "SAFE",
                tabId
            });

            chrome.action.setBadgeBackgroundColor({

                color: "#16a34a",
                tabId
            });

            return;
        }

        // ---------------------------------------------------
        // SAFE WHITELIST
        // ---------------------------------------------------

        const safeUrls = [

            "http://localhost",
            "http://127.0.0.1",

            "http://localhost:8501",
            "http://127.0.0.1:8501",

            "https://google.com",
            "https://github.com",
            "https://openai.com",

            "https://ai-phishing-detection-system-y2dn.onrender.com"
        ];

        for (const safe of safeUrls) {

            if (tab.url.startsWith(safe)) {

                chrome.action.setBadgeText({

                    text: "SAFE",
                    tabId
                });

                chrome.action.setBadgeBackgroundColor({

                    color: "#16a34a",
                    tabId
                });

                return;
            }
        }

        try {

            console.log(
                "Launching AI Scan:",
                tab.url
            );

            // ---------------------------------------------------
            // MARK URL
            // ---------------------------------------------------

            markAsScanned(tab.url);

            // ---------------------------------------------------
            // BADGE
            // ---------------------------------------------------

            chrome.action.setBadgeText({

                text: "...",
                tabId
            });

            chrome.action.setBadgeBackgroundColor({

                color: "#2563eb",
                tabId
            });

            // ---------------------------------------------------
            // OPEN SCANNING PAGE
            // ---------------------------------------------------

            const scanPage =

                chrome.runtime.getURL(

                    `scanning.html?url=${encodeURIComponent(tab.url)}`
                );

            await chrome.tabs.update(tabId, {

                url: scanPage
            });

        }

        catch (error) {

            console.error(
                "Scanner Error:",
                error
            );

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
);