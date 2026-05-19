import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HopfieldService } from '../../../services/hopfield';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-exercise-crud',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './exercise-crud.html'
})
export class ExerciseCrudComponent implements OnInit {
  exercises: any[] = [];
  machines: any[] = []; // Necesarias para el selector <select>
  exerciseForm: FormGroup;
  apiUrl = 'http://localhost:8000/api/exercises/';
  baseUrl = 'http://localhost:8000'; // Raíz para las imágenes de Django

  constructor(private hopfieldService: HopfieldService, private fb: FormBuilder) {
    this.exerciseForm = this.fb.group({
      machine: ['', Validators.required],
      inputs: ['', Validators.required]
    });
  }

  ngOnInit() {
    this.loadExercises();
    this.loadMachines();
  }

  loadExercises() {
    this.hopfieldService.getExercises().subscribe(data => this.exercises = data);
  }

  loadMachines() {
    this.hopfieldService.getMachines().subscribe(data => this.machines = data);
  }

  onSubmit() {
    if (this.exerciseForm.invalid) return;

    const formData = this.exerciseForm.value;
    try {
      const parsedInputs = JSON.parse(formData.inputs);
      const payload = {
        machine: parseInt(formData.machine),
        inputs: parsedInputs
      };

      this.hopfieldService.createExercise(payload).subscribe({
        next: () => {
          this.loadExercises();
          this.exerciseForm.reset();
          alert('¡Simulación completada con éxito!');
        },
        error: (err) => alert('Error en la red: ' + JSON.stringify(err.error))
      });
    } catch (e) {
      alert('Error en el input: Debe ser un array JSON de números. Ej: [[1, -1, 1], [-1, 1, -1], [1, 1, -1]]');
    }
  }

  deleteExercise(id: number) {
    if (confirm('¿Deseas eliminar el registro de este ejercicio?')) {
      this.hopfieldService.deleteExercise(id).subscribe(() => this.loadExercises());
    }
  }
}