import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { tap } from 'rxjs/operators';
import { UserStore } from './user.store';

@Injectable({ providedIn: 'root' })
export class UserService {
  constructor(private userStore: UserStore, private http: HttpClient) {}

  updateAuthentication(isAuthenticated: boolean, token: string, user: any): void {
    this.userStore.update({ isAuthenticated, token, user });
  }

  logout(): void {
    this.userStore.reset();
  }
}
