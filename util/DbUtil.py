import pymysql
import math

""" 用pymysql 操作数据库 """


def get_connection():
    host = '127.0.0.1'
    port = 13306
    db = 'area'
    user = 'root'
    password = 'xxx'
    conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    return conn


def initClientEncode(conn):
    '''mysql client encoding=utf8'''
    curs = conn.cursor()
    curs.execute("SET NAMES utf8")
    conn.commit()
    return curs


""" 使用 with 的方式来优化代码 """


class UsingMysql(object):

    def __init__(self, commit=True, log_label=' In total', numPerPage=20):
        """
        :param commit: 是否在最后提交事务(设置为False的时候方便单元测试)
        :param log_label:  自定义log的文字
        """
        self._commit = commit
        self._log_label = log_label
        self.numPerPage = numPerPage

    def queryForList(self, sql, param=None):
        totalPageNum = self.__calTotalPages(sql, param)
        for pageIndex in range(totalPageNum):
            yield self.__queryEachPage(sql, pageIndex, param)

    def __createPaginaionQuerySql(self, sql, currentPageIndex):
        startIndex = self.__calStartIndex(currentPageIndex)
        qSql = r'select * from (%s) total_table limit %s,%s' % (sql, startIndex, self.numPerPage)
        return qSql

    def __queryEachPage(self, sql, currentPageIndex, param=None):
        curs = initClientEncode(get_connection())
        qSql = self.__createPaginaionQuerySql(sql, currentPageIndex)
        if param is None:
            curs.execute(qSql)
        else:
            curs.execute(qSql, param)
        result = curs.fetchall()
        curs.close()
        return result

    def __calTotalRowsNum(self, sql, param=None):
        ''' 计算总行数 '''
        tSql = r'select count(*) from (%s) total_table' % sql
        curs = initClientEncode(get_connection())
        if param is None:
            curs.execute(tSql)
        else:
            curs.execute(tSql, param)
        result = curs.fetchone()
        curs.close()
        totalRowsNum = 0
        if result != None:
            totalRowsNum = int(result[0])
        return totalRowsNum

    def __calTotalPages(self, sql, param):
        ''' 计算总页数 '''
        totalRowsNum = self.__calTotalRowsNum(sql, param)
        totalPages = 0
        tempTotal = totalRowsNum / self.numPerPage
        if (totalRowsNum % self.numPerPage) == 0:
            totalPages = tempTotal
        else:
            totalPages = math.ceil(tempTotal)
        return totalPages

    def __calStartIndex(self, currentPageIndex):
        startIndex = currentPageIndex * self.numPerPage
        return startIndex;

    def __calLastIndex(self, totalRows, totalPages, currentPageIndex):
        '''计算结束时候的索引'''
        lastIndex = 0
        if totalRows < self.numPerPage:
            lastIndex = totalRows
        elif ((totalRows % self.numPerPage == 0)
              or (totalRows % self.numPerPage != 0 and currentPageIndex < totalPages)):
            lastIndex = currentPageIndex * self.numPerPage
        elif (totalRows % self.numPerPage != 0 and currentPageIndex == totalPages):  # 最后一页
            lastIndex = totalRows
        return lastIndex

    def __enter__(self):

        """ 在进入的时候自动获取连接和cursor """
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        conn.autocommit = False

        self._conn = conn
        self._cursor = cursor
        return self

    def __exit__(self, *exc_info):
        """ 提交事务 """
        if self._commit:
            self._conn.commit()
        """ 在退出的时候自动关闭连接和cursor """
        self._cursor.close()
        self._conn.close()

    @property
    def cursor(self):
        return self._cursor
