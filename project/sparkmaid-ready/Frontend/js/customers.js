document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.querySelector("#customersTable tbody");
    const messageEl = document.getElementById("message");

    const role = sessionStorage.getItem("role");
    if (!role || role !== "admin") {
        alert("Access denied! Admins only.");
        window.location.href = "/index.html";
        return;
    }

    // Function to load customers
    function loadCustomers() {
        tableBody.innerHTML = ""; // Clear previous rows
        fetch("http://127.0.0.1:5000/customers", {
            method: "GET",
            credentials: "include"
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success" && data.data.length > 0) {
                data.data.forEach(customer => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${customer.name || "-"}</td>
                        <td>${customer.username || "-"}</td>
                        <td>${customer.email || "-"}</td>
                        <td>${customer.phone_number || "-"}</td>
                        <td>${customer.gender || "-"}</td>
                        <td>${customer.address || "-"}</td>
                        <td>${customer.dob || "-"}</td>
                        <td>${customer.age || "-"}</td>
                        <td>${customer.service_registered || "-"}</td>
                        <td><span class="status-badge ${customer.status.toLowerCase()}">${customer.status}</span></td>
                        <td>${customer.created_date || "-"}</td>
                        <td>
                            <button class="action-btn update-btn" onclick="updateCustomer(${customer.customer_id})">Update</button>
                            <button class="action-btn delete-btn" onclick="deleteCustomer(${customer.customer_id})">Delete</button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });
            } else {
                messageEl.style.color = "red";
                messageEl.textContent = data.message || "No customers found.";
            }
        })
        .catch(err => {
            console.error(err);
            messageEl.style.color = "red";
            messageEl.textContent = "Error fetching customers.";
        });
    }

    // Initial load
    loadCustomers();

    // Delete function
    window.deleteCustomer = function(customerId) {
        if (!confirm("Are you sure you want to deactivate this customer?")) return;

        fetch(`http://127.0.0.1:5000/customer/${customerId}`, {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ deleted_by: role }) // Using session role as deleted_by
        })
        .then(res => res.json())
        .then(data => {
            messageEl.style.color = data.status === "success" ? "green" : "red";
            messageEl.textContent = data.message;
            loadCustomers(); // Reload table after deletion
        })
        .catch(err => {
            console.error(err);
            messageEl.style.color = "red";
            messageEl.textContent = "Error deleting customer.";
        });
    }

    // Update function (you can keep your existing logic)
    window.updateCustomer = function(customerId) {
        sessionStorage.setItem("customerId", customerId);
        window.location.href = "/update_customer.html";
    }
});
