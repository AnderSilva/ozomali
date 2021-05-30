import { Component, EventEmitter, Output } from '@angular/core';
import { Observable } from 'rxjs';
import { UserQuery } from 'src/app/stores/user';

@Component({
  selector: 'app-header-menu',
  templateUrl: './header-menu.component.html',
  styleUrls: ['./header-menu.component.scss'],
})
export class HeaderMenuComponent {
  @Output() public shouldLogout: EventEmitter<void> = new EventEmitter();
  userInfo$: Observable<any>;

  constructor(private userQuery: UserQuery) {
    this.userInfo$ = this.userQuery.userInfo$;
  }

  public logout(): void {
    this.shouldLogout.emit();
  }
}
