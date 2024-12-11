-- Drop tables in reverse order to avoid dependency issues
DROP TABLE IF EXISTS EstadoEncomendaFornecedor CASCADE;
DROP TABLE IF EXISTS EncomendaFornecedor CASCADE;
DROP TABLE IF EXISTS Pecas_Manutencao CASCADE;
DROP TABLE IF EXISTS Manutencao CASCADE;
DROP TABLE IF EXISTS Pecas CASCADE;
DROP TABLE IF EXISTS Fornecedor CASCADE;
DROP TABLE IF EXISTS Reserva CASCADE;
DROP TABLE IF EXISTS Utilizador CASCADE;
DROP TABLE IF EXISTS TipoUtilizador CASCADE;
DROP TABLE IF EXISTS EstadoReserva CASCADE;
DROP TABLE IF EXISTS Viatura CASCADE;
DROP TABLE IF EXISTS EstadoViatura CASCADE;
DROP TABLE IF EXISTS Traccao CASCADE;
DROP TABLE IF EXISTS TipoCaixa CASCADE;
DROP TABLE IF EXISTS Combustivel CASCADE;
DROP TABLE IF EXISTS TipoViatura CASCADE;
DROP TABLE IF EXISTS Cores CASCADE;
DROP TABLE IF EXISTS Modelo CASCADE;
DROP TABLE IF EXISTS Marca CASCADE;


CREATE TABLE Marca (
    ID_Marca SERIAL PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL, 
    IsActive BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE Modelo (
    ID_Modelo SERIAL PRIMARY KEY,
    Nome VARCHAR,
    ID_Marca INTEGER REFERENCES Marca(ID_Marca),
    IsActive BOOLEAN
);

CREATE TABLE Cores (
    ID_Cor SERIAL PRIMARY KEY,
    Nome VARCHAR,
    IsActive BOOLEAN
);

CREATE TABLE TipoViatura (
    ID_TipoViatura SERIAL PRIMARY KEY,
    Nome VARCHAR,
    IsActive BOOLEAN
);

CREATE TABLE EstadoViatura (
    ID_EstadoViatura SERIAL PRIMARY KEY,
    Estado VARCHAR,
    IsActive BOOLEAN
);

CREATE TABLE Combustivel (
    ID_Combustivel SERIAL PRIMARY KEY,
    Nome VARCHAR,
    IsActive BOOLEAN
);

CREATE TABLE TipoCaixa (
    ID_Caixa SERIAL PRIMARY KEY,
    Nome VARCHAR,
    IsActive BOOLEAN
);

CREATE TABLE Traccao (
    ID_Traccao SERIAL PRIMARY KEY,
    Nome VARCHAR,
    IsActive BOOLEAN
);

CREATE TABLE Viatura (
    ID_Viatura SERIAL PRIMARY KEY,
    Matricula VARCHAR,
    Ano INTEGER,
    KM INTEGER,
    Cilindrada VARCHAR,
    Potencia VARCHAR,
    Portas INTEGER,
    Lotacao INTEGER,
    NumeroMudancas INTEGER,
    Inspecao DATE,
    IUC MONEY,
    Preco MONEY,
    ID_Traccao INTEGER REFERENCES Traccao(ID_Traccao),
    ID_Tipocaixa INTEGER REFERENCES TipoCaixa(ID_Caixa),
    ID_Combustivel INTEGER REFERENCES Combustivel(ID_Combustivel),
    ID_Tipo_Viatura INTEGER REFERENCES TipoViatura(ID_TipoViatura),
    ID_Marca INTEGER REFERENCES Marca(ID_Marca),
    ID_Modelo INTEGER REFERENCES Modelo(ID_Modelo),
    ID_Cor INTEGER REFERENCES Cores(ID_Cor),
    ID_Estado_Viatura INTEGER REFERENCES EstadoViatura(ID_EstadoViatura)
);

CREATE TABLE EstadoReserva (
    ID_Estado_Reserva SERIAL PRIMARY KEY,
    Estado VARCHAR,
    IsActive BOOLEAN
);

CREATE TABLE TipoUtilizador (
    ID_TipoUtilizador SERIAL PRIMARY KEY,
    Tipo VARCHAR,
    IsActive BOOLEAN
);

CREATE TABLE Utilizador (
    ID_Utilizador SERIAL PRIMARY KEY,
    Nome VARCHAR,
    Password VARCHAR,
    IsActive BOOLEAN,
    ID_TipoUtilizador INTEGER REFERENCES TipoUtilizador(ID_TipoUtilizador)
);

CREATE TABLE Reserva (
    ID_Reserva SERIAL PRIMARY KEY,
    Data_Inicio DATE,
    Data_Fim DATE,
    Danos BOOLEAN,
    DanosTexto VARCHAR,
    KMPercorridos INTEGER,
    ID_Viatura INTEGER REFERENCES Viatura(ID_Viatura),
    ID_Utilizador INTEGER REFERENCES Utilizador(ID_Utilizador),
    ID_EstadoReserva INTEGER REFERENCES EstadoReserva(ID_Estado_Reserva)
);

CREATE TABLE Fornecedor (
    ID_Fornecedor SERIAL PRIMARY KEY,
    Nome VARCHAR,
    Valor DECIMAL,
    IsActive BOOLEAN
);

CREATE TABLE Pecas (
    ID_Peca SERIAL PRIMARY KEY,
    Nome VARCHAR,
    Stock INTEGER,
    ID_Marca INTEGER REFERENCES Marca(ID_Marca),
    ID_Modelo INTEGER REFERENCES Modelo(ID_Modelo)
);

CREATE TABLE Manutencao (
    ID_Manutencao SERIAL PRIMARY KEY,
    Valor DECIMAL,
    Descricao TEXT,
    Data DATE,
    ID_Viatura INTEGER REFERENCES Viatura(ID_Viatura)
);

CREATE TABLE Pecas_Manutencao (
    ID_Peca INTEGER REFERENCES Pecas(ID_Peca),
    ID_Manutencao INTEGER REFERENCES Manutencao(ID_Manutencao),
    Quantidade INTEGER,
    PRIMARY KEY (ID_Peca, ID_Manutencao)
);

CREATE TABLE EstadoEncomendaFornecedor (
    ID_EstadoEncomenda SERIAL PRIMARY KEY,
    Estado VARCHAR NOT NULL UNIQUE
);

CREATE TABLE EncomendaFornecedor (
    ID_Encomenda_Fornecedor SERIAL PRIMARY KEY, 
    Quantidade INTEGER NOT NULL,               
    Valor DECIMAL NOT NULL,
    ID_Peca INTEGER NOT NULL REFERENCES Pecas(ID_Peca), 
    ID_Fornecedor INTEGER NOT NULL REFERENCES Fornecedor(ID_Fornecedor),
    ID_EstadoEncomenda INTEGER NOT NULL REFERENCES EstadoEncomendaFornecedor(ID_EstadoEncomenda) 
);