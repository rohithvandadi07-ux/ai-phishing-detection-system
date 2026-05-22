const API_BASE_URL =
    "http://localhost:8080";

const API_KEY =
    "2727253faaca7b371e5954da68df3971ec2679a317eaf8f6c3986ea77e1770c8";

// --------------------------------------------------
// GET URL PARAM
// --------------------------------------------------

const params =
    new URLSearchParams(
        window.location.search
    );

const targetUrl =
    params.get("url");

// --------------------------------------------------
// UPDATE UI
// --------------------------------------------------

document.getElementById(
    "urlText"
).textContent = targetUrl;

// --------------------------------------------------
// SAVE RESULT
// --------------------------------------------------

function saveResult(result) {

    chrome.storage.local.set({

        latestScan: {

            url: targetUrl,
            result: result,

            timestamp:
                new Date().toISOString()
        }
    });
}

// --------------------------------------------------
// SAFE REDIRECT
// --------------------------------------------------

function redirectSafe() {

    setTimeout(() => {

        window.location.href =
            targetUrl;

    }, 1200);
}

// --------------------------------------------------
// BLOCK PAGE
// --------------------------------------------------

function redirectBlocked(result) {

    const blockUrl =

        chrome.runtime.getURL(

            `blocker.html` +
            `?url=${encodeURIComponent(targetUrl)}` +
            `&risk=${result.risk_score}` +
            `&level=${result.risk_level}` +
            `&confidence=${result.confidence}`
        );

    window.location.href =
        blockUrl;
}

// --------------------------------------------------
// MAIN SCAN
// --------------------------------------------------

async function performScan() {

    try {

        console.log(
            "Scanning:",
            targetUrl
        );

        // ------------------------------------------
        // HEALTH
        // ------------------------------------------

        const health =
            await fetch(
                `${API_BASE_URL}/health`
            );

        if (!health.ok) {

            throw new Error(
                "Backend Offline"
            );
        }

        // ------------------------------------------
        // PREDICT
        // ------------------------------------------

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

                        url: targetUrl
                    })
                }
            );

        if (!response.ok) {

            console.error(
                "Prediction Error:",
                response.status
            );

            throw new Error(
                "Prediction Failed"
            );
        }

        const result =
            await response.json();

        console.log(
            "Prediction:",
            result
        );

        saveResult(result);

        // ------------------------------------------
        // MALICIOUS
        // ------------------------------------------

        if (
            result.prediction ===
            "malicious"
        ) {

            redirectBlocked(
                result
            );

            return;
        }

        // ------------------------------------------
        // SAFE
        // ------------------------------------------

        redirectSafe();
    }

    catch (error) {

        console.error(
            "Scanning Error:",
            error
        );

        document.getElementById(
            "urlText"
        ).textContent =

            "Backend connection failed";

        setTimeout(() => {

            window.location.href =
                targetUrl;

        }, 3000);
    }
}

performScan();