#encoding=utf-8
import requests,re,bs4,time,sys,hashlib,uuid,time,json,base64,rsa,platform,datetime,os,urllib
from lxml import etree
UserAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
def get_time(format_date,time_pull = None):
    if time_pull:
        return int(time.mktime(time.strptime(time_pull, format_date))*1000)
def standard_work_list():
    return_data = []
    headers = {'User-Agent': UserAgent}
    res = requests.get('http://www.jkb.com.cn/news/industryNews/', headers=headers)
    res.raise_for_status()
    reg_content = res.content.decode('utf-8')
    html_page = bs4.BeautifulSoup(reg_content, 'lxml')
    infos = html_page.findAll(class_='ellipsis fl')

    for one_info in infos:
        _one_info = str(one_info)
        content_dir = one_info

        _datetime = 0
        _url_tmp = content_dir['href']
        print({'url': _url_tmp, 'title': content_dir.text.strip()})
        return_data.append({'url': _url_tmp, 'title': "", 'datetime': _datetime})
    return return_data


def standard_work_article(target_url):
    return_data = []
    headers = {'User-Agent': UserAgent}
    res = requests.get(target_url, headers=headers)
    res.raise_for_status()
    reg_content = res.content.decode('utf-8','ignore')
    html_page = bs4.BeautifulSoup(reg_content, 'lxml')
    infos = html_page.find(id='nc_con').text

    return_data.append(infos.strip())
    tim = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", reg_content)
    datetime_dir = re.match('(?P<year>\d{4})-(?P<month>\d+?)-(?P<day>\d+?) (?P<hour>\d+?):(?P<minute>\d+)',
                            tim[0])
    tt_tmp = '%s-%s-%s %s:%s' % (
    datetime_dir['year'], datetime_dir['month'], datetime_dir['day'], datetime_dir['hour'], datetime_dir['minute'])
    _datetime = 0
    if datetime_dir:
        _datetime = get_time('%Y-%m-%d %H:%M', tt_tmp)
    _title = html_page.find('h3').text
    return _datetime, '%s<replace title>%s' % (_title, '\n'.join(return_data))

def main():
   list = standard_work_list()
   for url in list:
       print(standard_work_article(url['url']))



if __name__ == '__main__':
    main()
