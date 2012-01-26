from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from edex_app.models import Keyword
from edex_app.models import Institution
from edex_app.models import Course
from edex_app.models import Lecture

import feedparser
import opml
import re

allowed_universities = ['Massachusetts Institute of Technology']

def import_lectures():
    ocw_link = 'http://www.ocwconsortium.org/feeds/ocwcmemberfeeds.opml'

    outline = opml_reader(ocw_link)
    for line in outline:
        institution_name = line.text
        institution_link = line.url
        if institution_name == 'Massachusetts Institute of Technology':
            MIT_parser(institution_link)

def opml_reader(link):
    return opml.parse(link)

def rss_reader(link):
    return feedparser.parse(link)

def MIT_parser(link):
    institution_data = rss_reader(link)
    institution_name = 'MIT'
    institution_link = 'ocw.mit.edu'
    institution = None

    try:
        institution = Institution.objects.get(name=institution_name)
    except Institution.DoesNotExist:
        institution = Institution(name=institution_name, link=institution_link, rss=link)
    finally:
        institution.save()

    for entry in institution_data['entries']:
        course_link     = entry['link']
        video_urls = ['/video-lectures/rss.xml', '/lecture-notes-and-video/rss.xnl', '/video-discussions/rss.xml']
        accept_lecture = None
        for check_link in ['%s%s' % (course_link, video_url) for video_url in video_urls]:

            try:
                url_validator = URLValidator(verify_exists=True)
                url_validator(check_link)
                accept_lecture = check_link
                break
            except ValidationError:
                accept_lecture = None

        if accept_lecture != None:
            course_title    = entry['title']
            course = None

            try:
                course = Course.objects.get(title=course_title)
            except Course.DoesNotExist:
                keywords = []
                keyword = None
                if entry.has_key('dc_relation'):
                    if entry.has_key('tags'):
                        entry['tags'].append({'term': entry['dc_relation']})
                    else:
                        entry['tags'] = [{'term': entry['dc_relation']}]
                if entry.has_key('tags'):
                    for key in entry['tags']:
                        try:
                            keyword = Keyword.objects.get(keyword=key['term'])
                        except Keyword.DoesNotExist:
                            keyword = Keyword(keyword=key['term'])
                            keyword.save()
                        finally:
                            if keyword != None:
                                keywords.append(keyword)
                course_detail   = entry['summary']
                course_lecturer = entry['author']
                course = Course(title=course_title, description=course_detail, url=course_link, lecturer=course_lecturer, institution=institution)
                course.save()
                course.keywords.add(*keywords)
                course.save()

                lecture_data    = rss_reader(accept_lecture)
                lecture_entries = lecture_data['entries']
                for lecture_number in range(len(lecture_entries)):
                    match = re.search('(?<="http://www.youtube.com/v/)[\w\-_]+(?=")', lecture_entries[lecture_number]['summary'])
                    youtube_link = ''
                    if match != None:
                        youtube_link = match.group(0)
                    lecture = Lecture(number=(lecture_number + 1), title=lecture_entries[lecture_number]['title'].encode('utf-8'), description=lecture_entries[lecture_number]['summary'].encode('utf-8'), url=lecture_entries[lecture_number]['link'], video=youtube_link, lecturer=lecture_entries[lecture_number]['author'], course=course)
                    lecture.save()
