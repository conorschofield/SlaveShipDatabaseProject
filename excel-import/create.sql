CREATE DATABASE IF NOT EXISTS SeniorProject2
   CHARACTER SET utf8mb4;

USE SeniorProject2;

DROP TABLE IF EXISTS AdjudicationDatesVerbatim;
DROP TABLE IF EXISTS AdjudicationDates;
DROP TABLE IF EXISTS CaptureDatesVerbatim;
DROP TABLE IF EXISTS CaptureDates;
DROP TABLE IF EXISTS SlaveStats;
DROP TABLE IF EXISTS CaseImage;
DROP TABLE IF EXISTS ImageConcordance;
DROP TABLE IF EXISTS Images;
DROP TABLE IF EXISTS Cases;
DROP TABLE IF EXISTS Captor;
DROP TABLE IF EXISTS Location;


CREATE TABLE Captor (
   CapID INTEGER AUTO_INCREMENT PRIMARY KEY,  -- primary key maintained by DB
   Captor VARCHAR(512)  -- name of captor ship
);

CREATE TABLE Location (
   LocID INTEGER AUTO_INCREMENT PRIMARY KEY,
   Location VARCHAR(512)
);

CREATE TABLE ImageConcordance (
   Volume INT,
   PageNumber INT,
   ImagePath VARCHAR(64),
   Weight INT,
   OtherPageNumber INT,
   PRIMARY KEY(Volume, PageNumber, Weight)
);

CREATE TABLE Cases (
    Uniq INT PRIMARY KEY,  -- internal id assigned by the DB itself, can make AUTO_INCREMENT
    RedNumber VARCHAR(96),      --  should be unique for each case, comes from spreadsheet
    Volume INT,                 --  volume of the archive in which the data resides
    StartPage INT,                 -- first page in the volume for information about this case
    EndPage INT,                 -- last page ins the volume for information about this case
    CaseN VARCHAR(1024),        -- from spreadsheet
    Court VARCHAR(128),         -- court location
    Ocean VARCHAR(32),
    Mixed VARCHAR(128),         -- from spreadsheet
    Register VARCHAR(300),         -- from spreadsheet
    Captor INTEGER,             -- id of the ship that captured the slave vessel
    Location INTEGER,             -- id of the location where the slave vessel was captured/tried ???
    Notes VARCHAR(2048),        -- from spreadsheet
    TranscriberNotes VARCHAR(256),
    FOREIGN KEY (Captor) REFERENCES Captor(CapID),
    FOREIGN KEY (Location) REFERENCES Location(LocID)
 );

CREATE TABLE SlaveStats (
   Uniq INTEGER PRIMARY KEY,
   Men INTEGER,
   Women INTEGER,
   Children_m INTEGER,
   Children_f INTEGER,
   Died INTEGER,
   Total INTEGER,
	FOREIGN KEY(Uniq) REFERENCES Cases(Uniq)  -- SlaveStats represents a weak entity set belonging to Cases
);

CREATE TABLE CaptureDates (
   CaseId INTEGER NOT NULL,
   CaptureDate DATE,
   FOREIGN KEY (CaseId) REFERENCES Cases (Uniq)
);

CREATE TABLE CaptureDatesVerbatim (
   CaseId INTEGER NOT NULL,
   CaptureDateVerbatim VARCHAR(256),
   FOREIGN KEY (CaseId) REFERENCES Cases (Uniq)
);

CREATE TABLE AdjudicationDates (
   CaseId INTEGER NOT NULL,
   AdjudicationDate DATE,
   FOREIGN KEY (CaseId) REFERENCES Cases (Uniq)
);

CREATE TABLE AdjudicationDatesVerbatim (
   CaseId INTEGER NOT NULL,
   AdjudicationDateVerbatim VARCHAR(256),
   FOREIGN KEY (CaseId) REFERENCES Cases (Uniq)
);
