
# Biblitecas Tensorflow
import tensorflow as tf
from tensorflow.keras.layers import Layer

# Bibliotecas de operações
import os
import numpy as np
from collections import Counter 

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

class L1Dist(Layer):
  # Inicia a classe
  def __init__(self, **kwargs):
    super().__init__()

  # Realiza o calculo da distância
  def call(self, inputs):
     input_embedding, validation_embedding = inputs
     return tf.math.abs(input_embedding - validation_embedding)

def preprocess (file_path):
  # Lê a imagem
  byte_img = tf.io.read_file(file_path)
  # Carrega a imagem como JPEG
  img = tf.io.decode_jpeg(byte_img)
  # Modifica o tamanho da imagem em 100x100x3(RGB) - Especificado pelo artigo RN Siamesa
  img = tf.image.resize(img, (100,100))
  # Escala as informações da imagem para estarem entre 0 e 1
  img = img / 255.0
  return img

# Importando o modelo
model = tf.keras.models.load_model('media/ai_model/siamese_model_1.h5',
                                   custom_objects={'L1Dist':L1Dist, 'BinaryCrossentropy':tf.losses.BinaryCrossentropy})

# Detecção de cachorro por pastas de imagem
def detectar_cachorro(detection_threshold, verification_threshold, ANCHOR_PATH, POSITIVES_PATH, model=model):
    results = []
    cachorros_encontrados = []  # Lista para armazenar os nomes dos cachorros verificados

    anchor_image_path = os.path.join('media', ANCHOR_PATH, 'esp32_image.jpeg')

    if not os.path.exists(anchor_image_path):
        raise FileNotFoundError(f"Imagem âncora não encontrada: {anchor_image_path}")

    input_img = preprocess(anchor_image_path)
    # input_img = anchor_image_path

    for cachorro_nome in os.listdir(os.path.join('media', POSITIVES_PATH)):
        cachorro_path = os.path.join('media', POSITIVES_PATH, cachorro_nome)

        if not os.path.isdir(cachorro_path):
            continue

        for image in os.listdir(cachorro_path):
            validation_image_path = os.path.join(cachorro_path, image)
            validation_image = preprocess(validation_image_path)

            result = model.predict(list(np.expand_dims([input_img, validation_image], axis=1)))
            results.append(result)

            if np.sum(np.array(result) > detection_threshold) > 0:
                cachorros_encontrados.append(cachorro_nome)

    detection = np.sum(np.array(results) > detection_threshold)
    verification = detection / len(results) if len(results) > 0 else 0
    verified = verification > verification_threshold

    if verification < 0.5:
       return results, verified, "Nenhum cachorro foi identificado"
    
    # Retorna mensagem caso nenhum cachorro seja detectado
    if not cachorros_encontrados:
        return results, verified, "Nenhum cachorro foi detectado"
    
    cachorro_mais_frequente = Counter(cachorros_encontrados).most_common(1)[0][0]

    return results, verified, cachorro_mais_frequente