import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VendorScreenComponent } from './vendor-screen.component';

describe('VendorScreenComponent', () => {
  let component: VendorScreenComponent;
  let fixture: ComponentFixture<VendorScreenComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ VendorScreenComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(VendorScreenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
