#comandos utilizados para criacao de usuarios/tabelas

sudo mysql

CREATE DATABASE OPE2;

CREATE USER 'ope2'@'localhost' identified by 'ope2';
GRANT ALL PRIVILEGES ON OPE2.* TO 'ope2'@'172.27.64.1' IDENTIFIED BY 'ope2';
GRANT ALL PRIVILEGES ON OPE2.* TO 'ope2'@'localhost' IDENTIFIED BY 'ope2';
FLUSH PRIVILEGES;


CREATE TABLE OPE2.`tbl_user` (
  `user_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_email` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_password` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


insert into OPE2.tbl_user (user_name, user_email,user_password) VALUES ('Joao','joao@email.com','senha');