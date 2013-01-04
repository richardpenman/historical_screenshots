import os
import sys
from optparse import OptionParser
import re
import datetime
import webbrowser
from webscraping import common, download, webkit, xpath

DELAY = 5 # delay between downloads
IMAGE_DIR = 'images' # directory to store screenshots
D = download.Download(delay=DELAY, num_retries=1)



def historical_screenshots(website, days):
    """Download screenshots for website since archive.org started crawling

    website:
        the website to generate screenshots for
    days:
        the number of days difference between archived pages

    Returns a list of the downloaded screenshots
    """
    # the earliest archived time
    t0 = get_earliest_crawl(website)
    print 'Earliest version:', t0
    # the current time
    t1 = datetime.datetime.now()
    delta = datetime.timedelta(days=days)
    wb = webkit.WebkitBrowser(gui=True, enable_plugins=True, load_images=True)

    domain_folder = os.path.join(IMAGE_DIR, common.get_domain(website))
    if not os.path.exists(domain_folder):
        os.makedirs(domain_folder)

    screenshots = []
    while t0 <= t1:
        timestamp = t0.strftime('%Y%m%d')
        url = 'http://web-beta.archive.org/web/%s/%s/' % (timestamp, website)
        html = D.get(url)
        # remove wayback toolbar
        html = re.compile('<!-- BEGIN WAYBACK TOOLBAR INSERT -->.*?<!-- END WAYBACK TOOLBAR INSERT -->', re.DOTALL).sub('', html)
        html = re.compile('<!--\s+FILE ARCHIVED ON.*?-->', re.DOTALL).sub('', html)
        html = re.sub('http://web\.archive\.org/web/\d+/', '', html)
        # load webpage in webkit to render screenshot
        screenshot_filename = os.path.join(domain_folder, timestamp + '.jpg')
        wb.get(url, html)
        wb.screenshot(screenshot_filename)
        screenshots.append((url, t0, screenshot_filename))
        t0 += delta
    return screenshots


def get_earliest_crawl(website):
    """Return the datetime of the earliest crawl by archive.org for this website
    """
    url = 'http://web-beta.archive.org/web/*/' + website
    html = D.get(url)
    earliest_crawl_url = xpath.get(html, '//div[@id="wbMeta"]/p/a[2]/@href')
    try:
        earliest_crawl = earliest_crawl_url.split('/')[2]
    except IndexError:
        # unable to parse the date so assume just current data
        ts = datetime.datetime.now()        
    else:    
        ts = datetime.datetime.strptime(earliest_crawl, '%Y%m%d%H%M%S')
    return ts


def show_screenshots(website, screenshots):
    """Generate HTML page with links to screenshots
    """
    # reverse the order so newest screenshots are first
    screenshots = screenshots[::-1]
    index_filename = os.path.join(IMAGE_DIR, common.get_domain(website), 'index.html')
    open(index_filename, 'w').write(
"""<html>
    <head>
        <title>%(domain)s</title>
        <style>
            td { vertical-align: top; padding: 10px }
            img { width: 300px }
        </style>
    </head>
    <body>
        <h1>History of <a href="%(website)s">%(domain)s</a></h1>
        <table>
            <tr>
                %(header)s
            </tr>
            <tr>
                %(images)s
            </tr>
        </table>
    </body>
</html>""" % {
    'website': website,
    'domain': common.get_domain(website),
    'header': '\n'.join('<th><a href="%s">%s</a></th>' % (url, timestamp.strftime('%Y-%m-%d')) for url, timestamp, _ in screenshots),
    'images': '\n'.join('<td><a href="%(filename)s"><img src="%(filename)s" /></a></td>' % {'filename': os.path.basename(filename)} for url, timestamp, filename in screenshots)
    })
    print 'Opening', index_filename
    webbrowser.open(index_filename)
    

def main():
    parser = OptionParser(usage='%prog [options] <website>')
    parser.add_option('-s', '--show-browser', dest='show_browser', action='store_true', help='Show the generated screenshots in a web browser', default=False)
    parser.add_option('-d', '--days', dest='days', type='int', help='Days between archived webpages to generate screenshots (default 365)', default=365)
    options, args = parser.parse_args()
    if options.days <= 0:
        parser.error('The number of days must be greater than zero')

    if args:
        website = args[0]
        filenames = historical_screenshots(website, days=options.days)
        if options.show_browser:
            show_screenshots(website, filenames)
    else:
        parser.error('Need to specify the website')


if __name__ == '__main__':
    main()
