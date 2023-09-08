CREATE TABLE Users (
   LoginID     VARCHAR(30)  PRIMARY KEY,
   Fullname    VARCHAR(30) ,
   Password    VARCHAR(30) ,
   isAdmin     BOOLEAN NOT NULL,
   Affiliation VARCHAR(30) NOT NULL,
   email       VARCHAR(30) 
);

CREATE TABLE Observers (
   email             VARCHAR(30)  PRIMARY KEY,
   FieldLeader       VARCHAR(30) ,
   DataRecorderName  VARCHAR(30) ,
   LoginID           VARCHAR(30) ,
   FOREIGN KEY (LoginID) REFERENCES Users(LoginID)
);

ALTER TABLE Users
ADD CONSTRAINT email_constraint
FOREIGN KEY (email) REFERENCES Observers(email);

CREATE TABLE Seasons (
   Year              INTEGER NOT NULL PRIMARY KEY,
   StartMonth        DATE NOT NULL,
   EndMonth          DATE NOT NULL
);

 CREATE TABLE Rookery (
    Code        VARCHAR(30) NOT NULL PRIMARY KEY,
    TagColor    VARCHAR(30) NOT NULL,
    Name        VARCHAR(30) NOT NULL
 );

 CREATE TABLE Beach (
    SLOCode        VARCHAR(30) NOT NULL PRIMARY KEY,
    USCCCode       VARCHAR(30) NOT NULL,
    Name           VARCHAR(30) NOT NULL,
    Description    VARCHAR(240) NOT NULL,
    Code           VARCHAR(30) NOT NULL,
    FOREIGN KEY (Code) REFERENCES Rookery(Code)
 );


CREATE TABLE Observations (
   ObservationID     INTEGER NOT NULL PRIMARY KEY, 
   email             VARCHAR(30) NOT NULL,
   sex               VARCHAR(4),
   date              DATE,
   MoltPercent       INTEGER,
   Comments          VARCHAR(240),
   AgeClass          VARCHAR(30),
   Year              INTEGER,
   SLOCode           VARCHAR(30),
   FOREIGN KEY (email) REFERENCES Observers(email),
   FOREIGN KEY (SLOCode) REFERENCES Beach(SLOCode),
   FOREIGN KEY (Year) REFERENCES Seasons(Year)
);


CREATE TABLE Measurements (
   MeasurementID     INTEGER AUTO_INCREMENT PRIMARY KEY,
   ObservationID     INTEGER NOT NULL,
   AuxillaryGirth    DOUBLE(12,2),
   AnimalMass        DOUBLE(12,2),
   TotalMass         DOUBLE(12,2),
   CurvilinearLength DOUBLE(12,2),
   StandardLength    DOUBLE(12,2),
   FOREIGN KEY (ObservationID) REFERENCES Observations(ObservationID)
);

CREATE TABLE Seals (
   SealID         INTEGER AUTO_INCREMENT PRIMARY KEY,
   ObservationID  INTEGER NOT NULL,
   Sex            VARCHAR(4),
   proc           BOOLEAN NOT NULL,
   FOREIGN KEY (ObservationID) REFERENCES Observations(ObservationID)
);


CREATE TABLE Marks (
   MarkID         INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
   Mark           VARCHAR(30) NOT NULL,
   MarkPosition   VARCHAR(30),
   markDate       DATE,
   Year           INTEGER NOT NULL,
   MarkSeal       INTEGER NOT NULL,
   FOREIGN KEY (Year) REFERENCES Seasons(Year),
   FOREIGN KEY (MarkSeal) REFERENCES Seals(SealID)
);

CREATE TABLE Tags (
   TagNumber   VARCHAR(30) NOT NULL PRIMARY KEY,
   TagColor    VARCHAR(30), 
   TagPosition VARCHAR(30),
   TagDate     DATE NOT NULL,
   TagSeal     INTEGER NOT NULL,
   FOREIGN KEY (TagSeal) REFERENCES Seals(SealID)
);

CREATE TABLE ObserveTags (
   OTAG_ID           INTEGER AUTO_INCREMENT PRIMARY KEY,
   ObservationID     INTEGER NOT NULL,
   TagNumber         VARCHAR(30) NOT NULL,
   FOREIGN KEY (TagNumber) REFERENCES Tags(TagNumber),
   FOREIGN KEY (ObservationID) REFERENCES Observations(ObservationID)
);

CREATE TABLE ObserveMarks (
   ObservationID     INTEGER NOT NULL PRIMARY KEY,
   MarkID            INTEGER NOT NULL,
   FOREIGN KEY (ObservationID) REFERENCES Observations(ObservationID),
   FOREIGN KEY (MarkID) REFERENCES Marks(MarkID)
);

CREATE TABLE ObserveSeal (
   SealID            INTEGER NOT NULL,
   ObservationID     INTEGER NOT NULL,
   PRIMARY KEY (SealID, ObservationID),
   FOREIGN KEY (SealID) REFERENCES Seals(SealID),
   FOREIGN KEY (ObservationID) REFERENCES Observations(ObservationID)
);

CREATE TABLE BeachSection (
   Code           VARCHAR(30) NOT NULL PRIMARY KEY,
   Description    VARCHAR(240) NOT NULL,
   SLOCode        VARCHAR(30) NOT NULL,
   FOREIGN KEY (SLOCode) REFERENCES Beach(SLOCode)
);

CREATE TABLE Events (
   EventID        INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
   EventTypeName  VARCHAR(30) NOT NULL,
   Description    VARCHAR(240) NOT NULL,
   LoginID        VARCHAR(30) NOT NULL,
   Year           INTEGER NOT NULL,
   FOREIGN KEY (LoginID) REFERENCES Users(LoginID),
   FOREIGN KEY (Year) REFERENCES Seasons(Year)
)
