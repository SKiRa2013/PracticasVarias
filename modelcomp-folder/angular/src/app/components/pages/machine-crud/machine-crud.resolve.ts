import { inject } from '@angular/core';
import { tap, map } from 'rxjs';
import { HopfieldService } from '../../../services/hopfield';

export const MachineResolver = () => {
  const service = inject(HopfieldService);
  // Esperamos a ambos datos antes de continuar la navegación
  return service.getMachines().pipe(
    map(machines => ({ machines })),
    tap(result => console.log("¡El resolver de machine ha recibido esto del backend!", result))
  );
};