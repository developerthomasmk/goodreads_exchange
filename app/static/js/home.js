document.addEventListener("DOMContentLoaded", async function () {
    const booksList = document.getElementById("booksList");

    async function fetchBooks() {
        try {
            let response = await fetch(BOOKS_API_URL);
            let books = await response.json();

            booksList.innerHTML = "";
            books.forEach(book => {
                let bookCard = document.createElement("div");
                bookCard.classList.add("book-card");

                console.log("BookId:::"+book.book_id)

                bookCard.innerHTML = `
                    <img src="${imageUrl + book.image}" alt="${book.username}" class="card-image">
                    <h3>${book.title}</h3>
                    <p>Author: ${book.author}</p>
                    <p>Location: ${book.location}</p>
                    <button onclick="viewBook(${book.book_id})">View Details</button>
                `;

                booksList.appendChild(bookCard);
            });

        } catch (error) {
            console.error("Error fetching books:", error);
        }
    }

    fetchBooks();

    document.getElementById("myBooksBtn").addEventListener("click", function () {
        window.location.href = "/mybooks";
    });

    document.getElementById("historyBtn").addEventListener("click", function () {
        window.location.href = "/history";
    });

    document.getElementById("logoutBtn").addEventListener("click", function () {
        window.location.href = "/logout";
    });
});

function viewBook(bookId) {
    window.location.href = `/view_book/${bookId}`;
}