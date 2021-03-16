import { Component, EventEmitter, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-header-menu',
  templateUrl: './header-menu.component.html',
  styleUrls: ['./header-menu.component.scss'],
})
export class HeaderMenuComponent implements OnInit {
  @Output() public shouldLogout: EventEmitter<void> = new EventEmitter();
  constructor() {}

  ngOnInit(): void {}

  public logout(): void {
    this.shouldLogout.emit();
  }
}
