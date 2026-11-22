-- Esquema documentado para estudo no MySQL Workbench.
-- OPCIONAL: o aplicativo cria essas tabelas automaticamente por SQLAlchemy.
-- Se quiser criá-las manualmente, execute após sql/criar_banco.sql.
USE conectavagas;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    salt VARCHAR(32) NOT NULL,
    hash_senha VARCHAR(64) NOT NULL,
    tipo VARCHAR(15) NOT NULL,
    telefone VARCHAR(25) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    resumo TEXT NOT NULL,
    criado_em DATETIME NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_usuarios_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS vagas (
    id INT NOT NULL AUTO_INCREMENT,
    empresa_id INT NOT NULL,
    titulo VARCHAR(120) NOT NULL,
    area VARCHAR(80) NOT NULL,
    descricao TEXT NOT NULL,
    requisitos TEXT NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    modalidade VARCHAR(25) NOT NULL,
    contrato VARCHAR(25) NOT NULL,
    remuneracao VARCHAR(100) NOT NULL,
    ativa BOOLEAN NOT NULL,
    criada_em DATETIME NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_vagas_empresa FOREIGN KEY (empresa_id) REFERENCES usuarios(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS candidaturas (
    id INT NOT NULL AUTO_INCREMENT,
    candidato_id INT NOT NULL,
    vaga_id INT NOT NULL,
    mensagem TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,
    enviada_em DATETIME NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT uq_candidato_vaga UNIQUE (candidato_id, vaga_id),
    CONSTRAINT fk_candidaturas_candidato FOREIGN KEY (candidato_id) REFERENCES usuarios(id),
    CONSTRAINT fk_candidaturas_vaga FOREIGN KEY (vaga_id) REFERENCES vagas(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
