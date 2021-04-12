import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class VendorService {
  private readonly baseUrl: string;

  constructor(private http: HttpClient) {
    this.baseUrl = 'https://ozomali.herokuapp.com/providers';
  }

  public createVendor(params: any): Observable<any> {
    return this.http.post(this.baseUrl, params);
  }

  public updateVendor(params: any): Observable<any> {
    return this.http.put(this.baseUrl, params);
  }

  public getVendors(): Observable<any> {
    return this.http.get(this.baseUrl);
  }

  public getVendorById(id: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/${id}`);
  }

  public deleteVendorById(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/${id}`);
  }
}
