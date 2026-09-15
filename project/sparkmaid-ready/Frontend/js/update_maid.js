document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("updateMaidForm");
    const messageEl = document.getElementById("message");

    // Get maid_id from URL query
    const urlParams = new URLSearchParams(window.location.search);
    const maidId = urlParams.get("maid_id");

    if (!maidId) {
        alert("Maid ID not found.");
        window.location.href = "/maid.html";
        return;
    }

    // Fetch existing maid details
    fetch(`http://127.0.0.1:5000/maid/${maidId}`, { method: "GET", credentials: "include" })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            const maid = data.data;
            document.getElementById("name").value = maid.name || "";
            document.getElementById("phone_number").value = maid.phone_number || "";
            document.getElementById("email").value = maid.email || "";
            document.getElementById("gender").value = maid.gender || "Male";
            document.getElementById("dob").value = maid.dob ? new Date(maid.dob).toISOString().split("T")[0] : "";
            document.getElementById("service").value = maid.service || "";
            document.getElementById("experience_years").value = maid.experience_years || "";
            document.getElementById("salary").value = maid.salary || "";
            document.getElementById("availability_status").value = maid.availability_status || "AVAILABLE";
        } else {
            messageEl.style.color = "red";
            messageEl.textContent = data.message || "Maid not found.";
        }
    });

    // Submit updated data
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        data.updated_by = sessionStorage.getItem("name") || "admin";

        fetch(`http://127.0.0.1:5000/maid/${maidId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(result => {
            if (result.status === "success") {
                alert(result.message);
                window.location.href = "/maid.html";
            } else {
                messageEl.style.color = "red";
                messageEl.textContent = result.message;
            }
        })
        .catch(err => {
            console.error(err);
            messageEl.style.color = "red";
            messageEl.textContent = "Error updating maid.";
        });
    });
});
