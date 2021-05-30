import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { take } from 'rxjs/operators';
import { UserService } from 'src/app/stores/user/user.service';
import { UserQuery } from 'src/app/stores/user';
import { NotificationService } from 'src/app/services/notification/notification.service';
import jwt_decode from 'jwt-decode';

@Component({
  selector: 'app-login-screen',
  templateUrl: './login-screen.component.html',
  styleUrls: ['./login-screen.component.scss'],
})
export class LoginScreenComponent {
  public isAuthenticated$: Observable<boolean>;
  public isAuthLoading: boolean;
  public loginForm: FormGroup;

  constructor(
    private formBuilder: FormBuilder,
    private userQuery: UserQuery,
    private userService: UserService,
    private notifications: NotificationService,
  ) {
    this.isAuthLoading = false;
    this.isAuthenticated$ = this.userQuery.isAuthenticated$;

    this.loginForm = this.formBuilder.group({
      login: ['', Validators.required],
      senha: ['', Validators.required],
    });
  }

  public login(): void {
    if (this.loginForm.invalid || this.isAuthLoading) {
      return;
    }

    this.isAuthLoading = true;
    const formValues = this.loginForm.getRawValue();

    this.userService
      .login(formValues)
      .pipe(take(1))
      .subscribe(
        response => {
          this.isAuthLoading = false;
          const userInfo = jwt_decode(response.Authorization);
          this.userService.updateAuthentication(response.Authorization, userInfo);
          this.loginForm.reset();
          this.notifications.feedbackModal(response);
        },
        response => {
          this.isAuthLoading = false;
          this.notifications.feedbackModal(response);
        },
      );
  }

  public logoff(): void {
    this.userService.logout();
  }
}
