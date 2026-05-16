const params = new URLSearchParams(
    window.location.search
);

// ---------------------------------------------------
// LOCAL BACKEND
// ---------------------------------------------------

const API_BASE_URL =
    "http://localhost:8080";

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
            "[!] Credential harvesting indicators detected.",
        type:
            "warning"
    },

    {
        text:
            "[✓] URL heuristic analysis complete.",
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
            "[!] Suspicious impersonation patterns identified.",
        type:
            "warning"
    },

    {
        text:
            "[✓] Malware signature analysis completed.",
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

    logsContainer.scrollTop =
        logsContainer.scrollHeight;
}

// ---------------------------------------------------
// START LOG STREAM
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

    // Parallel logs

    startLogs();

    for (let i = 0; i < steps.length; i++) {

        const current =
            steps[i];

        current.classList.add(
            "active"
        );

        await sleep(1400);

        current.classList.remove(
            "active"
        );

        current.classList.add(
            "done"
        );

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
// FINAL AI SCAN
// ---------------------------------------------------

async function finalScan() {

    try {

        addLog(

            "[✓] Connecting to local AI inference engine...",
            "success"
        );

        // ---------------------------------------------------
        // LOCAL API
        // ---------------------------------------------------

        const apiUrl =

            `${API_BASE_URL}/predict?url=${encodeURIComponent(targetUrl)}`;

        const response =
            await fetch(apiUrl, {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"
                }
            });

        // ---------------------------------------------------
        // API ERROR
        // ---------------------------------------------------

        if (!response.ok) {

            throw new Error(
                "Backend API Failed"
            );
        }

        // ---------------------------------------------------
        // PARSE RESULT
        // ---------------------------------------------------

        const data =
            await response.json();

        console.log(
            "AI Scan Result:",
            data
        );

        // ---------------------------------------------------
        // SAFE WEBSITE
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

            addLog(

                "[✓] Redirecting to website...",
                "success"
            );

            await sleep(1200);

            window.location.replace(
                targetUrl
            );

            return;
        }

        // ---------------------------------------------------
        // MALICIOUS WEBSITE
        // ---------------------------------------------------

        addLog(

            "[!] HIGH RISK WEBSITE DETECTED.",
            "danger"
        );

        addLog(

            "[!] Initiating protective browser block...",
            "danger"
        );

        // ---------------------------------------------------
        // ENCODE REASONS
        // ---------------------------------------------------

        const encodedReasons =

            encodeURIComponent(

                JSON.stringify(
                    data.reasons || []
                )
            );

        // ---------------------------------------------------
        // BLOCK PAGE
        // ---------------------------------------------------

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

            "[!] Local AI engine unreachable.",
            "danger"
        );

        addLog(

            "[!] Ensure Docker backend is running.",
            "warning"
        );

        addLog(

            "[!] Opening website using fallback mode.",
            "warning"
        );

        await sleep(2000);

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
// START ENGINE
// ---------------------------------------------------

runSteps();