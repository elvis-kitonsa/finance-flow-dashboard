document.addEventListener("DOMContentLoaded", () => updateFinancials());

function saveExpense() {
  const expenseData = {
    title: document.getElementById("title").value,
    amount: document.getElementById("amount").value,
    category: document.getElementById("category").value,
    date: document.getElementById("expenseDate").value,
  };

  if (!expenseData.title || !expenseData.amount || !expenseData.date) {
    alert("Please fill in all fields!");
    return;
  }

  fetch("/add_expense", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(expenseData),
  })
    .then((res) => res.json())
    .then((data) => {
      alert("Success: " + data.message);
      location.reload();
    });
}

function updateFinancials() {
  const initialBalance = parseFloat(localStorage.getItem("userBalance") || 0);
  document.getElementById("initialBalanceDisplay").innerText = "UGX " + initialBalance.toLocaleString();

  let totalSpent = 0;
  const categoryTotals = { Housing: 0, Food: 0, Transport: 0, Savings: 0 };
  const rows = document.querySelectorAll("tbody tr");

  rows.forEach((row) => {
    const categoryCell = row.cells[1];
    const amountCell = row.cells[3]; // Amount is now the 4th column

    if (amountCell && !amountCell.innerText.includes("No expenses")) {
      const amount = parseFloat(amountCell.innerText.replace(/[^\d.]/g, ""));
      totalSpent += amount;
      const cat = categoryCell.innerText.trim();
      if (categoryTotals.hasOwnProperty(cat)) categoryTotals[cat] += amount;
    }
  });

  const remaining = initialBalance - totalSpent;
  const remainingDisplay = document.getElementById("remainingDisplay");
  remainingDisplay.innerText = "UGX " + remaining.toLocaleString();

  // Toggle color if overspent
  const card = remainingDisplay.closest(".card");
  if (remaining < 0) {
    card.classList.add("bg-danger", "text-white");
    card.classList.remove("glass-card");
  } else {
    card.classList.remove("bg-danger", "text-white");
    card.classList.add("glass-card");
  }

  renderChart(categoryTotals);
}

function renderChart(dataValues) {
  const ctx = document.getElementById("categoryChart").getContext("2d");
  if (window.myPieChart) window.myPieChart.destroy();
  window.myPieChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: Object.keys(dataValues),
      datasets: [
        {
          data: Object.values(dataValues),
          backgroundColor: ["#4361ee", "#ef476f", "#06d6a0", "#ffd166"],
          borderWidth: 0,
        },
      ],
    },
    options: { plugins: { legend: { position: "bottom" } }, cutout: "80%" },
  });
}

function setBalance() {
  const val = prompt("Enter initial balance:", "2000000");
  if (val) {
    localStorage.setItem("userBalance", val);
    updateFinancials();
  }
}
