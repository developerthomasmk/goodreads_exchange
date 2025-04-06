document.addEventListener("DOMContentLoaded", function () {
    fetch('/get_my_books')
        .then(response => response.json())
        .then(data => {
            const booksContainer = document.getElementById("booksContainer");
            booksContainer.innerHTML = "";

            if (!data) {
                booksContainer.innerHTML = "<p>You haven't added any books yet.</p>";
                return;
            }

            if (data.books.length === 0) {
                booksContainer.innerHTML = "<p>You haven't added any books yet.</p>";
                return;
            }

            console.log("Data:::" + data.books.length)

            data.books.forEach(book => {
                const bookCard = document.createElement("div");
                bookCard.classList.add("book-card");

                bookCard.innerHTML = `
                    <img src="${imageUrl + book.image}" alt="${book.username}" class="card-image">
                    <h3>${book.title}</h3>
                    <p><strong>Author:</strong> ${book.author}</p>
                    <p><strong>Genre:</strong> ${book.genre}</p>
                    <p><strong>Status:</strong> ${book.status}</p>
                    <button class="delete-book">Delete</button>
                `;

                booksContainer.appendChild(bookCard);


                const deleteBtn = bookCard.querySelector('.delete-book');
                deleteBtn.addEventListener('click', (event) => {
                    event.stopPropagation();
                    const confirmDelete = confirm(`Are you sure you want to delete "${book.title}"?`);
                    if (confirmDelete) {
                        fetch(`/delete_book/${book.book_id}`)
                            .then(response => {
                                if (response.ok) {
                                    bookCard.remove();
                                    location.reload();
                                } else {
                                    console.error('Failed to delete book');
                                }
                            })
                            .catch(error => console.error('Error deleting book:', error));
                    }
                });

            });
        })
        .catch(error => console.error("Error fetching books:", error));

    document.getElementById("addBookBtn").addEventListener("click", function () {
        window.location.href = "/addbook";
    });
});
