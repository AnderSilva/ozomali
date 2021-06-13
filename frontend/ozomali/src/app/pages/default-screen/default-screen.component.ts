import { Component } from '@angular/core';
import { UserQuery, UserService } from 'src/app/stores/user';
@Component({
  selector: 'app-default-screen',
  templateUrl: './default-screen.component.html',
  styleUrls: ['./default-screen.component.scss'],
})
export class DefaultScreenComponent {
  constructor(private userService: UserService, private userQuery: UserQuery) {}

  invalidateToken(): void {
    const currentUserInfo = this.userQuery.userInfo;

    this.userService.updateAuthentication('tokenInvalido', currentUserInfo);
  }
}
