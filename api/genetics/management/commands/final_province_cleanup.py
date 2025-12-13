from django.core.management.base import BaseCommand
from django.db import transaction
from genetics.models import Province


class Command(BaseCommand):
    help = 'Final cleanup: assign code IR18 to Kohgiluyeh and Boyer-Ahmad'

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            from genetics.models import Country
            iran_country = Country.objects.get(name="Iran")
        except:
            self.stdout.write(self.style.ERROR('Iran country not found'))
            return

        # Find the province without code
        try:
            province = Province.objects.get(
                country=iran_country,
                name="Kohgiluyeh and Boyer-Ahmad",
                code__isnull=True
            )
            province.code = "IR18"
            province.save()
            self.stdout.write(
                self.style.SUCCESS(f'Assigned code IR18 to "{province.name}"')
            )
        except Province.DoesNotExist:
            self.stdout.write(
                self.style.WARNING('Province "Kohgiluyeh and Boyer-Ahmad" not found or already has a code')
            )
        except Province.MultipleObjectsReturned:
            self.stdout.write(
                self.style.ERROR('Multiple provinces found with name "Kohgiluyeh and Boyer-Ahmad"')
            )

        # Verify final state
        self.stdout.write(self.style.SUCCESS('\n=== Final State ==='))
        provinces = Province.objects.filter(country=iran_country).order_by('code')
        
        missing_codes = []
        for province in provinces:
            if province.code:
                self.stdout.write(f'{province.code}: {province.name}')
            else:
                missing_codes.append(province.name)
        
        if missing_codes:
            self.stdout.write(self.style.ERROR(f'\nProvinces without codes: {", ".join(missing_codes)}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'\n✓ All {provinces.count()} provinces have codes!'))