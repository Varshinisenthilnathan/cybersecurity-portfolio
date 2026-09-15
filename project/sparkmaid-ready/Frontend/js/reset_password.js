document.addEventListener("DOMContentLoaded", () => {
    const email = new URLSearchParams(window.location.search).get("email");
    const otpContainer = document.getElementById("otpContainer");
    const messageEl = document.getElementById("message");
    const resetBtn = document.getElementById("resetBtn");

    if (!email) {
        messageEl.style.color = "red";
        messageEl.textContent = "Email not found. Please go back and try again.";
        resetBtn.disabled = true;
        return;
    }
    const togglePassword = document.getElementById("togglePassword");
    const newPasswordInput = document.getElementById("new_password");

togglePassword.addEventListener("click", () => {
    const isPasswordVisible = newPasswordInput.type === "text";
    newPasswordInput.type = isPasswordVisible ? "password" : "text";
    togglePassword.textContent = isPasswordVisible ? "👁️" : "🙈";
});


    // Detect if it's a customer (OTP needed)
    fetch("http://127.0.0.1:5000/check-user-role", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email })
    })
    .then(res => res.json())
    .then(data => {
        if (data.role === "customer") {
            otpContainer.style.display = "block";
        } else {
            otpContainer.style.display = "none";
        }
    })
    .catch(() => {
        otpContainer.style.display = "block"; 
    });

    resetBtn.addEventListener("click", () => {
        const otp = document.getElementById("otp").value.trim();
        const newPassword = document.getElementById("new_password").value.trim();

        if (!newPassword) {
            messageEl.style.color = "red";
            messageEl.textContent = "Please enter a new password.";
            return;
        }

        const payload = { email, new_password: newPassword };
        if (otpContainer.style.display === "block") payload.otp = otp;

        fetch("http://127.0.0.1:5000/resetpassword", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                messageEl.style.color = "green";
                messageEl.textContent = data.message;
                setTimeout(() => {
                    window.location.href = "index.html";
                }, 2000);
            } else {
                messageEl.style.color = "red";
                messageEl.textContent = data.message;
            }
        })
        .catch(() => {
            messageEl.style.color = "red";
            messageEl.textContent = "Something went wrong. Please try again.";
        });
    });
});
