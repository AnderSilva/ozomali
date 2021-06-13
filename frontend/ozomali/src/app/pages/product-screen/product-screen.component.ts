import { Component, OnInit } from '@angular/core';
import { take } from 'rxjs/operators';
import { VendorService } from 'src/app/services/vendor/vendor.service';

@Component({
  selector: 'app-product-screen',
  templateUrl: './product-screen.component.html',
  styleUrls: ['./product-screen.component.scss'],
})
export class ProductScreenComponent implements OnInit {
  public products: any;
  public resultProduct: any;
  public shouldSearch: boolean;

  public vendors: any;
  public vendorNames: string[];

  constructor(private vendorService: VendorService) {
    this.shouldSearch = true;
    this.vendors = [];
    this.vendorNames = [];
  }

  ngOnInit(): void {
    this.initializeVendors();
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

  public initializeVendors(): void {
    this.vendorService
      .getVendors()
      .pipe(take(1))
      .subscribe(vendors => {
        this.vendors = vendors?.data;

        vendors?.data.forEach((vendor: any) => {
          this.vendorNames.push(vendor.nome);
        });
      });
  }
}
