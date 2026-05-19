import { Routes } from '@angular/router';
import { DashboardComponent } from './components/layouts/dashboard/dashboard';
import { MainDashboardComponent } from './components/pages/main-dashboard/main-dashboard';
import { MachineCrudComponent } from './components/pages/machine-crud/machine-crud';
import { ExerciseCrudComponent } from './components/pages/exercise-crud/exercise-crud';

export const routes: Routes = [
  {
    path: '',
    component: DashboardComponent,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: MainDashboardComponent },
      { path: 'machines', component: MachineCrudComponent },
      { path: 'exercises', component: ExerciseCrudComponent }
    ]
  },
  { path: '**', redirectTo: 'dashboard' },
];