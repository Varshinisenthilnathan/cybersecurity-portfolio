document.getElementById("registerBtn").addEventListener("click", registerCustomer);

function registerCustomer() {
    const data = {
        name: document.getElementById("name").value,
        phone_number: document.getElementById("phone_number").value,
        address: document.getElementById("address").value,
        email: document.getElementById("email").value,
        gender: document.getElementById("gender").value,
        age: document.getElementById("age").value,
        dob: document.getElementById("dob").value,
        username: document.getElementById("username").value,
        password: document.getElementById("password").value,
        service_registered: document.getElementById("service_registered").value
    };

    const messageEl = document.getElementById("message");

    fetch("http://127.0.0.1:5000/customer/register", {  
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",  
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(res => {
        if(res.status === "success") {
            messageEl.style.color = "green";
            messageEl.textContent = res.message;

            // Redirect to OTP verification page
            setTimeout(() => {
                window.location.href = `verify_otp.html?email=${encodeURIComponent(data.email)}`;
            }, 1500);
        } else {
            messageEl.style.color = "red";
            messageEl.textContent = res.message;
        }
    })
    .catch(err => {
        messageEl.style.color = "red";
        messageEl.textContent = "Error connecting to server.";
        console.error(err);
    });
}
