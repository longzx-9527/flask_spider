# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-04-20 21:50:57
# @cnblog:http://www.cnblogs.com/lonelyhiker/

import datetime
from . import db
from .models import Commparam


def generate_id(param_name):
    # 序号产生器
    dt = str(datetime.date.today()).replace('-', '')
    commparam = Commparam.query.filter_by(param_name=param_name).first()

    # 如果不存在,就创建
    if commparam is None:
        # 创建参数对象
        commparam = Commparam(param_name=param_name)
        # 提交数据库
        db.session.add(commparam)
        num = 1
    else:
        commparam.param_value += 1
        num = commparam.param_value
        db.session.add(commparam)

    id = '%s%08d' % (dt, num)

    return id
