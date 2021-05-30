import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-product-card',
  templateUrl: './product-card.component.html',
  styleUrls: ['./product-card.component.scss'],
})
export class ProductCardComponent {
  @Input() product: any;
  @Output() public clickProduct = new EventEmitter<any>();

  public chooseCard() {
    this.clickProduct.emit(this.product);
  }
}
