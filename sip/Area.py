class Area:
    "Area class 行政区域实例"

    def __init__(self, url, name, code, sup_code, lv):
        self.name = name
        self.code = code
        self.url = url
        self.sup_code = sup_code
        self.lv = lv

    def __str__(self) -> str:
        return 'URL：%s\t  NAME：%s\t  Code：%s\t SUPER_CODE：%s\t LV：%s\t' % (
            self.url, self.name, self.code, self.sup_code, self.lv)
