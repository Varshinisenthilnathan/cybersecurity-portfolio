document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("createMaidForm");
    const messageEl = document.getElementById("message");

    const role = sessionStorage.getItem("role");
    if (!role || role !== "admin") {
        alert("Access denied! Admins only.");
        window.location.href = "/index.html";
        return;
    }

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        fetch("http://127.0.0.1:5000/maid/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",

            },
            credentials: "include",
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(result => {
            if (result.status === "success") {
                messageEl.style.color = "green";
                messageEl.textContent = result.message;
                form.reset();

                setTimeout(() => {
                    window.location.href = "/maid.html";
                }, 1500);
            } else {
                messageEl.style.color = "red";
                messageEl.textContent = result.message;
            }
        })
        .catch(err => {
            console.error(err);
            messageEl.style.color = "red";
            messageEl.textContent = "Error creating maid.";
        });
    });
});
