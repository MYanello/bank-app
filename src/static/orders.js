document.addEventListener("DOMContentLoaded", function () {
  fetchOrders();
});

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
    <h2>Orders</h2>
    <table class="orders-table">
      <thead>${tableHeaders}</thead>
      <tbody>${tableRows}</tbody>
    </table>
  `;
}
