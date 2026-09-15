document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.querySelector("#bookingsTable tbody");
    const messageEl = document.getElementById("message");
    const role = sessionStorage.getItem("role");

    // Allow only admin
    if (!role || role !== "admin") {
        alert("Access denied! Admins only.");
        window.location.href = "/index.html";
        return;
    }

    // Fetch all bookings
    fetch("http://127.0.0.1:5000/booking/admin", {
        method: "GET",
        credentials: "include"
    })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success" && data.bookings.length > 0) {
                data.bookings.forEach(b => {
                    const row = document.createElement("tr");

                    const statusClass = b.status
                        ? `status-${b.status.toLowerCase()}`
                        : "status-pending";

                    row.innerHTML = `
                        <td>${b.booking_id}</td>
                        <td>${b.customer_name || "-"}</td>
                        <td>${b.maid_name || "-"}</td>
                        <td>${b.service || "-"}</td>
                        <td>${b.duration || "-"}</td>
                        <td>${b.payment ? "₹" + b.payment : "-"}</td>
                        <td>${b.payment_date || "-"}</td>
                        <td><span class="status-badge ${statusClass}">${b.status}</span></td>
                        <td>${b.booking_date ? new Date(b.booking_date).toLocaleString() : "-"}</td>
                        <td>
                            <button class="edit-btn" onclick="editBooking(${b.booking_id})">✏️</button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });
            } else {
                messageEl.style.color = "red";
                messageEl.textContent = data.message || "No bookings found.";
            }
        })
        .catch(err => {
            console.error("Error fetching bookings:", err);
            messageEl.style.color = "red";
            messageEl.textContent = "Error loading booking data.";
        });
});


function editBooking(bookingId) {
    window.location.href = `/update_bookings.html?booking_id=${bookingId}`;
}
