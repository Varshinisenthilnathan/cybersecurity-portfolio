document.addEventListener("DOMContentLoaded", () => {
    const maidContainer = document.getElementById("maidContainer");
    const filterAvailability = document.getElementById("filterAvailability");
    const filterGender = document.getElementById("filterGender");
    const filterService = document.getElementById("filterService");
    const applyFiltersBtn = document.getElementById("applyFilters");

    if (createMaidBtn) {
        createMaidBtn.addEventListener("click", () => {
            window.location.href = "/create_maid.html";
        });
    }
    // Function to redirect to update page
    window.editMaid = function(maidId) {
        window.location.href = `/update_maid.html?maid_id=${maidId}`;
    };

    // Function to fetch and display maids
    function loadMaids(filters = {}) {
        // Construct query parameters
        const query = new URLSearchParams(filters).toString();
        const url = query ? `/maid?${query}` : `/maid`;

        fetch(`http://127.0.0.1:5000${url}`, { credentials: "include" })
        .then(res => res.json())
        .then(data => {
            maidContainer.innerHTML = "";

            if (data.status === "success" && data.data.length > 0) {
                data.data.forEach(maid => {
                    const statusClass = maid.availability_status ? maid.availability_status.toLowerCase() : "inactive";

                    const card = document.createElement("div");
                    card.className = `maid-card ${statusClass}`;
                    card.innerHTML = `
                        <div class="maid-info">
                            <h3>${maid.name || "Unnamed Maid"}</h3>
                            <p><strong>ID:</strong> ${maid.maid_id || "-"}</p>
                            <p><strong>Gender:</strong> ${maid.gender || "-"}</p>
                            <p><strong>Service:</strong> ${maid.service || "-"}</p>
                            <p><strong>Experience:</strong> ${maid.experience_years || "N/A"} years</p>
                            <p><strong>Phone:</strong> ${maid.phone_number || "N/A"}</p>
                            <p><strong>Address:</strong> ${maid.address || "N/A"}</p>
                            <p><strong>DOB:</strong> ${maid.dob || "N/A"}</p>
                            <p><strong>Age:</strong> ${maid.age || "N/A"}</p>
                            <p><strong>Salary:</strong> ${maid.salary || "N/A"}</p>
                            <p><strong>Status:</strong> 
                                <span class="status-badge ${statusClass}">
                                    ${maid.availability_status || "UNKNOWN"}
                                </span>
                            </p>
                            <button class="edit-btn" onclick="editMaid(${maid.maid_id})">✏️</button>
                             <button class="delete-btn" onclick="deleteMaid(${maid.maid_id})">❌</button>
                        </div>
                    `;
                    maidContainer.appendChild(card);
                });
            } else {
                maidContainer.innerHTML = `<p class="no-data">No maids found.</p>`;
            }
        })
        .catch(err => {
            console.error("Error fetching maids:", err);
            maidContainer.innerHTML = `<p class="no-data">Failed to load maid data.</p>`;
        });
    }
     
    window.deleteMaid = function(maidId) {
    if (!confirm("Are you sure you want to deactivate this maid?")) return;

    fetch(`http://127.0.0.1:5000/maid/${maidId}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ deleted_by: sessionStorage.getItem("name") || "system" })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            alert(data.message);

            // Update the status badge of the specific card without reloading everything
            const card = document.querySelector(`.maid-card[data-id='${maidId}']`);
            if (card) {
                const statusBadge = card.querySelector(".status-badge");
                statusBadge.textContent = "INACTIVE";
                statusBadge.className = "status-badge inactive";
                card.classList.add("inactive"); // Optional: change card styling
            }

        } else {
            alert(data.message || "Failed to deactivate maid.");
        }
    })
    .catch(err => {
        console.error("Error deactivating maid:", err);
        alert("Error deactivating maid.");
    });
}

    // Load all maids initially
    loadMaids();

    // Apply filters
    applyFiltersBtn.addEventListener("click", () => {
        const filters = {
            availability_status: filterAvailability.value,
            gender: filterGender.value,
            service: filterService.value
        };
        loadMaids(filters);
    });
});
