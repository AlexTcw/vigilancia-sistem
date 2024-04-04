import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class CamServiceService {
  baseCamURL: string = 'http://127.0.0.1:8000/vigilancia/';

  constructor(private httpClient: HttpClient) {}

  getAllAvailableCams(): Observable<any> {
    return this.httpClient.get<any>(`${this.baseCamURL}camaras-disponibles/`);
  }

  getCamVideoByID(idcam: number): Observable<any> {
    return this.httpClient.get<any>(
      `${this.baseCamURL}transmitir-video/${idcam}/`
    );
  }

  videoFeed(): Observable<any> {
    return this.httpClient.get('video_feed/', {
      responseType: 'blob',
    });
  }
}
