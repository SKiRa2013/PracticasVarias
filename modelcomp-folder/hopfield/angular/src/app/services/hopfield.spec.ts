import { TestBed } from '@angular/core/testing';

import { Hopfield } from './hopfield';

describe('Hopfield', () => {
    let service: Hopfield;

    beforeEach(() => {
        TestBed.configureTestingModule({});
        service = TestBed.inject(Hopfield);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });
});
