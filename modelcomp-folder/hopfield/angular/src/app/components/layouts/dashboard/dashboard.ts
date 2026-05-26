import { Component } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-dashboard-layout',
  standalone: true,
  // ¡CRUCIAL! Si no importas estos tres, las etiquetas del HTML fallarán
  imports: [RouterOutlet, RouterLink, RouterLinkActive], 
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css'] // Si decides añadirle estilos personalizados
})
export class DashboardComponent {
  // Aquí no necesitas lógica de Hopfield, solo maneja el diseño estructural
}