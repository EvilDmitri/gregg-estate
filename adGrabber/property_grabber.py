
from lxml import html
from google.appengine.api import urlfetch

# HTML Cleaner


from templates.ad_html_template import CraigList

import jinja2
import os

jinja_enviroment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__name__)))


def PropertyGrabber(mls, amount):

    # Address for search by mls number requests
    mls_search_address = 'http://www.propertyinsantacruz.com/idx/search.html?refine=true&view=grid&search_mls={0}&idx=mlslistings'
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
    try:

        link = tree.xpath('//a[@class="info-links"]')[0].attrib['href']
    except IndexError:
        return 'No such MLS#'

    try:
        website = urlfetch.fetch(link)
    except Exception:
        return 'Try again later'

    page = str(website.content)
    #Parse the HTML
    tree = html.fromstring(page)

    # We are on the page we are interesting

    try:
        property_type = tree.xpath('//dl[@class="data-ListingType"]')[0].text_content().split(':')[1].strip().rstrip()
        property_type = '+'.join(property_type.split(' '))
    except Exception:
        property_type = ''


    try:
        area = tree.xpath('//dl[@class="data-AddressArea"]')[0].text_content().split(':')[1].strip().rstrip()
        area = ''.join(area.split(' - ')[1:]) # Remove leading number
        area = '+'.join(area.split(' '))
    except IndexError:
        area = ''


    min_price = ''
    max_price = ''
    price_text = ''
    try:
        price_text = tree.xpath('//dl[@class="data-ListingPrice"]')[0].text_content().split(':')[1].strip().rstrip()
        min_price = int(price_text.replace(',', '').replace('$', ''))
        max_price = min_price + int(amount)
    except Exception:
        pass


    # Complete search url
    search_by_type_area = 'http://www.propertyinsantacruz.com/idx/?refine=true&search_type[]={0}&idx=mlslistings&search_area[]={1}&maximum_price={2}'
    search_link = search_by_type_area.format(property_type, area, max_price)


    try:
        images = tree.xpath('//div[@id="image_wrap"]')
        image_link = images[0][0].attrib['src']
    except Exception:
        image_link = ''

    try:
        desc_text = tree.xpath('//div[@class="description"]')[0].getchildren()[0].text_content().strip().rstrip()
    except Exception:
        desc_text = ''

    try:
        listing_office = tree.xpath('//dd')[-1].text_content()
    except Exception:
        listing_office = ''

    icon_equalhousing = 'www.propertyinsantacruz.com'
    home = 'http://www.propertyinsantacruz.com/'

    final_html = CraigList(image_link=image_link, price_text=price_text, desc_text=desc_text,
                        search_by_type_area=search_link, home=home, listing_office=listing_office,
                        link=link, icon_equalhousing=icon_equalhousing)


    return final_html
