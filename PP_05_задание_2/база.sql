CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    family_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    inn VARCHAR(255),
    salesman BOOLEAN
);

CREATE TABLE employee_positions (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL UNIQUE,
    code VARCHAR(255) NOT NULL
);

CREATE TABLE employee_roles (
    id INTEGER PRIMARY KEY,
    code VARCHAR(255) NOT null unique
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    family_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    position_id INTEGER,
    FOREIGN KEY (position_id) REFERENCES employee_positions(id)
);

create table order_statuses (
	id integer primary key,
	code varchar(50)
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    customer_id INTEGER NOT NULL,
    status_id INTEGER NOT NULL,
    manager_id INTEGER NOT NULL,
    foreign key (status_id) REFERENCES  order_statuses(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (manager_id) REFERENCES employees(id)
);

CREATE TABLE materials (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    unit_of_measure VARCHAR(50),
    cost integer
);

create table units_of_measures (
	id serial primary key,
	code VARCHAR(255) NOT null unique
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    unit_of_measure VARCHAR(50),
    code VARCHAR(100) UNIQUE
);

create table bill_of_material (
	id integer PRIMARY key,
	product_id integer,
	material_id integer,
	quantity integer,
	foreign key (material_id) references materials(id),
	foreign key (product_id) references products(id)
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_at_sale INTEGER NOT NULL CHECK (price_at_sale >= 0),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE product_batches (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    order_id INTEGER,
    date TIMESTAMP,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

alter table customers 
add column buyer boolean DEFAULT FALSE;


alter table customers 
add column name VARCHAR(255);

alter table customers
drop column first_name;


alter table customers
drop column last_name;


alter table customers
drop column family_name;

ALTER TABLE order_statuses ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY;
ALTER TABLE employee_positions ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY;
ALTER TABLE employees ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY;
ALTER TABLE orders ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY;
ALTER TABLE order_items ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY;
ALTER TABLE products ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY;
ALTER TABLE materials ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY;
ALTER TABLE customers ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY;
ALTER TABLE product_batches ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY;
ALTER TABLE order_statuses ADD COLUMN title varchar(255);
alter table employees add column login varchar(255) unique not null;
alter table employees add column password varchar(255);
ALTER TABLE employees ADD COLUMN role_id INTEGER REFERENCES employee_roles(id);
ALTER TABLE employee_roles ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY;
alter table employees add column blocked boolean default false not null;

alter table products drop column unit_of_measure;
ALTER TABLE products ADD COLUMN unit_of_measure_id INTEGER REFERENCES units_of_measures(id);
ALTER TABLE products ADD COLUMN deleted BOOLEAN DEFAULT false;

alter table materials drop column unit_of_measure;
ALTER TABLE materials ADD COLUMN unit_of_measure_id INTEGER REFERENCES units_of_measures(id);

alter table products
add column default_price integer check (default_price > 0) default 1;

alter table bill_of_material ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY;
alter table bill_of_material alter column quantity type float;
ALTER TABLE bill_of_material ADD COLUMN deleted BOOLEAN DEFAULT false;

alter table products alter column default_price type float;

alter table order_items alter column price_at_sale type float;

alter table materials alter column cost type float;

INSERT INTO customers (id, name, inn, address, phone, salesman, buyer) VALUES
('000000001', 'ООО "Поставка"', '', 'г.Пятигорск', '+79198634592', TRUE, TRUE),
('000000002', 'ООО "Кинотеатр Квант"', '26320045123', 'г. Железноводск, ул. Мира, 123', '+79884581555', TRUE, FALSE),
('000000008', 'ООО "Новый JDTO"', '26320045111', 'г. Железноводсу', '+79884581555', TRUE, FALSE),
('000000003', 'ООО "Ромашка"', '4140784214', 'г. Омск, ул. Строителей, 294', '+79882584546', FALSE, TRUE),
('000000009', 'ООО "Ипподром"', '5874045632', 'г. Уфа, ул. Набережная, 37', '+79627486389', TRUE, TRUE),
('000000010', 'ООО "Ассоль"', '2629011278', 'г. Калуга, ул. Пушкина, 94', '+79184572398', FALSE, TRUE);


INSERT INTO order_statuses (code, title) VALUES
('cancelled', 'Отменена'),
('active', 'Открыта'),
('closed', 'Закрыта');

INSERT INTO employee_positions (title, code) VALUES
('Генеральный директор', 'CEO'),
('Исполнительный директор', 'COO'),
('Финансовый директор', 'CFO'),
('Технический директор', 'CTO'),
('Руководитель отдела продаж', 'SALES_HEAD'),
('Менеджер по продажам', 'SALES_MGR'),
('Младший менеджер по продажам', 'JUNIOR_SALES'),
('Бухгалтер', 'ACCOUNTANT'),
('Менеджер по закупкам', 'PURCHASE_MGR'),
('Логист', 'LOGISTICIAN'),
('Складской работник', 'WAREHOUSE'),
('Менеджер по персоналу', 'HR_MGR'),
('Системный администратор', 'SYS_ADMIN'),
('Оператор колл-центра', 'CALL_OPERATOR'),
('Водитель-экспедитор', 'DRIVER');

insert into employee_roles(code) values
('user'),
('admin');

INSERT INTO employees (first_name, last_name, family_name, email, phone, address, position_id, login, role_id) VALUES
('Иван', 'Иванов', 'Иванович', 'ivanov@company.ru', '+7(901)123-45-67', 'г. Москва, ул. Ленина, д. 10, кв. 5', 1, 'ivanov', 
    (select id from employee_roles er where er.code = 'user')
),
('Петр', 'Петров', 'Петрович', 'petrov@company.ru', '+7(902)234-56-78', 'г. Москва, ул. Гагарина, д. 25, кв. 12', 2, 'petrov',
    (select id from employee_roles er where er.code = 'user')
),
('Сергей', 'Сидоров', 'Александрович', 'sidorov@company.ru', '+7(903)345-67-89', 'г. Москва, ул. Пушкина, д. 7, кв. 3', 3, 'sidorov',
    (select id from employee_roles er where er.code = 'user')
),
('Анна', 'Смирнова', 'Викторовна', 'smirnova@company.ru', '+7(904)456-78-90', 'г. Москва, ул. Тверская, д. 15, кв. 8', 4, 'smirnova',
    (select id from employee_roles er where er.code = 'user')
),
('Елена', 'Козлова', 'Дмитриевна', 'kozlova@company.ru', '+7(905)567-89-01', 'г. Москва, ул. Арбат, д. 30, кв. 45', 5, 'kozlova',
    (select id from employee_roles er where er.code = 'user')
),
('Дмитрий', 'Морозов', 'Сергеевич', 'morozov@company.ru', '+7(906)678-90-12', 'г. Москва, ул. Новый Арбат, д. 12, кв. 67', 6, 'morozov',
    (select id from employee_roles er where er.code = 'user')
),
('Ольга', 'Волкова', 'Андреевна', 'volkova@company.ru', '+7(907)789-01-23', 'г. Москва, ул. Красная Пресня, д. 8, кв. 23', 7, 'volkova',
    (select id from employee_roles er where er.code = 'user')
),
('Алексей', 'Соколов', 'Игоревич', 'sokolov@company.ru', '+7(908)890-12-34', 'г. Москва, ул. Кутузовский пр., д. 45, кв. 89', 8, 'sokolov',
    (select id from employee_roles er where er.code = 'user')
),
('Татьяна', 'Михайлова', 'Алексеевна', 'mihailova@company.ru', '+7(909)901-23-45', 'г. Москва, ул. Профсоюзная, д. 56, кв. 34', 9, 'mihailova',
    (select id from employee_roles er where er.code = 'user')
),
('Николай', 'Федоров', 'Владимирович', 'fedorov@company.ru', '+7(910)012-34-56', 'г. Москва, ул. Ленинградский пр., д. 78, кв. 56', 10, 'fedorov',
    (select id from employee_roles er where er.code = 'user')
),
('Мария', 'Андреева', 'Сергеевна', 'andreeva@company.ru', '+7(911)123-45-67', 'г. Москва, ул. Мичуринский пр., д. 90, кв. 12', 6, 'andreeva',
    (select id from employee_roles er where er.code = 'user')
),
('Андрей', 'Николаев', 'Павлович', 'nikolaev@company.ru', '+7(912)234-56-78', 'г. Москва, ул. Вернадского, д. 34, кв. 78', 6, 'nikolaev',
    (select id from employee_roles er where er.code = 'user')
),
('Екатерина', 'Морозова', 'Денисовна', 'morozova@company.ru', '+7(913)345-67-89', 'г. Москва, ул. Лобачевского, д. 23, кв. 45', 11, 'morozova',
    (select id from employee_roles er where er.code = 'user')
),
('Владимир', 'Зайцев', 'Викторович', 'zaitsev@company.ru', '+7(914)456-78-90', 'г. Москва, ул. Удальцова, д. 67, кв. 23', 12, 'zaitsev',
    (select id from employee_roles er where er.code = 'user')
),
('Наталья', 'Павлова', 'Ильинична', 'pavlova@company.ru', '+7(915)567-89-01', 'г. Москва, ул. Мосфильмовская, д. 45, кв. 67', 13, 'pavlova',
    (select id from employee_roles er where er.code = 'user')
),
('Михаил', 'Григорьев', 'Анатольевич', 'grigoriev@company.ru', '+7(916)678-90-12', 'г. Москва, ул. Строителей, д. 89, кв. 34', 14, 'grigoriev',
    (select id from employee_roles er where er.code = 'user')
),
('Юлия', 'Тарасова', 'Максимовна', 'tarasova@company.ru', '+7(917)789-01-23', 'г. Москва, ул. Вавилова, д. 12, кв. 56', 15, 'tarasova',
    (select id from employee_roles er where er.code = 'user')
),
('Админ', 'Админ', 'Админ', 'admin@company.ru', '+7(777)777-77-7', 'г. Москва, ул. Вавилова, д. 12, кв. 56', 1, 'admin',
    (select id from employee_roles er where er.code = 'admin')
);

insert into units_of_measures (code) values 
('шт');

insert into units_of_measures (code) values 
('кг');

insert into products ("name", code, unit_of_measure_id) values 
('Кефир 2,5% 900г.', 'Kefir_1', (select u.id from units_of_measures u where u.code = 'шт')),
('Кефир 3,2% 900г.', 'Kefir_2', (select u.id from units_of_measures u where u.code = 'шт')),
('Молоко 2,5% 900г.', 'Milk_1', (select u.id from units_of_measures u where u.code = 'шт')),
('Молоко 3,2% 900г.', 'Milk_2', (select u.id from units_of_measures u where u.code = 'шт')),
('Сметана классическая 15% 540г.', 'Smetana_1', (select u.id from units_of_measures u where u.code = 'шт')),
('Сметана классическая 20% 540г.', 'Smetana_2', (select u.id from units_of_measures u where u.code = 'шт'));

update products
set default_price = 80.00
where id = (select id from products p1 where p1.code = 'Kefir_1');

update products
set default_price = 82.00
where id = (select id from products p1 where p1.code = 'Kefir_2');

update products
set default_price = 70.00
where id = (select id from products p1 where p1.code = 'Milk_1');

update products
set default_price = 76.00
where id = (select id from products p1 where p1.code = 'Milk_2');

update products
set default_price = 89.00
where id = (select id from products p1 where p1.code = 'Smetana_1');

update products
set default_price = 92.00
where id = (select id from products p1 where p1.code = 'Smetana_2');

insert into materials ("name", unit_of_measure_id, "cost") values 
('Закваска сметанная', (select u.id from units_of_measures u where u.code = 'кг'), 4500),
('Молоко нормализованное', (select u.id from units_of_measures u where u.code = 'кг'), 3400);

update materials
set cost = 45
where name = 'Закваска сметанная';

update materials
set cost = 34
where name = 'Молоко нормализованное';

insert into bill_of_material (product_id, material_id, quantity) values
((select id from products p where p.code = 'Smetana_1'), (select id from materials m where m.name = 'Закваска сметанная'), 0.07),
((select id from products p where p.code = 'Smetana_1'), (select id from materials m where m.name = 'Молоко нормализованное'), 0.9);

insert into bill_of_material (product_id, material_id, quantity) values
((select id from products p where p.code = 'Kefir_1'), (select id from materials m where m.name = 'Закваска сметанная'), 0.1),
((select id from products p where p.code = 'Kefir_2'), (select id from materials m where m.name = 'Закваска сметанная'), 0.1),
((select id from products p where p.code = 'Milk_1'), (select id from materials m where m.name = 'Молоко нормализованное'), 0.1);

start transaction;

WITH new_order AS (
    INSERT INTO orders (date, customer_id, status_id, manager_id) VALUES
    (
        NOW(),
        (select id from customers c where c.name = 'ООО "Ассоль"'),
        (select id from order_statuses os where os.code = 'active'),
        (select e.id from employees e inner join employee_positions ep on e.position_id = ep.id where ep.code = 'SALES_MGR' limit 1)
    )
    RETURNING id
)
INSERT INTO order_items (order_id, product_id, quantity, price_at_sale) VALUES
((SELECT id FROM new_order), (select p.id from products p where p.code = 'Kefir_1'), 12, 80.00),
((SELECT id FROM new_order), (select p.id from products p where p.code = 'Kefir_2'), 9, 82.00),
((SELECT id FROM new_order), (select p.id from products p where p.code = 'Milk_1'), 10, 79.00);

end transaction;

-- Пунтк 2

select 
	o.id,
	oi.quantity,
	oi.price_at_sale,
	oi.price_at_sale * oi.quantity as total, -- конечна цена
	bom2.quantity * m."cost" * oi.quantity as cost_price, -- себестоимость
	(oi.price_at_sale * oi.quantity) - (bom2.quantity * m."cost" * oi.quantity) as net_income -- чистая прибыль 
from orders o
inner join order_items oi on oi.order_id = o.id
inner join products p on product_id = p.id
inner join bill_of_material bom2 on bom2.product_id = p.id
inner join materials m on bom2.material_id = m.id
where 
	o.id = $1
	


