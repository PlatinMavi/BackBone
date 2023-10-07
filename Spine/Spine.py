import pychrome
import subprocess

def getPageSource(tab, url):
    tab.start()
    tab.Page.enable()
    page_loaded = False

    def load_event_fired(**kwargs):
        nonlocal page_loaded
        page_loaded = True
    tab.Page.loadEventFired = load_event_fired

    tab.Page.navigate(url=url, _timeout=10)

    while not page_loaded:
        tab.wait(0.1)  

    result = tab.Runtime.evaluate(expression="document.documentElement.outerHTML")

    return result

def Scrape(target_url = "https://www.ruyamanga.com/"):

    command = "C:/Users/PC/AppData/Local/Google/Chrome/Application/chrome.exe --remote-debugging-port=9222"
    subprocess.Popen(command, shell=True)

    browser = pychrome.Browser(url="http://127.0.0.1:9222")
    tab = browser.list_tab()[0]
    page_source = getPageSource(tab, target_url)

    browser.close_tab(tab)
    tab.stop()

    return page_source