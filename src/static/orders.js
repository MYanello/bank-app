document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("new-order-form").onsubmit = submitOrder;

  fetchOrders();
});

function submitOrder(event) {
  event.preventDefault(); // prevent form from submitting from refreshing the page
  const form = event.target;
  const term = form.term.value;
  const amount = form.amount.value;

  fetch("/api/v1/order", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      term: Number(term),
      amount: Number(amount),
    }),
  })
    .then((response) => {
      if (response.ok) {
        flashMessage("Order received");
        fetchOrders(); // refresh the order list
      } else {
        response.text().then((text) => {
          alert("Failed to create order: " + text);
        });
      }
    })
    .catch((error) => {
      alert("Failed to create order: " + error);
    });
}

function fetchOrders() {
  const ordersContainer = document.getElementById("orders-container");
  ordersContainer.innerHTML = `
    <div class="loading-container" id="fetch-btn-spinner">
      <div class="loading-spinner"></div>
      <span>Loading...</span>
    </div>
  `;

  fetch(`/api/v1/orders`)
    .then((response) => response.json())
    .then((data) => {
      displayOrders(data.orders);
    })
    .catch((error) => {
      console.error("Error fetching orders:", error);
      const ordersTable = document.getElementById("orders-table");
      ordersTable.innerHTML =
        '<div class="error">Failed to fetch orders. Please refresh to try again.</div>';
      restoreFetchButton();
    });
}

function displayOrders(orders) {
  const container = document.getElementById("orders-container");
  if (!container) return;

  if (!orders || orders.length === 0) {
    container.innerHTML = "<p>No orders found.</p>";
    return;
  }
  const tableHeaders = `
    <tr>
      <th>Submitted</th>
      <th>Term</th>
      <th>Amount</th>
    </tr>
  `;
  const tableRows = orders
    .map((order) => {
      const submitted = new Date(order.submitted).toLocaleString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
      return `
        <tr>
          <td>${submitted.toLocaleString()}</td>
          <td>${order.term}</td>
          <td>${order.amount.toLocaleString()}</td>
        </tr>
      `;
    })
    .join("");
  container.innerHTML = `
    <table class="orders-table">
      <thead>${tableHeaders}</thead>
      <tbody>${tableRows}</tbody>
    </table>
  `;
}

function flashMessage(text, duration = 1000) {
  const msgDiv = document.getElementById("flash-message");
  msgDiv.textContent = text;
  msgDiv.style.display = "block";
  setTimeout(() => {
    msgDiv.style.display = "none";
    msgDiv.textContent = "";
  }, duration);
}
