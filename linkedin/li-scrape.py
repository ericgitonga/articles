from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("https://www.linkedin.com/in/brantleycoile/detail/recent-activity/shares/")
bs = BeautifulSoup(html.read(), "html.parser")
print(bs.span)