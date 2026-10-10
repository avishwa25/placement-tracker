const body = document.getElementById("app-body");

async function loadApplications() {
    const res = await fetch("/api/applications");
    const apps = await res.json();
    body.innerHTML = "";

    apps.forEach(a => {
        const tr = document.createElement("tr");

        const company = document.createElement("td");
        if (a.job_link) {
            const link = document.createElement("a");
            link.href = a.job_link;
            link.target = "_blank";
            link.rel = "noopener";
            link.textContent = a.company_name;
            company.appendChild(link);
        } else {
            company.textContent = a.company_name;
        }

        const role = document.createElement("td");
        role.textContent = a.job_role;

        const applied = document.createElement("td");
        applied.textContent = a.applied_on;

        const statusTd = document.createElement("td");
        const select = document.createElement("select");
        STATUSES.forEach(s => {
            const opt = document.createElement("option");
            opt.value = s;
            opt.textContent = s;
            if (s === a.status) opt.selected = true;
            select.appendChild(opt);
        });
        select.addEventListener("change", async () => {
            await fetch(`/api/applications/${a.id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ status: select.value }),
            });
        });
        statusTd.appendChild(select);

        const notes = document.createElement("td");
        notes.textContent = a.notes || "";

        const actions = document.createElement("td");
        const del = document.createElement("button");
        del.textContent = "Delete";
        del.addEventListener("click", async () => {
            if (!confirm("Delete this application?")) return;
            await fetch(`/api/applications/${a.id}`, { method: "DELETE" });
            loadApplications();
        });
        actions.appendChild(del);

        tr.append(company, role, applied, statusTd, notes, actions);
        body.appendChild(tr);
    });
}

document.getElementById("add-form").addEventListener("submit", async e => {
    e.preventDefault();
    const payload = {
        company_name: document.getElementById("company").value,
        job_role: document.getElementById("role").value,
        job_link: document.getElementById("link").value,
        notes: document.getElementById("notes").value,
    };
    const res = await fetch("/api/applications", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
    if (res.ok) {
        e.target.reset();
        loadApplications();
    } else {
        const err = await res.json();
        alert(err.error || "Could not add application.");
    }
});

loadApplications();