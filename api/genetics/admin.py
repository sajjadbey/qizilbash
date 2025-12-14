# admin.py
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import HistoricalPeriod, Country, Province, City, YDNATree, MTDNATree, GeneticSample, Ethnicity, Tribe, Clan


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ProvinceInline(admin.TabularInline):
    model = Province
    extra = 0


@admin.register(Province)
class ProvinceAdmin(LeafletGeoAdmin):
    list_display = ('name', 'code', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'code', 'country__name')
    autocomplete_fields = ('country',)
    
    # This enables the Leaflet map widget
    settings_overrides = {
        'DEFAULT_CENTER': (32.0, 53.0),
        'DEFAULT_ZOOM': 5,
    }


class CityInline(admin.TabularInline):
    model = City
    extra = 0


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'province_country')
    list_filter = ('province__country', 'province')
    search_fields = ('name', 'province__name', 'province__country__name')
    autocomplete_fields = ('province',)

    def province_country(self, obj):
        return obj.province.country.name
    province_country.short_description = 'Country'


@admin.register(Ethnicity)
class EthnicityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('provinces',)


# --- NEW ADMIN CLASSES: TRIBE and CLAN ---

@admin.register(Tribe)
class TribeAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_ethnicities')
    list_filter = ('ethnicities',)
    search_fields = ('name', 'ethnicities__name')
    filter_horizontal = ('ethnicities',)
    fields = ('name', 'ethnicities', 'historical_note')
    
    def get_ethnicities(self, obj):
        return ", ".join([e.name for e in obj.ethnicities.all()])
    get_ethnicities.short_description = 'Ethnicities'


@admin.register(Clan)
class ClanAdmin(admin.ModelAdmin):
    list_display = ('name', 'tribe', 'common_ancestor_display')
    list_filter = ('tribe__ethnicities', 'tribe',)
    search_fields = ('name', 'tribe__name', 'common_ancestor')
    autocomplete_fields = ('tribe',)
    fields = ('name', 'tribe', 'common_ancestor')

    def common_ancestor_display(self, obj):
        return obj.common_ancestor if obj.common_ancestor else '-'
    common_ancestor_display.short_description = 'Common Ancestor'

# ------------------------------------------


@admin.register(YDNATree)
class YDNATreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)
    autocomplete_fields = ('parent',)


@admin.register(MTDNATree)
class MTDNATreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)
    autocomplete_fields = ('parent',)


@admin.register(HistoricalPeriod)
class HistoricalPeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_year', 'end_year', 'display_range')
    list_editable = ('start_year', 'end_year')
    search_fields = ('name',)

    def display_range(self, obj):
        return str(obj)
    display_range.short_description = "Period Range"


@admin.register(GeneticSample)
class GeneticSampleAdmin(admin.ModelAdmin):
    list_display = ('name', 'ethnicity', 'tribe', 'clan', 'y_dna', 'mt_dna', 'historical_period', 'count')
    
    list_editable = ('ethnicity', 'count', 'tribe')

    list_filter = (
        'city__province__country',
        'city__province',
        'ethnicity',
        'tribe', # Added
        'clan', # Added
        'y_dna',
        'mt_dna',
        'historical_period',
    )
    search_fields = (
        'name',
        'city__name',
        'ethnicity__name',
        'tribe__name', # Added
        'clan__name', # Added
        'y_dna__name',
        'mt_dna__name',
        'historical_period__name',
    )
    autocomplete_fields = ('city', 'ethnicity', 'tribe', 'clan', 'y_dna', 'mt_dna', 'historical_period') # Updated
    fields = (
        'name',
        'country',
        'province',
        'city',
        'ethnicity',
        'tribe', # Added
        'clan', # Added
        'y_dna',
        'mt_dna',
        'historical_period',
        'count',
        'description'
    )