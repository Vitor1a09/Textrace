from django.urls import path
from .views import (
    IndexView, LoteResiduoView, EntidadeView, MovimentacaoView,
    CertificadoView, InspecaoView, AgendamentoView, RelatorioView,
    CadastroView, LoginView, LogoutView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('lotes/', LoteResiduoView.as_view(), name='lotes'),
    path('entidades/', EntidadeView.as_view(), name='entidades'),
    path('movimentacoes/', MovimentacaoView.as_view(), name='movimentacoes'),
    path('certificados/', CertificadoView.as_view(), name='certificados'),
    path('inspecoes/', InspecaoView.as_view(), name='inspecoes'),
    path('agendamentos/', AgendamentoView.as_view(), name='agendamentos'),
    path('relatorios/', RelatorioView.as_view(), name='relatorios'),
]