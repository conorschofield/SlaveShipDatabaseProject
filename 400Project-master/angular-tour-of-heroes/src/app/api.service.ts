import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Hero } from './hero';
import { Observable } from  'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  PHP_API_SERVER = "http://127.0.0.1:8080";
  constructor(private httpClient: HttpClient) { }

  readPolicies(): Observable<Hero[]>{
    return this.httpClient.get<Hero[]>(`${this.PHP_API_SERVER}/api/read.php`);
  }
}
