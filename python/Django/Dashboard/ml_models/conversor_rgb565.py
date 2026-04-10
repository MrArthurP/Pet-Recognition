
import numpy as np
from PIL import Image

def rgb565_to_rgb888(rgb565_data, width, height):
    """
    Converte uma imagem no formato RGB565 para RGB888 e retorna um objeto PIL Image.
    """
    # Converte os bytes brutos para um array numpy de 16 bits (Big Endian)
    rgb565_array = np.frombuffer(rgb565_data, dtype=np.uint16).byteswap()  # Ajusta endianness

    # Extrai os componentes de cor corretamente
    r = ((rgb565_array >> 11) & 0x1F) * 255 // 31  # 5 bits para 8 bits
    g = ((rgb565_array >> 5) & 0x3F) * 255 // 63   # 6 bits para 8 bits
    b = (rgb565_array & 0x1F) * 255 // 31          # 5 bits para 8 bits

    # Cria uma matriz RGB correta
    rgb888_array = np.dstack((r, g, b)).astype(np.uint8)

    # Garante que a imagem tem as dimensões corretas
    img = Image.fromarray(rgb888_array.reshape((height, width, 3)), 'RGB')

    return img
