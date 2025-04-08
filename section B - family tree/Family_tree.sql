--Part B.1: People, Relations and Family Tree schema
CREATE TABLE Person (
    Person_Id INTEGER PRIMARY KEY,
    Personal_Name TEXT,
    Family_Name TEXT,
    Gender TEXT,
    Father_Id INTEGER,
    Mother_Id INTEGER,
    Spouse_Id INTEGER,
    
    FOREIGN KEY (Father_Id) REFERENCES Person(Person_Id),
    FOREIGN KEY (Mother_Id) REFERENCES Person(Person_Id),
    FOREIGN KEY (Spouse_Id) REFERENCES Person(Person_Id)
);

CREATE TABLE Relationship (
    Type TEXT PRIMARY KEY
);

CREATE TABLE Family_Tree (
    Person_ID INTEGER,
    Relative_ID INTEGER,
    Connection_Type TEXT,
    
    CONSTRAINT Related PRIMARY KEY (Person_ID, Relative_ID, Connection_Type),

    FOREIGN KEY (Person_ID) REFERENCES Person(Person_Id),
    FOREIGN KEY (Relative_ID) REFERENCES Person(Person_Id),
    FOREIGN KEY (Connection_Type) REFERENCES Relationship(Type)
);

INSERT INTO Relationship(Type) VALUES ("Father"), ("Mother"), ("Brother"), ("Sister"), ("Son"), ("Daughter"), ("Spouse");


--Part B.2: Bidirectional completion of spouses
--example db--
INSERT INTO Person (Person_Id, Personal_Name, Family_Name, Gender, Father_Id, Mother_Id, Spouse_Id)
VALUES (1, 'Moshe', 'Shwartz', 'Male', NULL, NULL, NULL);

INSERT INTO Person (Person_Id, Personal_Name, Family_Name, Gender, Father_Id, Mother_Id, Spouse_Id)
VALUES (2, 'Shoshi', 'Cohen', 'Female', NULL, NULL, NULL);

INSERT INTO Person (Person_Id, Personal_Name, Family_Name, Gender, Father_Id, Mother_Id, Spouse_Id)
VALUES (3, 'Yael', 'Shwartz', 'Female', NULL, NULL, 1);


INSERT INTO Person (Person_Id, Personal_Name, Family_Name, Gender, Father_Id, Mother_Id, Spouse_Id)
VALUES (4, 'Nathan', 'Cohen', 'Male', NULL, NULL, 2);
--------------
--add to Family Tree table, bidirectionally
INSERT OR IGNORE INTO Family_Tree (Person_ID, Relative_ID, Connection_Type)
SELECT
    p1.Person_Id,
    p1.Spouse_Id,
    'Spouse'
FROM
    Person p1
WHERE
    p1.Spouse_Id IS NOT NULL;

INSERT OR IGNORE INTO Family_Tree (Person_ID, Relative_ID, Connection_Type)
SELECT
    p1.Spouse_Id,
    p1.Person_Id,
    'Spouse'
FROM
    Person p1
WHERE
    p1.Spouse_Id IS NOT NULL;

--update Person table
INSERT OR REPLACE INTO Person (
    Person_Id, Personal_Name, Family_Name, Gender, Father_Id, Mother_Id, Spouse_Id
)
SELECT
    p2.Person_Id,
    p2.Personal_Name,
    p2.Family_Name,
    p2.Gender,
    p2.Father_Id,
    p2.Mother_Id,
    p1.Person_Id 
FROM Person p1
JOIN Person p2 ON p1.Spouse_Id = p2.Person_Id
WHERE p2.Spouse_Id IS NULL;