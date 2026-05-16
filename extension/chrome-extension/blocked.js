const params = new URLSearchParams(
    window.location.search
);

// ---------------------------------------------------
// URL PARAMETERS
// ---------------------------------------------------

const blockedUrl =
    params.get("url");

const risk =
    params.get("risk");

const score =
    params.get("score");

const confidence =
    params.get("confidence");

const reasons =
    params.get("reasons");

// ---------------------------------------------------
// BASIC INFO
// ---------------------------------------------------

document.getElementById(
    "blocked-url"
).textContent =
    blockedUrl || "Unknown URL";

document.getElementById(
    "risk-level"
).textContent =
    risk || "UNKNOWN";

document.getElementById(
    "risk-score"
).textContent =
    score || "0";

document.getElementById(
    "confidence"
).textContent =
    confidence || "0";

// ---------------------------------------------------
// THREAT REASONS CONTAINER
// ---------------------------------------------------

const reasonsContainer =
    document.getElementById(
        "reasons-list"
    );

// ---------------------------------------------------
// DEFAULT REASON
// ---------------------------------------------------

let parsedReasons = [

    "Hybrid AI engine detected suspicious behavior."
];

// ---------------------------------------------------
// PARSE REAL REASONS
// ---------------------------------------------------

if (reasons) {

    try {

        parsedReasons = JSON.parse(

            decodeURIComponent(reasons)
        );

    } catch (e) {

        console.error(
            "Reason parsing failed:",
            e
        );
    }
}

// ---------------------------------------------------
// ICON DETECTION
// ---------------------------------------------------

function getThreatIcon(reason) {

    const lower =
        reason.toLowerCase();

    if (
        lower.includes("bert") ||
        lower.includes("semantic")
    ) {

        return "🧠";
    }

    if (
        lower.includes("virus") ||
        lower.includes("malware")
    ) {

        return "☣️";
    }

    if (
        lower.includes("login") ||
        lower.includes("credential")
    ) {

        return "🔐";
    }

    if (
        lower.includes("paypal") ||
        lower.includes("bank")
    ) {

        return "🏦";
    }

    if (
        lower.includes("domain")
    ) {

        return "🌐";
    }

    if (
        lower.includes("phishing")
    ) {

        return "🎣";
    }

    return "⚠️";
}

// ---------------------------------------------------
// SEVERITY DETECTION
// ---------------------------------------------------

function getSeverity(reason) {

    const lower =
        reason.toLowerCase();

    if (

        lower.includes("critical") ||
        lower.includes("virus") ||
        lower.includes("malware")

    ) {

        return "critical";
    }

    if (

        lower.includes("phishing") ||
        lower.includes("credential") ||
        lower.includes("login")

    ) {

        return "high";
    }

    return "medium";
}

// ---------------------------------------------------
// RENDER THREAT CARDS
// ---------------------------------------------------

parsedReasons.forEach((reason, index) => {

    const div =
        document.createElement("div");

    div.className =
        "reason-item";

    // Animation delay
    div.style.animationDelay =
        `${index * 0.08}s`;

    const severity =
        getSeverity(reason);

    // Dynamic border color
    if (severity === "critical") {

        div.style.borderLeft =
            "5px solid #ff2d2d";
    }

    else if (severity === "high") {

        div.style.borderLeft =
            "5px solid #ff7b00";
    }

    else {

        div.style.borderLeft =
            "5px solid #00eaff";
    }

    const icon =
        getThreatIcon(reason);

    div.innerHTML = `

        <div style="
            display:flex;
            align-items:center;
            gap:12px;
        ">

            <div style="
                font-size:22px;
            ">

                ${icon}

            </div>

            <div style="
                flex:1;
            ">

                <div style="
                    font-weight:700;
                    margin-bottom:4px;
                    color:white;
                ">

                    ${severity.toUpperCase()} RISK

                </div>

                <div style="
                    color:#ffdede;
                    line-height:1.6;
                ">

                    ${reason}

                </div>

            </div>

        </div>
    `;

    reasonsContainer.appendChild(div);
});

// ---------------------------------------------------
// RETURN TO SAFETY
// ---------------------------------------------------

document.getElementById(
    "back-button"
).addEventListener(
    "click",
    () => {

        window.location.href =
            "https://google.com";
    }
);

// ---------------------------------------------------
// PROCEED ANYWAY
// ---------------------------------------------------

document.getElementById(
    "proceed-button"
).addEventListener(
    "click",
    () => {

        const confirmProceed =
            confirm(

                "WARNING:\n\nThis website may steal passwords, banking information, or sensitive data.\n\nProceed at your own risk."

            );

        if (
            confirmProceed &&
            blockedUrl
        ) {

            window.location.href =
                blockedUrl;
        }
    }
);

// ---------------------------------------------------
// DYNAMIC SCORE COLORS
// ---------------------------------------------------

const riskLevel =
    (risk || "").toUpperCase();

const scoreElement =
    document.getElementById(
        "risk-score"
    );

if (riskLevel === "CRITICAL") {

    scoreElement.style.color =
        "#ff2d2d";
}

else if (riskLevel === "HIGH") {

    scoreElement.style.color =
        "#ff5c5c";
}

else if (riskLevel === "MEDIUM") {

    scoreElement.style.color =
        "#ffb020";
}

else {

    scoreElement.style.color =
        "#00ff9d";
}

// ---------------------------------------------------
// LIVE STATUS EFFECT
// ---------------------------------------------------

const statusElement =
    document.querySelector(
        ".status"
    );

let glow = true;

setInterval(() => {

    if (!statusElement) return;

    if (glow) {

        statusElement.style.boxShadow =
            "0 0 18px rgba(255,0,0,0.7)";
    }

    else {

        statusElement.style.boxShadow =
            "0 0 4px rgba(255,0,0,0.2)";
    }

    glow = !glow;

}, 700);