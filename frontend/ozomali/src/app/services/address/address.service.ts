import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AddressService {
  private readonly baseUrl: string;

  constructor(private http: HttpClient) {
    this.baseUrl = 'https://viacep.com.br/ws';
  }

  public getAddress(cep: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/${cep}/json`, { headers: { skip: 'true' } });
  }
}
