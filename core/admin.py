from django.contrib import admin
from .models import Terminal, Printer, Document, Payment,TemplateDocumentGroup
admin.site.register(TemplateDocumentGroup)


# Админка для терминалов
@admin.register(Terminal)
class TerminalAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'supports_color', 'price_per_page_bw', 'price_per_page_color', 'main_wallet', 'commission_wallet')
    list_filter = ('supports_color',)
    search_fields = ('name', 'location')
    ordering = ('name',)

# Админка для принтеров
@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ('name', 'terminal', 'paper_count')
    list_filter = ('terminal',)
    search_fields = ('name', 'terminal__name')
    ordering = ('terminal',)

# Админка для документов
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'pages', 'terminal', 'is_color')
    list_filter = ('terminal', 'is_color')
    search_fields = ('title', 'terminal__name')
    ordering = ('uploaded_at',)

# Админка для платежей
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('terminal', 'document', 'amount', 'status', 'created_at')
    list_filter = ('status', 'terminal')
    search_fields = ('terminal__name', 'document__title')
    ordering = ('created_at',)

    # Для отображения статуса платежа в виде красивых кнопок
    def status_button(self, obj):
        if obj.status == 'pending':
            return "<button class='button-pending'>В ожидании</button>"
        elif obj.status == 'completed':
            return "<button class='button-completed'>Завершен</button>"
        else:
            return "<button class='button-failed'>Ошибка</button>"

    status_button.allow_tags = True  # Чтобы HTML работал
    status_button.short_description = "Статус"

from django.contrib import admin
from .models import TemplateDocument

@admin.register(TemplateDocument)
class TemplateDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "paper_count")
    list_editable = ("paper_count",)  # Разрешаем редактировать остаток прямо в списке
