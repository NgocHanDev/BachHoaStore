from .models import Category

def get_all_category(request):
    list_all_category = Category.objects.all()  
    return dict(links=list_all_category)