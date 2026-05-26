import { inject } from '@angular/core';
import { forkJoin, tap } from 'rxjs';
import { HopfieldService } from '../../../services/hopfield';

export const MainDashboardResolver = () => {
  const service = inject(HopfieldService);
  // Esperamos a ambos datos antes de continuar la navegación
  return forkJoin({
    machines: service.getMachines(),
    exercises: service.getExercises()
  }).pipe(
    tap(result => console.log("¡El resolver de main-dashboard ha recibido esto del backend!", result))
  );
};