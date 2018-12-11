/* Create a table */
CREATE TABLE user_details (
    id int(5) AUTO_INCREMENT PRIMARY KEY,
    fname varchar(30) NOT NULL,
    lname varchar(30) NOT NULL
);

/* Insert entries into the table */
INSERT INTO user_details (fname,lname) VALUES ('$fname','$lname');

/* Select entries from the table */
SELECT fname, lname FROM user_details WHERE id='$user_id';