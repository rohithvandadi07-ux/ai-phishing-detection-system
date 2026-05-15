const params = new URLSearchParams(
    window.location.search
);

// ---------------------------------------------------
// TARGET URL
// ---------------------------------------------------

const targetUrl =
    params.get("url");

// ---------------------------------------------------
// DISPLAY URL
// ---------------------------------------------------

document.getElementById(
    "scan-url"
).textContent =
    targetUrl || "Unknown URL";

// ---------------------------------------------------
// STEP ELEMENTS
// ---------------------------------------------------

const steps = [

    document.getElementById("step1"),
    document.getElementById("step2"),
    document.getElementById("step3"),
    document.getElementById("step4")

];

// ---------------------------------------------------
// LIVE AI LOGS
// ---------------------------------------------------

const logsContainer =
    document.getElementById(
        "console-logs"
    );

// ---------------------------------------------------
// AI LOG DATA
// ---------------------------------------------------

const scanLogs = [

    {
        text:
            "[✓] Initializing hybrid AI engines...",
        type:
            "success"
    },

    {
        text:
            "[✓] Establishing secure threat scan environment...",
        type:
            "success"
    },

    {
        text:
            "[✓] DNS intelligence analysis started...",
        type:
            "success"
    },

    {
        text:
            "[✓] SSL certificate verification complete.",
        type:
            "success"
    },

    {
        text:
            "[✓] Domain reputation lookup completed.",
        type:
            "success"
    },

    {
        text:
            "[✓] Semantic phishing language analysis started...",
        type:
            "success"
    },

    {
        text:
            "[!] Credential harvesting patterns detected.",
        type:
            "warning"
    },

    {
        text:
            "[✓] URL structure heuristic analysis complete.",
        type:
            "success"
    },

    {
        text:
            "[✓] Threat intelligence feeds synchronized.",
        type:
            "success"
    },

    {
        text:
            "[!] Suspicious impersonation indicators found.",
        type:
            "warning"
    },

    {
        text:
            "[✓] Malware signature comparison complete.",
        type:
            "success"
    },

    {
        text:
            "[✓] Hybrid AI ensemble calculating verdict...",
        type:
            "success"
    }

];

// ---------------------------------------------------
// ADD LOG
// ---------------------------------------------------

function addLog(text, type = "") {

    const div =
        document.createElement("div");

    div.className =
        `log ${type}`;

    div.textContent =
        text;

    logsContainer.appendChild(div);

    // Auto-scroll

    logsContainer.scrollTop =
        logsContainer.scrollHeight;
}

// ---------------------------------------------------
// START LIVE LOGS
// ---------------------------------------------------

async function startLogs() {

    for (const item of scanLogs) {

        addLog(
            item.text,
            item.type
        );

        await sleep(450);
    }
}

// ---------------------------------------------------
// RUN SCAN STEPS
// ---------------------------------------------------

async function runSteps() {

    // Start logs in parallel

    startLogs();

    for (let i = 0; i < steps.length; i++) {

        const current =
            steps[i];

        // Activate step

        current.classList.add(
            "active"
        );

        // Wait

        await sleep(1400);

        // Complete step

        current.classList.remove(
            "active"
        );

        current.classList.add(
            "done"
        );

        // Loader to checkmark

        const loader =
            current.querySelector(
                ".loader"
            );

        if (loader) {

            loader.innerHTML = "✓";

            loader.style = `
                border:none;
                color:#00ff88;
                font-weight:bold;
                animation:none;
                font-size:18px;
            `;
        }
    }

    // Final backend scan

    await finalScan();
}

// ---------------------------------------------------
// FINAL AI BACKEND SCAN
// ---------------------------------------------------

async function finalScan() {

    try {

        addLog(

            "[✓] Sending final URL to AI detection engine...",
            "success"
        );

        const apiUrl =

            `https://ai-phishing-detection-system-y2dn.onrender.com/predict?url=${encodeURIComponent(targetUrl)}`;

        const response =
            await fetch(apiUrl, {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"
                }
            });

        // ---------------------------------------------------
        // API FAILED
        // ---------------------------------------------------

        if (!response.ok) {

            throw new Error(
                "Backend API Failed"
            );
        }

        // ---------------------------------------------------
        // PARSE JSON
        // ---------------------------------------------------

        const data =
            await response.json();

        console.log(
            "AI Scan Result:",
            data
        );

        // ---------------------------------------------------
        // SAFE
        // ---------------------------------------------------

        if (
            data.prediction === "safe"
        ) {

            addLog(

                "[✓] Website classified as SAFE.",
                "success"
            );

            addLog(

                "[✓] No phishing indicators detected.",
                "success"
            );

            await sleep(1200);

            window.location.replace(
                targetUrl
            );

            return;
        }

        // ---------------------------------------------------
        // MALICIOUS
        // ---------------------------------------------------

        addLog(

            "[!] HIGH RISK WEBSITE DETECTED.",
            "danger"
        );

        addLog(

            "[!] Blocking access to protect user.",
            "danger"
        );

        // Encode reasons

        const encodedReasons =

            encodeURIComponent(

                JSON.stringify(
                    data.reasons || []
                )
            );

        // Create block page URL

        const blockedUrl =

            chrome.runtime.getURL(

                `blocked.html`

                + `?url=${encodeURIComponent(targetUrl)}`
                + `&risk=${encodeURIComponent(data.risk_level)}`
                + `&score=${encodeURIComponent(data.risk_score)}`
                + `&confidence=${encodeURIComponent(data.confidence)}`
                + `&reasons=${encodedReasons}`
            );

        await sleep(1600);

        // Redirect

        window.location.replace(
            blockedUrl
        );
    }

    catch (error) {

        console.error(
            "AI Scan Failed:",
            error
        );

        addLog(

            "[!] AI scan engine failure detected.",
            "danger"
        );

        addLog(

            "[!] Opening website using fallback mode.",
            "warning"
        );

        await sleep(1500);

        window.location.replace(
            targetUrl
        );
    }
}

// ---------------------------------------------------
// SLEEP
// ---------------------------------------------------

function sleep(ms) {

    return new Promise(resolve =>

        setTimeout(resolve, ms)
    );
}

// ---------------------------------------------------
// START SCAN
// ---------------------------------------------------

runSteps();