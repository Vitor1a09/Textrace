from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import (
    LoteResiduo, Entidade, Movimentacao, Certificado, 
    InspecaoQualidade, AgendamentoColeta, RelatorioSustentabilidade
)
from .forms import CadastroForm, LoginForm

class IndexView(View):
    def get(self, request):
        context = {
            'total_lotes': LoteResiduo.objects.count(),
            'total_entidades': Entidade.objects.count(),
            'total_movimentacoes': Movimentacao.objects.count(),
            'total_certificados': Certificado.objects.count(),
            'ultimos_lotes': LoteResiduo.objects.all().order_by('-data_criacao')[:5],
            'ultimas_movimentacoes': Movimentacao.objects.all().order_by('-data_evento')[:5],
            'certificados_recentes': Certificado.objects.all().order_by('-data_emissao')[:5],
        }
        return render(request, 'index.html', context)

class CadastroView(View):
    def get(self, request):
        form = CadastroForm()
        return render(request, 'cadastro.html', {'form': form})
    
    def post(self, request):
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('index')
        return render(request, 'cadastro.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.username}!')
                return redirect('index')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'Você saiu do sistema.')
        return redirect('index')

# Protege as views que exigem login
@method_decorator(login_required, name='dispatch')
class LoteResiduoView(View):
    def get(self, request):
        lotes = LoteResiduo.objects.all().order_by('-data_criacao')
        return render(request, 'lote/lista.html', {'lotes': lotes})

@method_decorator(login_required, name='dispatch')
class EntidadeView(View):
    def get(self, request):
        entidades = Entidade.objects.all()
        return render(request, 'entidade/lista.html', {'entidades': entidades})

@method_decorator(login_required, name='dispatch')
class MovimentacaoView(View):
    def get(self, request):
        movimentacoes = Movimentacao.objects.all().order_by('-data_evento')
        return render(request, 'movimentacao/lista.html', {'movimentacoes': movimentacoes})

@method_decorator(login_required, name='dispatch')
class CertificadoView(View):
    def get(self, request):
        certificados = Certificado.objects.all().order_by('-data_emissao')
        return render(request, 'certificado/lista.html', {'certificados': certificados})

@method_decorator(login_required, name='dispatch')
class InspecaoView(View):
    def get(self, request):
        inspecoes = InspecaoQualidade.objects.all().order_by('-data_inspecao')
        return render(request, 'inspecao/lista.html', {'inspecoes': inspecoes})

@method_decorator(login_required, name='dispatch')
class AgendamentoView(View):
    def get(self, request):
        agendamentos = AgendamentoColeta.objects.all().order_by('data_prevista')
        return render(request, 'agendamento/lista.html', {'agendamentos': agendamentos})

@method_decorator(login_required, name='dispatch')
class RelatorioView(View):
    def get(self, request):
        relatorios = RelatorioSustentabilidade.objects.all().order_by('-periodo_fim')
        return render(request, 'relatorio/lista.html', {'relatorios': relatorios})