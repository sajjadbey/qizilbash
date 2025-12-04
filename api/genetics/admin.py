# admin.py

from django.contrib import admin
from .models import HistoricalPeriod, Country, Province, City, YDNATree, MTDNATree, GeneticSample


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ProvinceInline(admin.TabularInline):
    model = Province
    extra = 0


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'country__name')
    autocomplete_fields = ('country',)


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
    province_country.short_description = 'Country'  # type: ignore


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
        return str(obj)  # Reuse __str__ logic
    display_range.short_description = "Period Range"  # type: ignore


# Update GeneticSampleAdmin
@admin.register(GeneticSample)
class GeneticSampleAdmin(admin.ModelAdmin):
    list_display = ('name', 'y_dna', 'mt_dna', 'historical_period')
    list_filter = (
        'city__province__country',
        'city__province',
        'y_dna',
        'mt_dna',
        'historical_period',
    )
    search_fields = (
        'name',
        'city__name',
        'y_dna__name',
        'mt_dna__name',
        'historical_period__name',
    )
    autocomplete_fields = ('city', 'y_dna', 'mt_dna', 'historical_period')
    fields = ('name','country', 'province', 'city', 'y_dna', 'mt_dna', 'historical_period', 'description')

    #def city_with_province(self, obj):
        #return f"{obj.city.province.name}"
    #city_with_province.short_description = 'Location' # type: ignore