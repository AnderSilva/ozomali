import { Component, EventEmitter, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-header-menu',
  templateUrl: './header-menu.component.html',
  styleUrls: ['./header-menu.component.scss'],
})
export class HeaderMenuComponent implements OnInit {
  @Output() public shouldLogout: EventEmitter<void>;
  constructor() {
    this.shouldLogout = new EventEmitter();
  }

  ngOnInit(): void {}

  public logout(): void {
    this.shouldLogout.emit();
  }
}
