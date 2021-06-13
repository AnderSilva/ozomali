import { Component, OnInit } from '@angular/core';
import { take } from 'rxjs/operators';
import { ProductService } from 'src/app/services/product/product.service';

@Component({
  selector: 'app-movings-screen',
  templateUrl: './movings-screen.component.html',
  styleUrls: ['./movings-screen.component.scss'],
})
export class MovingsScreenComponent implements OnInit {
  public movings: any;

  public products: any;
  public productNames: string[];

  constructor(private productService: ProductService) {
    this.products = [];
    this.productNames = [];
  }

  ngOnInit(): void {
    this.initializeProducts();
  }

  public setMovings(movings: any): void {
    this.movings = movings;
  }

  public initializeProducts(): void {
    this.productService
      .getProducts()
      .pipe(take(1))
      .subscribe(products => {
        this.products = products.data;

        products.data.forEach((vendor: any) => {
          this.productNames.push(vendor.nome);
        });
      });
  }
}
