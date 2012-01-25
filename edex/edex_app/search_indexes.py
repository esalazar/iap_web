from haystack.indexes import *
from haystack import site

from edex_app.models import *

class CourseIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    description = CharField(model_attr='description')
    title = CharField(model_attr='title')
    lecturer = CharField(model_attr='lecturer')
    keywords = MultiValueField()

    def prepare_keywords(self, obj):
        return [keyword for keyword in obj.keywords.all()]

class LectureIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    description = CharField(model_attr='description')
    title = CharField(model_attr='title')
    lecturer = CharField(model_attr='lecturer')

site.register(Course, CourseIndex)
site.register(Lecture, LectureIndex)
