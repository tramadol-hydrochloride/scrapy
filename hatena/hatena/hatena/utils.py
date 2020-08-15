import logging
import lxml.html
import readability

logging.getLogger('readability.readability').setLevel(logging.WARNING)


def get_content(html):
    """ Get the title and body from the HTML """

    document = readability.Document(html)
    content_html = document.summary()

    # Remove HTML tags
    content_text = lxml.html.fromstring(content_html).text_content().strip()
    short_title = document.short_title()

    return short_title, content_text
