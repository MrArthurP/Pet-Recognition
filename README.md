# 🐶🐱 Rede Neural para Reconhecimento de Pets
Este repositório contém o código de implementação de uma rede neural siamesa para o reconhecimento de pets (cães e gatos) usando o TensorFlow e o dataset cats_vs_dogs. O objetivo é criar um modelo capaz de identificar pets com base em suas imagens, diferenciando entre indivíduos específicos.

# 🚀 Principais Componentes:
## Pré-processamento de dados:

* As imagens são carregadas utilizando bibliotecas como PIL e OpenCV.

* Foi implementado um processo de data augmentation para aumentar a diversidade dos dados de treino.

* Organização dos dados em pastas para facilitar o treinamento (positive, negative, anchor).

## Construção da rede neural:

* Rede neural siamesa desenvolvida com TensorFlow e Keras, utilizando camadas convolucionais (Conv2D), de pooling (MaxPooling2D) e de ativação (Dense).

* Utilização de uma camada personalizada para calcular a distância entre embeddings.

## Treinamento e validação:

* O modelo é treinado utilizando o algoritmo de loss contrastiva para minimizar a distância entre imagens similares.

* Geração de gráficos de perda para monitoramento do desempenho.

# 📊 Resultados:
As métricas de desempenho (Recall, Precision, Accuracy e F1-Score) foram avaliadas para identificar pontos de melhoria no modelo.

#  🖼️ Dataset:
O dataset cats_vs_dogs foi utilizado como base para o treinamento e validação do modelo.

