import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UserQuery } from '../stores/user';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(public userQuery: UserQuery) {}

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

    return next.handle(request);
  }
}
