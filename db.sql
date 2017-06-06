create table if not exists canteen_user
(
 id int unsigned primary key auto_increment,
 name varchar(64) not null,
 password varchar(1024) not null
)engine=InnoDB, charset=utf8;

insert into canteen_user(id, name, password) values(1, "admin", "3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2");
