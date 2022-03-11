from pages.models import Logo

def get_navbar_footer_data(request):
    logo = Logo.objects.first()
    return {'logo': logo, }
