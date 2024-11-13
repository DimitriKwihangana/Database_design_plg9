CREATE TABLE chemical_properties (
    id SERIAL PRIMARY KEY,
    ph FLOAT NOT NULL,
    chloramines FLOAT NOT NULL,
    sulfate FLOAT NOT NULL,
    conductivity FLOAT NOT NULL,
    organic_carbon FLOAT NOT NULL,
    trihalomethanes FLOAT NOT NULL
);

CREATE TABLE physical_properties (
    id SERIAL PRIMARY KEY,
    hardness FLOAT NOT NULL,
    solids FLOAT NOT NULL,
    turbidity FLOAT NOT NULL
);

CREATE TABLE water_quality (
    id SERIAL PRIMARY KEY,
    potability INTEGER NOT NULL,
    chemical_properties_id INTEGER NOT NULL,
    physical_properties_id INTEGER NOT NULL,
    FOREIGN KEY (chemical_properties_id) REFERENCES chemical_properties(id) ON DELETE CASCADE,
    FOREIGN KEY (physical_properties_id) REFERENCES physical_properties(id) ON DELETE CASCADE
);
