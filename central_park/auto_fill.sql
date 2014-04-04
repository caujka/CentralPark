DELETE FROM ParkingLot;

INSERT INTO ParkingLot VALUES (0, 'parking №1', 'Pasternaka str.');
INSERT INTO ParkingLot VALUES (1, 'parking №2', 'Fedkivycha str.');
INSERT INTO ParkingLot VALUES (2, 'parking №3', 'V. Velykogo str.');

DELETE FROM ParkingPlace;

INSERT INTO ParkingPlace VALUES (0, 'name01', 0, 0);
INSERT INTO ParkingPlace VALUES (1, 'name02', 0, 0);
INSERT INTO ParkingPlace VALUES (2, 'name03', 1, 0);
INSERT INTO ParkingPlace VALUES (3, 'name11', 1, 1);
INSERT INTO ParkingPlace VALUES (4, 'name12', 1, 1);
INSERT INTO ParkingPlace VALUES (5, 'name13', 0, 1);
INSERT INTO ParkingPlace VALUES (6, 'name21', 0, 2);
INSERT INTO ParkingPlace VALUES (7, 'name22', 1, 2);
INSERT INTO ParkingPlace VALUES (8, 'name23', 0, 2);

DELETE FROM PriceHistory;

INSERT INTO PriceHistory VALUES (0, 0, '2013-10-07 08:23:19.120', 30);
INSERT INTO PriceHistory VALUES (1, 1, '2013-112-07 12:23:19.120', 25);
INSERT INTO PriceHistory VALUES (2, 3, '2013-11-07 23:23:19.120', 35);
