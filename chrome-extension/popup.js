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

// --------------------------------------------------
// SET STATUS UI
// --------------------------------------------------

function setStatusUI(
    prediction,
    result
) {

    // RESET CLASSES

    statusCard.classList.remove(
        "safe",
        "malicious",
        "warning",
        "scanning",
        "error"
    );

    // --------------------------------------------------
    // SAFE
    // --------------------------------------------------

    if (
        prediction === "safe"
    ) {

        statusCard.classList.add(
            "safe"
        );

        statusText.textContent =
            "SAFE";

        riskLevel.textContent =
            "SAFE";
    }

    // --------------------------------------------------
    // MALICIOUS
    // --------------------------------------------------

    else if (
        prediction === "malicious"
    ) {

        statusCard.classList.add(
            "malicious"
        );

        statusText.textContent =
            "DANGEROUS";

        riskLevel.textContent =
            result.risk_level || "HIGH";
    }

    // --------------------------------------------------
    // ERROR
    // --------------------------------------------------

    else {

        statusCard.classList.add(
            "error"
        );

        statusText.textContent =
            "ERROR";

        riskLevel.textContent =
            "ERROR";
    }
}

// --------------------------------------------------
// UPDATE POPUP
// --------------------------------------------------

function updatePopup(
    scanData
) {

    if (!scanData) {

        statusCard.classList.add(
            "scanning"
        );

        statusText.textContent =
            "SCANNING";

        urlText.textContent =
            "Waiting for scan...";

        return;
    }

    const result =
        scanData.result;

    // URL

    urlText.textContent =
        scanData.url || "Unknown URL";

    // RISK SCORE

    riskScore.textContent =
        result.risk_score || 0;

    // CONFIDENCE

    confidence.textContent =
        `${(
            (result.confidence || 0) * 100
        ).toFixed(2)}%`;

    // UI STATE

    setStatusUI(
        result.prediction,
        result
    );
}

// --------------------------------------------------
// LOAD INITIAL DATA
// --------------------------------------------------

chrome.storage.local.get(
    ["latestScan"],
    (data) => {

        updatePopup(
            data.latestScan
        );
    }
);

// --------------------------------------------------
// LIVE REAL-TIME UPDATES
// --------------------------------------------------

chrome.storage.onChanged.addListener(

    (changes, areaName) => {

        if (
            areaName === "local" &&
            changes.latestScan
        ) {

            updatePopup(
                changes.latestScan.newValue
            );
        }
    }
);

// --------------------------------------------------
// AUTO REFRESH ACTIVE TAB
// --------------------------------------------------

setInterval(() => {

    chrome.storage.local.get(
        ["latestScan"],
        (data) => {

            updatePopup(
                data.latestScan
            );
        }
    );

}, 1000);

console.log(
    "Popup Live Monitoring Enabled"
);