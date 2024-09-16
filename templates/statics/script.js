document.addEventListener("DOMContentLoaded", () => {
    const hotelSelect = document.getElementById("hotel-select");
    const tagSelect = document.getElementById("tag-select");
    const generateBtn = document.getElementById("generate-btn");
    const resultDiv = document.getElementById("result");

    // Fetch hotels and populate select
    fetch("/hotels")
        .then(response => response.json())
        .then(hotels => {
            hotels.forEach(hotel => {
                const option = document.createElement("option");
                option.value = hotel.id;
                option.textContent = hotel.name;
                hotelSelect.appendChild(option);
            });
        });

    // Fetch tags and populate select
    fetch("/tags")
        .then(response => response.json())
        .then(tags => {
            tags.forEach(tag => {
                const option = document.createElement("option");
                option.value = tag.name;
                option.textContent = tag.name;
                tagSelect.appendChild(option);
            });
        });

    generateBtn.addEventListener("click", () => {
        const hotelId = hotelSelect.value;
        const tag = tagSelect.value;

        if (!hotelId || !tag) {
            resultDiv.textContent = "Please select both a hotel and a category.";
            return;
        }

        fetch("/plan_trip", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ hotel_id: parseInt(hotelId), tag }),
        })
            .then(response => response.json())
            .then(plan => {
                let resultHTML = "<h2>Trip Plan</h2>";
                plan.destinations.forEach((item, index) => {
                    if (index == 0)
                        resultHTML += `<p><b>${index + 1}. ${item}</b><br>Distance from hotel: ${plan.distances[index].toFixed(2)} km</p>`;
                    else
                        resultHTML += `<p><b>${index + 1}. ${item}</b><br>Distance from <b>${plan.destinations[index - 1]}</b>: ${plan.distances[index].toFixed(2)} km</p>`;
                });
                resultHTML += `<p><strong>Total distance:</strong> ${plan.total_distance.toFixed(2)} km</p>`;
                resultDiv.innerHTML = resultHTML;
            })
            .catch(error => {
                resultDiv.textContent = "An error occurred while generating the trip plan.";
                console.error("Error:", error);
            });
    });
});
