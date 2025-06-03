from django.contrib import admin
from .models import Place, EntryFee, Tag


class EntryFeeInline(admin.TabularInline):  # nebo admin.StackedInline
    model = EntryFee
    extra = 1
    verbose_name = "Typ vstupného"
    verbose_name_plural = "Ceník vstupného"


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "google_maps_url")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [EntryFeeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
