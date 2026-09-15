document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("createBookingForm");
    const messageEl = document.getElementById("message");

    // Bind customer ID from sessionStorage
    const customerId = sessionStorage.getItem("id");
    if (!customerId) {
        alert("Please login first!");
        window.location.href = "/index.html";
        return;
    }
    document.getElementById("customer_id").value = customerId;

    // Optional: created_by info from session
    const createdBy = sessionStorage.getItem("name") || "system";

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        data.created_by = createdBy;

        fetch("http://127.0.0.1:5000/booking", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(result => {
            if (result.status === "success") {
                messageEl.style.color = "green";
                messageEl.textContent = result.message;
                form.reset();

                setTimeout(() => {
                    window.location.href = "/show_maid.html";
                }, 1500);
            } else {
                messageEl.style.color = "red";
                messageEl.textContent = result.message;
            }
        })
        .catch(err => {
            console.error(err);
            messageEl.style.color = "red";
            messageEl.textContent = "Error creating booking.";
        });
    });
});
