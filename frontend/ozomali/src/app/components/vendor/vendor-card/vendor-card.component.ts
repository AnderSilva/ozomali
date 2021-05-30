import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-vendor-card',
  templateUrl: './vendor-card.component.html',
  styleUrls: ['./vendor-card.component.scss'],
})
export class VendorCardComponent {
  @Input() vendor: any;
  @Output() public clickVendor = new EventEmitter<any>();

  public chooseCard() {
    this.clickVendor.emit(this.vendor);
  }
}
