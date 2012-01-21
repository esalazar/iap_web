from django.contrib import admin
from edex_app.models import Keyword
from edex_app.models import Profile
from edex_app.models import Institution
from edex_app.models import Class
from edex_app.models import Lecture
from edex_app.models import Note
from edex_app.models import Question
from edex_app.models import Answer

admin.site.register(Keyword)
admin.site.register(Profile)
admin.site.register(Institution)
admin.site.register(Class)
admin.site.register(Lecture)
admin.site.register(Note)
admin.site.register(Question)
admin.site.register(Answer)
