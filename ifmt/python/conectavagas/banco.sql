-- Execute este arquivo no Workbench antes de abrir o aplicativo.
CREATE DATABASE IF NOT EXISTS conectavagas_aula
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE conectavagas_aula;

-- Uma conta pode publicar várias vagas.
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(97) NOT NULL
);

-- usuario_id guarda quem publicou o anúncio.
CREATE TABLE IF NOT EXISTS vagas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    titulo VARCHAR(120) NOT NULL,
    empresa VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    contato VARCHAR(150) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
