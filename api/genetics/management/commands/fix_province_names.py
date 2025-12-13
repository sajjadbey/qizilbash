from django.core.management.base import BaseCommand
from django.db import transaction
from genetics.models import Province, GeneticSample


class Command(BaseCommand):
    help = 'Fix province names by migrating data from duplicates and updating old names'

    # Mapping of old names to new names with their codes
    NAME_UPDATES = {
        "IR01": ("East Azarbaijan", "East Azerbaijan"),
        "IR02": ("West Azarbaijan", "West Azerbaijan"),
        "IR04": ("Esfahan", "Isfahan"),
        "IR08": ("Chahar Mahall and Bakhtiari", "Chaharmahal and Bakhtiari"),
        "IR16": ("Kordestan", "Kurdistan"),
        "IR18": ("Kohgiluyeh and Buyer Ahmad", "Kohgiluyeh and Boyer-Ahmad"),
        "IR30": ("Razavi Khorasan", "Khorasan"),
    }

    @transaction.atomic
    def handle(self, *args, **options):
        iran_country = None
        try:
            from genetics.models import Country
            iran_country = Country.objects.get(name="Iran")
        except:
            self.stdout.write(self.style.ERROR('Iran country not found'))
            return

        # Step 1: Migrate GeneticSamples from duplicate provinces (without codes) to the correct ones (with codes)
        duplicates = Province.objects.filter(country=iran_country, code__isnull=True)
        migrated_samples = 0
        
        for duplicate in duplicates:
            # Find the correct province with code for this name
            try:
                # Check if this duplicate name matches any of our new names
                correct_province = None
                for code, (old_name, new_name) in self.NAME_UPDATES.items():
                    if duplicate.name == new_name:
                        # This is a new name, find the province with the code
                        correct_province = Province.objects.get(code=code, country=iran_country)
                        break
                
                if correct_province:
                    # Migrate all GeneticSamples from duplicate to correct province
                    samples = GeneticSample.objects.filter(province=duplicate)
                    sample_count = samples.count()
                    if sample_count > 0:
                        samples.update(province=correct_province)
                        migrated_samples += sample_count
                        self.stdout.write(
                            self.style.SUCCESS(f'Migrated {sample_count} samples from duplicate "{duplicate.name}" to "{correct_province.name}" ({correct_province.code})')
                        )
                    
                    # Now delete the duplicate
                    duplicate.delete()
                    self.stdout.write(
                        self.style.WARNING(f'Deleted duplicate province: "{duplicate.name}"')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'No matching province with code found for duplicate: "{duplicate.name}"')
                    )
                    
            except Province.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Could not find correct province for: "{duplicate.name}"')
                )

        # Step 2: Update the old names to new names
        updated_count = 0
        for code, (old_name, new_name) in self.NAME_UPDATES.items():
            try:
                province = Province.objects.get(code=code, country=iran_country)
                if province.name == old_name:
                    province.name = new_name
                    province.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'{code}: "{old_name}" → "{new_name}"')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'{code}: Already updated (current name: "{province.name}")')
                    )
            except Province.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Province not found with code: {code}')
                )

        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Summary ==='))
        self.stdout.write(self.style.SUCCESS(f'Genetic samples migrated: {migrated_samples}'))
        self.stdout.write(self.style.SUCCESS(f'Provinces updated: {updated_count}'))
        
        # Show final count
        final_count = Province.objects.filter(country=iran_country).count()
        self.stdout.write(self.style.SUCCESS(f'Total Iran provinces: {final_count}'))