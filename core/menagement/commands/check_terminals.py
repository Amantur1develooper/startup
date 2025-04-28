from django.core.management.base import BaseCommand
from core.utils import check_terminals  # Импортируем функцию проверки серверов

class Command(BaseCommand):
    help = "Проверяет доступность всех терминалов"

    def handle(self, *args, **kwargs):
        check_terminals()
        self.stdout.write("✅ Проверка серверов завершена!")
