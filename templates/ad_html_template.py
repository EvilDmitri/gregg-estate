def CraigList(image_link=None, price_text=None, desc_text=None, search_by_type_area=None, home=None, logo_name=None,
              listing_office=None, link=None, icon_equalhousing=None):
    header_div = '<div style="text-align:center;">\n'
    big_photo = '<img src="{0}"/>\n'
    price = '<p><b>{0}</b></p>\n'
    description = '<p>{0}</p>\n'

    all_photos = '<h2><a href="{0}">Click here to see all photos and all details</a></h2>\n'


    header_div_end = '</div>\n'

    footer_div = '<div style="font-size:10px; text-align: left"><p><strong>Gregg Camp</strong><br>CA DRE#00904586<br>\n'

    logo = '<img border="0" src="http://gregg-estate.appspot.com/images/logo/{0}"/><br><br></p>\n'

    all_homes = '<h2>Search All homes in the region at <a href="{0}">{1}</a></h2>\n'

    courtesy = '<p>Listing courtesy of {0}</p>\n'

    cellar = '<p><img src="{0}/images/site_functionality_photos/icon_equalhousing_59.png" alt="Equal Housing Logo"/></p>\n'
    footer_div_end = '</div>\n'



    html = ''.join([
        header_div,
        big_photo.format(image_link),
        price.format(price_text),
        description.format(desc_text),
        all_photos.format(link),
        all_homes.format(search_by_type_area, home),
        header_div_end,
        footer_div,
        logo.format(logo_name),
        courtesy.format(listing_office),
        cellar.format(home),
        footer_div_end,
        ])
    
    return html

def BackPage():
    pass
