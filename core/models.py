from django.db import models
import os
from django.utils import timezone
from PyPDF2 import PdfReader
from pptx import Presentation
from django.core.exceptions import ValidationError

from django.db import models
from django.contrib.auth.models import User

class Terminal(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название терминала")
    location = models.CharField(max_length=255, blank=True, verbose_name="Расположение")
    supports_color = models.BooleanField(default=False, verbose_name="Поддержка цветной печати")
    price_per_page_bw = models.DecimalField(max_digits=5, decimal_places=2, default=5.00, verbose_name="Цена за страницу (Ч/Б)")
    price_per_page_color = models.DecimalField(max_digits=5, decimal_places=2, default=15.00, verbose_name="Цена за страницу (Цветная)")
    main_wallet = models.CharField(max_length=255, verbose_name="Основной кошелек")
    commission_wallet = models.CharField(max_length=255, blank=True, null=True, verbose_name="Кошелек для комиссии")
    ngrok_url = models.URLField(blank=True, null=True, verbose_name="Текущий URL `ngrok`")
    is_active = models.BooleanField(default=True, verbose_name="Сервер активен?")
    last_ping = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Printer(models.Model):
    img1 = models.ImageField(blank=True, null=False, upload_to='terminal_img',verbose_name='первое изображение' )
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE, related_name="printers", verbose_name="Терминал")
    name = models.CharField(max_length=255, verbose_name="Название устройства")
    location = models.TextField(blank=True,null=True, verbose_name="локация ...")
    latitude = models.FloatField(blank=True,null=True, verbose_name="Широта")   # Широта
    longitude = models.FloatField(blank=True,null=True, verbose_name="Долгота") 
    paper_count = models.PositiveIntegerField(default=100, verbose_name="Остаток бумаги (листов)")

    def __str__(self):
        return f"{self.name} (Бумага: {self.paper_count})"

# timeweb umai
class Document(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название документа")
    file = models.FileField(upload_to="documents/", verbose_name="Файл")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    pages = models.PositiveIntegerField(default=0, verbose_name="Количество страниц")
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE,default=1, verbose_name="Терминал")
    is_color = models.BooleanField(default=False, verbose_name="Цветная печать")
    is_duplex = models.BooleanField(default=False, null=True, blank=True, verbose_name="Цветная печать")
    price_document = models.DecimalField(max_digits=5, decimal_places=2, default=10.00, verbose_name="Цена")

    def save(self, *args, **kwargs):
        # extension = os.path.splitext(self.file.name)[1].lower()
        # try:
        #     if extension == ".pdf":
        #         self.pages = self.get_pdf_page_count(self.file)
        #     elif extension == ".pptx":
        #         self.pages = self.get_pptx_page_count(self.file)
        #     else:
        #         self.pages = 1  # По умолчанию считаем 1 страницу для изображений
        # except Exception:
            # raise ValidationError("Ошибка при обработке файла.")

        super().save(*args, **kwargs)

    def get_pdf_page_count(self, file):
        file.seek(0)
        pdf = PdfReader(file)
        return len(pdf.pages)

    def get_pptx_page_count(self, file):
        file.seek(0)
        ppt = Presentation(file)
        return len(ppt.slides)

from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=[('credit', 'Пополнение'), ('debit', 'Списание')])
    created_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "В ожидании"),
        ("completed", "Завершен"),
        ("failed", "Ошибка"),
    ]

    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE, verbose_name="Терминал")
    document = models.ForeignKey(Document, on_delete=models.CASCADE, verbose_name="Документ", blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма оплаты")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Статус платежа")
    transaction_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID транзакции")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")

    def process_payment(self):
        """Метод обработки платежа (в реальном коде тут будет API вызов платежного сервиса)"""
        if self.status == "pending":
            self.status = "completed"
            self.save()

            # Разделение платежа (если указан кошелек для комиссии)
            if self.terminal.commission_wallet:
                commission_amount = self.amount * 0.1  # 10% комиссии
                main_amount = self.amount - commission_amount
                print(f"Отправка {main_amount} в {self.terminal.main_wallet}")
                print(f"Отправка {commission_amount} в {self.terminal.commission_wallet}")

        return self.status

    def __str__(self):
        return f"Оплата {self.amount} для {self.terminal} ({self.get_status_display()})"




from django.db import models

class TemplateDocumentGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название группы")
    parent_group = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subgroups', verbose_name="Родительская группа"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.parent_group.name + ' -> ' if self.parent_group else ''}{self.name}"

class TemplateDocument(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название шаблона")
    file = models.FileField(upload_to="templates/", verbose_name="Файл шаблона")
    preview_image = models.ImageField(upload_to="template_previews/", verbose_name="Превью документа", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    paper_count = models.PositiveIntegerField(default=1, verbose_name="Количество страниц")
    group = models.ForeignKey(
        TemplateDocumentGroup, on_delete=models.CASCADE, null=True, blank=True, related_name="documents", verbose_name="Группа"
    )

    def __str__(self):
        return self.title

# class TemplateDocument(models.Model):
#     title = models.CharField(max_length=255, verbose_name="Название шаблона")
#     file = models.FileField(upload_to="templates/", verbose_name="Файл шаблона")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
#     paper_count = models.PositiveIntegerField(default=100, verbose_name="лист")

#     def __str__(self):
#         return self.title

class PrintJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    document = models.ForeignKey(TemplateDocument, on_delete=models.CASCADE, verbose_name="Документ")
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE, verbose_name="Терминал")
    status = models.CharField(max_length=50, choices=[("pending", "Ожидание"), ("paid", "Оплачен"), ("printed", "Распечатан")], default="pending", verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата запроса")

    def __str__(self):
        return f"{self.user.username} - {self.document.title} ({self.status})"
