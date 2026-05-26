import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';

import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';

import { HopfieldService } from '../../../services/hopfield';

@Component({
  selector: 'app-exercise-crud',
  standalone: true,
  templateUrl: './exercise-crud.html',
  imports: [
    CommonModule,
    ReactiveFormsModule
  ]
})
export class ExerciseCrudComponent implements OnInit {

  exercises: any[] = [];
  machines: any[] = [];

  selectedMachine: any = null;

  exerciseForm: FormGroup;

  loading = false;
  loadingTable = false;
  error = false;

  @ViewChild('imageCanvas') canvasRef!: ElementRef<HTMLCanvasElement>;

  constructor(
    private hopfieldService: HopfieldService,
    private fb: FormBuilder,
    private route: ActivatedRoute
  ) {
    this.exerciseForm = this.fb.group({
      machine: ['', Validators.required],
      inputs: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    const resolvedData = this.route.snapshot.data['data'];
    
    if (!resolvedData) {
      console.error("No se detectaron valores de resolvedData", resolvedData);
      return;
    } 

    if (!resolvedData.machines) {
      console.error("No se detectaron valores de resolvedData para máquinas", resolvedData.machines);
      return;
    }

    if (!resolvedData.exercises) {
      console.error("No se detectaron valores de resolvedData para ejercicios", resolvedData.exercises);
      return;
    }

      this.machines = resolvedData.machines;
      this.exercises = resolvedData.exercises;
  }

  refreshData(): void {
    this.loadExercises();
    this.loadMachines();
  }

  loadExercises(): void {
    this.loadingTable = true;
    this.error = false;

    this.hopfieldService.getExercises().subscribe({
        next: (data) => {
          this.exercises = data;
          this.loadingTable = false;
        },

        error: (err) => {
          console.error(err);

          this.loadingTable = false;
          this.error = true;
        }
      });
  }

  loadMachines(): void {
    this.hopfieldService.getMachines().subscribe({
        next: (data) => {
          this.machines = data;
        },

        error: (err) => {
          console.error(err);
        }
      });
  }

  onMachineChange(event: any) {
    const machineId = event.target.value;
    // Buscamos la máquina completa en el array que ya cargaste con el resolver
    this.selectedMachine = this.machines.find(m => m.id == machineId);
    
    if (this.selectedMachine) {
      console.log("Máquina seleccionada, dimensiones:", this.selectedMachine.dims);
    }
  }

  async onFileSelected(event: any) {
    const file = event.target.files[0];
    
    if (!file || !this.selectedMachine ) { 
      alert("¡Primero selecciona una máquina para saber sus dimensiones!");
      event.target.value = '';
      return;
    }

    try {
      const matrix = await this.imageToMatrix(file, this.selectedMachine.dims);
      this.exerciseForm.patchValue({
        inputs: JSON.stringify(matrix)
      });
    } catch (error) {
      console.error("Error al procesar la imagen:", error);
      alert("No se pudo procesar la imagen. Intenta con otra.");
    }
  }

  async imageToMatrix(file: File, dims: number): Promise<number[][]> {
    const size = Math.floor(Math.sqrt(dims));
    
    // Usamos una Promesa para envolver la carga de la imagen
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.src = URL.createObjectURL(file);
      
      img.onload = async () => {
        // Ahora estamos seguros de que la imagen tiene ancho y alto
        const canvas = this.canvasRef.nativeElement;
        canvas.width = size;
        canvas.height = size;
        const ctx = canvas.getContext('2d')!;
        
        ctx.drawImage(img, 0, 0, size, size);
        const imageData = ctx.getImageData(0, 0, size, size);
        const data = imageData.data;

        const matrix: number[] = [];
        for (let i = 0; i < data.length; i += 4) {
          const grayscale = (data[i] + data[i + 1] + data[i + 2]) / 3;
          matrix.push(grayscale > 128 ? 1.0 : -1.0);
        }
        
        // Liberamos la memoria del objeto URL
        URL.revokeObjectURL(img.src);
        resolve([matrix]);
      };
      
      img.onerror = (err) => reject(err);
    });
  }

  onSubmit(): void {
    if (this.exerciseForm.invalid) {
      return;
    }

    this.loading = true;

    const formData = this.exerciseForm.value;

    try {
      const parsedInputs = JSON.parse(formData.inputs);

      const payload = {
        machine: parseInt(formData.machine),
        inputs: parsedInputs
      };

      this.hopfieldService.createExercise(payload).subscribe({
          next: ( newExercise ) => {
            this.exercises = [...this.exercises, newExercise];

            // Reset limpio
            this.exerciseForm.reset({
              machine: '',
              inputs: ''
            });

            this.loading = false;

            alert('¡Simulación completada!');
          },

          error: (err) => {
            console.error(err);

            this.loading = false;

            alert('Error en backend: ' + JSON.stringify(err.error));
          }
        });
    } catch (e) {

      this.loading = false;

      alert('JSON inválido en inputs.');
    }
  }

  deleteExercise(id: number): void {
    const confirmed = confirm('¿Deseas eliminar este ejercicio?');

    if (!confirmed) return;
    
    this.hopfieldService.deleteExercise(id).subscribe({
        next: () => {
          this.exercises = this.exercises.filter(e => e.id !== id);
        },

        error: (err) => {
          console.error(err);

          alert('No se pudo eliminar. Recargando tabla...');

          // Recargar tabla
          this.loadMachines();
          this.loadExercises();
        }
      });
  }
}