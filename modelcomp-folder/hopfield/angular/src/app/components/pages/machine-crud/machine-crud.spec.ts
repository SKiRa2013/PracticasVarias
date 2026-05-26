import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MachineCrud } from './machine-crud';

describe('MachineCrud', () => {
    let component: MachineCrud;
    let fixture: ComponentFixture<MachineCrud>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [MachineCrud],
        }).compileComponents();

        fixture = TestBed.createComponent(MachineCrud);
        component = fixture.componentInstance;
        await fixture.whenStable();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
