
## 1. 说明

这是本人使用 `Python` 编写第一个爬虫软件，命名方式依然采用个人钟爱一部文学巨著 `指环王` 来命名，当然这次是用原著中的一个超级大反派，并没有其他含义，纯粹是随心胡乱编写而已。

本工程截止当前主要完成两类数据的爬取。

- 全国统计用区划代码和城乡划分代码

![20210929180146](https://abram.oss-cn-shanghai.aliyuncs.com/blog/gradle/20210929180146.png)

- 中国电信阳光采购网公告信息
  
![20210929180406](https://abram.oss-cn-shanghai.aliyuncs.com/blog/github/python/20210929180406.png)

## 工程

~~~cmd


~~~

### 区划代码


~~~sql
CREATE TABLE tb_locations (  
  local_code VARCHAR(30) DEFAULT NULL,
  local_name VARCHAR(100) DEFAULT NULL,
  lv INT(11) DEFAULT NULL,
  sup_local_code VARCHAR(30) DEFAULT NULL,
  flag VARCHAR(6) DEFAULT NULL,
  url VARCHAR(60) DEFAULT NULL
) ;
~~~


### 公告