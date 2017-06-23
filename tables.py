#-*- coding: utf-8 -*-

import hashlib

from sqlalchemy import Column, String, Integer, Date, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# 创建对象的基类:
Base = declarative_base()

class User(Base):
    def __init__(self, name, password):
        self.id       = 0
        self.name     = name
        self.password = password
# 表的名字:
    __tablename__ = 'canteen_user'

# 表的结构:
    #用户的id
    id = Column(Integer, primary_key=True)
    #用户的名字
    name = Column(String(64))
    #用户的密码hash值
    password = Column(String(1024))

class Dish(Base):
# 表的名字:
    __tablename__ = 'dish'
    def __init__(self, **arr):
        self.id = arr['id']
        self.name = arr['name']
        self.pic_loc = arr['pic_loc']
        self.time = arr['time']
        self.one    = int(arr.get('one', '0'))
        self.two    = int(arr.get('two', '0'))
        self.three  = int(arr.get('three', '0'))
        self.four   = int(arr.get('four', '0'))
        self.five   = int(arr.get('five', '0'))
# 表的结构:
    #图片的id
    id = Column(Integer, primary_key=True)
    #图片的名字
    name = Column(String(128))
    #图片存储的位置
    pic_loc = Column(String(256))
    #图片上传的时间
    time  = Column(Date)
    one   = Column(Integer)
    two   = Column(Integer)
    three = Column(Integer)
    four  = Column(Integer)
    five  = Column(Integer)

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
"""
将上传的图片信息写入数据库，图片存放在本地服务器上
一个图片对应一道菜
"""
def write_dish(**dic):
    session = DBSession()
    for e in dic:
        [pic_loc, timestamp] = dic[e].split('\3')
        d = Dish(id=0, name=e, pic_loc=pic_loc, time=timestamp)
        session.add(d)
    session.commit()
    session.close()
"""
查询指定日期的菜谱信息, 指定日期是yyyymmdd
"""
def query_menu_list(timestamp):
    session = DBSession()
    res = session.query(Dish).filter(Dish.time == timestamp).all()
    if not res:
        return []
    data = [[str(e.name), str(e.pic_loc), "%4d%02d%02d"%(e.time.year, e.time.month, e.time.day), e.one, e.two, e.three, e.four, e.five] for e in res]
    return data

def regist_user(info):
    [uname, passwd] = info.split('\3');
    if not uname or not passwd:
        return -1#name or password is None
    session = DBSession()
    res = session.query(User).filter(User.name == uname).count()
    if not res:
        sha512 = hashlib.sha512(passwd.encode()).hexdigest()
        u = User(uname, sha512)
        ret = session.add(u)
        session.commit()
        return 0#regist successfully
    return 1#name duplicated

if __name__ == "__main__":
    uname   = "tiger";
    passwd  = "456";
    ret = regist_user(uname + '\3' + passwd)
    print ret
