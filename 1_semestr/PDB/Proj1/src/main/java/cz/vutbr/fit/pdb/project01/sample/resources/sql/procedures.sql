CREATE OR REPLACE PROCEDURE PictureRotateLeft
    (img_id IN NUMBER)
IS
    obj ORDSYS.ORDImage;
BEGIN
    SELECT picture INTO obj FROM ImageIdentity
    WHERE id = img_id FOR UPDATE;

    obj.process('rotate=-90');

    UPDATE ImageIdentity SET picture = obj WHERE id = img_id;

    COMMIT;
END;
/

CREATE OR REPLACE PROCEDURE PictureRotateRight
    (img_id IN NUMBER)
IS
    obj ORDSYS.ORDImage;
BEGIN
    SELECT picture INTO obj FROM ImageIdentity
    WHERE id = img_id FOR UPDATE;

    obj.process('rotate=90');

    UPDATE ImageIdentity SET picture = obj WHERE id = img_id;

    COMMIT;
END;
/

CREATE OR REPLACE PROCEDURE PictureFlip
    (img_id IN NUMBER)
IS
    obj ORDSYS.ORDImage;
BEGIN
    SELECT picture INTO obj FROM ImageIdentity
    WHERE id = img_id FOR UPDATE;

    obj.process('flip');

    UPDATE ImageIdentity SET picture = obj WHERE id = img_id;

    COMMIT;
END;
/

CREATE OR REPLACE PROCEDURE PictureMirror
    (img_id IN NUMBER)
IS
    obj ORDSYS.ORDImage;
BEGIN
    SELECT picture INTO obj FROM ImageIdentity
    WHERE id = img_id FOR UPDATE;

    obj.process('mirror');

    UPDATE ImageIdentity SET picture = obj WHERE id = img_id;

    COMMIT;
END;
/

CREATE OR REPLACE PROCEDURE PictureContrastUp
    (img_id IN NUMBER)
IS
    obj ORDSYS.ORDImage;
BEGIN
    SELECT picture INTO obj FROM ImageIdentity
    WHERE id = img_id FOR UPDATE;

    obj.process('contrast 5');

    UPDATE ImageIdentity SET picture = obj WHERE id = img_id;

    COMMIT;
END;
/

CREATE OR REPLACE PROCEDURE PictureContrastDown
    (img_id IN NUMBER)
IS
    obj ORDSYS.ORDImage;
BEGIN
    SELECT picture INTO obj FROM ImageIdentity
    WHERE id = img_id FOR UPDATE;

    obj.process('contrast 20');

    UPDATE ImageIdentity SET picture = obj WHERE id = img_id;

    COMMIT;
END;
/

CREATE OR REPLACE PROCEDURE PictureGammaUp
    (img_id IN NUMBER)
IS
    obj ORDSYS.ORDImage;
BEGIN
    SELECT picture INTO obj FROM ImageIdentity
    WHERE id = img_id FOR UPDATE;

    obj.process('gamma 1.2');

    UPDATE ImageIdentity SET picture = obj WHERE id = img_id;

    COMMIT;
END;
/

CREATE OR REPLACE PROCEDURE PictureGammaDown
    (img_id IN NUMBER)
IS
    obj ORDSYS.ORDImage;
BEGIN
    SELECT picture INTO obj FROM ImageIdentity
    WHERE id = img_id FOR UPDATE;

    obj.process('gamma 0.8');

    UPDATE ImageIdentity SET picture = obj WHERE id = img_id;

    COMMIT;
END;
/

CREATE OR REPLACE TRIGGER auto_increment_klient BEFORE
INSERT ON klient
FOR EACH ROW
BEGIN
  SELECT klient_seq.nextval
  INTO :new.ID_user
  from dual;
END;
/

CREATE OR REPLACE TRIGGER auto_increment_hotel BEFORE
INSERT ON hotel
FOR EACH ROW
BEGIN
  SELECT hotel_seq.nextval
  INTO :new.ID_hotelu
  from dual;
END;
/

CREATE OR REPLACE TRIGGER auto_increment_doprovodna_akce BEFORE
INSERT ON doprovodna_akce
FOR EACH ROW
BEGIN
  SELECT doprovodna_akce_seq.nextval
  INTO :new.ID_doprovodne_akce
  from dual;
END;
/

CREATE OR REPLACE TRIGGER auto_increment_lyzarsky_zajezd BEFORE
INSERT ON lyzarsky_zajezd
FOR EACH ROW
BEGIN
  SELECT lyzarsky_zajezd_seq.nextval
  INTO :new.ID_zajezdu
  from dual;
END;
/

CREATE OR REPLACE TRIGGER auto_increment_objednavka_uzivatel BEFORE
INSERT ON objednavka_uzivatel
FOR EACH ROW
BEGIN
  SELECT objednavka_uzivatel_seq.nextval
  INTO :new.ID_objednavka_uzivatel
  from dual;
END;
/

CREATE OR REPLACE TRIGGER auto_increment_objednavka BEFORE
INSERT ON objednavka
FOR EACH ROW
BEGIN
  SELECT objednavka_seq.nextval
  INTO :new.ID_objednavky
  from dual;
END;
/

CREATE OR REPLACE TRIGGER auto_increment_objednavka_zajezdu BEFORE
INSERT ON objednavka_zajezdu
FOR EACH ROW
BEGIN
  SELECT objednavka_zajezdu_seq.nextval
  INTO :new.ID_objednavky_zajezdu
  from dual;
END;
/

CREATE OR REPLACE TRIGGER auto_increment_objednavka_doprovodne_akce BEFORE
INSERT ON objednavka_doprovodne_akce
FOR EACH ROW
BEGIN
  SELECT objednavka_doprovodne_akce_seq.nextval
  INTO :new.ID_objednavky_doprovodne_akce
  from dual;
END;
/

CREATE OR REPLACE PROCEDURE DELETE_TMP (THE_TABLE VARCHAR, PK_COLUMN VARCHAR, THE_ID NUMBER) AS
  COMMAND VARCHAR(1024);
  BEGIN
    COMMAND := 'UPDATE ' || DELETE_TMP.THE_TABLE || ' SET ENDING=SYSTIMESTAMP WHERE ' || DELETE_TMP.PK_COLUMN || '=' || DELETE_TMP.THE_ID || ' AND ENDING IS NULL';
    EXECUTE IMMEDIATE COMMAND;
    COMMIT;
  END;
/

CREATE OR REPLACE PROCEDURE INSERT_TMP (THE_TABLE VARCHAR, THE_COLUMNS VARCHAR, THE_VALUES VARCHAR) AS
  COMMAND VARCHAR(1024);
  BEGIN
    COMMAND := 'INSERT INTO ' || INSERT_TMP.THE_TABLE || ' (' || INSERT_TMP.THE_COLUMNS || ', BEGINING) VALUES (' || INSERT_TMP.THE_VALUES || ', SYSTIMESTAMP)';
    EXECUTE IMMEDIATE COMMAND;
    COMMIT;
  END;
/

CREATE OR REPLACE PROCEDURE UPDATE_TMP(THE_TABLE VARCHAR, THE_COLUMNS VARCHAR, THE_VALUES VARCHAR, PK_COLUMN VARCHAR, THE_ID NUMBER) AS
  COMMAND VARCHAR(1024);
  NEW_ID NUMBER;
  BEGIN
    COMMAND := 'UPDATE ' || UPDATE_TMP.THE_TABLE || ' SET ENDING=SYSTIMESTAMP WHERE ' || UPDATE_TMP.PK_COLUMN || '=' || UPDATE_TMP.THE_ID;
    EXECUTE IMMEDIATE COMMAND;
    COMMAND := 'SELECT ' || UPDATE_TMP.THE_TABLE || '_seq.CURRVAL FROM DUAL';
    EXECUTE IMMEDIATE COMMAND INTO NEW_ID;
    COMMAND := 'INSERT INTO ' || UPDATE_TMP.THE_TABLE || ' (' || UPDATE_TMP.PK_COLUMN || ',' || UPDATE_TMP.THE_COLUMNS || ', BEGINING) VALUES ('|| NEW_ID || ',' || UPDATE_TMP.THE_VALUES || ', SYSTIMESTAMP)';
    EXECUTE IMMEDIATE COMMAND;
    COMMIT;
  END;
/

CREATE OR REPLACE PROCEDURE UPDATE_CONN_TMP(THE_TABLE VARCHAR, FK_COLUMN_1 VARCHAR, FK_COLUMN_2 VARCHAR, PK_COLUMN_3 VARCHAR, THE_ID_1 NUMBER, THE_ID_2 NUMBER, THE_ID_3 NUMBER) AS
  COMMAND VARCHAR(1024);
  NEW_ID NUMBER;
  BEGIN
    COMMAND := 'CALL DELETE_TMP (''' || UPDATE_CONN_TMP.THE_TABLE || ''', ''' || UPDATE_CONN_TMP.PK_COLUMN_3 ||  ''', ' || UPDATE_CONN_TMP.THE_ID_3 || ')';
    EXECUTE IMMEDIATE COMMAND;
    COMMAND := 'SELECT ' || UPDATE_CONN_TMP.THE_TABLE || '_seq.CURRVAL FROM DUAL';
    EXECUTE IMMEDIATE COMMAND INTO NEW_ID;
    NEW_ID := NEW_ID - 1;
    COMMAND := 'CALL INSERT_TMP (''' || UPDATE_CONN_TMP.THE_TABLE || ''', ''' || UPDATE_CONN_TMP.FK_COLUMN_1 || ', ' || UPDATE_CONN_TMP.FK_COLUMN_2 || ', ' || UPDATE_CONN_TMP.PK_COLUMN_3 || ''', ''' || UPDATE_CONN_TMP.THE_ID_1 || ', ' || UPDATE_CONN_TMP.THE_ID_2 || ', ' ||  NEW_ID || ''')';
    EXECUTE IMMEDIATE COMMAND;
    COMMIT;
  END;
/

CREATE OR REPLACE FUNCTION SELECT_SIM_ACT_TMP(THE_SELECT VARCHAR, THE_FROM VARCHAR, THE_WHERE VARCHAR, THE_ELSE VARCHAR) RETURN SYS_REFCURSOR AS
  RET SYS_REFCURSOR;
  COMMAND VARCHAR(1024);
  BEGIN
    IF SELECT_SIM_ACT_TMP.THE_WHERE IS NULL THEN
      IF SELECT_SIM_ACT_TMP.THE_ELSE IS NULL THEN
        COMMAND := 'SELECT ' || SELECT_SIM_ACT_TMP.THE_SELECT || ' FROM ' || SELECT_SIM_ACT_TMP.THE_FROM || ' WHERE ENDING IS NULL';
      ELSE
        COMMAND := 'SELECT ' || SELECT_SIM_ACT_TMP.THE_SELECT || ' FROM ' || SELECT_SIM_ACT_TMP.THE_FROM || ' WHERE ENDING IS NULL ' || SELECT_SIM_ACT_TMP.THE_ELSE;
      END IF;
    ELSE
      IF SELECT_SIM_ACT_TMP.THE_ELSE IS NULL THEN
        COMMAND := 'SELECT ' || SELECT_SIM_ACT_TMP.THE_SELECT || ' FROM ' || SELECT_SIM_ACT_TMP.THE_FROM || ' WHERE ' || SELECT_SIM_ACT_TMP.THE_WHERE || ' AND ENDING IS NULL';
      ELSE
        COMMAND := 'SELECT ' || SELECT_SIM_ACT_TMP.THE_SELECT || ' FROM ' || SELECT_SIM_ACT_TMP.THE_FROM || ' WHERE ' || SELECT_SIM_ACT_TMP.THE_WHERE || ' AND ENDING IS NULL ' || SELECT_SIM_ACT_TMP.THE_ELSE;
      END IF;
    END IF;
    OPEN RET FOR COMMAND;
    RETURN RET;
  END;
/

CREATE OR REPLACE FUNCTION SELECT_COM_ACT_TMP(THE_SELECT VARCHAR, TABLE_ONE VARCHAR, TABLE_TWO VARCHAR, THE_WHERE VARCHAR, THE_ELSE VARCHAR) RETURN SYS_REFCURSOR AS
  RET SYS_REFCURSOR;
  COMMAND VARCHAR(1024);
  BEGIN
    IF SELECT_COM_ACT_TMP.THE_WHERE IS NULL THEN
      IF SELECT_COM_ACT_TMP.THE_ELSE IS NULL THEN
        COMMAND := 'SELECT ' || SELECT_COM_ACT_TMP.THE_SELECT || ' FROM ' || SELECT_COM_ACT_TMP.TABLE_ONE || ', ' || SELECT_COM_ACT_TMP.TABLE_TWO || ' WHERE ' || SELECT_COM_ACT_TMP.TABLE_ONE || '.ENDING IS NULL AND ' || SELECT_COM_ACT_TMP.TABLE_TWO || '.ENDING IS NULL';
      ELSE
        COMMAND := 'SELECT ' || SELECT_COM_ACT_TMP.THE_SELECT || ' FROM ' || SELECT_COM_ACT_TMP.TABLE_ONE || ', ' || SELECT_COM_ACT_TMP.TABLE_TWO || ' WHERE ' || SELECT_COM_ACT_TMP.TABLE_ONE || '.ENDING IS NULL AND ' || SELECT_COM_ACT_TMP.TABLE_TWO || '.ENDING IS NULL ' || SELECT_COM_ACT_TMP.THE_ELSE;
      END IF;
    ELSE
      IF SELECT_COM_ACT_TMP.THE_ELSE IS NULL THEN
        COMMAND := 'SELECT ' || SELECT_COM_ACT_TMP.THE_SELECT || ' FROM ' || SELECT_COM_ACT_TMP.TABLE_ONE || ', ' || SELECT_COM_ACT_TMP.TABLE_TWO || ' WHERE ' || SELECT_COM_ACT_TMP.THE_WHERE || ' AND ' || SELECT_COM_ACT_TMP.TABLE_ONE || '.ENDING IS NULL AND ' || SELECT_COM_ACT_TMP.TABLE_TWO || '.ENDING IS NULL';
      ELSE
        COMMAND := 'SELECT ' || SELECT_COM_ACT_TMP.THE_SELECT || ' FROM ' || SELECT_COM_ACT_TMP.TABLE_ONE || ', ' || SELECT_COM_ACT_TMP.TABLE_TWO || ' WHERE ' || SELECT_COM_ACT_TMP.THE_WHERE || ' AND ' || SELECT_COM_ACT_TMP.TABLE_ONE || '.ENDING IS NULL AND ' || SELECT_COM_ACT_TMP.TABLE_TWO || '.ENDING IS NULL ' || SELECT_COM_ACT_TMP.THE_ELSE;
      END IF;
    END IF;
    OPEN RET FOR COMMAND;
    RETURN RET;
  END;
/
