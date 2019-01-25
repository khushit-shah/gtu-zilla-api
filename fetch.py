from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
import requests
from pathlib import Path
import time
import json
allPapers = list()
crawled = list()


def page(url):
    global allPapers
    print(url, "Is what i got in page..")
    if(url.endswith(".zip") or url.endswith(".pdf")):
        print(url, "is valid..")
        t1 = ""
        if(url.startswith("http://old.gtu.ac.in/GTU_Papers/")):
            t1 = url.split("http://old.gtu.ac.in/GTU_Papers/")[1]
        else:
            t1 = url.split("http://files.gtu.ac.in/GTU_Papers/")[1]
        t2 = t1.split("/")
        t2 = t2[t2.__len__() - 1]
        t1 = t1.split(t2)[0]
        if(t2.endswith(".zip")):
            code = t2.split(".zip")[0]
        else:
            code = t2.split(".pdf")[0]
        curPaper = [code, url]
        allPapers.append(curPaper)
        print(curPaper)
    else:
        print("URL IS NOT AN ZIP OR PDF",url)
        rec(url)


def rec(baseURL):
    basePage = requests.get(baseURL).text
    aTags = bs(basePage, "html.parser").find_all("a")
    for a in aTags:
        hreflink = urljoin(baseURL,a.get("href"))
        print(hreflink)
        valid = ((
            hreflink.startswith("http://www.gtu.ac.in")) or (hreflink.startswith(
        "http://old.gtu.ac.in")) or (hreflink.startswith("http://files.gtu.ac.in")))
        if((hreflink == "http://www.gtu.ac.in") or (hreflink == "http://gtu.ac.in/Download1.aspx") or (hreflink == "http://www.gtu.ac.in/")):
            continue
        else:
            if valid:
                if(not crawled.__contains__(hreflink)):
                    print("GOING TO :" + hreflink)
                    crawled.append(hreflink)
                    page(hreflink)
                else:
                    print('Already Gone Here!!!!! ',hreflink ,allPapers.count)
                    print(crawled.index(hreflink),crawled[crawled.index(hreflink)]);
                    input()
            else:
                print("INVALID" ,hreflink ,valid)
base = "http://old.gtu.ac.in/Qpaper.html"
page(base)
papers_json = json.dumps(allPapers)
print(papers_json)
file = open("./papers.json", "w+")
file.write(papers_json)
file.close()