document.addEventListener("DOMContentLoaded", () => {
    console.log("Offers page loaded ✅");

    const offersContainer = document.getElementById("offersContainer");

    const offers = [
        {
            title: "Cleaning Services",
            description: "Get your home sparkling clean with our professional cleaning staff!",
            discount: "30% OFF",
            img: "https://images.unsplash.com/photo-1581574209461-99d6b1f1ef3b?auto=format&fit=crop&w=800&q=60"
        },
        {
            title: "Cooking Assistance",
            description: "Hire skilled cooks for daily meals or special occasions.",
            discount: "25% OFF",
            img: "https://images.unsplash.com/photo-1606787366850-de6330128bfc?auto=format&fit=crop&w=800&q=60"
        },
        {
            title: "Carpenter Services",
            description: "Repair, customize, or install wooden furniture effortlessly.",
            discount: "20% OFF",
            img: "https://images.unsplash.com/photo-1581091870622-84b47eb4f16b?auto=format&fit=crop&w=800&q=60"
        },
        {
            title: "Painting Services",
            description: "Transform your walls with vibrant colors and expert painters.",
            discount: "35% OFF",
            img: "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=800&q=60"
        }
    ];

    if (!offersContainer) {
        console.error("❌ offersContainer not found in HTML");
        return;
    }

    offers.forEach(offer => {
        const offerCard = document.createElement("div");
        offerCard.classList.add("offer-card");

        offerCard.innerHTML = `
            <img src="${offer.img}" alt="${offer.title}">
            <div class="offer-content">
                <h3>${offer.title}</h3>
                <p>${offer.description}</p>
                <span class="discount">${offer.discount}</span>
            </div>
        `;
        offersContainer.appendChild(offerCard);
    });

    document.getElementById("backBtn").addEventListener("click", () => {
        window.location.href = "/dashboard.html";
    });
});
