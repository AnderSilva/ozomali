import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-vendor-screen',
  templateUrl: './vendor-screen.component.html',
  styleUrls: ['./vendor-screen.component.scss'],
})
export class VendorScreenComponent implements OnInit {
  public vendors: any;
  public resultVendor: any;
  public shouldSearch: boolean = true;

  constructor() {}

  ngOnInit(): void {}

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
