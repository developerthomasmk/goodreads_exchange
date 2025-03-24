document.addEventListener("DOMContentLoaded", function () {
    fetch('/get_my_books')
        .then(response => response.json())
        .then(data => {
            const booksContainer = document.getElementById("booksContainer");
            booksContainer.innerHTML = "";

            if(!data){
                booksContainer.innerHTML = "<p>You haven't added any books yet.</p>";
                return;
            }

            if (data.books.length === 0) {
                booksContainer.innerHTML = "<p>You haven't added any books yet.</p>";
                return;
            }

            console.log("Data:::"+data.books.length)

            data.books.forEach(book => {
                const bookCard = document.createElement("div");
                bookCard.classList.add("book-card");

                bookCard.innerHTML = `
                    <img src="${imageUrl + book.image}" alt="${book.username}" class="card-image">
                    <h3>${book.title}</h3>
                    <p><strong>Author:</strong> ${book.author}</p>
                    <p><strong>Genre:</strong> ${book.genre}</p>
                    <p><strong>Status:</strong> ${book.status}</p>
                `;

                booksContainer.appendChild(bookCard);
            });
        })
        .catch(error => console.error("Error fetching books:", error));

    document.getElementById("addBookBtn").addEventListener("click", function () {
        window.location.href = "/addbook";
    });
});
