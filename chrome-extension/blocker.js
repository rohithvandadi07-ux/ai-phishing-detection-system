const params =
    new URLSearchParams(
        window.location.search
    );

const url =
    params.get("url") || "";

const risk =
    params.get("risk") || "0";

const level =
    params.get("level") || "UNKNOWN";

const confidence =
    params.get("confidence") || "0";

document.getElementById(
    "blockedUrl"
).innerText = url;

document.getElementById(
    "riskScore"
).innerText = risk;

document.getElementById(
    "threatLevel"
).innerText = level;

document.getElementById(
    "confidence"
).innerText =
    `${(
        Number(confidence) * 100
    ).toFixed(1)}%`;

const reasonsDiv =
    document.getElementById(
        "reasons"
    );

chrome.storage.local.get(
    "latestScan",
    (data) => {

        const reasons =
            data?.latestScan?.result?.reasons || [];

        reasons.forEach(
            reason => {

                const div =
                    document.createElement(
                        "div"
                    );

                div.className =
                    "reason";

                div.innerText =
                    reason;

                reasonsDiv.appendChild(
                    div
                );
            }
        );
    }
);

// -------------------------------------
// BUTTONS
// -------------------------------------

const goBackBtn =
    document.getElementById(
        "goBack"
    );

const proceedBtn =
    document.getElementById(
        "proceed"
    );

if (goBackBtn) {

    goBackBtn.onclick = () => {

        window.location.href =
            "https://www.google.com";

    };
}

// -------------------------------------
// AUTO RETURN COUNTDOWN
// -------------------------------------

let countdown = 10;

let timer = null;

if (proceedBtn) {

    proceedBtn.disabled = true;

    proceedBtn.textContent =
        `Continue At My Own Risk (${countdown})`;

    timer = setInterval(() => {

        countdown--;

        if (countdown > 0) {

            proceedBtn.textContent =
                `Continue At My Own Risk (${countdown})`;

        } else {

            clearInterval(
                timer
            );

            proceedBtn.disabled =
                false;

            proceedBtn.textContent =
                "Continue At My Own Risk";
        }

    }, 1000);

    proceedBtn.onclick = () => {

        clearInterval(
            timer
        );

        window.location.href =
            url;
    };
}