const showIp = document.getElementById("show-ip");
const fileName = window.location.pathname.split("/").pop();
showIp.textContent = `Corriendo ${fileName} en ${window.location.origin}`;
export {};
//# sourceMappingURL=main.js.map