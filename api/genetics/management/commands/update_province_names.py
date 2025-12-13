from django.core.management.base import BaseCommand
from genetics.models import Province


class Command(BaseCommand):
    help = 'Update province names to match the new naming convention'

    # Mapping of old names to new names
    NAME_UPDATES = {
        "East Azarbaijan": "East Azerbaijan",
        "West Azarbaijan": "West Azerbaijan",
        "Esfahan": "Isfahan",
        "Chahar Mahall and Bakhtiari": "Chaharmahal and Bakhtiari",
        "Kohgiluyeh and Buyer Ahmad": "Kohgiluyeh and Boyer-Ahmad",
        "Kordestan": "Kurdistan",
        "Razavi Khorasan": "Khorasan",
    }

    def handle(self, *args, **options):
        updated_count = 0
        not_found_count = 0

        for old_name, new_name in self.NAME_UPDATES.items():
            try:
                province = Province.objects.get(name=old_name)
                province.name = new_name
                province.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Updated: "{old_name}" → "{new_name}"')
                )
            except Province.DoesNotExist:
                not_found_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Province not found: "{old_name}"')
                )
            except Province.MultipleObjectsReturned:
                self.stdout.write(
                    self.style.ERROR(f'Multiple provinces found with name: "{old_name}"')
                )

        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Summary ==='))
        self.stdout.write(self.style.SUCCESS(f'Provinces updated: {updated_count}'))
        self.stdout.write(self.style.WARNING(f'Provinces not found: {not_found_count}'))