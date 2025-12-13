import json
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from genetics.models import Province


class Command(BaseCommand):
    help = 'Load GeoJSON data for provinces from a file'

    def add_arguments(self, parser):
        parser.add_argument(
            'geojson_file',
            type=str,
            help='Path to the GeoJSON file containing province boundaries'
        )
        parser.add_argument(
            '--code-field',
            type=str,
            default='code',
            help='Field name in GeoJSON properties that contains the province code (default: code)'
        )
        parser.add_argument(
            '--name-field',
            type=str,
            default='name',
            help='Field name in GeoJSON properties that contains the province name (default: name)'
        )

    def handle(self, *args, **options):
        geojson_file = options['geojson_file']
        code_field = options['code_field']
        name_field = options['name_field']

        try:
            with open(geojson_file, 'r', encoding='utf-8') as f:
                geojson_data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {geojson_file}'))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f'Invalid JSON file: {geojson_file}'))
            return

        # Handle both FeatureCollection and single Feature
        if geojson_data.get('type') == 'FeatureCollection':
            features = geojson_data.get('features', [])
        elif geojson_data.get('type') == 'Feature':
            features = [geojson_data]
        else:
            self.stdout.write(self.style.ERROR('GeoJSON must be a Feature or FeatureCollection'))
            return

        updated_count = 0
        not_found_count = 0
        error_count = 0

        for feature in features:
            properties = feature.get('properties', {})
            geometry = feature.get('geometry')

            # Get province code or name from properties
            province_code = properties.get(code_field)
            province_name = properties.get(name_field)

            if not province_code and not province_name:
                self.stdout.write(
                    self.style.WARNING(f'Skipping feature: no {code_field} or {name_field} in properties')
                )
                continue

            # Try to find the province by code first, then by name
            try:
                if province_code:
                    province = Province.objects.get(code=province_code)
                elif province_name:
                    province = Province.objects.get(name=province_name)
                else:
                    not_found_count += 1
                    continue

                # Convert geometry to GEOSGeometry
                if geometry:
                    try:
                        geom = GEOSGeometry(json.dumps(geometry))
                        
                        # Ensure it's a MultiPolygon
                        if geom.geom_type == 'Polygon':
                            from django.contrib.gis.geos import MultiPolygon
                            geom = MultiPolygon(geom)
                        
                        province.geom = geom
                        province.save()
                        
                        updated_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'Updated geometry for: {province.name} ({province.code})')
                        )
                    except Exception as e:
                        error_count += 1
                        self.stdout.write(
                            self.style.ERROR(f'Error processing geometry for {province.name}: {str(e)}')
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'No geometry found for: {province.name}')
                    )

            except Province.DoesNotExist:
                not_found_count += 1
                identifier = province_code or province_name
                self.stdout.write(
                    self.style.WARNING(f'Province not found in database: {identifier}')
                )
            except Province.MultipleObjectsReturned:
                error_count += 1
                identifier = province_code or province_name
                self.stdout.write(
                    self.style.ERROR(f'Multiple provinces found for: {identifier}')
                )

        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Summary ==='))
        self.stdout.write(self.style.SUCCESS(f'Provinces updated: {updated_count}'))
        self.stdout.write(self.style.WARNING(f'Provinces not found: {not_found_count}'))
        self.stdout.write(self.style.ERROR(f'Errors: {error_count}'))