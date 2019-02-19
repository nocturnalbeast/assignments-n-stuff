/* SQL queries */

/* Create a table */
CREATE TABLE leaked_data (
    id int(5) AUTO_INCREMENT PRIMARY KEY,
    email varchar(200) NOT NULL,
    password varchar(100) NOT NULL
);

/* Insert values into the table */
INSERT INTO leaked_data (email, password) VALUES ('$umail', '$upass');

/* Select values from the table */
SELECT * FROM leaked_data WHERE email='$umail' AND password='$upass';
SELECT password FROM leaked_data WHERE email='$umail';