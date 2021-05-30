import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UserQuery, UserService } from '../stores/user';
import { tap } from 'rxjs/operators';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private userQuery: UserQuery, private userService: UserService) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const skipIntercept = request.headers.has('skip');

    if (skipIntercept) {
      request = request.clone({
        headers: request.headers.delete('skip'),
      });

      return next.handle(request);
    }

    request = request.clone({
      setHeaders: {
        Authorization: `Bearer ${this.userQuery.token}`,
      },
    });

    return next.handle(request).pipe(
      tap(
        () => {},
        (err: any) => {
          if (err instanceof HttpErrorResponse && err.status !== 401) {
            return;
          }
          this.userService.logout();
        },
      ),
    );
  }
}
