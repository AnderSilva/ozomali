import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private readonly baseUrl: string;

  constructor(private http: HttpClient) {
    this.baseUrl = 'https://ozomali.herokuapp.com/users';
  }

  public createUser(params: any): Observable<any> {
    return this.http.post(this.baseUrl, params);
  }

  public getUsers(): Observable<any> {
    return this.http.get(this.baseUrl);
  }
}
