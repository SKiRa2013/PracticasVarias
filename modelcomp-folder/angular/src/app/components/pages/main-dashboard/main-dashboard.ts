import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HopfieldService } from '../../../services/hopfield';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-main-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './main-dashboard.html'
})
export class MainDashboardComponent implements OnInit {
  machines: any[] = [];
  exercises: any[] = [];
  apiUrl = 'http://localhost:8000/api';

  constructor(private hopfieldService: HopfieldService) {}

  ngOnInit() {
    // Cargamos en paralelo máquinas y ejercicios para cruzarlos en el cliente
    this.hopfieldService.getMachines().subscribe(m => this.machines = m);
    this.hopfieldService.getExercises().subscribe(e => this.exercises = e);
  }

  // Filtra los ejercicios que pertenecen a una máquina específica
  getExercisesForMachine(machineId: number) {
    return this.exercises.filter(ex => ex.machine === machineId);
  }
}