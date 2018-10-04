/* SQL queries for ECS_SQLi */

/* Create a table */
CREATE TABLE user_creds_vtwo (
    id int(5) AUTO_INCREMENT PRIMARY KEY,
    username varchar(30) NOT NULL UNIQUE,
    password varchar(250) NOT NULL,
    fname varchar(30) NOT NULL,
    lname varchar(30)
);

/* Insert values into the table */
INSERT INTO user_creds_vtwo (fname,lname,username,password) VALUES ('$fname','$lname','$uname','$upass');

/* Select values from the table */
SELECT * FROM user_creds_vtwo WHERE username='$uname' AND password='$upass';
SELECT fname FROM user_creds_vtwo WHERE username='$uname';