import os, mimetypes

from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import get_object_or_404

from photologue.models import PhotoSizeCache

from models import Image
from forms import ImageFilterForm

@login_required
@require_http_methods(["GET"])
def list(request, page=1):

    form = ImageFilterForm()

    return object_list(request,
                       queryset=Image.objects.filter(is_public=True),
                       template_name = 'image_list.html',
                       template_object_name='image',
                       page=page,
                       paginate_by=10,
                       extra_context={'form':form})

@login_required
@require_http_methods(["GET"])
def filter(request, page=1):
    form = ImageFilterForm(request.GET)
    if form.is_valid():
        lookup_args = dict((key, value) for (key, value) in form.cleaned_data.items() if value)
        qs = Image.objects.filter(is_public=True, **lookup_args)

        return object_list(request,
                           queryset=qs,
                           template_name = 'image_list.html',
                           template_object_name='image',
                           page=page,
                           paginate_by=10,
                           extra_context={'form':form})
    else:
        return HttpResonseBadRequest(form.errors)

@login_required
@require_http_methods(["GET"])
def detail(request, image_id):
    return object_detail(request,
                         queryset=Image.objects.filter(is_public=True),
                         template_name = 'image_detail.html',
                         template_object_name = 'image',
                         object_id = image_id)

@login_required
def send_file(request, image_id, size):
    """                                                                         
    Send a file through Django without loading the whole file into              
    memory at once. The FileWrapper will turn the file object into an           
    iterator for chunks of 8KB.                                                 
    """

    image = get_object_or_404(Image, pk=image_id)

    filenames = \
        {'admin_thumbnail':(image.get_admin_thumbnail_filename, False),
         'thumbnail':(image.get_thumbnail_filename, False),
         'display':(image.get_display_filename, False),
         'small':(image.get_small_filename, True),
         'medium':(image.get_medium_filename, True),
         'large':(image.get_large_filename, True),
         'original':(lambda: image.image.path, True)}

    photosize = PhotoSizeCache().sizes.get(size)
    if photosize and not image.size_exists(photosize):
        image.create_size(photosize)

    filename = filenames[size][0]()
    mimetype, encoding = mimetypes.guess_type(filename)

    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type=mimetype or 'image/jpeg')
    response['Content-Length'] = os.path.getsize(filename)
    if filenames[size][1]:
        response['Content-Disposition'] = 'attachment; filename=%s' % image._get_filename_for_size(size)
    return response

