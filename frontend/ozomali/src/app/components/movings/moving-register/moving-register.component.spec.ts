import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MovingRegisterComponent } from './moving-register.component';

describe('MovingRegisterComponent', () => {
  let component: MovingRegisterComponent;
  let fixture: ComponentFixture<MovingRegisterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MovingRegisterComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MovingRegisterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
