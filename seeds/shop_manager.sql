/*

USER STORIES

As a shop manager
So I can know which items I have in stock
I want to keep a list of my shop items with their name and unit price.

As a shop manager
So I can know which items I have in stock
I want to know which quantity (a number) I have for each item.

As a shop manager
So I can manage items
I want to be able to create a new item.

As a shop manager
So I can know which orders were made
I want to keep a list of orders with their customer name.

As a shop manager
So I can know which orders were made
I want to assign each order to their corresponding item.

As a shop manager
So I can know which orders were made
I want to know on which date an order was placed. 

As a shop manager
So I can manage orders
I want to be able to create a new order.

NOUNS - items, orders, customer_name, quantity, unit_price, date_placed

DESIGN

items
id | name | quantity | unit_price

orders
id | customer_name | date_placed

orders_items
order_id | item_id

*/

drop table if exists orders_items;
drop table if exists orders;
drop table if exists items;

drop sequence if exists orders_id_seq;
drop sequence if exists items_id_seq;

create sequence items_id_seq;
create sequence orders_id_seq;

create table items (
    id serial primary key,
    name varchar(255),
    quantity int,
    unit_price float
)

create table orders (
    id serial primary key,
    customer_name varchar(255),
    date_placed date
)

create table orders_items (
    order_id int,
    item_id int,
    constraint fk_order_id foreign key (order_id) references orders(id) on delete cascade,
    constraint fk_item_id foreign key (item_id) references items(id) on delete cascade
)

insert into items (name, quantity, unit_price) values ('apple', 10, 0.5);
insert into items (name, quantity, unit_price) values ('banana', 5, 0.75);
insert into items (name, quantity, unit_price) values ('pizza', 7, 4.99);
insert into items (name, quantity, unit_price) values ('chocolate', 12, 1.99);
insert into items (name, quantity, unit_price) values ('milk', 2, 3);

insert into orders (customer_name, date_placed) values ('John', '2019-01-01');
insert into orders (customer_name, date_placed) values ('Jane', '2019-01-02');
insert into orders (customer_name, date_placed) values ('Jack', '2019-01-03');

insert into orders_items (order_id, item_id) values (1, 1);
insert into orders_items (order_id, item_id) values (1, 2);
insert into orders_items (order_id, item_id) values (1, 5);

insert into orders_items (order_id, item_id) values (2, 3);
insert into orders_items (order_id, item_id) values (2, 4);

insert into orders_items (order_id, item_id) values (3, 1);
insert into orders_items (order_id, item_id) values (3, 2);