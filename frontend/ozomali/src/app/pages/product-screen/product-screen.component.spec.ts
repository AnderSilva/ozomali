import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProductScreenComponent } from './product-screen.component';

describe('ProductScreenComponent', () => {
  let component: ProductScreenComponent;
  let fixture: ComponentFixture<ProductScreenComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProductScreenComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProductScreenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
