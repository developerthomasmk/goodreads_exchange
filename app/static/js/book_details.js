const latitude = "{{ book.owner.latitude }}";
const longitude = "{{ book.owner.longitude }}";
const bookTitle = "{{ book.title }}";

console.log("Title:::" + bookTitle)
console.log("Lat:::" + latitude)

document.addEventListener("DOMContentLoaded", function () {
    var map = L.map("map").setView([latitude, longitude], 13);


    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);


    L.marker([latitude, longitude]).addTo(map)
        .bindPopup(`<b>${bookTitle}</b><br>Available here.`)
        .openPopup();

    document.getElementById("exchangeBook").addEventListener("click", function () {

        fetch("/exchange_book/{{ book.book_id }}", { method: "POST" })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                window.location.href = "/home";
            })
            .catch(error => console.error("Error:", error));
    });
});