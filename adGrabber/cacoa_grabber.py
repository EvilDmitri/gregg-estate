
from lxml import html
from google.appengine.api import urlfetch

# HTML Cleaner

from templates.ad_html_template import CraigList


import jinja2
import os

jinja_enviroment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__name__)))


from adGrabber.cacoa_areas import areas


def CacoaGrabber(mls, amount):
    #mls = '81300538'
    mls_search_address = 'http://www.cacoastalhome.com/idx/search.html?search_by=mls&search_mls={0}'
    url = mls_search_address.format(mls)


    # Go to search page
    try:
        website = urlfetch.fetch(url)
    except Exception:
        return 'Try again later'


    # Save page content to string
    page = str(website.content)

    #Parse the HTML
    tree = html.fromstring(page)

    # Get link to page
    elemID = 'vdi-' + mls
    try:
        link = tree.get_element_by_id(elemID).attrib['href']
    except KeyError:
        return 'No such MLS#'

    try:
        website = urlfetch.fetch(link)
        page = str(website.content)
    except Exception:
        return 'Try again later'

    #Parse the HTML
    tree = html.fromstring(page)

    try:
        property_type = tree.xpath('//span[@class="idx-data type"]')[0][1].text_content()
        property_type = '+'.join(property_type.split(' '))
        if property_type.startswith('Single'):
            property_type = '1'
        elif property_type.startswith('Condo'):
            property_type = '2'
        elif property_type.startswith('Mobile'):
            property_type = '4'
        elif property_type.startswith('Multi'):
            property_type = '3'
        elif property_type.startswith('Residential'):
            property_type = '5'
    except Exception:
        property_type = ''


    area = tree.xpath('//span[@class="idx-data area"]')[0][1].text_content()
    area = '+'.join(area.split(' '))
    try:
        area = areas[area]
    except KeyError:
        #area = GetArea(mls)
        area = ''


    min_price = ''
    max_price = ''
    price_text = ''
    try:
        price_text = tree.xpath('//span[@class="idx-data price"]')[0][1].text_content()

        min_price = int(price_text.replace(',', '').replace('$', ''))
        max_price = min_price + int(amount)
    except Exception:
        price_text = ''


    search_link = 'http://www.cacoastalhome.com/idx/search.html?search_by=area&search_area[]={0}&search_type={1}&maximum_price={2}&submit=Search+Now'
    # Complete search url
    #search_link = 'http://www.propertyinsantacruz.com/idx/?refine=true&sortorder=DESC-ListingPrice&search_type={0}&search_city={1}'

    search_link = search_link.format(area, property_type, max_price)

    try:
        image_link = tree.xpath('//span[@class="imgs"]')[0][0].attrib['src']
    except Exception:
        image_link = ''

    try:
        desc_text = tree.xpath('//span[@class="idx-data remarks"]')[0].text_content()
        desc_text = desc_text.split(':')[1].strip().rstrip()
    except Exception:
        desc_text = 'No description'


    try:
        listing_office = tree.xpath('//div[@class="clear"]')[0].getnext().text_content()
        listing_office = listing_office.split(':')[1]
    except Exception:
        listing_office = ''

    all_homes = '<h2>Search All homes in the region at <a href="{0}">http://www.cacoastalhome.com/</a></h2>\n'

    icon_equalhousing = 'www.cacoastalhome.com'
    home = 'http://www.cacoastalhome.com/'

    final_html = CraigList(image_link=image_link, price_text=price_text, desc_text=desc_text,
                               search_by_type_area=search_link, home=home,
                               listing_office=listing_office, link=link, icon_equalhousing=icon_equalhousing)


    return final_html