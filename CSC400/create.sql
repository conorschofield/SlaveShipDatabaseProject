CREATE TABLE Captor (
   CapID       INTEGER AUTO_INCREMENT PRIMARY KEY,
   Captor      VARCHAR(100)
);

 CREATE TABLE Location (
    LocID       INTEGER AUTO_INCREMENT PRIMARY KEY,
    Location    VARCHAR(100)
 );

 CREATE TABLE SlaveStats (
    Uniq        INTEGER PRIMARY KEY,
    Men         INTEGER,
    Women       INTEGER,
    Children_m  INTEGER,
    Children_f  INTEGER,
    Died        INTEGER,
    Total       INTEGER -- ,
--    FOREIGN KEY CaseID REFERENCES Cases(RedNumber)
 );



CREATE TABLE Images (
   UniqID      INT PRIMARY KEY,
   imageURL    VARCHAR(500),
   Volume      INT,
   StartPage   INT,
   EndPage     INT
   -- assigns these so that program can tell what 
);

 CREATE TABLE Cases (
    Uniq        INT PRIMARY KEY,
    RedNumber   VARCHAR(50),
    Volume      INT,
    RedNumberraw VARCHAR(50),
    StartPage   INT,
    EndPage     INT,
    CaseN       varchar(100),
    Court       VARCHAR(30),
    Mixed       VARCHAR(40),
    Register    VARCHAR(30),
    Captor      INTEGER,
    Location    INTEGER,
    Notes       VARCHAR(300),
    FOREIGN KEY (Captor) REFERENCES Captor(CapID),
    FOREIGN KEY (Location) REFERENCES Location(LocID),
    FOREIGN KEY (Uniq) REFERENCES SlaveStats(Uniq)
 );

CREATE TABLE CaseImage (
   UniqID            INTEGER PRIMARY KEY,
   UniqImage         INTEGER NOT  NULL,
   UniqCase          INTEGER NOT NULL,
   FOREIGN KEY (UniqImage) REFERENCES Images(UniqID),
   FOREIGN KEY (UniqCase) REFERENCES Cases(Uniq)
);
