document.addEventListener("DOMContentLoaded", () => {
    const customerId = sessionStorage.getItem("id");
    if (!customerId) {
        alert("Customer ID not found. Redirecting to dashboard.");
        window.location.href = "/dashboard_admin.html";
        return;
    }

    const bookingsContainer = document.getElementById("bookingsContainer");
    const messageEl = document.getElementById("message");

    fetch(`http://127.0.0.1:5000/booking/customer/${customerId}`, {
        method: "GET",
        credentials: "include"
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            const bookings = data.bookings;
            if (bookings.length === 0) {
                bookingsContainer.innerHTML = "<p>No bookings found.</p>";
                return;
            }

            let tableHTML = `
                <table class="bookings-table">
                    <thead>
                        <tr>
                            <th>Booking ID</th>
                            <th>Date & Time</th>
                            <th>Service</th>
                            <th>Maid</th>
                            <th>Maid Number</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${bookings.map(booking => `
                            <tr>
                                <td>${booking.booking_id}</td>
                                <td>${new Date(booking.booking_date).toLocaleString()}</td>
                                <td>${booking.service}</td>
                                <td>${booking.maid_name} </td>
                                 <td>${booking.maid_phone}</td>
                                <td class="${booking.status.toLowerCase()}">${booking.status}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            bookingsContainer.innerHTML = tableHTML;
        } else {
            messageEl.style.color = "red";
            messageEl.textContent = data.message;
        }
    })
    .catch(err => {
        console.error(err);
        messageEl.style.color = "red";
        messageEl.textContent = "Error fetching bookings.";
    });
});
