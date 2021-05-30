import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class MovingsService {
  private readonly baseUrl: string;

  constructor(private http: HttpClient) {
    this.baseUrl = 'https://ozomali-api.herokuapp.com/api/v1/movimentacoes';
  }

  public registerMoving(params: any): Observable<any> {
    return this.http.post(this.baseUrl, params);
  }

  public listAllMovings(): Observable<any> {
    return this.http.get(this.baseUrl);
  }

  public getMovings(id: any): Observable<any> {
    return this.http.get(`${this.baseUrl}/${id}`);
  }

  public generateReport(params: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/report`, params);
  }
}
