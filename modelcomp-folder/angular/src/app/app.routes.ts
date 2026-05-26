import { Routes } from '@angular/router';
import { DashboardComponent } from './components/layouts/dashboard/dashboard';
import { MainDashboardComponent } from './components/pages/main-dashboard/main-dashboard';
import { MachineCrudComponent } from './components/pages/machine-crud/machine-crud';
import { ExerciseCrudComponent } from './components/pages/exercise-crud/exercise-crud';

import { MainDashboardResolver } from './components/pages/main-dashboard/main-dashboard.resolver';
import { MachineResolver } from './components/pages/machine-crud/machine-crud.resolve';
import { ExerciseResolver } from './components/pages/exercise-crud/exercise-crud.resolve';

export const routes: Routes = [
  {
    path: '',
    component: DashboardComponent,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { 
        path: 'dashboard',
        component: MainDashboardComponent,
        resolve: { data: MainDashboardResolver },
      },
      { 
        path: 'machines',
        component: MachineCrudComponent,
        resolve: { data: MachineResolver }
      },
      { 
        path: 'exercises',
        component: ExerciseCrudComponent,
        resolve: { data: ExerciseResolver }
      }
    ]
  },
  { path: '**', redirectTo: 'dashboard' },
];