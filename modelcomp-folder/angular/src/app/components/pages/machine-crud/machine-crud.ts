import {
  Component,
  OnInit
} from '@angular/core';

import {
  CommonModule
} from '@angular/common';

import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule
} from '@angular/forms';

import {
  HopfieldService
} from '../../../services/hopfield';

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

  constructor(
    private hopfieldService: HopfieldService,
    private fb: FormBuilder
  ) {

    this.machineForm = this.fb.group({

      name: [
        '',
        Validators.required
      ],

      dims: [
        0,
        Validators.required
      ],

      training_data: [
        '',
        Validators.required
      ]

    });

  }

  ngOnInit(): void {
    console.log('NGONINIT MACHINE');
    this.loadMachines();
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

  onSubmit(): void {

    if (this.machineForm.invalid) {
      return;
    }

    this.loading = true;

    const formData = this.machineForm.value;

    try {

      const parsedData =
        JSON.parse(formData.training_data);

      const payload = {

        name: formData.name,

        training_data: parsedData

      };

      this.hopfieldService
        .createMachine(payload)
        .subscribe({

          next: () => {

            // Recargar tabla
            this.loadMachines();

            // Reset limpio
            this.machineForm.reset({

              name: '',
              dims: 0,
              training_data: ''

            });

            this.loading = false;

            alert(
              '¡Máquina guardada con éxito!'
            );

          },

          error: (err) => {

            console.error(err);

            this.loading = false;

            alert(
              'Error en backend: ' +
              JSON.stringify(err.error)
            );

          }

        });

    } catch (e) {

      this.loading = false;

      alert(
        'JSON inválido en training_data.'
      );

    }

  }

  deleteMachine(id: number): void {

    const confirmed =
      confirm(
        '¿Seguro que deseas eliminar esta máquina?'
      );

    if (!confirmed) {
      return;
    }

    this.hopfieldService
      .deleteMachine(id)
      .subscribe({

        next: () => {

          this.loadMachines();

        },

        error: (err) => {

          console.error(err);

          alert(
            'No se pudo eliminar.'
          );

        }

      });

  }

}