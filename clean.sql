DELETE 
FROM Node
WHERE cont LIKE '%?%';  --case-insensitive

DROP TABLE is_in_2;

CREATE TABLE is_in_2 (
    id INTEGER,
    p_id INTEGER,
    ix INTEGER,
    FOREIGN KEY (id) REFERENCES Node (id),
    FOREIGN KEY (p_id) REFERENCES Path (id)
);

INSERT INTO is_in_2 SELECT Node.id, p_id, ix FROM is_in JOIN Node ON Node.id = is_in.id;
