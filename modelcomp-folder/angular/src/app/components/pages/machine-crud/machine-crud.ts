import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';

import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';

import { HopfieldService } from '../../../services/hopfield';

@Component({
  selector: 'app-machine-crud',
  standalone: true,
  templateUrl: './machine-crud.html',
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
})
export class MachineCrudComponent implements OnInit {

  machines: any[] = [];

  machineForm: FormGroup;

  loading = false;
  loadingTable = false;
  error = false;

  @ViewChild('imageCanvas') canvasRef!: ElementRef<HTMLCanvasElement>;

  constructor(
    private hopfieldService: HopfieldService,
    private fb: FormBuilder,
    private route: ActivatedRoute
  ) {

    this.machineForm = this.fb.group({
      name: ['', Validators.required],
      dims: [0, Validators.required],
      training_data: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    const resolvedData = this.route.snapshot.data['data'];
    
    if (resolvedData && resolvedData.machines) {
      this.machines = resolvedData.machines;
    } else {
      console.error("No se detectaron valores de resolvedData", resolvedData, resolvedData.machines)
    }
  }

  loadMachines(): void {

    console.log('LOAD MACHINES EJECUTADO');

    this.loadingTable = true;

    this.hopfieldService
      .getMachines()
      .subscribe({

        next: (data) => {
          console.log('DATOS RECIBIDOS:', data);

          this.machines = data;

          console.log('VARIABLE machines:', this.machines);
          
          this.loadingTable = false;
        },
      });
  }

  async onFileSelected(event: any) {
    const file = event.target.files[0];
    if (!file) return;

    try {
      const matrix = await this.imageToMatrix(file, this.machineForm.value.dims);
      this.machineForm.patchValue({
        training_data: JSON.stringify(matrix)
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
    if (this.machineForm.invalid) {
      return;
    }

    this.loading = true;

    const formData = this.machineForm.value;

    try {
      const parsedData = JSON.parse(formData.training_data);

      const payload = {
        name: formData.name,
        training_data: parsedData
      };

      this.hopfieldService.createMachine(payload).subscribe({
          next: ( newMachine ) => {
            this.machines = [...this.machines, newMachine];

            // Reset limpio
            this.machineForm.reset({
              name: '',
              dims: 0,
              training_data: ''
            });

            this.loading = false;

            alert('¡Máquina guardada con éxito!');
          },

          error: (err) => {
            console.error(err);

            this.loading = false;

            alert('Error en backend: ' + JSON.stringify(err.error));
          }
        });
    } catch (e) {

      this.loading = false;

      alert('JSON inválido en training_data.');
    }
  }

  deleteMachine(id: number): void {
    const confirmed = confirm('¿Seguro que deseas eliminar esta máquina?');

    if (!confirmed) return;
    
    this.hopfieldService.deleteMachine(id).subscribe({
        next: () => {
          this.machines = this.machines.filter(m => m.id !== id);
        },

        error: (err) => {
          console.error(err);

          alert('No se pudo eliminar. Recargando tabla...');

          // Recargar tabla
          this.loadMachines();
        }
      });
  }
}