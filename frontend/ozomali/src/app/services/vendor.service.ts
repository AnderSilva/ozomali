import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class VendorService {
  private readonly baseUrl: string;

  constructor(private http: HttpClient) {
    this.baseUrl = 'https://ozomali-api.herokuapp.com/providers';
  }

  public createVendor(params: any): Observable<any> {
    return this.http.post(this.baseUrl, params);
  }

  public getVendors(): Observable<any> {
    return this.http.get(this.baseUrl);
  }

  public getVendorById(id: string): Observable<any> {
    const params = new HttpParams({ fromString: 'id' });

    return this.http.get(`${this.baseUrl}/1`, { params });
  }

  public deleteVendorById(id: string): Observable<any> {
    const params = new HttpParams({ fromString: 'id' });

    return this.http.delete(`${this.baseUrl}/1`, { params });
  }
}
