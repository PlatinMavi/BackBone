import pychrome
import subprocess
import time
from more_itertools import chunked

def getPageSource(tab, url):
    tab.start()
    tab.Page.enable()
    page_loaded = False

    def load_event_fired(**kwargs):
        nonlocal page_loaded
        page_loaded = True
    tab.Page.loadEventFired = load_event_fired

    tab.Page.navigate(url=url, _timeout=20)

    while not page_loaded:
        tab.wait(0.1)

    result = tab.Runtime.evaluate(expression="document.documentElement.outerHTML")

    return result

def Scrape(urls=["https://www.ruyamanga.com/", "https://mangasehri.com/"], wait=0, tab_switch=0,path="C:/Users/PC/AppData/Local/Google/Chrome/Application/chrome.exe"):
    returnies = []
    index = 0

    # path = "C:/Users/PC/AppData/Local/Google/Chrome/Application/chrome.exe"
    command = "--remote-debugging-port=9222"
    subprocess.Popen([path,command])
    urlsParsed = list(chunked(urls, tab_switch))

    browser = pychrome.Browser(url="http://127.0.0.1:9222")

    if tab_switch == 0:
        tab = browser.new_tab()

        for url in urls:
            
            page_source = getPageSource(tab, url)
            returnies.append(page_source)

            index += 1
            print(index, "/", len(urls))
            time.sleep(wait)

        browser.close_tab(tab)
        tab.stop()

        for tb in browser.list_tab():
            browser.close_tab(tb)

    else:
        for urlss in urlsParsed:
            tab = browser.new_tab()
            for url in urlss:
        
                page_source = getPageSource(tab, url)
                returnies.append(page_source)

                index += 1
                print(index, "/", len(urls))
                time.sleep(wait)

            browser.close_tab(tab)
            tab.stop()

        for tb in browser.list_tab():
            browser.close_tab(tb)

    return returnies