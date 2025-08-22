document.addEventListener("DOMContentLoaded", function () {
  yearSelector();
  termSelector();

  document
    .getElementById("fetch-yields-btn")
    .addEventListener("click", function () {
      const yearSelect = document.getElementById("year");
      const selectedYear = yearSelect.value;
      const termSelect = document.getElementById("term");
      const selectedTerm = termSelect.value;
      fetchYields(selectedYear, selectedTerm);
    });
});

// TODO: DRY up these 2 selectors
function yearSelector() {
  const yearSelectorDiv = document.getElementById("year-selector");
  const select = document.createElement("select");
  select.id = "year";
  select.name = "year";

  const currentYear = new Date().getFullYear();
  for (let i = 0; i < 20; i++) {
    const year = currentYear - i;
    const option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    select.appendChild(option);
  }
  select.value = currentYear; // current year is default

  yearSelectorDiv.appendChild(select);
}
function termSelector() {
  const termSelectorDiv = document.getElementById("term-selector");
  const select = document.createElement("select");
  select.id = "term";
  select.name = "term";
  const terms = [
    "1 Mo",
    "2 Mo",
    "3 Mo",
    "6 Mo",
    "1 Yr",
    "2 Yr",
    "3 Yr",
    "5 Yr",
    "7 Yr",
    "10 Yr",
    "20 Yr",
    "30 Yr",
  ];
  for (const term of terms) {
    const option = document.createElement("option");
    option.value = term;
    option.textContent = term;
    select.appendChild(option);
  }

  select.value = "10 Yr"; // 10 Yr is default

  termSelectorDiv.appendChild(select);
}

function fetchYields(year, term) {
  if (!year || !term) {
    alert("Please select a year and term.");
    return;
  }

  // loading spinner
  const btnContainer = document.getElementById("fetch-btn-container");
  btnContainer.innerHTML = `
    <div class="loading-container" id="fetch-btn-spinner">
      <div class="loading-spinner"></div>
      <span>Loading...</span>
    </div>
  `;

  fetch(`/api/v1/yields?year=${year}&term=${term}`)
    .then((response) => response.json())
    .then((data) => {
      displayYields(data.yields, term);
      restoreFetchButton();
    })
    .catch((error) => {
      console.error("Error fetching yields:", error);
      const yieldsContainer = document.getElementById("yields-container");
      yieldsContainer.innerHTML =
        '<div class="error">Failed to fetch yields. Please try again.</div>';
      restoreFetchButton();
    });
}

function restoreFetchButton() {
  const btnContainer = document.getElementById("fetch-btn-container");
  btnContainer.innerHTML = `
      <button type="button" id="fetch-yields-btn">Get Treasury Yields</button>
    `;
  document
    .getElementById("fetch-yields-btn")
    .addEventListener("click", function () {
      const yearSelect = document.getElementById("year");
      const termSelect = document.getElementById("term");
      const selectedYear = yearSelect.value;
      const selectedTerm = termSelect.value;
      fetchYields(selectedYear, selectedTerm);
    });
}

function displayYields(yields, term) {
  let canvas = document.getElementById("yields-chart");
  if (!canvas) {
    const yieldsContainer = document.getElementById("yields-container");
    yieldsContainer.innerHTML =
      '<canvas id="yields-chart" width="800" height="400"></canvas>';
    canvas = document.getElementById("yields-chart");
  }
  const ctx = document.getElementById("yields-chart").getContext("2d");
  const dates = yields.map((row) => row["Date"]);
  const rates = yields.map((row) => parseFloat(row[term]));

  if (window.yieldsChart) {
    window.yieldsChart.destroy();
  }

  window.yieldsChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: dates.reverse(), // oldest to newest
      datasets: [
        {
          label: "Treasury Yield (%)",
          data: rates.reverse(),
          borderColor: "#3498db",
          backgroundColor: "rgba(52, 152, 219, 0.2)",
          fill: true,
          tension: 0.1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: true },
      },
      scales: {
        x: { title: { display: true, text: "Date" } },
        y: { title: { display: true, text: "Yield (%)" } },
      },
    },
  });
}
