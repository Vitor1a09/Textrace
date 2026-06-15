# app/views.py
from django.shortcuts import render
from django.views import View
from .models import (
    LoteResiduo, Entidade, Movimentacao, Certificado, 
    InspecaoQualidade, AgendamentoColeta, RelatorioSustentabilidade
)

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

class LoteResiduoView(View):
    def get(self, request):
        lotes = LoteResiduo.objects.all().order_by('-data_criacao')
        return render(request, 'lote/lista.html', {'lotes': lotes})

class EntidadeView(View):
    def get(self, request):
        entidades = Entidade.objects.all()
        return render(request, 'entidade/lista.html', {'entidades': entidades})

class MovimentacaoView(View):
    def get(self, request):
        movimentacoes = Movimentacao.objects.all().order_by('-data_evento')
        return render(request, 'movimentacao/lista.html', {'movimentacoes': movimentacoes})

# NOVAS VIEWS
class CertificadoView(View):
    def get(self, request):
        certificados = Certificado.objects.all().order_by('-data_emissao')
        return render(request, 'certificado/lista.html', {'certificados': certificados})

class InspecaoView(View):
    def get(self, request):
        inspecoes = InspecaoQualidade.objects.all().order_by('-data_inspecao')
        return render(request, 'inspecao/lista.html', {'inspecoes': inspecoes})

class AgendamentoView(View):
    def get(self, request):
        agendamentos = AgendamentoColeta.objects.all().order_by('data_prevista')
        return render(request, 'agendamento/lista.html', {'agendamentos': agendamentos})

class RelatorioView(View):
    def get(self, request):
        relatorios = RelatorioSustentabilidade.objects.all().order_by('-periodo_fim')
        return render(request, 'relatorio/lista.html', {'relatorios': relatorios})