DROP DATABASE IF EXISTS atm;
CREATE DATABASE atm;
USE atm;
DROP TABLE IF EXISTS accountinfo;
CREATE TABLE accountinfo (
  account_no char(4) NOT NULL PRIMARY KEY,
  name varchar(20) NOT NULL,
  pin char(4) DEFAULT '1234',
  balance int NOT NULL DEFAULT '0'
);


DROP TABLE IF EXISTS transactions;
CREATE TABLE transactions (
  transaction_time datetime NOT NULL,
  account_no char(4) NOT NULL,
  to_from_account char(4) DEFAULT NULL,
  deposit int DEFAULT NULL,
  withdrawal int DEFAULT NULL,
  balance int DEFAULT NULL,
  transaction_type varchar(8),
  foreign key (to_from_account) REFERENCES accountinfo (account_no),
  foreign key (account_no) REFERENCES accountinfo (account_no)
);
