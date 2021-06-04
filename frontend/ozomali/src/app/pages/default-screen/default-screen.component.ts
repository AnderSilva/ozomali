import { Component } from '@angular/core';
import { UserService } from 'src/app/stores/user';
@Component({
  selector: 'app-default-screen',
  templateUrl: './default-screen.component.html',
  styleUrls: ['./default-screen.component.scss'],
})
export class DefaultScreenComponent {
  constructor(private userService: UserService) {}

  invalidateToken() {
    this.userService.updateAuthentication('tokenInvalido', {
      exp: 1622931211,
      iat: 1622844806,
      uid: 20,
      name: 'Rubens de Andrade',
      login: 'bibull',
      perfil: 'admin',
    });
  }
}
