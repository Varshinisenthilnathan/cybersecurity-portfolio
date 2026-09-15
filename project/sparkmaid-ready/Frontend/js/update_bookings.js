document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("updateBookingForm");
    const messageEl = document.getElementById("message");

    // Get booking_id from URL
    const urlParams = new URLSearchParams(window.location.search);
    const bookingId = urlParams.get("booking_id");

    if (!bookingId) {
        alert("Booking ID not found!");
        window.location.href = "/bookings.html";
        return;
    }

    // Fetch booking details by ID
    fetch(`http://127.0.0.1:5000/booking/${bookingId}`, {
        method: "GET",
        credentials: "include"
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            const booking = data.bookings;

            document.getElementById("booking_id").value = booking.booking_id || "";
            document.getElementById("customer_name").value = booking.customer_name || "";
            document.getElementById("maid_name").value = booking.maid_name || "";
            document.getElementById("service").value = booking.service || "";
            document.getElementById("duration").value = booking.duration || "";
            document.getElementById("payment").value = booking.payment || "";
            document.getElementById("status").value = booking.booking_status || "PENDING";
        } else {
            messageEl.style.color = "red";
            messageEl.textContent = data.message || "Booking not found.";
        }
    })
    .catch(err => {
        console.error("Error fetching booking details:", err);
        messageEl.style.color = "red";
        messageEl.textContent = "Failed to load booking data.";
    });

    // Handle form submission (update)
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const data = {
            service: document.getElementById("service").value,
            duration: document.getElementById("duration").value,
            payment: document.getElementById("payment").value,
            status: document.getElementById("status").value,
            updated_by: sessionStorage.getItem("name") || "admin"
        };

        fetch(`http://127.0.0.1:5000/booking/${bookingId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(result => {
            if (result.status === "success") {
                alert("Booking updated successfully!");
                window.location.href = "/bookings.html";
            } else {
                messageEl.style.color = "red";
                messageEl.textContent = result.message;
            }
        })
        .catch(err => {
            console.error("Error updating booking:", err);
            messageEl.style.color = "red";
            messageEl.textContent = "Error updating booking.";
        });
    });
});
