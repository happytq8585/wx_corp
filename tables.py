#-*- coding: utf-8 -*-

import hashlib

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# 创建对象的基类:
Base = declarative_base()

class User(Base):
# 表的名字:
    __tablename__ = 'canteen_user'

# 表的结构:
    #用户的id
    id = Column(Integer, primary_key=True)
    #用户的名字
    name = Column(String(64))
    #用户的密码hash值
    password = Column(String(1024))

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:@localhost:3306/wxcorp',encoding='utf-8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

#失败返回None
#成功返回[priority, [branch], [agency]]
def query_user(line):
    session = DBSession()
    name, password = line.split('\3')
    sha512 = hashlib.sha512(password.encode()).hexdigest()
    res = session.query(User.name, User.password).filter(User.name==name, User.password==sha512).first()
    if not res:
        return None
    return True
    
if __name__ == "__main__":
    line = 'admin' + '\3' + '123'
    res = query_user(line)
    print(res)
