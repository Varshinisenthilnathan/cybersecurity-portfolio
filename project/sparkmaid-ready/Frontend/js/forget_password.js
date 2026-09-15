document.getElementById("submitBtn").addEventListener("click", () => {
    const email = document.getElementById("email").value.trim();
    const messageEl = document.getElementById("message");

    if (!email) {
        messageEl.style.color = "red";
        messageEl.textContent = "Please enter your email.";
        return;
    }

    fetch("http://127.0.0.1:5000/forgotpassword", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            messageEl.style.color = "green";
            messageEl.textContent = data.message;

            // Redirect to reset password page with email in query string
            setTimeout(() => {
                window.location.href = `reset_password.html?email=${encodeURIComponent(email)}`;
            }, 1500);
        } else {
            messageEl.style.color = "red";
            messageEl.textContent = data.message;
        }
    })
    .catch(err => {
        console.error("Error:", err);
        messageEl.style.color = "red";
        messageEl.textContent = "Something went wrong. Try again later.";
    });
});
