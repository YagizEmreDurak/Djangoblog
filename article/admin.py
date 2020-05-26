from django.contrib import admin
from .models import article,Yorumlar

# Register your models here.
admin.site.register(Yorumlar)


@admin.register(article)
class articleadmin(admin.ModelAdmin):

    list_display = ["title","author","created_date"]
    list_display_links = ["author","created_date"]
    search_fields = ["title"]
    list_filter = ["created_date"]
    class Meta:
        model = article


