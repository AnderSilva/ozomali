import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-user-card',
  templateUrl: './user-card.component.html',
  styleUrls: ['./user-card.component.scss'],
})
export class UserCardComponent {
  @Input() user: any;
  @Output() public clickUser = new EventEmitter<any>();

  public chooseCard(): void {
    this.clickUser.emit(this.user);
  }
}
