import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { HopfieldService } from '../../../services/hopfield';

@Component({
  selector: 'app-machine-crud',
  standalone: true,
  templateUrl: './machine-crud.html',
  imports: [CommonModule, ReactiveFormsModule],
})
export class MachineCrudComponent implements OnInit {
  machines: any[] = [];
  machineForm: FormGroup;

  constructor(private hopfieldService: HopfieldService, private fb: FormBuilder) {
    this.machineForm = this.fb.group({
      name: ['', Validators.required],
      training_data: ['', Validators.required]
    });
  }

  ngOnInit() {
    this.loadMachines();
  }

  loadMachines() {
    this.hopfieldService.getMachines().subscribe(data => this.machines = data);
  }

  onSubmit() {
    if (this.machineForm.invalid) return;

    const formData = this.machineForm.value;
    try {
      // Intentamos parsear el string a JSON (matriz) para que viaje como objeto estructurado
      const parsedData = JSON.parse(formData.training_data);
      
      // Armamos el payload EXACTO que espera tu endpoint de Django
      const payload = {
        name: formData.name,
        training_data: parsedData
      };

      this.hopfieldService.createMachine(payload).subscribe({
        next: () => {
          this.loadMachines(); // Refrescamos la tabla con los datos que nos devuelva Django (incluyendo el id y dims calculado)
          this.machineForm.reset();
          alert('¡Máquina guardada con éxito en el servidor!');
        },
        error: (err) => alert('Error en el backend: ' + JSON.stringify(err.error))
      });

    } catch (e) {
      alert('Error de formato local: Asegúrate de ingresar un JSON válido para los datos de entrenamiento.');
    }
  }

  deleteMachine(id: number) {
    if (confirm('¿Seguro que deseas eliminar esta máquina?')) {
      this.hopfieldService.deleteMachine(id).subscribe(() => this.loadMachines());
    }
  }
}