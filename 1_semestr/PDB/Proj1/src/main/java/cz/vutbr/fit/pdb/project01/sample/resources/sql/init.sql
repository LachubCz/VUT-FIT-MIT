DROP TABLE objednavka_doprovodne_akce;
DROP TABLE objednavka_zajezdu;
DROP TABLE objednavka_uzivatel;
DROP TABLE objednavka;
DROP TABLE lyzarsky_zajezd;
DROP TABLE doprovodna_akce;
DROP TABLE hotel;
DROP TABLE klient;

DROP TABLE ImageIdentity;
DROP TABLE ImageTour;
DROP TABLE ImageHotel;
DROP TABLE ImageAction;

DROP SEQUENCE klient_seq;
DROP SEQUENCE hotel_seq;
DROP SEQUENCE doprovodna_akce_seq;
DROP SEQUENCE lyzarsky_zajezd_seq;
DROP SEQUENCE objednavka_uzivatel_seq;
DROP SEQUENCE objednavka_seq;
DROP SEQUENCE objednavka_zajezdu_seq;
DROP SEQUENCE objednavka_doprovodne_akce_seq;

CREATE SEQUENCE klient_seq START WITH 1 INCREMENT BY 1 NOCYCLE;
CREATE SEQUENCE hotel_seq START WITH 1 INCREMENT BY 1 NOCYCLE;
CREATE SEQUENCE doprovodna_akce_seq START WITH 1 INCREMENT BY 1 NOCYCLE;
CREATE SEQUENCE lyzarsky_zajezd_seq START WITH 1 INCREMENT BY 1 NOCYCLE;
CREATE SEQUENCE objednavka_uzivatel_seq START WITH 1 INCREMENT BY 1 NOCYCLE;
CREATE SEQUENCE objednavka_seq START WITH 1 INCREMENT BY 1 NOCYCLE;
CREATE SEQUENCE objednavka_zajezdu_seq START WITH 1 INCREMENT BY 1 NOCYCLE;
CREATE SEQUENCE objednavka_doprovodne_akce_seq START WITH 1 INCREMENT BY 1 NOCYCLE;

CREATE TABLE ImageIdentity
(
	id NUMBER NOT NULL,
	picture ORDSYS.ORDIMAGE,
	picture_si ORDSYS.SI_STILLIMAGE,
	picture_ac ORDSYS.SI_AVERAGECOLOR,
	picture_ch ORDSYS.SI_COLORHISTOGRAM,
	picture_pc ORDSYS.SI_POSITIONALCOLOR,
	picture_tx ORDSYS.SI_TEXTURE
);

CREATE TABLE ImageTour
(
	id NUMBER NOT NULL,
	picture ORDSYS.ORDIMAGE,
	picture_si ORDSYS.SI_STILLIMAGE,
	picture_ac ORDSYS.SI_AVERAGECOLOR,
	picture_ch ORDSYS.SI_COLORHISTOGRAM,
	picture_pc ORDSYS.SI_POSITIONALCOLOR,
	picture_tx ORDSYS.SI_TEXTURE
);

CREATE TABLE ImageHotel
(
	id NUMBER NOT NULL,
	picture ORDSYS.ORDIMAGE,
	picture_si ORDSYS.SI_STILLIMAGE,
	picture_ac ORDSYS.SI_AVERAGECOLOR,
	picture_ch ORDSYS.SI_COLORHISTOGRAM,
	picture_pc ORDSYS.SI_POSITIONALCOLOR,
	picture_tx ORDSYS.SI_TEXTURE
);

CREATE TABLE ImageAction
(
	id NUMBER NOT NULL,
	picture ORDSYS.ORDIMAGE,
	picture_si ORDSYS.SI_STILLIMAGE,
	picture_ac ORDSYS.SI_AVERAGECOLOR,
	picture_ch ORDSYS.SI_COLORHISTOGRAM,
	picture_pc ORDSYS.SI_POSITIONALCOLOR,
	picture_tx ORDSYS.SI_TEXTURE
);

CREATE TABLE klient
(
	login VARCHAR2(30),
	heslo VARCHAR2(30),
	jmeno VARCHAR2(30),
	prijmeni VARCHAR2(30),
	pohlavi CHAR,
	rodne_cislo NUMBER(10),
	datum_narozeni VARCHAR2(10),
	telefon NUMBER(14),
	email VARCHAR2(40),
	adresa VARCHAR2(100),
  ID_user INT,
  begining TIMESTAMP,
  ending TIMESTAMP,
	CONSTRAINT PK_klient PRIMARY KEY(ID_user)
);

CREATE TABLE hotel
(
	ID_hotelu INT,
	nazev VARCHAR2(30),
	pocet_hvezdicek NUMBER(1),
	CONSTRAINT PK_hotel PRIMARY KEY(ID_hotelu)
);

CREATE TABLE doprovodna_akce
(
	ID_doprovodne_akce INT,
	typ_akce VARCHAR2(50),
	pocet_osob NUMBER(3),
	od VARCHAR2(10),
	do VARCHAR2(10),
	CONSTRAINT PK_doprovodna_akce PRIMARY KEY(ID_doprovodne_akce)
);

CREATE TABLE lyzarsky_zajezd
(
	ID_zajezdu INT,
	zeme VARCHAR2(50),
	lokace VARCHAR2(50),
	stredisko VARCHAR2(50),
	od VARCHAR2(10),
	do VARCHAR2(10),
	ID_hotelu NUMBER(6),
	CONSTRAINT PK_lyzarsky_zajezd PRIMARY KEY(ID_zajezdu),
	CONSTRAINT FK_lyzarsky_zajezd FOREIGN KEY(ID_hotelu) REFERENCES hotel(ID_hotelu) ON DELETE CASCADE
);

CREATE TABLE objednavka
(
	ID_objednavky INT,
  zrusena CHAR,
	termin VARCHAR2(10),
  begining TIMESTAMP,
  ending TIMESTAMP,
	CONSTRAINT PK_objednavka PRIMARY KEY(ID_objednavky)
);

CREATE TABLE objednavka_uzivatel
(
  ID_objednavka_uzivatel INT,
  ID_user INT,
  ID_objednavky INT,
  begining TIMESTAMP,
	ending TIMESTAMP,
  CONSTRAINT PK_objednavka_uzivatel PRIMARY KEY(ID_objednavka_uzivatel),
	CONSTRAINT FK_objednavka_uzivatel FOREIGN KEY(ID_user) REFERENCES klient(ID_user) ON DELETE CASCADE,
  CONSTRAINT FK2_objednavka_uzivatel FOREIGN KEY(ID_objednavky) REFERENCES objednavka(ID_objednavky) ON DELETE CASCADE
);

CREATE TABLE objednavka_zajezdu
(
	ID_objednavky_zajezdu INT,
	ID_objednavky NUMBER(6),
	ID_zajezdu NUMBER(6),
	strava CHAR,
	doprava CHAR,
	pocet_osob NUMBER(4),
  begining TIMESTAMP,
  ending TIMESTAMP, 
	CONSTRAINT PK_objednavka_zajezdu PRIMARY KEY(ID_objednavky_zajezdu),
	CONSTRAINT FK_objednavka_zajezdu FOREIGN KEY(ID_objednavky) REFERENCES objednavka(ID_objednavky) ON DELETE CASCADE,
	CONSTRAINT FK2_objednavka_zajezdu FOREIGN KEY(ID_zajezdu) REFERENCES lyzarsky_zajezd(ID_zajezdu) ON DELETE CASCADE
);

CREATE TABLE objednavka_doprovodne_akce
(
	ID_objednavky_doprovodne_akce INT,
	ID_objednavky_zajezdu NUMBER(6),
	ID_doprovodne_akce NUMBER(6),
  begining TIMESTAMP,
  ending TIMESTAMP,
	CONSTRAINT PK_objednavka_doprovodne_akce PRIMARY KEY(ID_objednavky_doprovodne_akce),
	CONSTRAINT FK_objednavka_doprovodne_akce FOREIGN KEY(ID_objednavky_zajezdu) REFERENCES objednavka_zajezdu(ID_objednavky_zajezdu) ON DELETE CASCADE,
	CONSTRAINT FK2_objednavka_doprovodne_akce FOREIGN KEY(ID_doprovodne_akce) REFERENCES doprovodna_akce(ID_doprovodne_akce) ON DELETE CASCADE
);

GRANT SELECT, UPDATE, DELETE, INSERT, ON COMMIT REFRESH ON objednavka_doprovodne_akce TO XBUCHA02;
GRANT SELECT, UPDATE, DELETE, INSERT, ON COMMIT REFRESH ON objednavka_zajezdu TO XBUCHA02;
GRANT SELECT, UPDATE, DELETE, INSERT, ON COMMIT REFRESH ON objednavka TO XBUCHA02;
GRANT SELECT, UPDATE, DELETE, INSERT, ON COMMIT REFRESH ON lyzarsky_zajezd TO XBUCHA02;
GRANT SELECT, UPDATE, DELETE, INSERT, ON COMMIT REFRESH ON doprovodna_akce TO XBUCHA02;
GRANT SELECT, UPDATE, DELETE, INSERT, ON COMMIT REFRESH ON hotel TO XBUCHA02;
GRANT SELECT, UPDATE, DELETE, INSERT, ON COMMIT REFRESH ON klient TO XBUCHA02;

GRANT SELECT, UPDATE, DELETE, INSERT, ON COMMIT REFRESH ON objednavka_doprovodne_akce TO XBARAN16;
GRANT SELECT, UPDATE, DELETE, INSERT, ON COMMIT REFRESH ON objednavka_zajezdu TO XBARAN16;
GRANT SELECT, UPDATE, DELETE, INSERT, ON COMMIT REFRESH ON objednavka TO XBARAN16;
GRANT SELECT, UPDATE, DELETE, INSERT, ON COMMIT REFRESH ON lyzarsky_zajezd TO XBARAN16;
GRANT SELECT, UPDATE, DELETE, INSERT, ON COMMIT REFRESH ON doprovodna_akce TO XBARAN16;
GRANT SELECT, UPDATE, DELETE, INSERT, ON COMMIT REFRESH ON hotel TO XBARAN16;
GRANT SELECT, UPDATE, DELETE, INSERT, ON COMMIT REFRESH ON klient TO XBARAN16;

INSERT INTO klient (ID_user, login, heslo, jmeno, prijmeni, pohlavi, rodne_cislo, datum_narozeni, telefon, email, adresa, begining) VALUES (1, 'Admin', 'Admin', 'Bill', 'Gates', 'M', 5510283391, '28-10-1955', 969010270, 'billTheKing@gmail.com', 'Seattle, Redmond, Park street, 911', TO_DATE('01-01-2018 00:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO klient (ID_user, login, heslo, jmeno, prijmeni, pohlavi, rodne_cislo, datum_narozeni, telefon, email, adresa, begining) VALUES (2, 'podhorka', 'podhorka42', 'Karel', 'Podhorka', 'M', 8612118725, '11-12-1986', 787593288, 'losCarlos42@gmail.com', 'Brno, Bystrc, Husova, 983', TO_DATE('01-01-2018 00:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO klient (ID_user, login, heslo, jmeno, prijmeni, pohlavi, rodne_cislo, datum_narozeni, telefon, email, adresa, begining) VALUES (3, 'mauricce', 'domingo', 'Dominik', 'Mauritz', 'M', 6701103125, '01-10-1967', 984112776, 'mauricceSilent@gmail.com', 'Prague, Praha 6, Pod jezerem, 1204', TO_DATE('01-01-2018 00:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO klient (ID_user, login, heslo, jmeno, prijmeni, pohlavi, rodne_cislo, datum_narozeni, telefon, email, adresa, begining) VALUES (4, 'bundis', '12345', 'Al', 'Bundi', 'M', 5302235597, '23-02-1953', 908888620, 'alBundi@gmail.com', 'Los Angeles, Glendale, Oak street, 339', TO_DATE('01-01-2018 00:00:00', 'DD-MM-YYYY HH24:MI:SS'));

INSERT INTO hotel (ID_hotelu, nazev, pocet_hvezdicek) VALUES (1, 'Hotel Grand', 4);
INSERT INTO hotel (ID_hotelu, nazev, pocet_hvezdicek) VALUES (2, 'Hotel Artemis', 3);
INSERT INTO hotel (ID_hotelu, nazev, pocet_hvezdicek) VALUES (3, 'Hotel California', 4);
INSERT INTO hotel (ID_hotelu, nazev, pocet_hvezdicek) VALUES (4, 'Hotel Excelsior', 4);
INSERT INTO hotel (ID_hotelu, nazev, pocet_hvezdicek) VALUES (5, 'Hotel Plaza', 4);
INSERT INTO hotel (ID_hotelu, nazev, pocet_hvezdicek) VALUES (6, 'King of hotels', 2);
INSERT INTO hotel (ID_hotelu, nazev, pocet_hvezdicek) VALUES (7, 'Hotel Panda', 5);
INSERT INTO hotel (ID_hotelu, nazev, pocet_hvezdicek) VALUES (8, 'Hotel Budget', 1);
INSERT INTO hotel (ID_hotelu, nazev, pocet_hvezdicek) VALUES (9, 'Ski paradise', 5);
INSERT INTO hotel (ID_hotelu, nazev, pocet_hvezdicek) VALUES (10, 'Hotel Vienna', 4);
INSERT INTO hotel (ID_hotelu, nazev, pocet_hvezdicek) VALUES (11, 'Hotel Europa', 3);
INSERT INTO hotel (ID_hotelu, nazev, pocet_hvezdicek) VALUES (12, 'Oak hotel', 5);

INSERT INTO doprovodna_akce (ID_doprovodne_akce, typ_akce, pocet_osob, od, do) VALUES (1, 'Slavnosti u grilu', 50, '15-02-2019', '30-11-2019');
INSERT INTO doprovodna_akce (ID_doprovodne_akce, typ_akce, pocet_osob, od, do) VALUES (2, 'Den cyklistiky', 6, '01-04-2019', '30-08-2019');
INSERT INTO doprovodna_akce (ID_doprovodne_akce, typ_akce, pocet_osob, od, do) VALUES (3, 'Silvestr a oslava', 30, '30-12-2019', '31-12-2019');
INSERT INTO doprovodna_akce (ID_doprovodne_akce, typ_akce, pocet_osob, od, do) VALUES (4, 'Slalom pro jednotlivce', 1, '01-10-2019', '14-03-2019');
INSERT INTO doprovodna_akce (ID_doprovodne_akce, typ_akce, pocet_osob, od, do) VALUES (5, 'Hiking pro rodinu', 10, '01-05-2019', '30-08-2019');
INSERT INTO doprovodna_akce (ID_doprovodne_akce, typ_akce, pocet_osob, od, do) VALUES (6, 'Ski maraton', 4, '01-02-2019', '31-12-2019');
INSERT INTO doprovodna_akce (ID_doprovodne_akce, typ_akce, pocet_osob, od, do) VALUES (7, 'Seskok z nebes', 2, '01-03-2019', '30-10-2019');
INSERT INTO doprovodna_akce (ID_doprovodne_akce, typ_akce, pocet_osob, od, do) VALUES (8, 'Plavba v mrazu', 5, '01-10-2019', '31-12-2019');
INSERT INTO doprovodna_akce (ID_doprovodne_akce, typ_akce, pocet_osob, od, do) VALUES (9, 'Ski jumping', 1, '10-02-2019', '16-12-2019');
INSERT INTO doprovodna_akce (ID_doprovodne_akce, typ_akce, pocet_osob, od, do) VALUES (10, 'Zima a zorbing', 4, '01-02-2019', '10-12-2019');
INSERT INTO doprovodna_akce (ID_doprovodne_akce, typ_akce, pocet_osob, od, do) VALUES (11, 'Sledge akce', 10, '15-01-2019', '20-12-2019');

INSERT INTO lyzarsky_zajezd (ID_zajezdu, zeme, lokace, stredisko, od, do, ID_hotelu) VALUES (1, 'Rakousko', 'Korutany', 'Mallnitz', '02-01-2019', '05-01-2019', 1);
INSERT INTO lyzarsky_zajezd (ID_zajezdu, zeme, lokace, stredisko, od, do, ID_hotelu) VALUES (2, 'Rakousko', 'Korutany', 'Mallnitz', '02-01-2019', '05-01-2019', 2);
INSERT INTO lyzarsky_zajezd (ID_zajezdu, zeme, lokace, stredisko, od, do, ID_hotelu) VALUES (3, 'Rakousko', 'Korutany', 'Mallnitz', '02-01-2019', '05-01-2019', 3);
INSERT INTO lyzarsky_zajezd (ID_zajezdu, zeme, lokace, stredisko, od, do, ID_hotelu) VALUES (4, 'Rakousko', 'Salcbursko', 'Abtenau', '12-02-2019', '16-02-2019', 4);
INSERT INTO lyzarsky_zajezd (ID_zajezdu, zeme, lokace, stredisko, od, do, ID_hotelu) VALUES (5, 'Rakousko', 'Tyrolsko', 'Telfes im Stubaital', '02-03-2019', '07-03-2019', 5);
INSERT INTO lyzarsky_zajezd (ID_zajezdu, zeme, lokace, stredisko, od, do, ID_hotelu) VALUES (6, 'Rakousko', 'Tyrolsko', 'Telfes im Stubaital', '02-03-2019', '07-03-2019', 6);
INSERT INTO lyzarsky_zajezd (ID_zajezdu, zeme, lokace, stredisko, od, do, ID_hotelu) VALUES (7, 'Rakousko', 'Salcbursko', 'Salzburg', '04-12-2019', '13-12-2019', 7);
INSERT INTO lyzarsky_zajezd (ID_zajezdu, zeme, lokace, stredisko, od, do, ID_hotelu) VALUES (8, 'Rakousko', 'Salcbursko', 'Salzburg', '04-12-2019', '13-12-2019', 8);
INSERT INTO lyzarsky_zajezd (ID_zajezdu, zeme, lokace, stredisko, od, do, ID_hotelu) VALUES (9, 'Rakousko', 'Korutany', 'Bad Kleinkirchheim', '19-02-2019', '24-02-2019', 9);
INSERT INTO lyzarsky_zajezd (ID_zajezdu, zeme, lokace, stredisko, od, do, ID_hotelu) VALUES (10, 'Rakousko', 'Korutany', 'Bad Kleinkirchheim', '19-02-2019', '24-02-2019', 10);
INSERT INTO lyzarsky_zajezd (ID_zajezdu, zeme, lokace, stredisko, od, do, ID_hotelu) VALUES (11, 'Francie', 'Les Arcs', 'Chalet Altitude', '03-01-2019', '17-01-2019', 11);
INSERT INTO lyzarsky_zajezd (ID_zajezdu, zeme, lokace, stredisko, od, do, ID_hotelu) VALUES (12, 'Rakousko', 'Burgenland', 'Lutzmannsburg', '01-02-2019', '12-02-2019', 12);

INSERT INTO objednavka (ID_objednavky, zrusena, termin, begining) VALUES (1, 'N', '03-12-2018', TO_DATE('03-12-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO objednavka (ID_objednavky, zrusena, termin, begining) VALUES (2, 'N', '14-11-2018', TO_DATE('14-11-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));

INSERT INTO objednavka_uzivatel (ID_objednavka_uzivatel, ID_user, ID_objednavky, begining) VALUES (1, 3, 1, TO_DATE('03-12-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO objednavka_uzivatel (ID_objednavka_uzivatel, ID_user, ID_objednavky, begining) VALUES (2, 2, 2, TO_DATE('14-11-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));

INSERT INTO objednavka_zajezdu (ID_objednavky_zajezdu, ID_objednavky, ID_zajezdu, strava, doprava, pocet_osob, begining) VALUES (1, 1, 2, 'Y', 'N', 10, TO_DATE('03-12-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO objednavka_zajezdu (ID_objednavky_zajezdu, ID_objednavky, ID_zajezdu, strava, doprava, pocet_osob, begining) VALUES (2, 1, 4, 'N', 'N', 7, TO_DATE('03-12-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO objednavka_zajezdu (ID_objednavky_zajezdu, ID_objednavky, ID_zajezdu, strava, doprava, pocet_osob, begining) VALUES (3, 1, 7, 'N', 'Y', 5, TO_DATE('03-12-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO objednavka_zajezdu (ID_objednavky_zajezdu, ID_objednavky, ID_zajezdu, strava, doprava, pocet_osob, begining) VALUES (4, 2, 6, 'N', 'Y', 10, TO_DATE('14-11-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO objednavka_zajezdu (ID_objednavky_zajezdu, ID_objednavky, ID_zajezdu, strava, doprava, pocet_osob, begining) VALUES (5, 2, 2, 'Y', 'Y', 3, TO_DATE('14-11-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO objednavka_zajezdu (ID_objednavky_zajezdu, ID_objednavky, ID_zajezdu, strava, doprava, pocet_osob, begining) VALUES (6, 2, 11, 'N', 'N', 5, TO_DATE('14-11-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));

INSERT INTO objednavka_doprovodne_akce (ID_objednavky_doprovodne_akce, ID_objednavky_zajezdu, ID_doprovodne_akce, begining) VALUES (1, 1, 3, TO_DATE('03-12-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO objednavka_doprovodne_akce (ID_objednavky_doprovodne_akce, ID_objednavky_zajezdu, ID_doprovodne_akce, begining) VALUES (2, 1, 5, TO_DATE('03-12-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO objednavka_doprovodne_akce (ID_objednavky_doprovodne_akce, ID_objednavky_zajezdu, ID_doprovodne_akce, begining) VALUES (3, 2, 7, TO_DATE('03-12-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO objednavka_doprovodne_akce (ID_objednavky_doprovodne_akce, ID_objednavky_zajezdu, ID_doprovodne_akce, begining) VALUES (4, 2, 1, TO_DATE('03-12-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO objednavka_doprovodne_akce (ID_objednavky_doprovodne_akce, ID_objednavky_zajezdu, ID_doprovodne_akce, begining) VALUES (5, 2, 2, TO_DATE('03-12-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO objednavka_doprovodne_akce (ID_objednavky_doprovodne_akce, ID_objednavky_zajezdu, ID_doprovodne_akce, begining) VALUES (6, 4, 2, TO_DATE('14-11-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO objednavka_doprovodne_akce (ID_objednavky_doprovodne_akce, ID_objednavky_zajezdu, ID_doprovodne_akce, begining) VALUES (7, 6, 2, TO_DATE('14-11-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO objednavka_doprovodne_akce (ID_objednavky_doprovodne_akce, ID_objednavky_zajezdu, ID_doprovodne_akce, begining) VALUES (8, 6, 3, TO_DATE('14-11-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO objednavka_doprovodne_akce (ID_objednavky_doprovodne_akce, ID_objednavky_zajezdu, ID_doprovodne_akce, begining) VALUES (9, 6, 5, TO_DATE('14-11-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));
INSERT INTO objednavka_doprovodne_akce (ID_objednavky_doprovodne_akce, ID_objednavky_zajezdu, ID_doprovodne_akce, begining) VALUES (10, 6, 9, TO_DATE('14-11-2018 12:00:00', 'DD-MM-YYYY HH24:MI:SS'));
