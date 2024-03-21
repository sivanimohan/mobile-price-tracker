import requests
from bs4 import BeautifulSoup
baseurl="https://www.amazon.in/"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

def mobiles(url):
    page=[]
    baseurl="https://www.amazon.in/"
    r=requests.get(url)
    soup = BeautifulSoup(r.content,'lxml')
    productlink=""
    productlist = soup.find_all('h2',class_='a-size-mini a-spacing-none a-color-base s-line-clamp-2')
    for item in productlist:
      for link in item.find_all('a',class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal', href=True):
        productlink=baseurl+link['href']
        print(productlink)

      
def main():
 for i in range(1, 401):
        if i == 1:
            url = "https://www.amazon.in/s?k=mobile+phones&rh=n%3A1389401031&ref=nb_sb_noss"
        else:
            url = f"https://www.amazon.in/s?k=mobile+phones&i=electronics&rh=n%3A1389401031&page={i}&qid=1710959218&ref=sr_pg_{i}"
        mobiles(url)

if __name__ == "__main__":
    main()
