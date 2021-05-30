import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MovingCardComponent } from './moving-card.component';

describe('MovingCardComponent', () => {
  let component: MovingCardComponent;
  let fixture: ComponentFixture<MovingCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MovingCardComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MovingCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
