const otpBoxes = document.querySelectorAll(".otp-box");
const messageEl = document.getElementById("message");
const verifyBtn = document.getElementById("verifyBtn");
const timerEl = document.getElementById("timer");

// Auto-focus next input
otpBoxes.forEach((box, index) => {
    box.addEventListener("input", () => {
        if (box.value.length === 1 && index < otpBoxes.length - 1) {
            otpBoxes[index + 1].focus();
        }
    });

    box.addEventListener("keydown", (e) => {
        if (e.key === "Backspace" && box.value === "" && index > 0) {
            otpBoxes[index - 1].focus();
        }
    });
});

// Timer
let timeLeft = 300;
const timerInterval = setInterval(() => {
    let minutes = Math.floor(timeLeft / 60);
    let seconds = timeLeft % 60;
    timerEl.textContent = `${minutes.toString().padStart(2,'0')}:${seconds.toString().padStart(2,'0')}`;
    timeLeft--;

    if (timeLeft < 0) {
        clearInterval(timerInterval);
        messageEl.style.color = "red";
        messageEl.textContent = "OTP expired. Please request a new one.";
        verifyBtn.disabled = true;
    }
}, 1000);

// Verify OTP
verifyBtn.addEventListener("click", () => {
    const otp = Array.from(otpBoxes).map(box => box.value).join("");
    const email = new URLSearchParams(window.location.search).get("email");

    if (otp.length < 6) {
        messageEl.style.color = "red";
        messageEl.textContent = "Please enter a 6-digit OTP.";
        return;
    }

    fetch("http://127.0.0.1:5000/customer/verifyotp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ email, otp })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            messageEl.style.color = "green";
            messageEl.textContent = data.message;
            setTimeout(() => {
                window.location.href = "/dashboard_admin.html";
            }, 1000);
        } else {
            messageEl.style.color = "red";
            messageEl.textContent = data.message;
        }
    })
    .catch(err => {
        messageEl.style.color = "red";
        messageEl.textContent = "Error connecting to server.";
        console.error(err);
    });
});
