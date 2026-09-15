document.addEventListener("DOMContentLoaded", () => {
    const adminContainer = document.getElementById("adminContainer");
    const messageEl = document.getElementById("message");

    // Helper to format date
    function formatDate(dateString) {
        if (!dateString) return "-";
        const date = new Date(dateString);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        return `${day}/${month}/${year}`;
    }

    // Load admins
    function loadAdmins() {
        fetch('http://127.0.0.1:5000/admins', {
            method: "GET",
            credentials: "include"
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success" && data.data.length > 0) {
                const admins = data.data;
                let cardsHTML = '';

                admins.forEach(admin => {
                    cardsHTML += `
                        <div class="admin-card" data-admin-id="${admin.admin_id}">
                            <div class="card-header">
                                <h3>${admin.name || "-"}</h3>
                                <button class="edit-btn" title="Edit Admin">✏️</button>
                            </div>
                            <div class="card-details">
                                <p><strong>Username:</strong> <span class="field" data-key="username">${admin.username || "-"}</span></p>
                                <p><strong>Email:</strong> <span class="field" data-key="email">${admin.email || "-"}</span></p>
                                <p><strong>Phone:</strong> <span class="field" data-key="phone_number">${admin.phone_number || "-"}</span></p>
                                <p><strong>Gender:</strong> <span class="field" data-key="gender">${admin.gender || "-"}</span></p>
                                <p><strong>Age:</strong> <span class="field" data-key="age">${admin.age || "-"}</span></p>
                                <p><strong>DOB:</strong> <span class="field" data-key="dob">${formatDate(admin.dob)}</span></p>
                                <p><strong>Address:</strong> <span class="field" data-key="address">${admin.address || "-"}</span></p>
                            </div>
                            <button class="save-btn" style="display:none;">💾 Save</button>
                        </div>
                    `;
                });

                adminContainer.innerHTML = cardsHTML;
                document.querySelectorAll(".admin-card").forEach(card => {
                    const editBtn = card.querySelector(".edit-btn");
                    const saveBtn = card.querySelector(".save-btn");
                    const fields = card.querySelectorAll(".field");

                    editBtn.addEventListener("click", () => {
                        fields.forEach(f => {
                            const key = f.dataset.key;
                            const value = f.textContent === "-" ? "" : f.textContent;

                            if (key === "dob") {
                                const [day, month, year] = value.split("/");
                                f.innerHTML = `<input type="date" class="input-field" value="${year}-${month}-${day}">`;
                            } else if (key === "gender") {
                                f.innerHTML = `
                                    <select class="input-field">
                                        <option value="Male" ${value==="Male"?"selected":""}>Male</option>
                                        <option value="Female" ${value==="Female"?"selected":""}>Female</option>
                                        <option value="Other" ${value==="Other"?"selected":""}>Other</option>
                                    </select>
                                `;
                            } else {
                                f.innerHTML = `<input type="text" class="input-field" value="${value}">`;
                            }
                        });
                        editBtn.style.display = "none";
                        saveBtn.style.display = "inline-block";
                    });

                    saveBtn.addEventListener("click", () => {
                        const adminId = card.dataset.adminId;
                        const updatedData = {};
                        fields.forEach(f => {
                            const key = f.dataset.key;
                            const input = f.querySelector(".input-field");
                            if (input) updatedData[key] = input.value;
                        });

                        fetch(`http://127.0.0.1:5000/admins/${adminId}`, {
                            method: "PUT",
                            headers: {"Content-Type":"application/json"},
                            credentials: "include",
                            body: JSON.stringify(updatedData)
                        })
                        .then(res => res.json())
                        .then(data => {
                            messageEl.style.color = data.status==="success"?"green":"red";
                            messageEl.textContent = data.message;
                            loadAdmins(); // reload cards after update
                        })
                        .catch(err => {
                            console.error(err);
                            messageEl.style.color = "red";
                            messageEl.textContent = "Error updating admin details.";
                        });
                    });
                });

            } else {
                messageEl.style.color = "red";
                messageEl.textContent = data.message || "No admin details found.";
            }
        })
        .catch(err => {
            console.error(err);
            messageEl.style.color = "red";
            messageEl.textContent = "Error fetching admin details.";
        });
    }

    // Initial load
    loadAdmins();

});
