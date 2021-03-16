import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-login-screen',
  templateUrl: './login-screen.component.html',
  styleUrls: ['./login-screen.component.scss'],
})
export class LoginScreenComponent implements OnInit {
  public isAuthenticated: boolean = false;

  public loginForm: FormGroup;

  constructor(private formBuilder: FormBuilder) {
    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  ngOnInit(): void {}

  public login(): void {
    if (this.loginForm.invalid) {
      return
    }

    this.isAuthenticated = !this.isAuthenticated
  }

  public logoff(): void {
    this.isAuthenticated = !this.isAuthenticated
  }
}
