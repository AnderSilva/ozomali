import { Component } from '@angular/core';

@Component({
  selector: 'app-product-screen',
  templateUrl: './product-screen.component.html',
  styleUrls: ['./product-screen.component.scss'],
})
export class ProductScreenComponent {
  public products: any;
  public resultProduct: any;
  public shouldSearch: boolean;

  constructor() {
    this.shouldSearch = true;
  }

  public setProducts(products: any): void {
    this.products = products;
  }

  public loadProduct(product: any): void {
    this.resultProduct = product;
    this.shouldSearch = false;
    this.products = undefined;
  }

  public clearSearch(): void {
    this.shouldSearch = true;
  }
}
