setup_command = """drop table  if exists product;
drop table if exists orderEnquiry;

create  table product(
    id bigint primary key,
    name varchar(200) not null ,
    price numeric,
    amount integer,
    created timestamp,
    constraint ck_product_price check ( price>=0 ),
    constraint ck_product_amount check ( amount>=0 )
);

create table orderEnquiry(
    id bigint primary key,
    amount int,
    customer varchar(200) not null ,
    created timestamp,
    productid bigint,
    constraint fk_orderEnquiry_product foreign key (productid) references product(id),
    constraint ck_orderEnquiry check ( amount>=0 )
);
"""
