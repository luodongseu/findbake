# coding: UTF-8

import web
#import sae.const
import sys

# sae.const.MYSQL_DB      # 数据库名
# sae.const.MYSQL_USER    # 用户名
# sae.const.MYSQL_PASS    # 密码
# sae.const.MYSQL_HOST    # 主库域名（可读写）
# sae.const.MYSQL_PORT    # 端口，类型为<type 'str'>，请根据框架要求自行转换为int
# sae.const.MYSQL_HOST_S  # 从库域名（只读）

# public db
db = web.database(dbn='mysql',
                  host='127.0.0.1',#sae.const.MYSQL_HOST,
                  port=3306,#int(sae.const.MYSQL_PORT),
                  db='findbake',#sae.const.MYSQL_DB,
                  user='root',#sae.const.MYSQL_USER,
                  pw='Luodongseu'#sae.const.MYSQL_PASS)
)
sys.path.append("..")

# public template render
render = web.template.render('templates/')
