import requests
import threading
import time

def sliceList(listw, partnum):
    part_size = len(listw) // partnum
    extra = len(listw) % partnum
    lists = []

    start = 0
    for i in range(partnum):
        end = start + part_size + (1 if i < extra else 0)
        lists.append(listw[start:end])
        start = end

    return lists

def ScrapeModule(urls=["https://www.ruyamanga.com/", "https://mangasehri.com/"],wait=0):
    returnies = []
    
    for url in urls:
        html = requests.get(url).content.decode("utf-8", errors="ignore") 
        returnies.append(html)
        time.sleep(wait)

    return returnies

def Scrape(urls=["https://www.ruyamanga.com/", "https://mangasehri.com/"],thread_count=0,wait=0):
    if len(urls) <= 3:
        scraped = ScrapeModule(urls,wait)
        return scraped

    sliced = sliceList(urls, thread_count)
    threads = []
    returnies = []

    def worker(url_chunk):
        result = ScrapeModule(url_chunk,wait)
        returnies.extend(result)

    for url_chunk in sliced:
        thread = threading.Thread(target=worker, args=(url_chunk,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return returnies