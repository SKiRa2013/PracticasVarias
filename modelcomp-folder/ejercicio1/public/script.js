const button = document.getElementById("calc");

button.addEventListener("click", () => {
    const lado_a = document.getElementById("lado1").value;
    const lado_b = document.getElementById("lado2").value;
    const lado_c = document.getElementById("lado3").value;

    const tipo_tri = document.getElementById("tipo-triangulo");
    const area_tri = document.getElementById("area-triangulo");

    const dibujo = document.getElementById("drawzone");
    const context = dibujo.getContext("2d");

    const a = Number.parseFloat(lado_a);
    const b = Number.parseFloat(lado_b);
    const c = Number.parseFloat(lado_c);

    let tipo = "";
    let area = 0;
    
    if ( (a <= 0 || b <= 0 || c <= 0) ) {
        alert("Datos incorrectos de lado");
    } else if ( !( (a + b > c) && (a + c > b) && (b + c > a) ) ) {
        alert("Los lados entregados no pueden formar un triángulo");
    } else {
        let semiper = (a + b + c) / 2;
        
        area = Math.sqrt(semiper * (semiper - a) * (semiper - b) * (semiper - c)); 

        if (a == b && b == c){
            tipo = "Equilátero";
        } else if (a == b || a == c || b == c){
            tipo = "Isósceles";
        } else {
            tipo = "Escaleno";
        }

        let offset_x = 10;
        let offset_y = dibujo.width / 2;

        let scale = 100;

        context.clearRect(0, 0, dibujo.width, dibujo.height);
        context.beginPath();

        context.moveTo(offset_x, offset_y);
        context.lineTo(offset_x + (c * scale), offset_y);

        let angle = Math.acos( (b * b + c * c - a * a) / (2 * b * c) );
        context.lineTo(offset_x + (b * Math.cos(angle) * scale),
                       offset_y - (b * Math.sin(angle) * scale));        
        
        context.lineTo(offset_x, offset_y);
        context.closePath();

        context.lineWidth = 2;
        context.strokeStyle = "red";
        context.stroke();          
        context.fillStyle = "rgba(250, 150, 208, 0.92)";
        context.fill();            
    }

    tipo_tri.innerText = tipo;
    area_tri.innerText = area.toFixed(6);
});
