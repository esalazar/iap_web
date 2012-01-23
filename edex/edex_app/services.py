import feedparser
import opml

allowed_universities = ["Massachusetts Institute of Technology"]

def import_video_lectures():
    ocw_link = "http://www.ocwconsortium.org/feeds/ocwcmemberfeeds.opml"

    outline = opml_reader(ocw_link)
    for line in outline:
        university_name = line.text
        university_link = line.url
        if university_link == "Massachusetts Institute of Technology":
            MIT_parser(university_link)

def opml_reader(link):
    return opml.parse(link)

def rss_parser(link):
    return feedparser.parse(link)

def MIT_parser(link)
    rss_data = rss_parser(link)
    for entry in rss_data:
        pass
