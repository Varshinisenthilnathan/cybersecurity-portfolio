document.addEventListener("DOMContentLoaded", () => {
    const customerId = sessionStorage.getItem("id");
    if (!customerId) {
        alert("No customer selected. Redirecting to dashboard.");
        window.location.href = "/dashboard_admin.html";
        return;
    }

    const profileContainer = document.getElementById("profileContainer");

    // Format DOB as dd/mm/yyyy for display
    function formatDOB(dateString) {
        if (!dateString) return "-";
        const date = new Date(dateString);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        return `${day}/${month}/${year}`;
    }

    // Fetch customer details
    function loadProfile() {
        fetch(`http://127.0.0.1:5000/customer/${customerId}`, {
            method: "GET",
            credentials: "include"
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                const customer = data.data;
                profileContainer.innerHTML = `
                    <h2>Customer Profile</h2>
                    <div class="profile-details">
                        <p><strong>Name:</strong> <span id="name">${customer.name}</span></p>
                        <p><strong>Email:</strong> <span id="email">${customer.email}</span></p>
                        <p><strong>Phone:</strong> <span id="phone_number">${customer.phone_number}</span></p>
                        <p><strong>Address:</strong> <span id="address">${customer.address}</span></p>
                        <p><strong>Username:</strong> <span id="username">${customer.username}</span></p>
                        <p><strong>Gender:</strong> <span id="gender">${customer.gender || "-"}</span></p>
                        <p><strong>Age:</strong> <span id="age">${customer.age || "-"}</span></p>
                        <p><strong>DOB:</strong> <span id="dob">${formatDOB(customer.dob)}</span></p>
                        <p><strong>Service Registered:</strong> <span id="service_registered">${customer.service_registered}</span></p>
                    </div>
                    <div id="buttons">
                        <button id="editBtn" class="edit-btn">Edit</button>
                        <button id="saveBtn" class="save-btn" style="display:none;">Save</button>
                    </div>
                    <p id="message"></p>
                `;

                const editBtn = document.getElementById("editBtn");
                const saveBtn = document.getElementById("saveBtn");
                editBtn.addEventListener("click", () => enableEdit(customer));
                saveBtn.addEventListener("click", saveChanges);
            } else {
                profileContainer.innerHTML = `<p style="color:red">${data.message}</p>`;
            }
        })
        .catch(err => {
            console.error(err);
            profileContainer.innerHTML = `<p style="color:red">Error fetching customer details.</p>`;
        });
    }

    // Enable editing
    function enableEdit(customer) {
        const fields = ["name","email","phone_number","address","username","gender","age","dob","service_registered"];
        fields.forEach(f => {
            const span = document.getElementById(f);
            const value = customer[f] || "";

            if(f === "dob") {
                // Show calendar input, bind existing value in yyyy-mm-dd format
                const isoDate = value ? new Date(value).toISOString().split("T")[0] : "";
                span.innerHTML = `<input type="date" id="input_${f}" value="${isoDate}">`;
            } else if(f === "gender") {
                span.innerHTML = `
                    <select id="input_${f}">
                        <option value="Male" ${value === "Male" ? "selected" : ""}>Male</option>
                        <option value="Female" ${value === "Female" ? "selected" : ""}>Female</option>
                        <option value="Other" ${value === "Other" ? "selected" : ""}>Other</option>
                    </select>
                `;
            } else {
                span.innerHTML = `<input type="text" id="input_${f}" value="${value}">`;
            }
        });

        document.getElementById("editBtn").style.display = "none";
        document.getElementById("saveBtn").style.display = "inline-block";
    }

    // Save changes
    function saveChanges() {
        const updatedData = {
            name: document.getElementById("input_name").value,
            email: document.getElementById("input_email").value,
            phone_number: document.getElementById("input_phone_number").value,
            address: document.getElementById("input_address").value,
            username: document.getElementById("input_username").value,
            gender: document.getElementById("input_gender").value,
            age: document.getElementById("input_age").value,
            dob: document.getElementById("input_dob").value,
            service_registered: document.getElementById("input_service_registered").value
        };

        fetch(`http://127.0.0.1:5000/customer/${customerId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify(updatedData)
        })
        .then(res => res.json())
        .then(data => {
            const messageEl = document.getElementById("message");
            if (data.status === "success") {
                messageEl.style.color = "green";
                messageEl.textContent = data.message;
                loadProfile(); // Reload profile after update
            } else {
                messageEl.style.color = "red";
                messageEl.textContent = data.message;
            }
        })
        .catch(err => {
            console.error(err);
            const messageEl = document.getElementById("message");
            messageEl.style.color = "red";
            messageEl.textContent = "Error updating customer details.";
        });
    }

    // Initial load
    loadProfile();
});
