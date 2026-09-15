document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("updateCustomerForm");
    const messageEl = document.getElementById("message");
    const customerId = sessionStorage.getItem("customerId");

    if (!customerId) {
        alert("Customer ID not found.");
        window.location.href = "/customerList.html";
        return;
    }

    // Fetch existing customer details
    fetch(`http://127.0.0.1:5000/customer/${customerId}`, {
        method: "GET",
        credentials: "include"
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            const customer = data.data;
            document.getElementById("name").value = customer.name || "";
            document.getElementById("username").value = customer.username || "";
            document.getElementById("email").value = customer.email || "";
            document.getElementById("phone_number").value = customer.phone_number || "";
            document.getElementById("gender").value = customer.gender || "Male";
            document.getElementById("address").value = customer.address || "";
            document.getElementById("dob").value = customer.dob ? new Date(customer.dob).toISOString().split("T")[0] : "";
            document.getElementById("service_registered").value = customer.service_registered || "";
        } else {
            messageEl.style.color = "red";
            messageEl.textContent = data.message || "Customer not found.";
        }
    })
    .catch(err => {
        console.error(err);
        messageEl.style.color = "red";
        messageEl.textContent = "Error fetching customer details.";
    });

    // Submit updated data
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        fetch(`http://127.0.0.1:5000/customer/${customerId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(result => {
            if (result.status === "success") {
                // Show success message briefly
                messageEl.style.color = "green";
                messageEl.textContent = result.message;

                // Redirect back to customer list after 1.5 seconds
                setTimeout(() => {
                    window.location.href = "/customers.html";
                }, 1000);
            } else {
                messageEl.style.color = "red";
                messageEl.textContent = result.message;
            }
        })
        .catch(err => {
            console.error(err);
            messageEl.style.color = "red";
            messageEl.textContent = "Error updating customer.";
        });
    });
});
