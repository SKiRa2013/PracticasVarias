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
  ReactiveFormsModule,
  Validators
} from '@angular/forms';

import {
  HopfieldService
} from '../../../services/hopfield';

@Component({
  selector: 'app-exercise-crud',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  templateUrl: './exercise-crud.html'
})
export class ExerciseCrudComponent implements OnInit {

  exercises: any[] = [];
  machines: any[] = [];

  exerciseForm: FormGroup;

  loading = false;
  loadingTable = false;
  error = false;

  constructor(
    private hopfieldService: HopfieldService,
    private fb: FormBuilder
  ) {

    this.exerciseForm = this.fb.group({

      machine: [
        '',
        Validators.required
      ],

      inputs: [
        '',
        Validators.required
      ]

    });

  }

  ngOnInit(): void {
    this.refreshData();
  }

  refreshData(): void {

    this.loadExercises();
    this.loadMachines();

  }

  loadExercises(): void {

    this.loadingTable = true;
    this.error = false;

    this.hopfieldService
      .getExercises()
      .subscribe({

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

    this.hopfieldService
      .getMachines()
      .subscribe({

        next: (data) => {

          this.machines = data;

        },

        error: (err) => {

          console.error(err);

        }

      });

  }

  onSubmit(): void {

    if (this.exerciseForm.invalid) {
      return;
    }

    this.loading = true;

    const formData = this.exerciseForm.value;

    try {

      const parsedInputs =
        JSON.parse(formData.inputs);

      const payload = {

        machine: parseInt(formData.machine),

        inputs: parsedInputs

      };

      this.hopfieldService
        .createExercise(payload)
        .subscribe({

          next: () => {

            // Recargar historial
            this.loadExercises();

            // Reset limpio
            this.exerciseForm.reset({

              machine: '',
              inputs: ''

            });

            this.loading = false;

            alert(
              '¡Simulación completada!'
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
        'JSON inválido en inputs.'
      );

    }

  }

  deleteExercise(id: number): void {

    const confirmed =
      confirm(
        '¿Deseas eliminar este ejercicio?'
      );

    if (!confirmed) {
      return;
    }

    this.hopfieldService
      .deleteExercise(id)
      .subscribe({

        next: () => {

          this.loadExercises();

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