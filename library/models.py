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
        help_text="Zadejte název zajímavého místa (např. St. Stephen's Green)"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        verbose_name="Slug",
        help_text="Jedná se o URL verzi názvu místa. Ponechte prázdné pro automatické vygenerování."
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
        help_text="Nahraj reprezentativní obrázek místa",
        null=True,
        blank=True
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
        blank=True,
        verbose_name="Štítky",
        help_text="Vyber odpovídající štítky pro místo (např. park, galerie)"
    )
    opening_hours = models.TextField(
        verbose_name="Otevírací doba",
        help_text="Uveď běžné otevírací hodiny místa",
        null=True,
        blank=True
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
        verbose_name='Místo',
        help_text='Místo, ke kterému tento obrázek patří'
    )
    image = models.ImageField(
        upload_to='places/gallery/',
        verbose_name='Obrázek',
        help_text='Přidej další obrázek místa'
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Popisek',
        help_text='Volitelný popisek k obrázku'
    )

    class Meta:
        verbose_name = 'Obrázek místa'
        verbose_name_plural = 'Galerie míst'

    def __str__(self):
        return f"{self.place.name} – Obrázek {self.id}"