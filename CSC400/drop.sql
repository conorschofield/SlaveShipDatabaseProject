DROP TABLE Events;

DROP TABLE BeachSection;

DROP TABLE ObserveTags;

DROP TABLE ObserveMarks;

DROP TABLE Tags;

DROP TABLE Marks;

DROP TABLE ObserveSeal;

DROP TABLE Seals;

DROP TABLE Measurements;

DROP TABLE Observations;

-- DROP TABLE Beach;

-- DROP TABLE Rookery;

DROP TABLE Seasons;

ALTER TABLE Users
DROP FOREIGN KEY email_constraint;

DROP TABLE Observers;

DROP TABLE Users;
