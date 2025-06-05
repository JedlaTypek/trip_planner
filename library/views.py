from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import DeleteView, UpdateView

from library.forms import PlaceForm, EntryFeeFormSet, UserRegisterForm, TripForm
from library.models import Place, Tag, EntryFee, PlaceImage, Trip


# Create your views here.

def place_list(request):
    context = {
        'page_title': 'Zajímavá místa',
        'places': Place.objects.all()
    }
    return render(request, 'place_list.html', context=context)


def place_list_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    places = Place.objects.filter(tags=tag)
    context = {
        'page_title': 'Štítek: ' + tag.name,
        'places': places
    }
    return render(request, 'place_list.html', context=context)


def place_detail(request, slug):
    place = get_object_or_404(Place, slug=slug)
    context = {
        'page_title': place.name,
        'hero_image': place.featured_image,
        'place': place,
        'entry_fees': EntryFee.objects.filter(place=place)
    }
    return render(request, 'place_detail.html', context=context)


def place_add(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES)
        formset = EntryFeeFormSet(request.POST, instance=None)  # instance bude nastaveno později
        files = request.FILES.getlist('gallery_images')  # více souborů pro galerii

        if form.is_valid() and formset.is_valid():
            place = form.save(commit=False)
            place.save()

            # Uložení M2M polí z formu (např. tags)
            form.save_m2m()

            # Zpracování nových štítků z pole new_tags
            new_tags = form.cleaned_data.get('new_tags')
            if new_tags:
                tag_names = [name.strip() for name in new_tags.split(',') if name.strip()]
                for name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=name)
                    place.tags.add(tag)

            # Přiřadit place k formsetu EntryFee a uložit
            formset.instance = place
            formset.save()

            # Vytvořit PlaceImage pro každý nahraný soubor
            for f in files:
                PlaceImage.objects.create(place=place, image=f)

            return redirect('place_detail', slug=place.slug)
    else:
        form = PlaceForm()
        formset = EntryFeeFormSet()

    return render(request, 'place_form.html', {
        'page_title': 'Vytvoření nového místa',
        'form': form,
        'formset': formset,
    })


def place_edit(request, slug): # TODO - nefunguje edit obrázků v galerii
    place = get_object_or_404(Place, slug=slug)

    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES, instance=place)
        formset = EntryFeeFormSet(request.POST, instance=place, prefix='entry_fees')
        files = request.FILES.getlist('gallery_images')

        if form.is_valid() and formset.is_valid():
            place = form.save()

            # Uložení nových štítků (pokud máš ve formu pole new_tags)
            new_tags = form.cleaned_data.get('new_tags')
            if new_tags:
                tag_names = [name.strip() for name in new_tags.split(',') if name.strip()]
                for name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=name)
                    place.tags.add(tag)

            formset.save()

            # Přidání nových obrázků k galerii
            for f in files:
                PlaceImage.objects.create(place=place, image=f)

            return redirect('place_detail', slug=place.slug)
        if not formset.is_valid():
            print(formset.errors)
    else:
        form = PlaceForm(instance=place)
        formset = EntryFeeFormSet(instance=place)

    return render(request, 'place_form.html', {
        'form': form,
        'formset': formset,
        'page_title': 'Úprava místa',  # můžeš si přidat, pokud chceš
    })

class PlaceDeleteView(DeleteView):
    model = Place
    context_object_name = 'place'
    template_name = 'place_delete.html'

    def get_success_url(self):
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        # Ověříme, že je next bezpečná URL (např. nepřesměrovává na cizí doménu)
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return next_url
        return reverse_lazy('places')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next') or reverse_lazy('places')
        return context


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrace proběhla úspěšně. Můžete se přihlásit.')
            return redirect('login')  # Django built-in login view
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def index(request):
    return render(request, 'index.html')

@login_required
def trip_list(request):
    trips = Trip.objects.filter(user=request.user).order_by('-date')
    return render(request, 'trip_list.html', {'trips': trips, 'page_title': 'Výlety'})


@login_required
def trip_detail(request, slug):
    trip = get_object_or_404(Trip, slug=slug, user=request.user)
    return render(request, 'trip_detail.html', {'trip': trip, 'page_title': trip.name})

@login_required
def trip_add(request):
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user  # přiřazení přihlášeného uživatele
            trip.save()
            form.save_m2m()  # pokud používáš ManyToMany pole (např. places)
            return redirect('trip_detail', slug=trip.slug)  # nebo slug, pokud ho máš
    else:
        form = TripForm()

    return render(request, 'trip_form.html', {'form': form, 'page_title': 'Vytváření nového výletu'})

@login_required
def trip_edit(request, slug):
    trip = get_object_or_404(Trip, slug=slug, user=request.user)

    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES, instance=trip)
        if form.is_valid():
            form.save()
            return redirect('trip_detail', slug=trip.slug)
    else:
        form = TripForm(instance=trip)

    return render(request, 'trip_form.html', {
        'form': form,
        'page_title': 'Úprava výletu'
    })

class TripDeleteView(LoginRequiredMixin, DeleteView):
    model = Trip
    template_name = 'trip_delete.html'
    success_url = reverse_lazy('trips')  # přesměrování po smazání

    def get_queryset(self):
        # zajistí, že uživatel může mazat jen své výlety
        return Trip.objects.filter(user=self.request.user)