import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TrainService {

  constructor(private http: HttpClient) {}

  getTrainRoute(from: string, to: string, criteria: string, departureTime: string): Observable<any> {
    const payload = { start_pos: from, destination: to, departure_time: departureTime };

    let apiUrl = '';

    if (criteria === 'cheapest') {
      apiUrl = 'http://127.0.0.1:5000/api/less_money'; 
    } else if (criteria === 'quickest') {
      apiUrl = 'http://127.0.0.1:5000/api/less_travel_time'; 
    } else {
      throw new Error('Invalid criteria');
    }

    return this.http.post<any>(apiUrl, payload);
  }
}