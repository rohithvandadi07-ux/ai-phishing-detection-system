// --------------------------------------------------
// ELEMENTS
// --------------------------------------------------

const statusCard =
    document.getElementById(
        "statusCard"
    );

const statusText =
    document.getElementById(
        "statusText"
    );

const urlText =
    document.getElementById(
        "urlText"
    );

const riskScore =
    document.getElementById(
        "riskScore"
    );

const confidence =
    document.getElementById(
        "confidence"
    );

const riskLevel =
    document.getElementById(
        "riskLevel"
    );

const safeCount =
    document.getElementById(
        "safeCount"
    );

const blockedCount =
    document.getElementById(
        "blockedCount"
    );

const historyList =
    document.getElementById(
        "historyList"
    );

const reasonsList =
    document.getElementById(
        "reasonsList"
    );

const meterFill =
    document.getElementById(
        "meterFill"
    );

const threatPercent =
    document.getElementById(
        "threatPercent"
    );

const threatCircle =
    document.getElementById(
        "threatCircle"
    );

const lgbScore =
    document.getElementById(
        "lgbScore"
    );

const rfScore =
    document.getElementById(
        "rfScore"
    );

const bertScore =
    document.getElementById(
        "bertScore"
    );

const hybridScore =
    document.getElementById(
        "hybridScore"
    );

const scanStatus =
    document.getElementById(
        "scanStatus"
    );

const reputationLevel =
    document.getElementById(
        "reputationLevel"
    );

const threatReputation =
    document.getElementById(
        "threatReputation"
    );

const whoisScore =
    document.getElementById(
        "whoisScore"
    );

const vtStatus =
    document.getElementById(
        "vtStatus"
    );

const reputationScore =
    document.getElementById(
        "reputationScore"
    );
// --------------------------------------------------
// STATUS UI
// --------------------------------------------------

function setStatusUI(
    prediction,
    result
) {

    statusCard.classList.remove(
        "safe",
        "malicious",
        "warning",
        "error"
    );

    threatCircle.classList.remove(
        "safe-circle",
        "danger-circle"
    );

    // ----------------------------------------------
    // SAFE
    // ----------------------------------------------

    if (
        prediction === "safe"
    ) {

        statusCard.classList.add(
            "safe"
        );

        threatCircle.classList.add(
            "safe-circle"
        );

        statusText.textContent =
            "SAFE";

        riskLevel.textContent =
            "SAFE";

        scanStatus.textContent =
            "PROTECTED";
    }

    // ----------------------------------------------
    // MALICIOUS
    // ----------------------------------------------

    else if (
        prediction === "malicious"
    ) {

        statusCard.classList.add(
            "malicious"
        );

        threatCircle.classList.add(
            "danger-circle"
        );

        statusText.textContent =
            "DANGEROUS";

        riskLevel.textContent =
            result.risk_level || "HIGH";

        scanStatus.textContent =
            "THREAT BLOCKED";
    }

    // ----------------------------------------------
    // ERROR
    // ----------------------------------------------

    else {

        statusCard.classList.add(
            "warning"
        );

        statusText.textContent =
            "ERROR";

        riskLevel.textContent =
            "UNKNOWN";

        scanStatus.textContent =
            "SCAN FAILED";
    }
}

// --------------------------------------------------
// THREAT METER
// --------------------------------------------------

function updateThreatMeter(
    confidenceValue
) {

    const percentage = Math.min(
        Math.max(
            confidenceValue * 100,
            0
        ),
        100
    );

    meterFill.style.width =
        `${percentage}%`;

    threatPercent.textContent =
        `${percentage.toFixed(0)}%`;
}

// --------------------------------------------------
// AI ENGINE SCORES
// --------------------------------------------------

function updateAIScores(
    ai
) {

    if (!ai) {

        lgbScore.textContent = "0%";
        rfScore.textContent = "0%";
        bertScore.textContent = "0%";
        hybridScore.textContent = "0%";

        return;
    }

    lgbScore.textContent =
        `${(
            (ai.lgb_probability || 0) * 100
        ).toFixed(0)}%`;

    rfScore.textContent =
        `${(
            (ai.rf_probability || 0) * 100
        ).toFixed(0)}%`;

    bertScore.textContent =
        `${(
            (ai.semantic_confidence || 0) * 100
        ).toFixed(0)}%`;

    hybridScore.textContent =
        `${(
            (ai.hybrid_probability || 0) * 100
        ).toFixed(0)}%`;
}


// --------------------------------------------------
// CLEAN REASON TEXT
// --------------------------------------------------

function cleanReasonText(
    text
) {

    if (!text) {

        return "";
    }

    return text

        // remove broken unicode chars

        .replace(/[^\x20-\x7E]/g, "")

        // remove duplicate spaces

        .replace(/\s+/g, " ")

        .trim();
}

// --------------------------------------------------
// AI THREAT ANALYSIS
// --------------------------------------------------

function renderReasons(
    result
) {

    reasonsList.innerHTML = "";

    // ----------------------------------------------
    // IGNORE SAFE / INFORMATIONAL REASONS
    // ----------------------------------------------

    const ignoredReasons = [

        "Old established domain",

        "Registrar not in trusted list",

        "Trusted registrar detected",

        "SAFE domain detected",

        "Domain age indicates legitimacy"

    ];

    const filteredReasons = (

        result.reasons || []

    ).filter(

        reason => !ignoredReasons.includes(reason)

    );

    // ----------------------------------------------
    // NO THREAT REASONS
    // ----------------------------------------------

    if (

        filteredReasons.length === 0

    ) {

        reasonsList.innerHTML =

            `
            <div class="reason-item safe-reason">

                <span class="reason-dot safe-dot"></span>

                <span class="reason-text">
                    No threat indicators detected
                </span>

            </div>
            `;

        return;
    }

    // ----------------------------------------------
    // SHOW REASONS
    // ----------------------------------------------

    filteredReasons
        .slice(0, 6)
        .forEach((reason) => {

            const cleanReason =
                cleanReasonText(reason);

            const div =
                document.createElement(
                    "div"
                );

            div.className =
                "reason-item";

            div.innerHTML =

                `
                <span class="reason-dot"></span>

                <span class="reason-text">
                    ${cleanReason}
                </span>
                `;

            reasonsList.appendChild(
                div
            );
        });
}

// --------------------------------------------------
// HISTORY
// --------------------------------------------------

function renderHistory(
    history
) {

    historyList.innerHTML = "";

    if (
        !history ||
        history.length === 0
    ) {

        historyList.innerHTML =

            `
            <p class="empty">

                No scans yet

            </p>
            `;

        return;
    }

    history
        .slice(-10)
        .reverse()
        .forEach((item) => {

            const div =
                document.createElement(
                    "div"
                );

            div.className =
                `history-item ${item.result.prediction}`;

            div.innerHTML =

                `
                <div class="history-url">
                    ${item.url}
                </div>

                <div class="history-status">

                    ${item.result.prediction.toUpperCase()}
                    •
                    Risk:
                    ${item.result.risk_score}

                </div>
                `;

            historyList.appendChild(
                div
            );
        });
}

// --------------------------------------------------
// ANALYTICS
// --------------------------------------------------

function updateAnalytics(
    history
) {

    if (!history) {

        safeCount.textContent = 0;

        blockedCount.textContent = 0;

        return;
    }

    const safeTotal =

        history.filter(
            item =>
                item.result.prediction ===
                "safe"
        ).length;

    const blockedTotal =

        history.filter(
            item =>
                item.result.prediction ===
                "malicious"
        ).length;

    safeCount.textContent =
        safeTotal;

    blockedCount.textContent =
        blockedTotal;
}

// --------------------------------------------------
// MAIN POPUP UPDATE
// --------------------------------------------------

function updatePopup(
    latestScan,
    history
) {

    if (!latestScan) {

        statusText.textContent =
            "SCANNING";

        urlText.textContent =
            "Waiting for scan...";

        return;
    }

    const result =
        latestScan.result;

    // ----------------------------------------------
    // URL
    // ----------------------------------------------

    urlText.textContent =
        latestScan.url ||
        "Unknown URL";

    // ----------------------------------------------
    // SCORE
    // ----------------------------------------------

    riskScore.textContent =
        result.risk_score || 0;

    // ----------------------------------------------
    // CONFIDENCE
    // ----------------------------------------------

    confidence.textContent =
        `${(
            (result.confidence || 0) * 100
        ).toFixed(2)}%`;

    // ----------------------------------------------
    // THREAT METER
    // ----------------------------------------------

    updateThreatMeter(
        result.confidence || 0
    );

    // ----------------------------------------------
    // STATUS
    // ----------------------------------------------

    setStatusUI(
        result.prediction,
        result
    );

    // ----------------------------------------------
    // AI SCORES
    // ----------------------------------------------

    updateAIScores(
        result.ai_engine
    );

    updateThreatIntel(
        result.ai_engine
    );

    // ----------------------------------------------
    // REASONS
    // ----------------------------------------------

    renderReasons(
        result
    );

    // ----------------------------------------------
    // ANALYTICS
    // ----------------------------------------------

    updateAnalytics(
        history
    );

    // ----------------------------------------------
    // HISTORY
    // ----------------------------------------------

    renderHistory(
        history
    );
}

// --------------------------------------------------
// LOAD DASHBOARD
// --------------------------------------------------

function loadDashboard() {

    chrome.storage.local.get(

        [
            "latestScan",
            "scanHistory"
        ],

        (data) => {

            updatePopup(
                data.latestScan,
                data.scanHistory || []
            );
        }
    );
}

// --------------------------------------------------
// LIVE STORAGE UPDATE
// --------------------------------------------------

chrome.storage.onChanged.addListener(

    (changes, areaName) => {

        if (
            areaName === "local"
        ) {

            loadDashboard();
        }
    }
);

// --------------------------------------------------
// AUTO REFRESH
// --------------------------------------------------

setInterval(() => {

    loadDashboard();

}, 1500);

// --------------------------------------------------
// START
// --------------------------------------------------

loadDashboard();

console.log(
    "Enterprise AI Cybersecurity Dashboard Loaded"
);

function updateThreatIntel(ai) {

    console.log("AI ENGINE:", ai);

    if (!ai) return;

    
    const domainAge =
        document.getElementById(
            "domainAge"
        );

    const vtDetections =
        document.getElementById(
            "vtDetections"
        );

    const trustScore =
        document.getElementById(
            "trustScore"
        );

    const threatReputation =
        document.getElementById(
            "threatReputation"
        );

    const reputationLevel =
        document.getElementById(
            "reputationLevel"
        );

    if (threatReputation)
        threatReputation.innerText =
            ai.reputation_level ?? "SAFE";

    if (reputationLevel)
        reputationLevel.innerText =
            ai.reputation_level ?? "SAFE";

    if (domainAge)
        domainAge.innerText =
            ai.domain_age_days
                ? `${ai.domain_age_days}d`
                : "--";

    if (vtDetections)
        vtDetections.innerText =
            ai.virustotal_detections ?? "0";

    if (trustScore)
        trustScore.innerText =
            ai.trust_score ?? "--";

    }