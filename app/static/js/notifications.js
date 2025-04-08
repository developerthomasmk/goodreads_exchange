document.addEventListener("DOMContentLoaded", () => {
    fetchRequests();
  });
  
  function fetchRequests() {
    fetch("/api/exchange_requests")
      .then((res) => res.json())
      .then((data) => {
        const container = document.getElementById("notification-div");
        container.innerHTML = "";
  
        if (data.requests.length === 0) {
          container.innerHTML = "<p>No exchange requests.</p>";
          return;
        }
  
        data.requests.forEach((req) => {
          const card = document.createElement("div");
          card.className = "notification-card";
  
          card.innerHTML = `
            <p><strong>From:</strong> ${req.sender_name}</p>
            <p><strong>Book:</strong> ${req.book_title}</p>
            <p><strong>Status:</strong> ${req.status}</p>
            ${
              req.status === "Pending"
                ? `<button class="approve" onclick="respond(${req.id}, 'Approved')">Approve</button>
                   <button class="reject" onclick="respond(${req.id}, 'Rejected')">Reject</button>`
                : ""
            }
          `;
  
          container.appendChild(card);
        });
      })
      .catch((err) => {
        console.error("Error loading exchange requests:", err);
      });
  }
  
  function respond(id, action) {
    fetch(`/api/exchange_requests/${id}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: action }),
    })
      .then((res) => res.json())
      .then((data) => {
        alert(data.message);
        fetchRequests();
      })
      .catch((err) => {
        console.error("Error updating request:", err);
      });
  }
  