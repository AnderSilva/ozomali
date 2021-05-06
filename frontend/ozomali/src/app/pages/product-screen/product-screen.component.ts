import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-product-screen',
  templateUrl: './product-screen.component.html',
  styleUrls: ['./product-screen.component.scss'],
})
export class ProductScreenComponent implements OnInit {
  public products: any;
  public resultProduct: any;
  public shouldSearch: boolean = true;

  constructor() {}

  ngOnInit(): void {}

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
