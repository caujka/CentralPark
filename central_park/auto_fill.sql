DELETE FROM ParkingPlace;

INSERT INTO ParkingPlace VALUES (0, 'name01', 0, "location", "address", 2);
INSERT INTO ParkingPlace VALUES (1, 'name02', 0, "location", "address", 3);
INSERT INTO ParkingPlace VALUES (2, 'name03', 1, "location", "address",1);
INSERT INTO ParkingPlace VALUES (3, 'name11', 1, "location", "address",2);
INSERT INTO ParkingPlace VALUES (4, 'name12', 1, "location", "address",3);
INSERT INTO ParkingPlace VALUES (5, 'name13', 0, "location", "address",1);
INSERT INTO ParkingPlace VALUES (6, 'name21', 0, "location", "address",2);
INSERT INTO ParkingPlace VALUES (7, 'name22', 1, "location", "address",1);
INSERT INTO ParkingPlace VALUES (8, 'name23', 0, "location", "address",2);

DELETE FROM PriceHistory;

INSERT INTO PriceHistory VALUES (0,'2013-10-07 08:23:19.120000',  '35;35;35;35;35;35;35;35;35;35;35;35;30;30;30;30;30;30;30;35;35;35;35;35',  0);
INSERT INTO PriceHistory VALUES (1,  '2013-11-07 12:23:19.120000', '35;35;35;35;35;35;35;35;35;35;35;35;30;30;30;30;30;30;30;35;35;35;35;35',1);
INSERT INTO PriceHistory VALUES (2,  '2013-11-07 23:23:19.120000', '35;35;35;35;35;35;35;35;35;35;35;35;30;30;30;30;30;30;30;35;35;35;35;35',2);
INSERT INTO PriceHistory VALUES (3, '2014-03-07 23:23:19.120000','5;5;5;5;5;5;15;15;15;15;15;15;10;10;10;10;10;10;10;15;15;15;15;15',  0);
INSERT INTO PriceHistory VALUES (4,  '2014-03-07 23:23:19.120000', '15;15;15;15;15;15;15;15;15;15;15;15;20;20;20;20;20;20;20;15;15;15;15;15',1);
INSERT INTO PriceHistory VALUES (5, '2014-03-07 23:23:19.120000', '25;25;25;25;25;25;35;35;35;35;35;35;30;30;30;30;30;30;30;25;25;25;25;25',  2);

DELETE FROM Payment;

INSERT INTO Payment VALUES (0, 'АТ0001СВ', '30','2014-04-07 08:20:19.120000', '2014-04-07 08:23:19.120000', 'string', '0', '0');
INSERT INTO Payment VALUES (1, 'АТ0002СВ', '40','2014-04-07 08:20:19.120000', '2014-04-07 09:23:19.120000', 'string', '1', '0');
INSERT INTO Payment VALUES (2, 'АТ0003СВ', '35','2014-04-06 09:20:19.120000', '2014-04-07 10:23:19.120000', 'string', '2', '0');
INSERT INTO Payment VALUES (3, 'АТ0004СВ', '10','2014-04-06 09:20:19.120000', '2014-04-07 11:23:19.120000', 'string','3', '1');
INSERT INTO Payment VALUES (4, 'АТ0005СВ', '10','2014-04-06 09:20:19.120000', '2014-04-07 12:23:19.120000', 'string','4', '1');
INSERT INTO Payment VALUES (5, 'АТ0006СВ', '11','2014-04-06 09:20:19.120000', '2014-04-07 13:23:19.120000', 'string','5', '1');
INSERT INTO Payment VALUES (6, 'АТ0007СВ', '15','2014-04-06 09:20:19.120000', '2014-04-07 14:23:19.120000', 'string','6', '2');
INSERT INTO Payment VALUES (7, 'АТ0008СВ', '80','2014-04-06 09:20:19.120000', '2014-04-07 09:23:19.120000', 'string','7', '2');
INSERT INTO Payment VALUES (8, 'АТ0009СВ', '20','2014-04-06 09:20:19.120000', '2014-04-07 08:23:19.120000', 'string', '8', '2');

INSERT INTO Payment VALUES (9, 'АТ0001СВ', '30','2014-04-07 15:20:19.120000', '2014-04-09 08:23:19.120000', 'string','0', '3');
INSERT INTO Payment VALUES (10, 'АТ0002СВ', '40','2014-04-07 15:20:19.120000', '2014-04-09 09:23:19.120000', 'string','1', '3');
INSERT INTO Payment VALUES (11, 'АТ0003СВ', '35','2014-04-07 15:20:19.120000', '2014-04-09 10:23:19.120000', 'string','2', '3');
INSERT INTO Payment VALUES (12, 'АТ0004СВ', '10','2014-04-07 15:20:19.120000', '2014-04-09 11:23:19.120000', 'string','3', '4');
INSERT INTO Payment VALUES (13, 'АТ0005СВ', '10','2014-04-07 15:20:19.120000', '2014-04-09 12:23:19.120000', 'string','4', '4');
INSERT INTO Payment VALUES (14, 'АТ0006СВ', '11','2014-04-07 15:20:19.120000', '2014-04-09 13:23:19.120000', 'string','5', '4');
INSERT INTO Payment VALUES (15, 'АТ0007СВ', '15','2014-04-07 15:20:19.120000', '2014-04-09 14:23:19.120000', 'string','6', '5');
INSERT INTO Payment VALUES (16, 'АТ0008СВ', '80','2014-04-07 15:20:19.120000', '2014-04-09 09:23:19.120000', 'string','7', '5');
INSERT INTO Payment VALUES (17, 'АТ0009СВ', '20','2014-04-07 15:20:19.120000', '2014-04-09 08:23:19.120000', 'string','8', '5');
