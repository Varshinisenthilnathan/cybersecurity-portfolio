document.getElementById('loginBtn').addEventListener('click', login);

function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const role = document.getElementById('role').value;
    const messageEl = document.getElementById('message');

    if (!email || !password || !role) {
        messageEl.textContent = "Please fill all fields.";
        messageEl.style.color = "red";
        return;
    }

    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ email, password, role })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            messageEl.style.color = "green";
            messageEl.textContent = data.message;

             sessionStorage.setItem("role", data.role);
            sessionStorage.setItem("name", data.name);
            sessionStorage.setItem("id", data.id);
            sessionStorage.setItem("email", data.email);

            if (role === "admin") {
                window.location.href = "/dashboard_admin.html";
            } else {
                window.location.href = "/dashboard_admin.html";
            }
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
}
