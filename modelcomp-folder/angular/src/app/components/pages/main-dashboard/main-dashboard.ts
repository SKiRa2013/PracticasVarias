import {
  Component,
  OnInit
} from '@angular/core';

import {
  CommonModule
} from '@angular/common';

import {
  RouterLink,
  Router,
  NavigationEnd
} from '@angular/router';

import {
  filter,
  forkJoin
} from 'rxjs';

import {
  HopfieldService
} from '../../../services/hopfield';

@Component({
  selector: 'app-main-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink
  ],
  templateUrl: './main-dashboard.html'
})
export class MainDashboardComponent
  implements OnInit {

  machinesWithExercises: any[] = [];

  loading = false;
  error = false;

  constructor(
    private hopfieldService: HopfieldService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.loadDashboard();
  }

  loadDashboard(): void {

    this.loading = true;
    this.error = false;

    forkJoin({

      machines:
        this.hopfieldService.getMachines(),

      exercises:
        this.hopfieldService.getExercises()

    }).subscribe({

      next: (result) => {

        this.machinesWithExercises =
          result.machines.map(
            (machine: any) => {

              const ejerciciosFiltrados =
                result.exercises.filter(
                  (ex: any) =>
                    ex.machine === machine.id
                );

              return {

                ...machine,

                ejerciciosFiltrados

              };

            }
          );


        this.loading = false;


      },

      error: (err) => {

        console.error(err);

        this.loading = false;
        this.error = true;

      }

    });

  }

}