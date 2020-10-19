import os,requests,json,re,csv,time

targeturl = 'https://rate.tmall.com/list_detail_rate.htm?itemId=609536024436&spuId=1478232357&sellerId=2088241559&order=3&currentPage=1&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvgvvPvo%2BvUvCkvvvvvjiWP2Mvgj18R25vsjEUPmPyQjE2PLzv0jnvPFFvljYb9vhvHnsGWltVzYswzHmG7%2FJhz8Sw2xiIdvhvHUZCajh9vvCpkmZNcweHns89RFBVdvhvmpvCLyY6vv2hTs9CvvpvvhCvi9hvCvvvpZpgvpvhvvCvpvvCvvOv9hCvvvmUvpvVvpCmp%2F2OuvhvmvvvpLLGgXQgKvhv8vvvphvvvvvvvvCHtpvv9pIvvhcDvvmCp9vvBJZvvUhKvvCHtpvv9ogUvpCW9bWQWCzxKLpZecCCtWAweXIOJhd9lEp7r3wQBw03HCeZHk62Qa7tnCpO4Z7xfBuK5iX1cwe9eBOXHkx%2F6j7ZHd8ram56rBwgrs3IppgCvvpvvPMM39hvCvmvphmvvpvJjFsc7S2NznswTAC4wgRIkveCS%2BPkRG5U9ZFVAcW2RvhvCvvvphv%3D&needFold=0&_ksTS=1603087688342_1774&callback=jsonp1775'
cookie = 'cna=x0rTF6DqGUACAXozQ6Jms28Y; lid=tb436223391; enc=QJEA5F9HqIhHIhRcACgejbvXe%2FtXxgya%2BAZ%2BIMi5oQeZqPsv0VLq%2BR60gGzrPSibLjZRAX9amHBRr8kIL7Z0%2ByEl0K4u9%2B2dgy0voVxbrq0%3D; sgcookie=E100Vc2%2BYzc0nkbDTjuG5IGZtDeDL7O9jWIHB2VaJHGY%2BeSq6%2F%2BHDfNfsuGzBU%2FI4NyTauDJP7%2BCc9QD8v9cSsGCgw%3D%3D; uc3=lg2=U%2BGCWk%2F75gdr5Q%3D%3D&nk2=F5RBxrCPx4B3vcs%3D&vt3=F8dCufBG1D4NDJarA7c%3D&id2=UUphzOvHrbkqNp5Gow%3D%3D; t=edaa2d7ee7b652c7f292b9fd993e23d1; tracknick=tb436223391; uc4=nk4=0%40FY4Ko%2BWVDLEjF6gZXpmPf3GTrql6QA%3D%3D&id4=0%40U2grF8CLksZpk3ddLqLRIv8WIEf%2BEnw9; lgc=tb436223391; _tb_token_=7373838835d70; cookie2=1acf523d006d02bf9187cbfde74e986b; xlly_s=1; isg=BBMTTL22SLaDNwQi6ZXqVWnropc9yKeK9kMQ3cUw7zJgRDHmTJon2kHSfrQqZP-C; tfstk=c765BpNG-407j4PEUgZ24DhzVBp5afaXm7TRV_nqyP8ztPIWksvqQF99960mHCKf.; l=eBL-gaWHOR_JumZwBO5aFurza77OoIRbzsPzaNbMiInca6NVwEhKMNQV9JuykdtjgtCf8eKybUMLyREH5LzdgZqhuJ1REpZZfxvO.'
referer = 'https://detail.tmall.com/item.htm?spm=a230r.1.14.1.19cf53c4AS20P3&id=581507384116&ns=1&abbucket=3'
useragent = 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0'
dirname = 'laoguanjia'
headers = {'cookie':cookie,'user-agnet':useragent,'referer':referer}
filename = 'csv' # 保存文件名称
startpage = 0 # 起始页
interval = 30 # 收集每页间隔秒数

def create_csv(rateheader):
    with open('./record/'+dirname + '/'+filename+'.csv','w',newline='',encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(rateheader)

def append_csv(ratelist):
    with open('./record/'+dirname + '/'+filename+'.csv','a+',newline='',encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        for rate in ratelist:
            csvwriter.writerow(rate)

def parse_ratetext(ratetext):
    try:
        startpos = re.search('jsonp[0-9]*\(',ratetext).end()
        ratetext = ratetext[startpos:]
        ratetext = ratetext[:-1]
        ratejson = json.loads(ratetext)
        ratejson = ratejson['rateDetail']
        ratelist = ratejson['rateList']
        pageinfo = ratejson['paginator']
        lastpage = pageinfo['lastPage']
        currentpage = pageinfo['page']
        result = {'totalpage':int(lastpage),'currentpage':int(currentpage),'list':[]}
        for rate in ratelist:
            result['list'].append([rate['id'],rate['rateDate'],rate['displayUserNick'],rate['rateContent'],rate['cmsSource']])
        return result        
    except KeyError:
        return None
    except json.JSONDecodeError:
        return None
    pass


if __name__ == "__main__":
    try:
        os.makedirs('./record/'+dirname)
        result = {'currentpage':startpage, 'totalpage':100}
        if(startpage == 0):
            rateheader = ['ID','日期','昵称','评论','来源']
            create_csv(rateheader)
    except:
        print('except in makedirs')

    while((result is not None) and (result['currentpage'] < result['totalpage'])):
        pagestr = re.findall('currentPage=[0-9]*',targeturl)[0]
        targeturl = targeturl.replace(pagestr,'currentPage='+str(result['currentpage']+1))
        r = requests.request('get',targeturl,headers=headers)
        #
        # with open('./record/'+ dirname + '/' +str(result['currentpage'])+".txt",'w',encoding='utf-8') as fff:
        #     fff.write(r.text)
        result = parse_ratetext(r.text)
        if(result != None):
            append_csv(result['list'])
            print('共'+str(result['totalpage'])+'页','完成第'+str(result['currentpage'])+'页')
        else:
            break
        time.sleep(interval)
        

   

