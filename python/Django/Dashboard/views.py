from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import paho.mqtt.publish as publish
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json
from Dashboard.models import Cachorro, EstadoBotao
from django.middleware.csrf import get_token
import threading
import time
import logging
import os
import shutil
import numpy as np
from django.templatetags.static import static

from .forms import CachorroForm, FotoForm
from .models import Cachorro, Foto, EstadoBotao
from .ml_models.inferencia import detectar_cachorro
from .ml_models.conversor_rgb565 import rgb565_to_rgb888

def sucesso(request):
    return render(request, 'sucesso.html')  # Renderiza um template de sucesso

logger = logging.getLogger(__name__)

def get_csrf_token(request):
    csrf_token = get_token(request)
    return HttpResponse(csrf_token)

def enviar_horarios(request):
    if request.method == 'POST':
        dados = json.loads(request.body)
        horario1 = dados.get('horario1')
        horario2 = dados.get('horario2')
        tempoMotor = dados.get('tempoMotor')

        # Adiciona um espaço antes dos horários
        horario1_formatado = f"{horario1}"
        horario2_formatado = f"{horario2}"
        tempoMotor_formatado = f"{tempoMotor}"

        print(f'{horario1_formatado}, {horario2_formatado}, {tempoMotor_formatado}')  # Debug

        # Lógica para enviar os horários via MQTT
        payload = f"Horarios: {horario1_formatado},{horario2_formatado},{tempoMotor_formatado}"
        publish.single(
            topic="Alimentador_TccRecebe",
            payload=payload,
            hostname="test.mosquitto.org",
            port=1883,
            client_id="Cliente"
        )
        
        # Inicia uma thread para ligar o motor
        threading.Thread(target=ligar_motor, args=(tempoMotor_formatado,)).start()

        return JsonResponse({'status': 'success', 'horario1': horario1_formatado, 'horario2': horario2_formatado, 'tempoMotor': tempoMotor_formatado})
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)

def ligar_motor(tempo):
    # Lógica para ligar o motor
    publish.single(
        topic="Alimentador_TccRecebe",
        payload="Start_Motor",
        hostname="test.mosquitto.org",
        port=1883,
        client_id="Cliente"
    )
    # Espera o tempo definido antes de desligar
    time.sleep(int(tempo))
    publish.single(
        topic="Alimentador_TccRecebe",
        payload="Stop_Motor",
        hostname="test.mosquitto.org",
        port=1883,
        client_id="Cliente"
    )
    publish.single(
        topic="Alimentador_TccRecebe",
        payload="Tirar_Foto",
        hostname="test.mosquitto.org",
        port=1883,
        client_id="Cliente"
    )

@login_required
def editar_cachorro(request, cachorro_id):
    cachorro = get_object_or_404(Cachorro, id=cachorro_id)
    
    if request.method == 'POST':
        form = CachorroForm(request.POST, request.FILES, instance=cachorro)
        if form.is_valid():
            form.save()

            # Salvando múltiplas imagens
            for imagem in request.FILES.getlist('imagens'):
                Foto.objects.create(cachorro=cachorro, imagem=imagem)
                
            return redirect('sucesso')  # O redirecionamento após salvar

    else:
        form = CachorroForm(instance=cachorro)
    
    return render(request, 'editar_cachorros.html', {'form': form, 'cachorro': cachorro})

@login_required
def deletar_cachorro(request, cachorro_id):
    cachorro = get_object_or_404(Cachorro, id=cachorro_id)
    if request.method == 'POST':
        cachorro.delete()

        caminho_diretorio = os.path.join('media','fotos_cachorros', str(cachorro.nome))
        if os.path.exists(caminho_diretorio):
            shutil.rmtree(caminho_diretorio)  # Deleta o diretório e seu conteúdo

        return redirect('dashboard')
    return render(request, 'editar_cachorros.html', {'cachorro': cachorro})

@login_required
def dashboard(request):
    cachorros = Cachorro.objects.all()
    return render(request, 'dashboard.html', {'cachorros': cachorros})

@login_required
def cadastrar_cachorro(request):
    if request.method == 'POST':
        cachorro_form = CachorroForm(request.POST, request.FILES)
        if cachorro_form.is_valid():
            cachorro = cachorro_form.save()  # Salva o cachorro

            # Processa as fotos
            fotos = request.FILES.getlist('fotos')  # Pega as fotos enviadas
            for foto in fotos:
                Foto.objects.create(cachorro=cachorro, imagem=foto)  # Associa as fotos ao cachorro

            return redirect('sucesso')  # Redireciona para uma página de sucesso
    else:
        cachorro_form = CachorroForm()

    return render(request, 'cadastrar_cachorro.html', {'cachorro_form': cachorro_form})

@login_required
def enviar_mensagem(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f'Dados recebidos: {data}')  # Adicione este log
            mensagem = data.get('mensagem', '')

            if not mensagem:
                return JsonResponse({'status': 'error', 'message': 'Mensagem vazia'}, status=400)

            publish.single(
                topic="Alimentador_TccRecebe",
                payload=mensagem,
                hostname="test.mosquitto.org",
                port=1883,
                client_id="Cliente"
            )
            return JsonResponse({'status': 'success', 'message': 'Mensagem enviada'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Erro ao processar dados'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)

@csrf_exempt
def envia_imagem(request):
    if request.method == "POST" and request.body:
        # Diretório onde a imagem será salva
        image_dir = "media/fotos_camera"
        os.makedirs(image_dir, exist_ok=True)  # Cria a pasta se não existir

        # Caminho completo do arquivo (sempre sobrescreve)
        image_path = os.path.join(image_dir, "esp32_image.jpeg")

        try:
            if os.path.exists(image_path):
                os.remove(image_path)

            img = rgb565_to_rgb888(request.body, 96, 96)  # Converte RGB565 para RGB888
            img.save(image_path, "JPEG")  # Salva como JPEG

            image_url = "fotos_camera/esp32_image.jpeg"

            return JsonResponse({"message": "Imagem recebida com sucesso!", "image_url": image_url}, status=200)

        except Exception as e:
            return JsonResponse({"error": f"Erro ao salvar a imagem: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método não permitido ou sem arquivo!"}, status=400)

def mostrar_imagem(request):
    ID='None'
    ANCHOR_PATH = "fotos_camera"
    POSITIVES_PATH = "fotos_cachorros"
    
    # A função verify (ou seu processamento) pode ser chamado aqui
    results,veredict, cachorro = detectar_cachorro(0.5, 0.5, ANCHOR_PATH, POSITIVES_PATH)

    publish.single(
        topic="Alimentador_TccRecebe",
        payload=str(cachorro),
        hostname="test.mosquitto.org",
        port=1883,
        client_id="Cliente"
    )

    if veredict == True:
        publish.single(
            topic="Alimentador_TccRecebe",
            payload='Start_Motor_IA',
            hostname="test.mosquitto.org",
            port=1883,
            client_id="Cliente",
    )
    veredict = False

    if veredict == False:
         publish.single(
            topic="Alimentador_TccRecebe",
            payload='Stop_Motor',
            hostname="test.mosquitto.org",
            port=1883,
            client_id="Cliente",
    )
         
    return JsonResponse({"message": str(str(cachorro) + str(results))})
#return JsonResponse({'status': 'success', 'message': 'Mensagem enviada'})

# Configurando o logger
logger = logging.getLogger(__name__)

@csrf_exempt
def update_button(request):
    if request.method == 'POST':
        # Obtendo os dados do payload
        nivel = request.POST.get('nivel')
        estado = request.POST.get('estado')
        PIR = request.POST.get('pir')
        logger.info(f'Dados recebidos: nivel={nivel}, estado={estado}')


        # Imprimindo os dados recebidos para debug
        print("Dados recebidos:", request.POST)

        # Verificação dos dados
        if nivel is None or estado is None:
            return JsonResponse({'status': 'error', 'message': 'Dados ausentes'}, status=400)

        try:
            # Atualiza o modelo EstadoBotao
            estado_botao, created = EstadoBotao.objects.get_or_create(pk=1)  # Obtém ou cria a instância
            estado_botao.nivel = int(nivel)  # Armazena o nível como um inteiro
            estado_botao.estado1 = (estado == "NivelBaixo")  # Define estado1 com base no valor recebido
            estado_botao.save()

            return JsonResponse({'status': 'success', 'message': 'Dados processados com sucesso', 'nivel': estado_botao.nivel, 'estado': estado})
        except Exception as e:
            logger.error(f'Erro ao processar dados: {e}')
            return JsonResponse({'status': 'error', 'message': 'Erro ao processar dados'}, status=500)
    
    # Retorno para métodos diferentes de POST
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)

# @csrf_exempt
# def detecta_pir(request):
#     if request.method == 'POST':
#         # Obtendo os dados do payload
#         detect = request.POST.get('PIR')
#         logger.info(f'Dados recebidos: PIR={detect}')

#         # Imprimindo os dados recebidos para debug
#         print("Dados recebidos:", request.POST)

#         # Verificação dos dados
#         if detect is None:
#             return JsonResponse({'status': 'error', 'message': 'Dados ausentes'}, status=400)

#         return JsonResponse({'status': 'success', 'message': 'Dados processados com sucesso', 'nivel': detect})
    
#     # Retorno para métodos diferentes de POST
#     return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)

from django.http import JsonResponse
from .models import EstadoBotao

def get_button_states(request):
    estado_botao = EstadoBotao.objects.first()  # Obtém o primeiro registro do banco de dados

    if estado_botao:
        data = {
            'nivel': estado_botao.nivel,  # Retorna o nível armazenado
            'estado': 'NivelBaixo' if estado_botao.estado1 else 'NivelAlto',  # Retorna o estado
        }
    else:
        data = {
            'nivel': 0,  # Valor padrão se não houver registro
            'estado': 'desconhecido',
        }

    print(data)  # Imprime os dados para depuração
    return JsonResponse(data)  # Retorna a resposta JSON


@csrf_exempt
def index(request):
    estado_botao = EstadoBotao.objects.filter(id=1).first()
    return render(request, 'dashboard.html', {'estado': estado_botao})
