import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MovingsScreenComponent } from './movings-screen.component';

describe('MovingsScreenComponent', () => {
  let component: MovingsScreenComponent;
  let fixture: ComponentFixture<MovingsScreenComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MovingsScreenComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MovingsScreenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
