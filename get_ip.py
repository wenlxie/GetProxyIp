import threading
import urllib
from time import sleep
from urllib import request
from bs4 import BeautifulSoup


def get_ip():
    of = open('proxy.txt', 'w')
    for page in range(11, 20):
        url = 'http://www.xicidaili.com/nn/%s' % page
        user_agent = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        my_request = urllib.request.Request(url)

        my_request.add_header("User-Agent", user_agent)
        my_url_open = urllib.request.urlopen(my_request)
        content = my_url_open.read()
        content = content.decode("utf8")
        my_url_open.close()
        soup = BeautifulSoup(content, "lxml")
        trs = soup.find('table', {"id": "ip_list"}).findAll('tr')

        for tr in trs[1:]:
            tds = tr.findAll('td')
            ip = tds[1].text.strip()
            port = tds[2].text.strip()
            protocol = tds[5].text.strip()
            if protocol == 'HTTP' or protocol == 'HTTPS':
                proxy = ip + ":" + port
                print('%s=%s\n' % (protocol, proxy))
                if check(protocol, proxy):
                    of.write('%s=%s\n' % (protocol, proxy))
                    print("可用！")
                else:
                    print("不可用！")
                print("=============================================")
        of.close()
        # sleep(100)


def check(protocol, proxy):
    url = 'http://www.baidu.com'
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': 'http://' + proxy})
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)

        my_request = urllib.request.Request(url)
        content = urllib.request.urlopen(my_request, timeout=4).read()
        if len(content) >= 1000:
            return True
        else:
            return False
    except Exception as error:
        print(error)


if __name__ == '__main__':
    get_ip()
