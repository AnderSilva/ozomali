import { Component } from '@angular/core';

@Component({
  selector: 'app-vendor-screen',
  templateUrl: './vendor-screen.component.html',
  styleUrls: ['./vendor-screen.component.scss'],
})
export class VendorScreenComponent {
  public vendors: any;
  public resultVendor: any;
  public shouldSearch: boolean;

  constructor() {
    this.shouldSearch = true;
  }

  public setVendors(vendors: any): void {
    this.vendors = vendors;
  }

  public loadVendor(vendor: any): void {
    this.resultVendor = vendor;
    this.shouldSearch = false;
    this.vendors = undefined;
  }

  public clearSearch(): void {
    this.shouldSearch = true;
  }
}
