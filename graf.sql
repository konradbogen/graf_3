DROP TABLE IF EXISTS Node;
DROP TABLE IF EXISTS Edge;

CREATE TABLE Node (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    cont VARCHAR(255) UNIQUE,
    cluster VARCHAR (10),
    type VARCHAR(10) CHECK (type == "m" or type == "t"),
    harm VARCHAR (255),
    syll INTEGER DEFAULT 1 NOT NULL,
    stress INTEGER DEFAULT 1 NOT NULL,
    CHECK (syll <= 9 AND syll >= 1),
    CHECK (stress <= 9 AND stress >= 1)
);

CREATE TABLE Edge (
    a INTEGER,
    b INTEGER,
    FOREIGN KEY (a) REFERENCES Node (id),
    FOREIGN KEY (b) REFERENCES Node (id)
);

