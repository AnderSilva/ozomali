import { Component, EventEmitter, Output } from '@angular/core';
import { Observable } from 'rxjs';
import { UserQuery, UserService } from 'src/app/stores/user';

@Component({
  selector: 'app-header-menu',
  templateUrl: './header-menu.component.html',
  styleUrls: ['./header-menu.component.scss'],
})
export class HeaderMenuComponent {
  userInfo$: Observable<any>;

  constructor(private userQuery: UserQuery, private userService: UserService) {
    this.userInfo$ = this.userQuery.userInfo$;
  }

  public logout(): void {
    this.userService.logout();
  }
}
