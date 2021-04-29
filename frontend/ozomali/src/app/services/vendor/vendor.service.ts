import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class VendorService {
  private readonly baseUrl: string;

  constructor(private http: HttpClient) {
    this.baseUrl = 'https://ozomali-api.herokuapp.com/api/v1/fornecedores';
  }

  public createVendor(params: any): Observable<any> {
    return this.http.post(this.baseUrl, params);
  }

  public getVendorById(id: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/${id}`);
  }

  public getVendors(): Observable<any> {
    return this.http.get(this.baseUrl);
  }

  public updateVendor(id: any, params: any): Observable<any> {
    return this.http.patch(`${this.baseUrl}/${id}`, params);
  }
}
