async function loadStats() {
    const res = await fetch("/api/stats");
    const counts = await res.json();

    const labels = Object.keys(counts);
    const values = Object.values(counts);
    const total = values.reduce((a, b) => a + b, 0);

    document.getElementById("card-total").textContent = total;
    document.getElementById("card-interview").textContent = counts["Interview"] || 0;
    document.getElementById("card-offer").textContent = counts["Offer"] || 0;

    if (total === 0) {
        document.getElementById("empty-msg").style.display = "block";
        return;
    }

    new Chart(document.getElementById("status-chart"), {
        type: "doughnut",
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: ["#4e79a7", "#f28e2b", "#edc948", "#59a14f", "#e15759"],
            }],
        },
        options: {
            plugins: { legend: { position: "bottom" } },
        },
    });
}

loadStats();