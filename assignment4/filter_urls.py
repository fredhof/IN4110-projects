from email.mime import base
import math
import re
from urllib.parse import urljoin
from requesting_urls import get_html

## -- Task 2 -- ##


def find_urls(
    html: str,
    base_url: str = "https://en.wikipedia.org",
    output: str = None,
) -> set:
    """Find all the url links in a html text using regex
    Arguments:
        html (str): html string to parse
    Returns:
        urls (set) : set with all the urls found in html text
    """
    # create and compile regular expression(s)
    
    a_pat = re.compile(r"<a[^>]+>", flags=re.IGNORECASE)
   
    # src finds the text between quotes of the `src` attribute
    href_pat = re.compile(r'href="([^"]+)"', flags=re.IGNORECASE)
    url_set = set()
    # first, find all the img tags
    for a_tag in a_pat.findall(html):
        # then, find the src attribute of the img, if any
        match = href_pat.search(a_tag)
        if match:
            if match[1].startswith('//'):
                url_set.add("https:" + match.group(1))
            
            elif "#" in match[1]:
                if not match[1].startswith('#'):
                    url_set.add(base_url + match[1].split("#")[0])
                
            elif match[1].startswith('/'):
                url_set.add(base_url + match.group(1))
            
            else: url_set.add(match.group(1))

    if output:
        with open(output, 'w', encoding='utf8') as file:
            [file.write(match + '\n') for match in url_set]
    
    
    
    return url_set




def find_articles(html: str, output:str = None) -> set:
    """Finds all the wiki articles inside a html text. Make call to find urls, and filter
    arguments:
        - text (str) : the html text to parse
    returns:
        - (set) : a set with urls to all the articles found
    """
    urls = find_urls(html)
    pattern = re.compile(r"wikipedia.org/wiki")
    articles = set()
    for url in urls:
        match = pattern.search(url)
        # the second removes links such as  "https://en.wikipedia.orghttps://en.wikipedia.org/wiki/Nobel_Prize_controversies"
        if match and url.count("wikipedia") < 2: articles.add(url)
    

    # Write to file if wanted
    if output:
        with open(output, 'w', encoding='utf8') as file:
            [file.write(match + '\n') for match in articles]

    return articles


## Regex example
def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string

    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attibute of an img tag in the given HTML.
    """
    # img_pat finds all the <img alt="..." src="..."> snippets
    # this finds <img and collects everything up to the closing '>'
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()
    # first, find all the img tags
    for img_tag in img_pat.findall(html):
        # then, find the src attribute of the img, if any
        match = src_pat.search(img_tag)
        if match:
            src_set.add(match.group(1))
    return src_set
