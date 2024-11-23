// loadHeader.js
document.addEventListener("DOMContentLoaded", function() {
  // ヘッダーを読み込む
  fetch("header.html")
    .then(response => response.text())
    .then(data => {
      document.getElementById("header-placeholder").innerHTML = data;
    })
    .catch(error => console.error("Error loading header:", error));
});
