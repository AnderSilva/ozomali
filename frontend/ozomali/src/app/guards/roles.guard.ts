import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router } from '@angular/router';
import { Observable, of } from 'rxjs';
import { UserQuery } from '../stores/user';

@Injectable({
  providedIn: 'root',
})
export class RolesGuard implements CanActivate {
  private userAccess: string;

  constructor(private router: Router, private userQuery: UserQuery) {
    this.userQuery.userInfo$.subscribe(userInfo => (this.userAccess = userInfo.perfil));
  }

  canActivate(route: ActivatedRouteSnapshot): Observable<boolean> {
    if (!this.userAccess) {
      this.router.navigate(['']);
      return of(false);
    }

    const permittedRoles = route.data?.roles;
    let permitted: any = false;

    if (permittedRoles) {
      Object.entries(permittedRoles).forEach(([role, permission]) => {
        if (role === this.userAccess) {
          permitted = permission;
        }
      });
    }

    if (!permitted) {
      this.router.navigate(['/401']);
      return of(false);
    }
    return of(true);
  }
}
