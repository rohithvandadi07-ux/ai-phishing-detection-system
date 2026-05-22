async function loadLatestScan() {

    const data =
        await chrome.storage.local.get(
            "latestScan"
        );

    if (!data.latestScan) {

        return;
    }

    const result =
        data.latestScan.result;

    const url =
        data.latestScan.url;

    // -------------------------------------------
    // ELEMENTS
    // -------------------------------------------

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

    // -------------------------------------------
    // VALUES
    // -------------------------------------------

    urlText.textContent =
        url;

    riskScore.textContent =
        result.risk_score;

    confidence.textContent =

        (
            result.confidence * 100
        ).toFixed(2) + "%";

    riskLevel.textContent =
        result.risk_level;

    // -------------------------------------------
    // STATUS
    // -------------------------------------------

    if (
        result.prediction ===
        "malicious"
    ) {

        statusCard.className =
            "status-card malicious";

        statusText.textContent =
            "MALICIOUS";
    }

    else {

        statusCard.className =
            "status-card safe";

        statusText.textContent =
            "SAFE";
    }
}

loadLatestScan();