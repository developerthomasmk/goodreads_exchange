document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("addBookForm").addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData();
        formData.append("title", document.getElementById("title").value);
        formData.append("author", document.getElementById("author").value);
        formData.append("genre", document.getElementById("genre").value);
        formData.append("description", document.getElementById("description").value);
        formData.append("bookImage", document.getElementById("bookImage").files[0]);


        fetch('/addbook', {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const message = document.getElementById("message");
            if (data.success) {
                message.textContent = "Book added successfully!";
                message.style.color = "green";
                document.getElementById("addBookForm").reset();
            } else {
                message.textContent = "Error adding book.";
                message.style.color = "red";
            }
        })
        .catch(error => console.error("Error:", error));
    });
});