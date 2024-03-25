import requests
from bs4 import BeautifulSoup
import time
import random



baseurl = "https://www.amazon.in/"

proxies = [
    {'http': 'http://122.185.44.46:8080'},
    {'http': 'http://14.143.130.210:80'},
    {'http': 'http://103.196.28.6:80'},
    {'http': 'http://139.59.1.14:8080'},
    {'http': 'http://103.48.71.130:80'},
    {'http': 'http://103.159.46.10:80'},
    {'http': 'http://103.159.46.10:80'},
    {'http': 'http://68.233.112.56:80'},
    {'http': 'http://36.255.87.133:8080'},
    {'http': 'http://103.24.125.33:80'}
]

user_agents = [
  
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.58",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 OPR/85.0.4344.41",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 OPR/85.0.4344.41",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
]




def get_brand(soup):
        br = soup.find('tr', class_='a-spacing-small po-brand')
        if br:
            return br.text.strip().replace("Brand", "")
        return None    
            
    

def get_model(soup):
    md = soup.find('tr', class_='a-spacing-small po-model_name')
    if md:
        return md.text.strip().replace("Model Name", "")
    return None


def get_rating(soup):
    rg = soup.find('span', class_='a-icon-alt')
    if rg:
        return rg.text.strip()
    return None

def get_price(soup):
    pr = soup.find('span', class_='aok-offscreen')
    if pr:
        return pr.text.strip()
    return None
def get_deliverytime(soup):
    de = soup.find('div', class_='a-spacing-base',id='mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE')
    if de:
        return de.text.strip().replace("Details","")
    return None
def get_colour(soup):
   return None

      
def operating_system(soup):
     os=soup.find('tr', class_='a-spacing-small po-operating_system')
     if os:
            return os.text.strip().replace("Operating System", "")
     return None
def get_memory(soup):
    memory = soup.find('div', id='variation_memory_size', class_='a-row')
    if memory:
        return memory.text.strip().replace("Memory:","")
    return None

def get_ram(soup):
    ram = soup.find('div', id='variation_ram_size', class_='a-row')
    if ram:
        return ram.text.strip().replace("RAM:","")
    return None

def get_condition(soup):
    condition = soup.find('span', id='productTitle', class_='a-size-large product-title-word-break')
    if condition:
            if "Refurbished" in condition:
                return "Refurbished" 
            else:
                return "New"

def get_image_url(soup):
    image_url = soup.find('img', class_='a-dynamic-image a-stretch-vertical')
    if image_url:
        return image_url['src']
    return None



def mobiles(url):
    page = []
    productlink=""
    productlinks=[]
    visited=[]
    v=[]
    while (url not in v):
            user_agent = random.choice(user_agents)
            proxy = random.choice(proxies)
            headers = {'User-Agent': user_agent}
            r = requests.get(url, headers=headers, proxies=proxy)
            time.sleep(2)  
            print("Response Code:", r.status_code)
            
            if r.status_code == 200:
                  soup = BeautifulSoup(r.content, 'lxml')
                  productlist = soup.find_all('h2', class_='a-size-mini a-spacing-none a-color-base s-line-clamp-2')
                  for item in productlist:
                    for link in item.find_all('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal', href=True):
                        if (link not in productlinks):
                            productlink = baseurl + link['href']
                            productlinks.append(productlink)
                            print(productlink)
                            scrape_mobile_data(productlink)
                            v.append(url)   
            elif r.status_code == 503:
                print("503 Service Unavailable - Retrying...")
                time.sleep(2)  
            else:
                r.raise_for_status()

def scrape_mobile_data(productlink):
    while True:
        user_agent = random.choice(user_agents)
        proxy = random.choice(proxies)
        headers = {'User-Agent': user_agent}
        s = requests.get(productlink, headers=headers)
        soup = BeautifulSoup(s.content, 'lxml')
        response = requests.get(productlink, headers=headers, proxies=proxy)
        

        if response.status_code == 200:
            brand = get_brand(soup)
            model = get_model(soup)
            rating = get_rating(soup)
            price = get_price(soup)
            delivery_time = get_deliverytime(soup)
            os=operating_system(soup)
            colour = get_colour(soup)
            memory = get_memory(soup)
            ram = get_ram(soup)
            condition = get_condition(soup)
            image_url = get_image_url(soup)  

            if all([brand, model, rating, price, delivery_time,image_url]):
                print("Brand:", brand)
                print("Model:", model)
                print("Rating:", rating)
                print("Price:", price)
                print("Delivery Time:", delivery_time)
                print("OS:",os)
                print("Colour:", colour)
                print("Memory:", memory)
                print("RAM:", ram)
                print("Condition:", condition)
                print("Image URL:", image_url)
                break
            else:
                    continue
        else:
            response.raise_for_status()

    

def main():
    for i in range(1, 401):
        if i == 1:
            url = "https://www.amazon.in/s?k=mobile+phones&rh=n%3A1389401031&ref=nb_sb_noss"
        else:
            url = f"https://www.amazon.in/s?k=mobile+phones&i=electronics&rh=n%3A1389401031&page={i}&qid=1710959218&ref=sr_pg_{i}"
        print(url)
        print(i)
        mobiles(url)


if __name__ == "__main__":
    main()

