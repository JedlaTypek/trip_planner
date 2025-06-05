from library.models import Tag

def all_tags(request):
    return {'all_tags': Tag.objects.all()}
