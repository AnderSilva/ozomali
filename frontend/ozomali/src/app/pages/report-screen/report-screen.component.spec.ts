import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReportScreenComponent } from './report-screen.component';

describe('ReportScreenComponent', () => {
  let component: ReportScreenComponent;
  let fixture: ComponentFixture<ReportScreenComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ReportScreenComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ReportScreenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
