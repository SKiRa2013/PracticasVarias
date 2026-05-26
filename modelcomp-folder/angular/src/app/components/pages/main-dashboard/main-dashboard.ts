import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';

@Component({
  selector: 'app-main-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './main-dashboard.html'
})
export class MainDashboardComponent implements OnInit {
  // Esta es la variable que tu HTML está esperando
  machinesWithExercises: any[] = [];

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.route.data.subscribe(({ data }) => {
    if (data && data.machines && data.exercises) {
      this.machinesWithExercises = data.machines.map((machine: any) => ({
        ...machine,
        ejerciciosFiltrados: data.exercises.filter((ex: any) => ex.machine === machine.id)
      }));
      console.log("Datos cargados y combinados:", this.machinesWithExercises);
    } else {
      console.error("Los datos recibidos en el componente están incompletos o vacíos:", data);
    }
  });
  }
}