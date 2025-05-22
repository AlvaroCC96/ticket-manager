const form = document.getElementById("uploadForm");
const fileInput = document.getElementById("file");
const btnSubmit = document.getElementById("btn-submit");

form.addEventListener("submit", async function(e) {
  e.preventDefault();
  fileInput.disabled = true;
  btnSubmit.disabled = true;

  if (!fileInput.files.length) {
    Swal.fire({ icon: "warning", title: "Selecciona un archivo" });
    fileInput.disabled = false;
    btnSubmit.disabled = false;
    return;
  }

  // 1) Construyo FormData explícitamente
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  console.log("FormData entries:", [...formData.entries()]);

  try {
    // 2) Ruta EXACTA sin barra si tu decorator no la lleva
    const res = await fetch("/api/upload/", {
      method: "POST",
      body: formData
    });

    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    const result = await res.json();

    await Swal.fire({
      icon: "success",
      title: "Boleta procesada",
      html: `
        <p><strong>Servicio:</strong> ${result.servicio}</p>
        <p><strong>Monto:</strong> $${result.monto.toLocaleString("es-CL")}</p>
        <p><strong>Fecha:</strong> ${new Date(result.fecha).toLocaleDateString("es-CL")}</p>
      `,
      timer: 5000,
      showConfirmButton: false
    });

    fileInput.value = "";

  } catch (err) {
    console.error(err);
    await Swal.fire({
      icon: "error",
      title: "Error al subir",
      text: err.message || "Revisa la consola",
      confirmButtonText: "Cerrar"
    });
  } finally {
    fileInput.disabled = false;
    btnSubmit.disabled = false;
  }
});