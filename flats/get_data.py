# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import codecs

import BeautifulSoup
from mechanize import Browser
from mechanize import Link

HEMNET_URL = 'http://www.hemnet.se'

ELEMENT = """
<div class="item sold result normal">
<h2 class="hide-element section-label text--subtle">

      Hedvägen 7 -

    såld Friliggande villa -

      Bergby

  </h2>
<ul class="attributes dates">
<li class="sold-date black item-result-meta-attribute-is-bold">Såld 2015-09-09</li>
<li>
<i class="hn-icon hn-icon-villa"></i>
<span class="hide-element">Friliggande villa</span>
</li>
</ul>
<ul class="attributes prices">
<li class="price item-result-meta-attribute-is-bold">
<span class="item-link">
        Slutpris 575 000 kr
      </span>
</li>
<li class="price-per-m2">
      5 808 kr/m²
    </li>
<li class="fee">
</li>
<li class="asked-price">
        Begärt pris: 695 000 kr
      </li>
<li class="price-change">
<i class="fa fa-arrow-down icon-color-red icon-rotate-45-counter-clockwise"></i> -120 000 kr (-17%)
      </li>
</ul>
<ul class="attributes locations">
<li class="address item-result-meta-attribute-is-bold">
<span class="primary-text item-link">Hedvägen 7</span>
</li>
<li class="area">
<span class="secondary-text item-link">
        Bergby
      </span>
</li>
<li class="city">
      Bergby
    </li>
<li class="broker">
<a href="http://www.gavle.svenskfast.se" target="_blank">Svensk Fastighetsförmedling</a>
</li>
</ul>
<ul class="attributes size">
<li class="living-area item-result-meta-attribute-is-bold">
<span class="item-link">
        99 m²
        &nbsp;
        4 rum
      </span>
</li>
<li class="land-area">
      1 334 m² tomt
    </li>
<li class="supplemental-area">
      65 m² biarea
    </li>
</ul>
<a href="villa-4rum-bergby-gavle-kommun-hedvagen-7-366074" class="item-link-container" target="_blank">
    &nbsp;
  </a>
</div>
"""
def initialize_br():
    br = Browser()
    # Ignore robots.txt
    br.set_handle_robots( False )
    br.set_handle_robots(False)   # ignore robots
    br.set_handle_refresh(False)
    br.addheaders = [('User-agent', 'Firefox')]

    return br

def broker_function(element):
    link = element.find("a")
    if link:
        return link.text
    return element.text

def final_price_function(element):
    span = element.find("span")
    if span:
        return span.text.replace("Slutpris", "").replace("kr", "")
    return element.text

def address_function(element):
    span = element.find("span")
    if span:
        return span.text
    return element.text

def area_function(element):
    span = element.find("span")
    if span:
        return span.text
    return element.text

def living_area_function(element):
    span = element.find("span")
    if span:
        return u";".join([v.strip() for v in span.text.replace(u"m²", "m2").replace("\n", "").split("&nbsp;")])
    return element.text

D = {
    u"sold-date black item-result-meta-attribute-is-bold": lambda element: element.text.replace(u"Såld ", ""),
    u"asked-price": lambda element: element.text.replace(u"Begärt pris: ", "").replace("kr", ""),
    u"price item-result-meta-attribute-is-bold": lambda element: final_price_function(element),
    u"price-per-m2": lambda element: element.text.replace(u"kr/m²", ""),
    u"living-area item-result-meta-attribute-is-bold": lambda element: living_area_function(element),
    u"land-area": lambda element: element.text.replace(u" m²", "").replace("tomt", ""),
    u"supplemental-area": lambda element: element.text.replace(u" m²", "").replace("biarea", ""),
    u"area": lambda element: area_function(element),
    u"city": lambda element: element.text,
    u"address item-result-meta-attribute-is-bold": lambda element: address_function(element),
    u"broker": lambda element: broker_function(element)
}


def get_element_info(element):
    attributes = []
    for li in element.findAll("li"):
        if li.has_key("class") and li["class"] in D:
            name = li["class"].split()[0]
            f = D[li["class"]]
            attributes.append((name, f(li)))

    for span in element.findAll("span"):
        if span.has_key("class") and span["class"] == "hide-element":
            attributes.append(("flat_type", span.text))

    return attributes

def write_to_file(outf, attributes):
    for (k, v) in attributes:
        outf.write(k + " : " + v + "\n")
    outf.write("-------------\n")
    outf.flush()


def parse_page(page_content, outf, page_number):
    print "------------- #" + str(page_number)
    outf.write("------------- #" + str(page_number)+ "\n")
    soup = BeautifulSoup.BeautifulSoup(page_content)
    for el in soup.findAll("div", {"class" :"item sold result normal"}):
        attributes = get_element_info(el)
        write_to_file(outf, attributes)

def get_data(br, outfile, page_start=1, page_end=10):
    if page_start == 1:
        outf = codecs.open(outfile, "w", "utf-8")
    else:
        outf = codecs.open(outfile, "a", "utf-8")

    # Retrieve hemnets webpage
    br.open(HEMNET_URL)

    # press the search button
    br.select_form(nr=0)
    #br.form['search[location_search]'] = area
    br.submit()

    # go to slutpriser
    req = br.follow_link(text_regex="Slutpriser")
    url = req.geturl()

    if page_start == 1:
        # scrape everything
        page_content = req.read()
        parse_page(page_content, outf, page_start)
        page_start = 2

    # do the same for all the pages
    for page_number in range(page_start, page_end):
        url_to_follow = Link(url, "?page=" + str(page_number), "", "", "")
        req = br.click_link(url_to_follow)
        resp = br.open(req)
        page_content = resp.read()
        parse_page(page_content, outf, page_number)

    outf.close()


def main():
    outfile = "sold_flats.txt"

    br = initialize_br()
    get_data(br, outfile, 1, 10800)
    #get_element_info(BeautifulSoup.BeautifulSoup(ELEMENT))


if __name__ == '__main__':
    main()
