import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ProductService {
  private readonly baseUrl: string;

  constructor(private http: HttpClient) {
    this.baseUrl = 'https://ozomali-api.herokuapp.com/api/v1/produtos';
  }

  public createProduct(params: any): Observable<any> {
    return this.http.post(this.baseUrl, params);
  }

  public getProductById(id: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/${id}`);
  }

  public getProducts(): Observable<any> {
    return this.http.get(this.baseUrl);
  }

  public updateProduct(id: any, params: any): Observable<any> {
    return this.http.patch(`${this.baseUrl}/${id}`, params);
  }
}
