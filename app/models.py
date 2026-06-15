from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# AbstractUser estende o User padrão do Django.
# Isso preserva login, senha criptografada, sessões, etc.
# Se criar do zero , perde tudo isso.
class Usuario(AbstractUser):
    entidade = models.ForeignKey(
        'Entidade',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Entidade vinculada"
    )
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

class Estado(models.Model):
    nome = models.CharField(max_length=40, verbose_name="Nome")
    sigla = models.CharField(max_length=2, verbose_name="Sigla")
    def __str__(self):
        return self.sigla
    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"

class Cidade(models.Model):
    nome = models.CharField(max_length=40, verbose_name="Nome")
    estado = models.ForeignKey(
        Estado,
        on_delete=models.CASCADE,
        verbose_name="Estado"
    )
    def __str__(self):
        return f"{self.nome} - {self.estado.sigla}"
    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"

class TipoEntidade(models.Model):
    nome = models.CharField(max_length=40, verbose_name="Nome")
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = "Tipo de Entidade"
        verbose_name_plural = "Tipos de Entidade"

class Entidade(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    email = models.CharField(max_length=100, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    cidade = models.ForeignKey(
        Cidade,
        on_delete=models.CASCADE,
        verbose_name="Cidade"
    )
    tipo_entidade = models.ForeignKey(
        TipoEntidade,
        on_delete=models.CASCADE,
        verbose_name="Tipo de Entidade"
    )
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = "Entidade"
        verbose_name_plural = "Entidades"

class MaterialTipo(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Nome")
    composicao_quimica = models.TextField(verbose_name="Composição Química")
    cor_predominante = models.CharField(max_length=30, verbose_name="Cor Predominante")
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = "Tipo de Material"
        verbose_name_plural = "Tipos de Material"

# peso_kg usa DecimalField em vez de IntegerField.
# Peso de resíduos precisa de casas decimais (ex: 12.75 kg).
# DecimalField(max_digits=10, decimal_places=2) = até 99999999.99
class LoteResiduo(models.Model):
    identificador_unico = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Identificador Único"
    )
    peso_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Peso (kg)"
    )
    data_criacao = models.DateField(
        auto_now_add=False,   # ← MUDE para False
        blank=True,
        null=True,            # ← Adicione null=True
        verbose_name="Data de Criação"
    )
    entidade_origem = models.ForeignKey(
        Entidade,
        on_delete=models.PROTECT,
        verbose_name="Entidade de Origem"
    )
    material_tipo = models.ForeignKey(
        MaterialTipo,
        on_delete=models.PROTECT,
        verbose_name="Tipo de Material"
    )

# RF09
class StatusMovimentacao(models.Model):
    nome = models.CharField(max_length=30, verbose_name="Nome")
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = "Status de Movimentação"
        verbose_name_plural = "Status de Movimentação"


#on_delete=models.PROTECT no lote_residuo
# implementa a RN03 — impede deletar lote que já tem movimentação registrada.
class Movimentacao(models.Model):
    data_evento = models.DateTimeField(verbose_name="Data do Evento")
    lote_residuo = models.ForeignKey(
        LoteResiduo,
        on_delete=models.PROTECT,  # RN03: lote com movimentação não pode ser deletado
        verbose_name="Lote de Resíduo"
    )
    entidade_destino = models.ForeignKey(
        Entidade,
        on_delete=models.CASCADE,
        verbose_name="Entidade Destino"
    )
    status_movimentacao = models.ForeignKey(
        StatusMovimentacao,
        on_delete=models.CASCADE,
        verbose_name="Status"
    )
    def __str__(self):
        return f"{self.lote_residuo} → {self.entidade_destino} ({self.status_movimentacao})"
    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"


#OneToOneField em vez de ForeignKey.
# Um lote só pode ter UM certificado. ForeignKey permitiria múltiplos.
class Certificado(models.Model):
    codigo_autenticidade = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Código de Autenticidade"
    )
    data_emissao = models.DateField(verbose_name="Data de Emissão")
    lote_residuo = models.OneToOneField(
        LoteResiduo,
        on_delete=models.PROTECT,
        verbose_name="Lote de Resíduo"
    )
    def __str__(self):
        return self.codigo_autenticidade
    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"


class RelatorioSustentabilidade(models.Model):
    periodo_inicio = models.DateField(verbose_name="Período Início")
    periodo_fim = models.DateField(verbose_name="Período Fim")
    total_reciclado_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Total Reciclado (kg)"
    )
    entidade = models.ForeignKey(
        Entidade,
        on_delete=models.CASCADE,
        verbose_name="Entidade"
    )
    def __str__(self):
        return f"Relatório {self.entidade} ({self.periodo_inicio} a {self.periodo_fim})"
    class Meta:
        verbose_name = "Relatório de Sustentabilidade"
        verbose_name_plural = "Relatórios de Sustentabilidade"


# este model é preenchido automaticamente via signal,
# não pelo usuário. Não tem ForeignKey para Usuario por simplicidade —
# guarda só o username como texto (o usuário pode ter sido deletado depois).
class Auditoria(models.Model):
    usuario = models.CharField(max_length=80, verbose_name="Usuário")
    acao = models.CharField(max_length=200, verbose_name="Ação")
    data_hora = models.DateTimeField(auto_now_add=True, verbose_name="Data e Hora")
    tabela_afetada = models.CharField(max_length=100, verbose_name="Tabela Afetada")
    def __str__(self):
        return f"{self.usuario} - {self.acao} ({self.data_hora})"
    class Meta:
        verbose_name = "Auditoria"
        verbose_name_plural = "Auditorias"


class AgendamentoColeta(models.Model):
    data_prevista = models.DateTimeField(verbose_name="Data Prevista")
    lote_residuo = models.ForeignKey(
        LoteResiduo,
        on_delete=models.CASCADE,
        verbose_name="Lote de Resíduo"
    )
    transportadora = models.ForeignKey(
        Entidade,
        on_delete=models.CASCADE,
        verbose_name="Transportadora"
    )
    def __str__(self):
        return f"Coleta {self.lote_residuo} em {self.data_prevista}"
    class Meta:
        verbose_name = "Agendamento de Coleta"
        verbose_name_plural = "Agendamentos de Coleta"

class InspecaoQualidade(models.Model):
    data_inspecao = models.DateTimeField(verbose_name="Data da Inspeção")
    observacoes = models.TextField(verbose_name="Observações")
    aprovado = models.BooleanField(verbose_name="Aprovado")
    lote_residuo = models.ForeignKey(
        LoteResiduo,
        on_delete=models.PROTECT,
        verbose_name="Lote de Resíduo"
    )
    def __str__(self):
        return f"Inspeção {self.lote_residuo} - {'Aprovado' if self.aprovado else 'Reprovado'}"
    class Meta:
        verbose_name = "Inspeção de Qualidade"
        verbose_name_plural = "Inspeções de Qualidade"