#ativar venv: cd .venv/scripts;activate.cd ../..
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Estado, Cidade, TipoEntidade, Entidade, 
    MaterialTipo, LoteResiduo, StatusMovimentacao, 
    Movimentacao, Certificado, 
    RelatorioSustentabilidade, Auditoria, 
    AgendamentoColeta, InspecaoQualidade
)

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'entidade', 'is_active')
    
    # Campos que serão usados para busca
    search_fields = ('username', 'email', 'entidade__nome')
    
    # Filtros laterais (simplificados)
    list_filter = ('is_active', 'entidade')
    
    # Organização dos campos no formulário de edição
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('username', 'email', 'password', 'entidade')
        }),
        ('Status', {
            'fields': ('is_active',),
            'classes': ('wide',)
        }),
    )
    
    # Campos exibidos no formulário de criação
    add_fieldsets = (
        ('Informações Pessoais', {
            'fields': ('username', 'email', 'password1', 'password2', 'entidade')
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
    )

    exclude = ('is_staff', 'is_superuser', 'groups', 'user_permissions', 
               'last_login', 'date_joined', 'first_name', 'last_name')
    
    ordering = ('username',)
    actions = ['marcar_como_ativo', 'marcar_como_inativo']
    
    def marcar_como_ativo(self, request, queryset):
        queryset.update(is_active=True)
    marcar_como_ativo.short_description = "Marcar usuários selecionados como ATIVO"
    
    def marcar_como_inativo(self, request, queryset):
        queryset.update(is_active=False)
    marcar_como_inativo.short_description = "Marcar usuários selecionados como INATIVO"


admin.site.register(Usuario, UsuarioAdmin)

class EntidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'email', 'telefone', 'cidade', 'tipo_entidade')
    search_fields = ('nome', 'cnpj', 'email')
    list_filter = ('tipo_entidade', 'cidade')
    ordering = ('nome',)


class LoteResiduoAdmin(admin.ModelAdmin):
    list_display = ('identificador_unico', 'peso_kg', 'data_criacao', 'entidade_origem', 'material_tipo')
    search_fields = ('identificador_unico', 'entidade_origem__nome')
    list_filter = ('material_tipo', 'data_criacao')
    ordering = ('-data_criacao',)

class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('data_evento', 'lote_residuo', 'entidade_destino', 'status_movimentacao')
    search_fields = ('lote_residuo__identificador_unico', 'entidade_destino__nome')
    list_filter = ('status_movimentacao', 'data_evento')
    ordering = ('-data_evento',)

class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('codigo_autenticidade', 'data_emissao', 'lote_residuo')
    search_fields = ('codigo_autenticidade', 'lote_residuo__identificador_unico')

class AgendamentoColetaAdmin(admin.ModelAdmin):
    list_display = ('data_prevista', 'lote_residuo', 'transportadora')
    search_fields = ('lote_residuo__identificador_unico', 'transportadora__nome')
    list_filter = ('data_prevista',)
    ordering = ('data_prevista',)


class InspecaoQualidadeAdmin(admin.ModelAdmin):
    list_display = ('data_inspecao', 'lote_residuo', 'aprovado')
    list_filter = ('aprovado', 'data_inspecao')
    search_fields = ('lote_residuo__identificador_unico', 'observacoes')
    ordering = ('-data_inspecao',)

admin.site.register(Estado)
admin.site.register(Cidade)
admin.site.register(TipoEntidade)
admin.site.register(Entidade, EntidadeAdmin)
admin.site.register(MaterialTipo)
admin.site.register(LoteResiduo, LoteResiduoAdmin)
admin.site.register(StatusMovimentacao)
admin.site.register(Movimentacao, MovimentacaoAdmin)
admin.site.register(Certificado, CertificadoAdmin)
admin.site.register(RelatorioSustentabilidade)
admin.site.register(Auditoria)
admin.site.register(AgendamentoColeta, AgendamentoColetaAdmin)
admin.site.register(InspecaoQualidade, InspecaoQualidadeAdmin)

admin.site.site_header = "TexTrace - Administração"
admin.site.site_title = "TexTrace Admin"
admin.site.index_title = "Painel de Controle TexTrace"