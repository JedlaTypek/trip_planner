from django.contrib import admin
from .models import Place, EntryFee, Tag, PlaceImage


class EntryFeeInline(admin.TabularInline):
    model = EntryFee
    extra = 1
    verbose_name = "Typ vstupného"
    verbose_name_plural = "Ceník vstupného"


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    extra = 1
    verbose_name = "Obrázek místa"
    verbose_name_plural = "Galerie obrázků"


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "google_maps_url")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [EntryFeeInline, PlaceImageInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
