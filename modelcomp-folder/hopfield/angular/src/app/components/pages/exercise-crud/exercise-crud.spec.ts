import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExerciseCrud } from './exercise-crud';

describe('ExerciseCrud', () => {
    let component: ExerciseCrud;
    let fixture: ComponentFixture<ExerciseCrud>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [ExerciseCrud],
        }).compileComponents();

        fixture = TestBed.createComponent(ExerciseCrud);
        component = fixture.componentInstance;
        await fixture.whenStable();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
