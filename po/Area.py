class Area:
    "Area class"

    def __init__(self, url, name, code, sup_code, lv):
        # 名称
        self.name = name
        # 编码
        self.code = code
        # 地址后缀
        self.url = url
        # 上级编码
        self.sup_code = sup_code
        # 层级
        self.lv = lv

    def __str__(self) -> str:
        return 'URL：%s\t  NAME：%s\t  Code：%s\t SUPER_CODE：%s\t LV：%s\t' % (
        self.url, self.name, self.code, self.sup_code, self.lv)
