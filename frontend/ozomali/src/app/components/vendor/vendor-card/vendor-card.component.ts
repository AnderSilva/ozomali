import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-vendor-card',
  templateUrl: './vendor-card.component.html',
  styleUrls: ['./vendor-card.component.scss'],
})
export class VendorCardComponent implements OnInit {
  @Input() vendor: any;
  @Output() public clickVendor = new EventEmitter<any>();

  constructor() {}

  ngOnInit(): void {}

  public chooseCard() {
    this.clickVendor.emit(this.vendor);
  }
}
