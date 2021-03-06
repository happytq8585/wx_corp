#-*- coding: utf-8 -*-

import time
import hashlib

from sqlalchemy import Column, String, Integer, Date, TIMESTAMP, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# 创建对象的基类:
Base = declarative_base()

class User(Base):
    def __init__(self, name, password, role):
        self.id       = 0
        self.name     = name
        self.password = password
        self.role     = role
# 表的名字:
    __tablename__ = 'wxcorp_user'

# 表的结构:
    #用户的id
    id = Column(Integer, primary_key=True)
    #用户的名字
    name = Column(String(64))
    #用户的密码hash值
    password = Column(String(1024))
    role     = Column(Integer)

class Dish(Base):
# 表的名字:
    __tablename__ = 'dish'
    def __init__(self, **arr):
        self.id             = arr['id']
        self.name           = arr['name']
        self.pic_loc        = arr['pic_loc']
        self.time           = arr['time']
        self.material       = arr.get('material', '')
        self.can_order      = int(arr.get('can_order', '0'))
        self.one            = int(arr.get('one', '0'))
        self.two            = int(arr.get('two', '0'))
        self.three          = int(arr.get('three', '0'))
        self.four           = int(arr.get('four', '0'))
        self.five           = int(arr.get('five', '0'))
# 表的结构:
    #图片的id
    id          = Column(Integer, primary_key=True)
    #图片的名字
    name        = Column(String(128))
    #图片存储的位置
    pic_loc     = Column(String(256))
    #图片上传的时间
    time        = Column(Date)
    material    = Column(String(128))
    can_order   = Column(Integer)
    one         = Column(Integer)
    two         = Column(Integer)
    three       = Column(Integer)
    four        = Column(Integer)
    five        = Column(Integer)

class Comment(Base):
    __tablename__ = "dish_comment"
    def __init__(self, id_, did_, uid_, s_, c_):
        t = time.localtime();
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", t)
        self.id          = id_
        self.dish_id     = did_
        self.user_id     = uid_
        self.stars       = s_
        self.time        = timestamp
        self.content     = c_
    #comment的id
    id          = Column(Integer, primary_key=True)
    dish_id     = Column(Integer)
    user_id     = Column(Integer)
    stars       = Column(Integer)
    time        = Column(TIMESTAMP)
    content     = Column(String(512))

class Order(Base):
    __tablename__ = "order_info"
    def __init__(self, id_, uid, uname, did, dname, img_url, num):
        self.id            = id_
        self.user_id       = uid
        self.user_name     = uname
        self.dish_id       = did
        self.dish_name     = dname
        self.img_url       = img_url
        self.num           = num
    id          = Column(Integer, primary_key=True)
    user_id     = Column(Integer)
    user_name   = Column(String(64))
    dish_id     = Column(Integer)
    dish_name   = Column(String(64))
    img_url     = Column(String(128))
    num         = Column(Integer)
    time        = Column(TIMESTAMP)

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:@localhost:3306/wxcorp',encoding='utf-8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

#失败返回None
#成功返回[role, id]
def query_user(line):
    session = DBSession()
    name, password = line.split('\3')
    sha512 = hashlib.sha512(password.encode()).hexdigest()
    res = session.query(User.name, User.password, User.role, User.id).filter(User.name==name, User.password==sha512).first()
    if not res:
        return None
    return [res[2], res[-1]]#[role, id]
"""
将上传的图片信息写入数据库，图片存放在本地服务器上
一个图片对应一道菜
"""
def write_dish(filename, dish_name, dish_material, dish_order):
    session = DBSession()
    [pic_loc, timestamp] = filename.split('\3')
    d = Dish(id=0, name=dish_name, pic_loc=pic_loc, time=timestamp, can_order=dish_order, material=dish_material)
    session.add(d)
    session.commit()
    session.close()
"""
将评论写入数据库，一个用户id对应一个菜的id
"""
def write_comment(userid, dish_id, star, words):
    session = DBSession()
    c = Comment(0, dish_id, userid, star, words)
    session.add(c)
    session.commit()
    session.close()
    return True
"""
将预订信息写入数据库
"""
def write_order(userid, username, dish_id, dish_name, img_url, num):
    session = DBSession()
    o = Order(0, userid, username, dish_id, dish_name, img_url, num)
    session.add(o)
    session.commit()
    session.close()
    return True
"""
查询菜的评论
"""
def query_comments_by_id(dish_id):
    session = DBSession()
    c       = session.query(Comment).filter(Comment.dish_id == dish_id).all()
    return c
"""
查询指定日期的菜谱信息, 指定日期是yyyy-mm-dd
"""
def query_dish_by_day(day):
    session = DBSession()
    res = session.query(Dish).filter(Dish.time == day).all()
    if not res:
        return []
    data = [[str(e.name), str(e.pic_loc), day, e.material, e.can_order, e.one, e.two, e.three, e.four, e.five, e.id] for e in res]
    return data

def dish_delete(imgid):
    session = DBSession()
    res = session.query(Dish).filter(Dish.id == imgid).delete(synchronize_session=False)
    session.commit()

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

def update_user_password(userid, old, passwd):
    session = DBSession()
    sha512 = hashlib.sha512(passwd.encode()).hexdigest()
    sha512old = hashlib.sha512(old.encode()).hexdigest()
    res = session.query(User).filter(User.id == userid).filter(User.password == sha512old).count()
    if not res:
        return None
    res = session.query(User).filter(User.id == userid).update({User.password:sha512})
    session.commit()
    session.close()
    return True

def query_order_list_by_uid(uid):
    session = DBSession()
    res = session.query(Order).filter(Order.user_id == uid).order_by(Order.time.desc()).all()
    ret = [{'img_url':e.img_url, 'num': e.num, 'dish_name': e.dish_name, 'time': e.time} for e in res]
    session.close()
    return ret

def query_all_users():
    session = DBSession()
    res = session.query(User).all()
    ret = [{"name": e.name, "role": e.role, "id":e.id, "passwd": e.password} for e in res]
    session.close()
    return ret

def update_user(name, passwd, role, uid):
    session = DBSession()
    res = session.query(User).filter(User.id == uid).first()
    if not res:
        return True
    sha512 = res.password
    if sha512 != passwd:
        sha512 = hashlib.sha512(passwd.encode()).hexdigest()
    res = session.query(User).filter(User.id == uid).update({User.password:sha512, User.name: name, User.role: role})
    session.commit()
    session.close()
    return True
def delete_user(uid):
    session = DBSession()
    res = session.query(User).filter(User.id == uid).delete()
    session.commit()
    session.close()
    return True
def add_user(name, passwd, role):
    session = DBSession()
    sha512 = hashlib.sha512(passwd.encode()).hexdigest()
    user    = User(name, sha512, role)
    res = session.add(user)
    session.commit()
    session.close()
    return True

if __name__ == "__main__":
    pass
