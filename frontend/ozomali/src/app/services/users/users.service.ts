import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class UsersService {
  private readonly baseUrl: string;

  constructor(private http: HttpClient) {
    this.baseUrl = 'https://ozomali-api.herokuapp.com/api/v1/usuarios';
  }

  public getUsers(): Observable<any> {
    return this.http.get(this.baseUrl);
  }

  public createUser(params: any): Observable<any> {
    return this.http.post(this.baseUrl, params);
  }

  public searchUsers(field: any, value: any): Observable<any> {
    return this.http.get(`${this.baseUrl}/${field}/${value}`);
  }

  public updateUser(id: any, params: any): Observable<any> {
    return this.http.patch(`${this.baseUrl}/${id}`, params);
  }
}
