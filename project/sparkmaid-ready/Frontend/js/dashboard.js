document.addEventListener("DOMContentLoaded", () => {
    const role = sessionStorage.getItem("role");
    const name = sessionStorage.getItem("name") || "User";
    const id = sessionStorage.getItem("id"); 
    // Update welcome name
    document.getElementById("userName").textContent = name;

    // Sidebar links based on role
    const sidebarLinks = document.getElementById("sidebarLinks");
    sidebarLinks.innerHTML = "";
    if (role === "admin") {
        sidebarLinks.innerHTML = `
            <li><a href="#">Dashboard</a></li>
            <li><a href="#" id="maidLink">Maid</a></li>
            <li><a href="#" id="customersLink">Customers</a></li>
            <li><a href="#" id="bookingsLink">All bookings</a></li>
            <li><a href="#" id="adminProfileLink">Profile</a></li>
            <li><a href="#" id="transactionLink">Transactions</a></li>
        `;
        document.getElementById("sidebarTitle").textContent = "Admin Panel";
        // Redirect to admin_profile.html when profile link is clicked
    const adminProfileLink = document.getElementById("adminProfileLink");
    adminProfileLink.addEventListener("click", () => {
        window.location.href = "/admin_profile.html";
    });

    const maidLink = document.getElementById("maidLink");
    maidLink.addEventListener("click", () => {
        window.location.href = "/maid.html";
    });

    const customersLink = document.getElementById("customersLink");
    customersLink.addEventListener("click", () => {
        window.location.href = "/customers.html";
    });
    
    const bookingsLink = document.getElementById("bookingsLink");
    bookingsLink.addEventListener("click", () => {
        window.location.href = "/bookings.html";
    });
    
    const transactionLink = document.getElementById("transactionLink");
    transactionLink.addEventListener("click", () => {
        window.location.href = "/transaction.html";
    });

    } else {
    sidebarLinks.innerHTML = `
        <li><a href="#">Dashboard</a></li>
        <li><a href="#" id="maidsLink">Maid</a></li>
        <li><a href="#" id="myBookingsLink">My Bookings</a></li>
        <li><a href="#" id="offersLink">Offers</a></li>
        <li><a href="#" id="careersLink">Careers</a></li>
        <li><a href="#" id="contactLink">Contacts</a></li>
        <li><a href="#" id="profileLink">Profile</a></li>
    `;
    document.getElementById("sidebarTitle").textContent = "Customer Panel";

    // Profile link click event
    const profileLink = document.getElementById("profileLink");
    profileLink.addEventListener("click", () => {
        if (!id) {
            alert("Customer ID not found. Please login again.");
            window.location.href = "/index.html";
            return;
        }
        sessionStorage.setItem("id", id);
        window.location.href = "/profile_customer.html";
    });

    // Offers link click event
    const offersLink = document.getElementById("offersLink");
    offersLink.addEventListener("click", () => {
        window.location.href = "/offer_customer.html";
    });

    // career link click event
    const careersLink = document.getElementById("careersLink");
    careersLink.addEventListener("click", () => {
        window.location.href = "/careers.html";
    });
    // My Bookings link click event (corrected)
    const myBookingsLink = document.getElementById("myBookingsLink");
    myBookingsLink.addEventListener("click", () => {
        window.location.href = "/my_bookings.html";
    });

    const maidsLink = document.getElementById("maidsLink");
    maidsLink.addEventListener("click", () => {
        window.location.href = "/show_maid.html";
    });
    const contactLink = document.getElementById("contactLink");
    contactLink.addEventListener("click", () => {
        window.location.href = "/contact.html";
    });
    
}

    // Cards based on role
    const cardsContainer = document.getElementById("cardsContainer");
    if (role === "admin") {
        cardsContainer.innerHTML = `
            <div class="card card-1">
                <h3>Our Services</h3>
                <p>Professional cleaning, cooking, laundry, and home assistance for all your needs.</p>
            </div>
            <div class="card card-2">
                <h3>Special Offers</h3>
                <p>Weekly discounts, seasonal promotions, and loyalty rewards for valued customers.</p>
            </div>
            <div class="card card-3">
                <h3>About Company</h3>
                <p>Reliable home services since 2010. Customer satisfaction is our priority.</p>
            </div>
        `;
    } else {
        cardsContainer.innerHTML = `
            <div class="card card-1">
                <h3>Book Services</h3>
                <p>Choose from cleaning, cooking, laundry, or other home services with ease.</p>
            </div>
            <div class="card card-2">
                <h3>Current Offers</h3>
                <p>Check out weekly discounts and seasonal promotions for you.</p>
            </div>
            <div class="card card-3">
                <h3>Why Choose Us?</h3>
                <p>Trusted professionals, flexible schedules, and 24/7 customer support.</p>
            </div>
        `;
    }

    // Info section
    const infoSection = document.getElementById("infoSection");
    if (role === "admin") {
        infoSection.innerHTML = `
            <h2>Highlights</h2>
            <p>• Verified and professional maids for all services.</p>
            <p>• 24/7 customer support for queries and emergencies.</p>
            <p>• Flexible booking schedules to suit your convenience.</p>
            <p>• Regular updates on service quality and improvements.</p>
        `;
    } else {
    infoSection.innerHTML = `
        <h2>Why SparkMaid?</h2>
        <p>• Book services anytime, anywhere from your dashboard.</p>
        <p>• Stay updated on offers and packages.</p>
        <p>• Reliable professionals for all household tasks.</p>
        <p>• Flexible scheduling to suit your lifestyle.</p>
        <p>• Transparent pricing with no hidden charges.</p>
        <p>• Experienced and background-verified staff.</p>
        <p>• 24/7 customer support for queries and emergencies.</p>
        <p>• Easy rescheduling or cancellation options.</p>
        <p>• Loyalty rewards and exclusive promotions for regular users.</p>
        <p>• Eco-friendly cleaning and sustainable practices.</p>
    `;
}


    // Logout button
    document.getElementById("logoutBtn").addEventListener("click", function() {
        sessionStorage.clear();
        window.location.href = "/index.html";
    });
});
