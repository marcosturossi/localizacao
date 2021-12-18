from django.contrib import admin
from .models import Documentation, Version, UpdateNotes


@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    pass

@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    pass

@admin.register(UpdateNotes)
class UpdateNotesAdmin(admin.ModelAdmin):
    pass