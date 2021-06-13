import { Injectable } from '@angular/core';
import { CanLoad, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { UserQuery } from '../stores/user';

@Injectable({
  providedIn: 'root',
})
export class AuthGuard implements CanLoad {
  private readonly isAuthenticated$: Observable<boolean>;

  constructor(private router: Router, private userQuery: UserQuery) {
    this.isAuthenticated$ = this.userQuery.isAuthenticated$;
  }

  canLoad(): boolean {
    let isAuthenticated = false;

    this.isAuthenticated$.subscribe(authenticated => (isAuthenticated = authenticated));

    if (!isAuthenticated) {
      this.router.navigate(['/login']);
    }

    return isAuthenticated;
  }
}
