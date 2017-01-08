from django.contrib import admin
from Main.models import Record,Tag,Category,Evaluate
# Register your models here.
# Create your models here.

class RecordAdmin(admin.ModelAdmin):
    list_display = ('title','source','publish_time','author','likenum')
class EvaluateAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_time', 'like', 'recorder', 'user')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Record,RecordAdmin)
admin.site.register(Evaluate,EvaluateAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Category,CategoryAdmin)