const historyBody =
    document.getElementById(
        "history-body"
    );

// ---------------------------------------------------
// LOAD HISTORY
// ---------------------------------------------------

chrome.storage.local.get(

    ["phishingHistory"],

    (result) => {

        const history =
            result.phishingHistory || [];

        // ---------------------------------------------------
        // COUNTERS
        // ---------------------------------------------------

        let totalScans = 0;

        let safeSites = 0;

        let blockedSites = 0;

        let mediumSites = 0;

        let highRisk = 0;

        let criticalRisk = 0;

        // ---------------------------------------------------
        // UPDATE COUNTERS
        // ---------------------------------------------------

        totalScans =
            history.length;

        history.forEach(item => {

            // SAFE

            if (
                item.prediction === "safe"
            ) {

                safeSites++;
            }

            // MALICIOUS

            else {

                blockedSites++;
            }

            // MEDIUM

            if (
                item.risk === "MEDIUM"
            ) {

                mediumSites++;
            }

            // HIGH

            if (
                item.risk === "HIGH"
            ) {

                highRisk++;
            }

            // CRITICAL

            if (
                item.risk === "CRITICAL"
            ) {

                criticalRisk++;
            }
        });

        // ---------------------------------------------------
        // UPDATE UI STATS
        // ---------------------------------------------------

        document.getElementById(
            "total-scans"
        ).textContent =
            totalScans;

        document.getElementById(
            "safe-sites"
        ).textContent =
            safeSites;

        document.getElementById(
            "blocked-sites"
        ).textContent =
            blockedSites;

        document.getElementById(
            "medium-sites"
        ).textContent =
            mediumSites;

        // ---------------------------------------------------
        // EMPTY STATE
        // ---------------------------------------------------

        if (history.length === 0) {

            const row =
                document.createElement("tr");

            row.innerHTML = `

                <td colspan="5"
                    style="
                        text-align:center;
                        padding:40px;
                        color:#8aa0b8;
                    "
                >

                    No scan activity found.

                </td>
            `;

            historyBody.appendChild(row);
        }

        // ---------------------------------------------------
        // RENDER HISTORY
        // ---------------------------------------------------

        history.forEach(item => {

            const row =
                document.createElement("tr");

            // ---------------------------------------------------
            // RISK COLORS
            // ---------------------------------------------------

            let riskClass =
                "risk-safe";

            if (

                item.risk === "HIGH" ||
                item.risk === "CRITICAL"

            ) {

                riskClass =
                    "risk-high";
            }

            else if (
                item.risk === "MEDIUM"
            ) {

                riskClass =
                    "risk-medium";
            }

            // ---------------------------------------------------
            // CONFIDENCE FORMAT
            // ---------------------------------------------------

            let confidence =
                item.confidence;

            if (
                confidence === undefined ||
                confidence === null
            ) {

                confidence = "N/A";
            }

            // ---------------------------------------------------
            // TABLE ROW
            // ---------------------------------------------------

            row.innerHTML = `

                <td class="url">

                    ${item.url}

                </td>

                <td>

                    ${item.prediction}

                </td>

                <td class="${riskClass}">

                    ${item.risk}

                </td>

                <td>

                    ${confidence}

                </td>

                <td>

                    ${item.time}

                </td>
            `;

            historyBody.appendChild(row);
        });

        // ---------------------------------------------------
        // PIE CHART
        // ---------------------------------------------------

        const pieCtx =
            document.getElementById(
                "pieChart"
            );

        new Chart(pieCtx, {

            type: "doughnut",

            data: {

                labels: [

                    "Safe",
                    "Blocked",
                    "Medium"

                ],

                datasets: [{

                    data: [

                        safeSites,
                        blockedSites,
                        mediumSites
                    ],

                    backgroundColor: [

                        "#00ff99",
                        "#ff4d4d",
                        "#ffb020"
                    ],

                    borderWidth: 0
                }]
            },

            options: {

                responsive: true,

                plugins: {

                    legend: {

                        labels: {

                            color: "white"
                        }
                    }
                }
            }
        });

        // ---------------------------------------------------
        // BAR CHART
        // ---------------------------------------------------

        const barCtx =
            document.getElementById(
                "barChart"
            );

        new Chart(barCtx, {

            type: "bar",

            data: {

                labels: [

                    "Safe",
                    "Medium",
                    "High",
                    "Critical"

                ],

                datasets: [{

                    label: "Threat Analytics",

                    data: [

                        safeSites,
                        mediumSites,
                        highRisk,
                        criticalRisk
                    ],

                    backgroundColor: [

                        "#00ff99",
                        "#ffb020",
                        "#ff7a00",
                        "#ff2d2d"
                    ],

                    borderRadius: 10
                }]
            },

            options: {

                responsive: true,

                scales: {

                    y: {

                        ticks: {

                            color: "white"
                        },

                        grid: {

                            color:
                                "rgba(255,255,255,0.08)"
                        }
                    },

                    x: {

                        ticks: {

                            color: "white"
                        },

                        grid: {

                            display: false
                        }
                    }
                },

                plugins: {

                    legend: {

                        labels: {

                            color: "white"
                        }
                    }
                }
            }
        });
    }
);