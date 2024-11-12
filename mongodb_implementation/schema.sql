-- Samples Table
CREATE TABLE Samples (
    SampleID INT PRIMARY KEY,
    LocationID INT,
    SampleDate DATE,
    Potability BOOLEAN,
    FOREIGN KEY (LocationID) REFERENCES Locations (LocationID)
);

-- Chemical Properties Table
CREATE TABLE ChemicalProperties (
    SampleID INT PRIMARY KEY,
    pH DECIMAL(5, 2),
    Hardness DECIMAL(10, 2),
    Solids DECIMAL(10, 2),
    Chloramines DECIMAL(10, 2),
    Sulfate DECIMAL(10, 2),
    FOREIGN KEY (SampleID) REFERENCES Samples (SampleID)
);

-- Physical Properties Table
CREATE TABLE PhysicalProperties (
    SampleID INT PRIMARY KEY,
    Conductivity DECIMAL(10, 2),
    OrganicCarbon DECIMAL(10, 2),
    Trihalomethanes DECIMAL(10, 2),
    Turbidity DECIMAL(5, 2),
    FOREIGN KEY (SampleID) REFERENCES Samples (SampleID)
);