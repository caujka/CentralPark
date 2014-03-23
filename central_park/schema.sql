DROP TABLE IF EXISTS Payments;
CREATE TABLE Payments (
id integer primary key autoincrement,
car_number text,
time texttime,
cost integer,
leave_before text,
id_place integer,
rate integer
);

DROP TABLE IF EXISTS Parking_Lots;
CREATE TABLE Parking_Lots (
id_lot integer primary key autoincrement,
name text,
adress text
);

INSERT INTO Parking_Lots VALUES (0, 'parking №1', 'Pasternaka str.');
INSERT INTO Parking_Lots VALUES (1, 'parking №2', 'Fedkivycha str.');
INSERT INTO Parking_Lots VALUES (2, 'parking №3', 'V. Velykogo str.');

DROP TABLE IF EXISTS Parking_Places;
CREATE TABLE Parking_Places (
id_lot integer,
id_place integer primary key autoincrement,
place_category integer,
place_name text,
FOREIGN KEY(id_lot) REFERENCES Parking_Lots(id_lot)
);

INSERT INTO Parking_Places VALUES (0, 0, 0, 'some name');
INSERT INTO Parking_Places VALUES (0, 1, 1, 'some name');
INSERT INTO Parking_Places VALUES (0, 2, 0, 'some name');
INSERT INTO Parking_Places VALUES (1, 3, 1, 'some name');
INSERT INTO Parking_Places VALUES (1, 4, 1, 'some name');
INSERT INTO Parking_Places VALUES (1, 5, 0, 'some name');
INSERT INTO Parking_Places VALUES (2, 6, 0, 'some name');
INSERT INTO Parking_Places VALUES (2, 7, 0, 'some name');
INSERT INTO Parking_Places VALUES (2, 8, 1, 'some name');

DROP TABLE IF EXISTS Lot_Statistics;
CREATE TABLE Lot_Statistics (
id integer primary key,
id_lot integer,
id_rate integer,
FOREIGN KEY(id_lot) REFERENCES Parking_Lots(id_lot)
);

DROP TABLE IF EXISTS Rate_Statistics;
CREATE TABLE Rate_Statistics (
id integer primary key autoincrement,
start text,
finish text,
id_rate integer
);

DROP TABLE IF EXISTS Rates;
CREATE TABLE Rates (
id_rate integer primary key autoincrement,
hour_0 integer,
hour_1 integer,
hour_2 integer,
hour_3 integer,
hour_4 integer,
hour_5 integer,
hour_6 integer,
hour_7 integer,
hour_8 integer,
hour_9 integer,
hour_10 integer,
hour_11 integer,
hour_12 integer,
hour_13 integer,
hour_14 integer,
hour_15 integer,
hour_16 integer,
hour_17 integer,
hour_18 integer,
hour_19 integer,
hour_20 integer,
hour_21 integer,
hour_22 integer,
hour_23 integer,
FOREIGN KEY(id_rate) REFERENCES Rate_Statistics(id_rate)
);

