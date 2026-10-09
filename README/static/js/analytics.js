document.addEventListener("DOMContentLoaded", function () {
    if (!window.METRICS_DATA || !document.getElementById("modelComparisonChart")) {
        return;
    }

    const metrics = window.METRICS_DATA;
    const modelNames = Object.keys(metrics.models);
    
    const accuracyData = modelNames.map(name => metrics.models[name].accuracy);
    const precisionData = modelNames.map(name => metrics.models[name].precision);
    const recallData = modelNames.map(name => metrics.models[name].recall);
    const f1Data = modelNames.map(name => metrics.models[name].f1_score);

    const ctx = document.getElementById("modelComparisonChart").getContext("2d");
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: modelNames,
            datasets: [
                {
                    label: "Accuracy %",
                    data: accuracyData,
                    backgroundColor: "rgba(59, 130, 246, 0.8)",
                    borderRadius: 4
                },
                {
                    label: "Precision %",
                    data: precisionData,
                    backgroundColor: "rgba(16, 185, 129, 0.8)",
                    borderRadius: 4
                },
                {
                    label: "Recall %",
                    data: recallData,
                    backgroundColor: "rgba(245, 158, 11, 0.8)",
                    borderRadius: 4
                },
                {
                    label: "F1 Score %",
                    data: f1Data,
                    backgroundColor: "rgba(139, 92, 246, 0.8)",
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    min: 90,
                    max: 100,
                    ticks: {
                        callback: function (val) {
                            return val + "%";
                        }
                    },
                    grid: {
                        color: "#f1f5f9"
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            plugins: {
                legend: {
                    position: "top",
                    labels: {
                        boxWidth: 12,
                        font: {
                            family: "'Plus Jakarta Sans', sans-serif",
                            size: 11
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `${context.dataset.label}: ${context.raw}%`;
                        }
                    }
                }
            }
        }
    });
});
