// ==========================================================================
// JobSafe AI - Model Benchmarks & Visual Analytics Dashboard
// Palette: PURPLE + BLUE + WHITE (Light SaaS Theme)
// ==========================================================================

document.addEventListener("DOMContentLoaded", function () {
    if (!window.METRICS_DATA) {
        return;
    }

    const metrics = window.METRICS_DATA;
    const modelNames = Object.keys(metrics.models);

    // 1. Model Comparison Bar Chart
    const compCanvas = document.getElementById("modelComparisonChart");
    if (compCanvas) {
        const accuracyData = modelNames.map(name => metrics.models[name].accuracy);
        const precisionData = modelNames.map(name => metrics.models[name].precision);
        const recallData = modelNames.map(name => metrics.models[name].recall);
        const f1Data = modelNames.map(name => metrics.models[name].f1_score);

        const ctx = compCanvas.getContext("2d");
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: modelNames,
                datasets: [
                    {
                        label: "Accuracy %",
                        data: accuracyData,
                        backgroundColor: "rgba(108, 43, 217, 0.9)", // Deep Purple #6C2BD9
                        borderColor: "#6C2BD9",
                        borderWidth: 1.5,
                        borderRadius: 6
                    },
                    {
                        label: "Precision %",
                        data: precisionData,
                        backgroundColor: "rgba(139, 92, 246, 0.9)", // Medium Purple #8B5CF6
                        borderColor: "#8B5CF6",
                        borderWidth: 1.5,
                        borderRadius: 6
                    },
                    {
                        label: "Recall %",
                        data: recallData,
                        backgroundColor: "rgba(168, 85, 247, 0.9)", // Accent Purple #A855F7
                        borderColor: "#A855F7",
                        borderWidth: 1.5,
                        borderRadius: 6
                    },
                    {
                        label: "F1-Score %",
                        data: f1Data,
                        backgroundColor: "rgba(192, 132, 252, 0.9)", // Soft Purple #C084FC
                        borderColor: "#C084FC",
                        borderWidth: 1.5,
                        borderRadius: 6
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
                            color: "#64748b",
                            font: { family: "'JetBrains Mono', monospace", size: 11 },
                            callback: function (val) {
                                return val + "%";
                            }
                        },
                        grid: {
                            color: "#f1f5f9"
                        }
                    },
                    x: {
                        ticks: {
                            color: "#334155",
                            font: { family: "'Plus Jakarta Sans', sans-serif", weight: '600', size: 12 }
                        },
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: "top",
                        labels: {
                            color: "#334155",
                            boxWidth: 12,
                            padding: 15,
                            font: {
                                family: "'Plus Jakarta Sans', sans-serif",
                                size: 12,
                                weight: '600'
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: "rgba(15, 23, 42, 0.92)",
                        titleColor: "#ffffff",
                        bodyColor: "#f8fafc",
                        borderColor: "rgba(124, 58, 237, 0.3)",
                        borderWidth: 1,
                        padding: 12,
                        callbacks: {
                            label: function (context) {
                                return ` ${context.dataset.label}: ${context.raw}%`;
                            }
                        }
                    }
                }
            }
        });
    }

    // 2. Class Distribution Doughnut Chart
    const distCanvas = document.getElementById("classDistributionChart");
    if (distCanvas && metrics.dataset_stats) {
        const realCount = metrics.dataset_stats.real_jobs || 2500;
        const fakeCount = metrics.dataset_stats.fake_jobs || 1500;

        const ctxDist = distCanvas.getContext("2d");
        new Chart(ctxDist, {
            type: "doughnut",
            data: {
                labels: ["Authentic Postings", "Fraudulent Postings"],
                datasets: [
                    {
                        data: [realCount, fakeCount],
                        backgroundColor: [
                            "#6C2BD9", // Brand Purple #6C2BD9
                            "#ef4444"  // Status Red
                        ],
                        borderColor: [
                            "#ffffff",
                            "#ffffff"
                        ],
                        borderWidth: 3,
                        hoverOffset: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "70%",
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: "rgba(15, 23, 42, 0.92)",
                        titleColor: "#ffffff",
                        bodyColor: "#f8fafc",
                        borderColor: "rgba(124, 58, 237, 0.3)",
                        borderWidth: 1,
                        padding: 10,
                        callbacks: {
                            label: function (context) {
                                const total = realCount + fakeCount;
                                const percentage = ((context.raw / total) * 100).toFixed(1);
                                return ` ${context.label}: ${context.raw} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
});
