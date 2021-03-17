import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ProductService {
  private readonly baseUrl: string;

  constructor(private http: HttpClient) {
    this.baseUrl = 'https://ozomali-api.herokuapp.com/products';
  }

  public createProduct(params: any): Observable<any> {
    return this.http.post(this.baseUrl, params);
  }

  public getProducts(): Observable<any> {
    return this.http.get(this.baseUrl);
  }

  public getProductById(id: string): Observable<any> {
    const params = new HttpParams({ fromString: 'id' });

    return this.http.get(`${this.baseUrl}/1`, { params });
  }

  public deleteProductById(id: string): Observable<any> {
    const params = new HttpParams({ fromString: 'id' });

    return this.http.delete(`${this.baseUrl}/1`, { params });
  }
}
