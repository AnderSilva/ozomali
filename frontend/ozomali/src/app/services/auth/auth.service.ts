import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly baseUrl: string;

  constructor(private http: HttpClient) {
    this.baseUrl = 'https://ozomali-api.herokuapp.com/api/v1/auth';
  }

  public login(params: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/login`, params);
  }

  // public createUser(params: any): Observable<any> {
  //   return this.http.post(`${this.baseUrl}/users`, params);
  // }
}
