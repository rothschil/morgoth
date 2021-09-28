class Announcement:
    "Announcement class"

    def __init__(self, provincetr, is_termination, name, code, anno_type, create_time, begin_time, end_time):
        # 省份
        self.provincetr = provincetr
        # 是否终止
        self.is_termination = is_termination
        # 公告名称
        self.name = name
        # 公告编码
        self.code = code
        # 公告类型
        self.anno_type = anno_type
        # 创建时间
        self.create_time = create_time
        # 开始时间
        self.begin_time = begin_time
        # 结束时间
        self.end_time = end_time

    def __str__(self) -> str:
        return 'provincetr：%s\t  isTermination：%s\t  name：%s\t code：%s\t type：%s\t createTime：%s\t beginTime：%s\t ' \
               'endTime：%s\t' % (self.provincetr, self.is_termination, self.name, self.code, self.anno_type, self.create_time, self.begin_time, self.end_time)
