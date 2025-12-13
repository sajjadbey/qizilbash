from django.core.management.base import BaseCommand
from genetics.models import Country, Province


class Command(BaseCommand):
    help = 'Load Iran country and its provinces into the database'

    # Iran provinces mapping with codes
    IRAN_PROVINCES = {
        "IR01": "East Azerbaijan",
        "IR02": "West Azerbaijan",
        "IR03": "Ardabil",
        "IR04": "Isfahan",
        "IR05": "Ilam",
        "IR06": "Bushehr",
        "IR07": "Tehran",
        "IR08": "Chaharmahal and Bakhtiari",
        "IR09": "Alborz",
        "IR10": "Khuzestan",
        "IR11": "Zanjan",
        "IR12": "Semnan",
        "IR13": "Sistan and Baluchestan",
        "IR14": "Fars",
        "IR15": "Kerman",
        "IR16": "Kurdistan",
        "IR17": "Kermanshah",
        "IR18": "Kohgiluyeh and Boyer-Ahmad",
        "IR19": "Gilan",
        "IR20": "Lorestan",
        "IR21": "Mazandaran",
        "IR22": "Markazi",
        "IR23": "Hormozgan",
        "IR24": "Hamadan",
        "IR25": "Yazd",
        "IR26": "Qom",
        "IR27": "Golestan",
        "IR28": "Qazvin",
        "IR29": "South Khorasan",
        "IR30": "Khorasan",
        "IR31": "North Khorasan"
    }

    def handle(self, *args, **options):
        # Create or get Iran country
        iran, created = Country.objects.get_or_create(name="Iran")
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created country: {iran.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Country already exists: {iran.name}'))

        # Create provinces
        provinces_created = 0
        provinces_existing = 0

        for code, province_name in self.IRAN_PROVINCES.items():
            province, created = Province.objects.get_or_create(
                name=province_name,
                country=iran,
                defaults={
                    'code': code,
                    'geom': None  # GeoJSON will be added later
                }
            )
            
            # Update code if province already exists but doesn't have a code
            if not created and not province.code:
                province.code = code
                province.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Updated code for existing province: {province_name} ({code})')
                )
            
            if created:
                provinces_created += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created province: {province_name} ({code})')
                )
            else:
                provinces_existing += 1
                self.stdout.write(
                    self.style.WARNING(f'Province already exists: {province_name} ({code})')
                )

        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Summary ==='))
        self.stdout.write(self.style.SUCCESS(f'Total provinces created: {provinces_created}'))
        self.stdout.write(self.style.WARNING(f'Total provinces already existing: {provinces_existing}'))
        self.stdout.write(self.style.SUCCESS(f'Total provinces in Iran: {Province.objects.filter(country=iran).count()}'))