const params = new URLSearchParams(window.location.search);

const blockedUrl = params.get("url");
const risk = params.get("risk");
const score = params.get("score");
const confidence = params.get("confidence");

// ---------------------------------------------------
// SET VALUES
// ---------------------------------------------------

document.getElementById("blocked-url").textContent =
    blockedUrl || "Unknown URL";

document.getElementById("risk-level").textContent =
    risk || "UNKNOWN";

document.getElementById("risk-score").textContent =
    score || "0";

document.getElementById("confidence").textContent =
    confidence || "0";

// ---------------------------------------------------
// BACK BUTTON
// ---------------------------------------------------

document.getElementById("back-button")
    .addEventListener("click", () => {

        window.location.href = "https://google.com";
    });