// 🔒 Avoid running multiple times on same page
if (window.__phishing_checked__) {
    return;
}
window.__phishing_checked__ = true;

const currentUrl = window.location.href;

// 🚫 Ignore non-web pages
if (
    currentUrl.startsWith("chrome://") ||
    currentUrl.startsWith("edge://") ||
    currentUrl.startsWith("about:") ||
    currentUrl.startsWith("file://")
) {
    console.log("Skipping internal page");
    return;
}

// 🔥 Call backend
fetch(`http://127.0.0.1:8000/predict?url=${encodeURIComponent(currentUrl)}`, {
    method: "POST"
})
.then(res => res.json())
.then(data => {
    if (data.prediction === "malicious") {
        showWarning(data);
    }
})
.catch(err => {
    console.log("API not reachable", err);
});


// 🔴 FULL PAGE BLOCK
function showWarning(data) {

    const overlay = document.createElement("div");

    overlay.innerHTML = `
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #b00020;
            color: white;
            z-index: 999999;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-family: Arial;
            text-align: center;
            padding: 20px;
        ">
            <h1>⚠️ Phishing Warning</h1>

            <p>This website may be dangerous</p>

            <p><b>Confidence:</b> ${data.confidence.toFixed(4)}</p>

            <div style="margin: 15px;">
                ${data.why_flagged.join("<br>")}
            </div>

            <div style="margin-top:20px;">
                <button id="goBack" style="
                    padding:10px 20px;
                    margin-right:10px;
                    background:black;
                    color:white;
                    border:none;
                    cursor:pointer;
                ">
                    ⬅ Go Back
                </button>

                <button id="proceed" style="
                    padding:10px 20px;
                    background:orange;
                    color:black;
                    border:none;
                    cursor:pointer;
                ">
                    ⚠ Proceed Anyway
                </button>
            </div>
        </div>
    `;

    // Clear page and inject warning
    document.body.innerHTML = "";
    document.body.appendChild(overlay);

    // 🔙 Go back button
    document.getElementById("goBack").onclick = () => {
        window.history.back();
    };

    // ⚠ Proceed anyway
    document.getElementById("proceed").onclick = () => {
        location.reload();
    };
}