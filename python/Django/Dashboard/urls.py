from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('enviar_Mensagem/', views.enviar_mensagem, name='enviar_mensagem'),
    path('get_csrf_token/', views.get_csrf_token, name='get_csrf_token'),
    path('update_button/', views.update_button, name='update_button'),
    path('get_button_states/', views.get_button_states, name='get_button_states'),
    path('cadastrar_cachorro/', views.cadastrar_cachorro, name='cadastrar_cachorro'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path('editar_cachorro/<int:cachorro_id>/', views.editar_cachorro, name='editar_cachorro'),
    path('deletar_cachorro/<int:cachorro_id>/', views.deletar_cachorro, name='deletar_cachorro'),
    path('enviar_horarios/', views.enviar_horarios, name='enviar_horarios'),
    path('envia_imagem/', views.envia_imagem, name='envia_imagem'),
    path("mostrar_imagem/", views.mostrar_imagem, name="mostrar_imagem"),
    # path("detecta_pir/", views.detecta_pir, name="detecta_pir"),
    path('', views.index, name='index'),
]
