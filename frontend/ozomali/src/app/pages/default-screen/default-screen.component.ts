import { Component } from '@angular/core';
import { UserQuery, UserService } from 'src/app/stores/user';
@Component({
  selector: 'app-default-screen',
  templateUrl: './default-screen.component.html',
  styleUrls: ['./default-screen.component.scss'],
})
export class DefaultScreenComponent {
  easterEggShown: boolean;

  constructor(private userService: UserService, private userQuery: UserQuery) {
    this.easterEggShown = false;
  }

  easterEgg(): void {
    this.easterEggShown = !this.easterEggShown;
  }

  invalidateToken(): void {
    const currentUserInfo = this.userQuery.userInfo;

    this.userService.updateAuthentication('tokenInvalido', currentUserInfo);
  }
}
