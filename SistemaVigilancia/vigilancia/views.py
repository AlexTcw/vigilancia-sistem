import cv2
import asyncio
import websockets
import base64
import serial
import time
import json

from django.shortcuts import render
from django.http import JsonResponse
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def conectar_Wifi(request):
    # Configura el puerto serie
    serial_port = serial.Serial('/dev/ttyUSB0', 115200)  # Ajusta el nombre del puerto según tu sistema operativo
    time.sleep(2)  # Espera un momento para que el puerto serie se inicie

    try:
        # Decodificar los datos JSON del cuerpo de la solicitud
        data = json.loads(request.body)
        
        # Obtener el SSID y la contraseña del objeto JSON
        ssid = data.get('ssid')
        password = data.get('password')

        # Verificar si se proporcionaron tanto el SSID como la contraseña
        if ssid and password:
            # Envía el SSID por el puerto serie
            serial_port.write(ssid.encode())
            time.sleep(0.5)  # Espera un breve momento para asegurar que el mensaje se envíe completamente

            # Envía la contraseña por el puerto serie
            serial_port.write(password.encode())

            # Muestra lo que el puerto serie está enviando antes de cerrarlo
            print("Datos recibidos desde el puerto serie:")
            while serial_port.in_waiting > 0:
                print(serial_port.readline().decode().strip())  # Lee una línea de datos del puerto serie y la muestra

            # Cierra el puerto serie
            serial_port.close()
        else:
            print("No se proporcionó SSID y/o contraseña.")

    except json.JSONDecodeError:
        print("Error al decodificar los datos JSON.")
        
    return JsonResponse({'status': 'success'})  # O cualquier otra respuesta que desees enviar de vuelta al cliente
    

def camaras_disponibles(request):
    # Intentar obtener las cámaras disponibles
    try:
        camaras = []
        for i in range(10):  # Intenta hasta 10 cámaras
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                camaras.append(i)
                cap.release()
        return JsonResponse({'camaras': camaras})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Create your views here.
"""def generador_fotogramas(camara_id):
    cap = cv2.VideoCapture(camara_id)

    # Verificar si la cámara se abrió correctamente
    if not cap.isOpened():
        raise Exception("No se pudo abrir la cámara deseada")

    while True:
        ret, frame = cap.read()

        # Verificar si se capturó correctamente un fotograma
        if not ret:
            raise Exception("No se pudo capturar un fotograma de la cámara")

        # Convertir el fotograma en bytes
        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

        # Devolver el fotograma como un generador
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    # Liberar la cámara
    cap.release()

@gzip.gzip_page
def transmitir_video(request, camara_id):
    try:
        return StreamingHttpResponse(generador_fotogramas(camara_id), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def video_feed(request):
    cap = cv2.VideoCapture(1)
    def generate():
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')"""
    
async def generador_fotogramas(camara_id, websocket):
    cap = cv2.VideoCapture(camara_id)

    # Verificar si la cámara se abrió correctamente
    if not cap.isOpened():
        raise Exception("No se pudo abrir la cámara deseada")

    while True:
        ret, frame = cap.read()

        # Verificar si se capturó correctamente un fotograma
        if not ret:
            raise Exception("No se pudo capturar un fotograma de la cámara")

        # Convertir el fotograma en bytes
        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

        # Enviar el fotograma al cliente a través del websocket
        await websocket.send(frame_bytes)

    # Liberar la cámara
    cap.release()

async def transmitir_video(websocket, camara_id):
    try:
        await generador_fotogramas(camara_id, websocket)
    except Exception as e:
        await websocket.send(str(e))