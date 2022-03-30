from pages.models import FooterLink, Logo


def get_navbar_footer_data(request):
    logo = Logo.objects.first()
    links = FooterLink.objects.all()
    return {"logo": logo, "f_links": links}
