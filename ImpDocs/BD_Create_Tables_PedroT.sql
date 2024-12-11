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
    Marca_ID INTEGER REFERENCES Marca(ID_Marca),
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
    Traccao_ID INTEGER REFERENCES Traccao(ID_Traccao),
    Tipocaixa_ID INTEGER REFERENCES TipoCaixa(ID_Caixa),
    Combustivel_ID INTEGER REFERENCES Combustivel(ID_Combustivel),
    Tipo_Viatura_ID INTEGER REFERENCES TipoViatura(ID_TipoViatura),
    Marca_ID INTEGER REFERENCES Marca(ID_Marca),
    Modelo_ID INTEGER REFERENCES Modelo(ID_Modelo),
    Cor_ID INTEGER REFERENCES Cores(ID_Cor),
    Estado_Viatura_ID INTEGER REFERENCES EstadoViatura(ID_EstadoViatura)
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
    TipoUtilizador_ID INTEGER REFERENCES TipoUtilizador(ID_TipoUtilizador)
);

CREATE TABLE Reserva (
    ID_Reserva SERIAL PRIMARY KEY,
    Data_Inicio DATE,
    Data_Fim DATE,
    Danos BOOLEAN,
    DanosTexto VARCHAR,
    KMPercorridos INTEGER,
    Viatura_ID INTEGER REFERENCES Viatura(ID_Viatura),
    Utilizador_ID INTEGER REFERENCES Utilizador(ID_Utilizador),
    EstadoReserva_ID INTEGER REFERENCES EstadoReserva(ID_Estado_Reserva)
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
    Marca_ID INTEGER REFERENCES Marca(ID_Marca),
    Modelo_ID INTEGER REFERENCES Modelo(ID_Modelo)
);

CREATE TABLE Manutencao (
    ID_Manutencao SERIAL PRIMARY KEY,
    Valor DECIMAL,
    Descricao TEXT,
    Data DATE,
    Viatura_ID INTEGER REFERENCES Viatura(ID_Viatura)
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
    ID_Encomenda_Fornecedor SERIAL PRIMARY KEY, -- Identificador único da encomenda
    Quantidade INTEGER NOT NULL,               -- Quantidade de peças encomendadas
    Valor DECIMAL NOT NULL,                    -- Valor da encomenda
    Peca_ID INTEGER NOT NULL REFERENCES Pecas(ID_Peca), -- Referência à peça encomendada
    Fornecedor_ID INTEGER NOT NULL REFERENCES Fornecedor(ID_Fornecedor), -- Referência ao fornecedor
    EstadoEncomenda_ID INTEGER NOT NULL REFERENCES EstadoEncomendaFornecedor(ID_EstadoEncomenda) -- Estado da encomenda
);

