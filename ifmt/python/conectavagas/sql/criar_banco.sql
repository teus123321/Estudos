-- Execute este arquivo no MySQL Workbench, conectado ao servidor MySQL.
-- Depois, o programa cria as tabelas automaticamente ao abrir.
CREATE DATABASE IF NOT EXISTS conectavagas
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE conectavagas;
-- Após executar app.py uma vez, confira:
SHOW TABLES;
SELECT * FROM usuarios;
SELECT * FROM vagas;
SELECT * FROM candidaturas;
