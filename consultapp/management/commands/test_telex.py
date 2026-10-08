from django.core.management.base import BaseCommand
import asyncio
from techcare.consultapp.telex_integration import test_telex_connection

class Command(BaseCommand):
    help = 'Test Telex webhook connection'

    def handle(self, *args, **options):
        async def run_test():
            success, message = await test_telex_connection()
            if success:
                self.stdout.write(self.style.SUCCESS(message))
            else:
                self.stdout.write(self.style.ERROR(message))

        asyncio.run(run_test()) 