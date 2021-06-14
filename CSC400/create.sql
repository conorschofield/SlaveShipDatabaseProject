CREATE TABLE Captor (
   CapID INTEGER AUTO_INCREMENT PRIMARY KEY,  -- primary key maintained by DB
   Captor VARCHAR(100)  -- name of captor ship
);

 CREATE TABLE Location (
    LocID INTEGER AUTO_INCREMENT PRIMARY KEY,
    Location VARCHAR(100)
 );

CREATE TABLE Images (
   UniqID INT PRIMARY KEY AUTO_INCREMENT,
   imageURL VARCHAR(500) UNIQUE
);

-- corresponds to the pages box and corresponds to diamond
CREATE TABLE ImageConcordance(
   UniqID INT,
   Volume INT,
   Page INT,
   PRIMARY KEY(UniqID, Volume, Page),
   FOREIGN KEY(UniqID) REFERENCES Images(UniqID)
     -- assigns these so that program can tell what
);


-- describe diamond in diagram
CREATE TABLE CaseImage (
   UniqImage INTEGER NOT NULL,
   UniqCase INTEGER NOT NULL,
   PRIMARY KEY(UniqImage, UniqCase),
   FOREIGN KEY (UniqImage) REFERENCES Images(UniqID),
   FOREIGN KEY (UniqCase) REFERENCES Cases(Uniq)
);

CREATE TABLE Cases (
    Uniq INT PRIMARY KEY,  -- internal id assigned by the DB itself, can make AUTO_INCREMENT
    RedNumber VARCHAR(50),      --  should be unique for each case, comes from spreadsheet
    Volume INT,                 --  volume of the archive in which the data resides
--    RedNumberraw VARCHAR(50),      --  unparsed red number
    StartPage INT,                 -- first page in the volume for information about this case
    EndPage INT,                 -- last page ins the volume for information about this case
    CaseN VARCHAR(300),        -- from spreadsheet
    Court VARCHAR(30),         -- court location
    Mixed VARCHAR(40),         -- from spreadsheet
    Register VARCHAR(30),         -- from spreadsheet
    Captor INTEGER,             -- id of the ship that captured the slave vessel
    Location INTEGER,             -- id of the location where the slave vessel was captured/tried ???
    Notes VARCHAR(300),        -- from spreadsheet
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
   DateId INTEGER AUTO_INCREMENT NOT NULL,
   CaseId INTEGER NOT NULL,
   DateOfCapture DATE,
   RAW_DateOfCapture VARCHAR(300),
   PRIMARY KEY(DateId, CaseId),
   FOREIGN KEY (CaseId) REFERENCES Cases(Uniq)
);

CREATE TABLE AdjudicationDates (
   DateId INTEGER AUTO_INCREMENT NOT NULL,
   CaseId INTEGER NOT NULL,
   DateOfAdjudication DATE,
   RAW_DateOfAdjudication VARCHAR(300)
   PRIMARY KEY(DateId, CaseId),
   FOREIGN KEY (CaseId) REFERENCES Cases(Uniq)
);