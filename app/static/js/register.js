document.addEventListener("DOMContentLoaded", function () {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
            async function (position) {  // SUCCESS CALLBACK
                let latitude = position.coords.latitude;
                let longitude = position.coords.longitude;

                console.log("Latitude:", latitude);
                console.log("Longitude:", longitude);

                document.getElementById("latitude").value = latitude;
                document.getElementById("longitude").value = longitude;

                try {
                    let response = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`);
                    let data = await response.json();

                    if (data.display_name) {
                        console.log("Location:", data.display_name);
                        document.getElementById("location").value = data.display_name;
                    } else {
                        console.log("Could not retrieve location name.");
                    }
                } catch (error) {
                    console.error("Error fetching location data:", error);
                }
            }, 

            function (error) {  // ERROR CALLBACK
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        alert("Location access denied by user. Please enable location permissions.");
                        break;
                    case error.POSITION_UNAVAILABLE:
                        alert("Location information is unavailable.");
                        break;
                    case error.TIMEOUT:
                        alert("Location request timed out.");
                        break;
                    default:
                        alert("An unknown error occurred.");
                        break;
                }
                console.error("Geolocation error:", error.message);
            }
        );
    } else {
        alert("Geolocation is not supported by this browser.");
    }
});

document.getElementById("registerForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const formData = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
        phone: document.getElementById("phone").value,
        location: document.getElementById("location").value,
        latitude: document.getElementById("latitude").value,
        longitude: document.getElementById("longitude").value
    };

    try {
        const response = await fetch(REGISTER_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        alert(result.message);
        if (response.ok) {
            window.location.href = LOGIN_URL;
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    }
});
