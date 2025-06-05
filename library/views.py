from django.shortcuts import render, get_object_or_404

from library.models import Place, Tag, EntryFee


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
