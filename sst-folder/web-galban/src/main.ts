const showIp = document.getElementById("show-ip") as HTMLParagraphElement;
const fileName = window.location.pathname.split("/").pop();

showIp.textContent = `Corriendo ${fileName} en ${window.location.origin}`;
