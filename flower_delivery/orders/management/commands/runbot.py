from django.core.management.base import BaseCommand
import django

class Command(BaseCommand):
    help = "Run the Telegram bot."

    def handle(self, *args, **options):
        django.setup()
        try:
            from bot import start_bot  # Убедись, что файл bot.py корректен
            self.stdout.write(self.style.SUCCESS("Запускаю телеграм-бот..."))
            start_bot()
        except ImportError as e:
            self.stderr.write(f"Ошибка импорта: {e}")
        except Exception as e:
            self.stderr.write(f"Произошла ошибка: {e}")

