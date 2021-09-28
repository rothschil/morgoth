import urllib.request

from po.Area import Area
from util.DbUtil import UsingMysql

from bs4 import BeautifulSoup

G_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

G_URL = r'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html'
# 获取URL前缀
G_URL_PREFIX = G_URL[0:G_URL.rindex('/') + 1]

'''
爬取国家统计局网站中 关于行政区划的数据，按照层级进行编辑，最终形成一个树形结构。
包含：省/直辖市/自治区、地级市、区县、乡/镇/街道、居委会/村

'''

# Init 执行入口，按照 1、2、3层级顺序执行
def main():
    """ 第一级 省|直辖市 """
    # init_province()
    """ 第二级 地级市 """
    # init_city()
    """ 第三级 区县 """
    init_county()
    # all_town = get_town(all_county)
    # all_village = get_village(all_town)
    # for el in all_village:
    #     print(el)


def get_by_lv(lv):
    with UsingMysql(log_time=True) as um:
        um.cursor.execute(f'select code,name,lv,sup_code,url from areas where lv=%s', lv)
        data = um.cursor.fetchall()
        return data


def get_by_lv_page(lv, last_id, is_next):
    _total = 0
    with UsingMysql(log_time=True) as um:
        um.cursor.execute(f'select count(1) from areas where lv=%s', lv)
        _total = um.cursor.fetchone()
    if _total != 0:
        _page = _total // 10



# 批量插入数据库
def batch_insert(_list):
    with UsingMysql(log_time=True) as um:
        um.cursor.executemany(""" INSERT INTO areas (code,name,lv,sup_code,url) VALUES (%s,%s,%s,%s,%s)""",
                              _list)


def splicing(paramsList):
    _list = list()
    for el in paramsList:
        _list.append((el.code, el.name, el.lv, el.sup_code, el.url))
    batch_insert(_list)


# 数据字典，维护 层级对应的 DIV标签
G_LV_DICT = {1: 'provincetr', 2: 'citytr', 3: 'countytr', 4: 'towntr', 5: 'villagetr'}


# 核心方法 通用处理方法，封装处理解析逻辑
def commons(_list, lv):
    all_area = []
    # 利用父级来遍历子级
    # print(type(_list))
    for lp in _list:
        req = urllib.request.Request(url=get_to_url(lp['url'], lp['code'], lv), headers=G_HEADERS)
        res = urllib.request.urlopen(req)
        html = res.read()
        soup = BeautifulSoup(html, 'html.parser', from_encoding='gb2312')
        all_tr = soup.find_all('tr', attrs={'class': G_LV_DICT[lv]}, limit=30)
        for row in all_tr:
            if lv == 5:
                """ 
                社区的元素发生变更，需要特殊处理
                """
                a_ary = row.find_all('td')
                all_area.append(Area(None, a_ary[2].get_text(), a_ary[0].get_text(), lp['code'], lv))
            else:
                a_ary = row.find_all('a')
                all_area.append(Area(a_ary[0].get('href'), a_ary[1].get_text(), a_ary[0].get_text(), lp['code'], lv))
        # 每次批量写入
        splicing(all_area)
        # 写完后 置空
        all_area = []


# 个性化处理URL地址，并根据层级获取对应URL
def get_to_url(url, code, lv):
    urs = {
        2: G_URL_PREFIX + url,
        3: G_URL_PREFIX + url,
        4: G_URL_PREFIX + code[0:2] + '/' + url,
        5: G_URL_PREFIX + code[0:2] + '/' + code[2:4] + '/' + url,
    }
    return urs.get(lv, None)


# 省/自治区
def init_province():
    all_area = []
    req = urllib.request.Request(url=G_URL, headers=G_HEADERS)
    res = urllib.request.urlopen(req)
    html = res.read()
    soup = BeautifulSoup(html, 'html.parser', from_encoding='gb2312')
    all_tr = soup.find_all('tr', attrs={'class': 'provincetr'}, limit=10)
    for row in all_tr:
        for r_td in row.find_all('a'):
            ars = Area(r_td.get('href'), r_td.get_text(), r_td.get('href')[0:2], '0', 1)
            all_area.append(ars)
    splicing(all_area)


# 市
def init_city():
    _list = get_by_lv(1)
    commons(_list, 2)


# 区县
def init_county():
    _list = get_by_lv(2)
    commons(_list, 3)


# 街道
def get_town(paramsList):
    return commons(paramsList, 4)


# 居委会
def get_village(paramsList):
    return commons(paramsList, 5)


if __name__ == '__main__':
    main()
