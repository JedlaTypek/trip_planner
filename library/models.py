from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Název štítku',
        help_text="Zadejte název štítku (např. park, muzeum, historické místo)"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=True,
        verbose_name="Slug",
        help_text="Jedná se o URL verzi názvu štítku. Ponechte prázdné pro automatické vygenerování."
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Štítek'
        verbose_name_plural = 'Štítky'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Place(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Název místa",
        help_text="Zadejte název zajímavého místa (např. St. Stephen's Green)",
        unique=True
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name="Slug",
        help_text="Jedná se o URL verzi názvu místa. Ponechte prázdné pro automatické vygenerování.",
        unique = True,
        blank = True,
    )
    description = models.TextField(
        verbose_name="Popis",
        help_text="Krátký popis místa a proč stojí za návštěvu",
        null=True,
        blank=True
    )
    featured_image = models.ImageField(
        upload_to='places/featured/',
        verbose_name="Hlavní obrázek",
        help_text="Nahraj reprezentativní obrázek místa"
    )
    google_maps_url = models.URLField(
        verbose_name="Odkaz na Google Mapy",
        help_text="Zadej URL odkaz na místo na Google mapách",
        max_length=500,
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name="Štítky",
        help_text="Vyber odpovídající štítky pro místo (např. park, galerie)",
        blank = True
    )
    opening_hours = models.TextField(
        verbose_name="Otevírací doba",
        help_text="Uveď běžné otevírací hodiny místa",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Místo'
        verbose_name_plural = 'Místa'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class EntryFee(models.Model):
    place = models.ForeignKey('Place', on_delete=models.CASCADE, related_name='entry_fees')
    category = models.CharField(
        max_length=50,
        verbose_name="Kategorie",
        help_text="Typ vstupného (např. dospělý, student, dítě)"
    )
    price = models.CharField(
        max_length=50,
        verbose_name="Cena",
        help_text="Cena vstupného (např. zdarma, 5 €, 2.50 €)"
    )

    class Meta:
        verbose_name = "Vstupné"
        verbose_name_plural = "Vstupné"

    def __str__(self):
        return f"{self.category} – {self.price}"


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='gallery',
    )
    image = models.ImageField(
        upload_to='places/gallery/',
    )

    class Meta:
        verbose_name = 'Obrázek místa'
        verbose_name_plural = 'Galerie míst'

    def __str__(self):
        return f"{self.place.name} – Obrázek {self.id}"


class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    name = models.CharField(max_length=200, verbose_name="Název výletu", unique=True)
    slug = models.SlugField(
        max_length=200,
        verbose_name="Slug",
        blank=True,
    )
    date = models.DateField(verbose_name="Datum výletu")
    places = models.ManyToManyField('Place', related_name='trips', verbose_name="Navštívená místa", blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Výlet'
        verbose_name_plural = 'Výlety'

    def __str__(self):
        return f"{self.name} ({self.date})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)