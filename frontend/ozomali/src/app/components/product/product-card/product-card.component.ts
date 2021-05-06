import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-product-card',
  templateUrl: './product-card.component.html',
  styleUrls: ['./product-card.component.scss'],
})
export class ProductCardComponent implements OnInit {
  @Input() product: any;
  @Output() public clickProduct = new EventEmitter<any>();

  constructor() {}

  ngOnInit(): void {}

  public chooseCard() {
    this.clickProduct.emit(this.product);
  }
}
