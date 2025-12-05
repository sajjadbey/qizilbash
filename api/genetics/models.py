from django.db import models

# models.py

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class Province(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='provinces')

    class Meta:
        unique_together = ('name', 'country')
        verbose_name = "Province"
        verbose_name_plural = "Provinces"

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')

    class Meta:
        unique_together = ('name', 'province')
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.name}, {self.province.name}"
    
class YDNATree(models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Y-DNA Haplogroup"
        verbose_name_plural = "Y-DNA Haplogroups"
        
    def get_root_haplogroup(self):
        """Return the top-level haplogroup (e.g., 'Q' for 'Q-L245')"""
        current = self
        while current.parent:
            current = current.parent
        return current.name

    def get_full_path(self):
        """Return full path like ['Q', 'Q-M242', 'Q-L245']"""
        path = []
        current = self
        while current:
            path.append(current.name)
            current = current.parent
        return list(reversed(path))


class MTDNATree(models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "mtDNA Haplogroup"
        verbose_name_plural = "mtDNA Haplogroups"
        
    
    def get_root_haplogroup(self):
        current = self
        while current.parent:
            current = current.parent
        return current.name

    def get_full_path(self):
        path = []
        current = self
        while current:
            path.append(current.name)
            current = current.parent
        return list(reversed(path))
        
        

class HistoricalPeriod(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_year = models.IntegerField(help_text="Use negative values for BCE (e.g., -500 = 500 BCE)")
    end_year = models.IntegerField(help_text="Use negative values for BCE")

    def __str__(self):
        def format_year(y):
            if y < 0:
                return f"{abs(y)} BCE"
            elif y == 0:
                return "1 CE"
            else:
                return f"{y} CE"

        end = "present" if self.end_year >= 2025 else format_year(self.end_year)
        return f"{self.name} ({format_year(self.start_year)} – {end})"

    class Meta:
        ordering = ['start_year']  # Chronological order
        verbose_name = "Historical Period"
        verbose_name_plural = "Historical Periods"

class GeneticSample(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.PROTECT)
    province = models.ForeignKey(Province, null=True, blank=True, on_delete=models.PROTECT)
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.PROTECT)
    y_dna = models.ForeignKey(YDNATree, null=True, blank=True, on_delete=models.SET_NULL)
    mt_dna = models.ForeignKey(MTDNATree, null=True, blank=True, on_delete=models.SET_NULL)
    historical_period = models.ForeignKey(
        HistoricalPeriod,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Approximate time period of the individual"
    )
    description = models.TextField(blank=True)
    count = models.PositiveIntegerField(default=1, help_text="Number of individuals represented by this sample")

    def __str__(self):
        return f"{self.name} (n={self.count})"

    class Meta:
        verbose_name = "Genetic Sample"
        verbose_name_plural = "Genetic Samples"