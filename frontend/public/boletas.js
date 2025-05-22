// boletas.js
async function loadBoletas() {
    try {
      const res = await fetch("/api/boletas/");
      const boletas = await res.json();
      const tbody = document.getElementById("boletasTableBody");
      tbody.innerHTML = "";
      boletas.forEach(b => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${b.id}</td>
          <td>${b.empresa??"-"}</td>
          <td>${b.servicio}</td>
          <td>${b.monto.toLocaleString('es-CL', {minimumFractionDigits: 0})}</td>
          <td>${new Date(b.fecha).toLocaleDateString('es-CL')}</td>
          <td><a href="/uploads/${b.archivo}" target="_blank">${b.archivo}</a></td>
        `;
        tbody.appendChild(tr);
      });
    } catch (e) {
      console.error(e);
    }
  }

document.addEventListener('DOMContentLoaded', () => {
// asumiendo que loadBoletas() está definido en boletas.js
if (typeof loadBoletas === 'function') {
    loadBoletas();
}
});
