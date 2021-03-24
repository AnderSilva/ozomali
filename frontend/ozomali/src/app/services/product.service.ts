import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ProductService {
  private readonly baseUrl: string;

  constructor(private http: HttpClient) {
    this.baseUrl = 'https://ozomali.herokuapp.com/products';
  }

  public createProduct(params: any): Observable<any> {
    return this.http.post(this.baseUrl, params);
  }

  public updateProduct(params: any): Observable<any> {
    return this.http.put(this.baseUrl, params);
  }

  public getProducts(): Observable<any> {
    return this.http.get(this.baseUrl);
  }

  public getProductById(id: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/${id}`);
  }

  public deleteProductById(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/${id}`);
  }
}
