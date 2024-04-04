import { HttpClient } from '@angular/common/http';
import { Component, ElementRef, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { CamServiceService } from 'src/app/services/cam-service.service';
import { webSocket } from 'rxjs/webSocket';

@Component({
  selector: 'app-selected-camera',
  templateUrl: './selected-camera.component.html',
  styleUrls: ['./selected-camera.component.scss'],
})
export class SelectedCameraComponent implements OnInit {
  videoUrl: any;

  constructor(
    private camService: CamServiceService,
    private elementRef: ElementRef,
    private sanitizer: DomSanitizer,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    this.camService.getAllAvailableCams().subscribe((data) => {
      console.log(data);
    });
    this.startVideoStream();
  }

  startVideoStream() {
    const subject = webSocket(
      'ws://http://127.0.0.1:8000/vigilancia//ws/transmitir_video/1/'
    ); // Reemplaza la URL con la correcta
    //const streamUrl = 'http://127.0.0.1:8000/vigilancia/transmitir-video/1/'; // Cambia esto según tu configuración de servidor
    subject.subscribe(
      (frameBytes: Uint8Array) => {
        // Manipula los fotogramas recibidos aquí
        const frameBlob = new Blob([frameBytes], { type: 'image/jpeg' });
        const imageUrl = URL.createObjectURL(frameBlob);
        // Actualiza la imagen en tu interfaz de usuario, por ejemplo:
        document.getElementById('video-frame').setAttribute('src', imageUrl);
      },
      (err) => console.error('Error en la conexión WebSocket:', err),
      () => console.log('La conexión WebSocket se cerró')
  }
}
