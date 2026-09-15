document.addEventListener("DOMContentLoaded", () => {
    const maidContainer = document.getElementById("maidContainer");
    const filterAvailability = document.getElementById("filterAvailability");
    const filterGender = document.getElementById("filterGender");
    const filterService = document.getElementById("filterService");
    const applyFiltersBtn = document.getElementById("applyFilters");

    document.getElementById("createBookingBtn").addEventListener("click", () => {
    window.location.href = "/create_bookings.html";
});

    function loadMaids(filters = {}) {
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
                        <p><strong>Status:</strong> <span class="status-badge ${statusClass}">${maid.availability_status || "UNKNOWN"}</span></p>
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
