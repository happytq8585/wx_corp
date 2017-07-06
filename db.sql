create table if not exists wxcorp_user
(
 id int unsigned primary key auto_increment,
 name varchar(64) not null,
 password varchar(1024) not null,
 role int unsigned default 100 /*1=admin   100=common user*/
)engine=InnoDB, charset=utf8;

insert into wxcorp_user(id, name, password, role) values(1, "admin", "3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2", 1);

create table if not exists order_info
(
 id int unsigned primary key auto_increment,
 user_id int unsigned not null,
 dish_id int unsigned not null,
 num     int unsigned not null,
 time date not null
) engine=InnoDB, charset=utf8;

/*菜的数据库表*/
create table if not exists dish
(
 id int unsigned primary key auto_increment,
 name varchar(128) not null,           /*菜的名字*/
 pic_loc  varchar(256) not null,       /*菜图片存放的位置*/
 time date not null,                   /*菜的日期 年-月-日*/
 material varchar(128) default "",     /*菜的食材*/
 can_order int unsigned default 0,     /*菜是否可预订 0=不可以 1=可以*/
 one int unsigned default 0,           /*菜得1颗星的个数*/
 two int unsigned default 0,           /*菜得2颗星的个数*/
 three int unsigned default 0,         /*菜得3颗星的个数*/
 four int unsigned default 0,          /*菜得4颗星的个数*/
 five int unsigned default 0           /*菜得5颗星的个数*/
) engine=InnoDB, charset=utf8;

/*菜的评论*/
create table if not exists dish_comment
(
 id int unsigned primary key auto_increment,
 dish_id int unsigned not null,       /*菜的id*/
 user_id int unsigned not null,       /*用户的id*/
 starts  int unsigned default 1,      /*用户对该菜评价了几颗星*/
 time date not null,                  /*评论的时间*/
 content varchar(512)                 /*评价的内容*/
) engine=InnoDB, charset=utf8;
