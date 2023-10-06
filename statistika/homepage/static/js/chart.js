let ctx = document.getElementById("chart").getContext("2d");
const chartData = JSON.parse(document.getElementById('chart-1').textContent)
let chart = new Chart(ctx, {
  type: "bar",
  data: {
     labels: chartData.labels,
     datasets: [
        {
          label: "Total Guests per Month",
          backgroundColor: "#79AEC8",
          borderColor: "#417690",
          data: chartData.values
        }
     ]
  },
  options: {
     title: {
        text: "Total per Month",
        display: true
     }
  }
});