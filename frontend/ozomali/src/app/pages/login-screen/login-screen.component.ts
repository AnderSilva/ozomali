import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { take } from 'rxjs/operators';
import { FeedbackModalComponent } from 'src/app/components/feedback-modal/feedback-modal.component';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-login-screen',
  templateUrl: './login-screen.component.html',
  styleUrls: ['./login-screen.component.scss'],
})
export class LoginScreenComponent implements OnInit {
  public isAuthenticated: boolean = false;
  public isAuthLoading: boolean = false;

  public loginForm: FormGroup;

  constructor(private formBuilder: FormBuilder, private authService: AuthService, private dialog: MatDialog) {
    this.loginForm = this.formBuilder.group({
      login: ['', Validators.required],
      senha: ['', Validators.required],
    });
  }

  ngOnInit(): void {}

  public login(): void {
    if (this.loginForm.invalid) {
      return;
    }

    this.isAuthLoading = true;
    const formValues = this.loginForm.getRawValue();

    this.authService
      .login(formValues)
      .pipe(take(1))
      .subscribe(
        () => {
          this.isAuthLoading = false;
          this.isAuthenticated = !this.isAuthenticated;
          this.loginForm.reset();
          const feedbackModal = this.dialog.open(FeedbackModalComponent, {
            data: {
              text: 'Bem vindo!',
              continueText: 'Fechar',
            },
          });
        },
        () => {
          this.isAuthLoading = false;
          const feedbackModal = this.dialog.open(FeedbackModalComponent, {
            data: {
              text: 'Desculpe, ocorreu um erro!',
              warning: 'Tente novamente ou entre em contado com nosso suporte.',
              continueText: 'Fechar',
            },
          });
        },
      );
  }

  public createUser(): void {
    if (this.loginForm.invalid) {
      return;
    }

    this.isAuthLoading = true;
    let formValues = this.loginForm.getRawValue();

    formValues = { ...formValues, nome: 'Rubens de Andrade' };

    this.authService
      .createUser(formValues)
      .pipe(take(1))
      .subscribe(
        () => {
          this.isAuthLoading = false;
          this.isAuthenticated = !this.isAuthenticated;
          this.loginForm.reset();
          const feedbackModal = this.dialog.open(FeedbackModalComponent, {
            data: {
              text: 'Usuário criado com Sucesso!',
              continueText: 'Fechar',
            },
          });
        },
        () => {
          this.isAuthLoading = false;
          const feedbackModal = this.dialog.open(FeedbackModalComponent, {
            data: {
              text: 'Desculpe, ocorreu um erro!',
              warning: 'Tente novamente ou entre em contado com nosso suporte.',
              continueText: 'Fechar',
            },
          });
        },
      );
  }

  public logoff(): void {
    this.isAuthenticated = !this.isAuthenticated;
  }
}
