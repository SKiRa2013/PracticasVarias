import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root' // Disponible en toda la app moderna
})
export class HopfieldService {
  private apiUrl = 'http://localhost:8000/neural';

  constructor(private http: HttpClient) {}

  getMachines(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/machines/`);
  }

  createMachine(payload: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/machines/`, payload);
  }

  deleteMachine(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/machines/${id}/`);
  }
  
  getExercises(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/exercises/`);
  }
  
  createExercise(payload: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/exercises/`, payload);
  }

  deleteExercise(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/exercises/${id}/`);
  }
}