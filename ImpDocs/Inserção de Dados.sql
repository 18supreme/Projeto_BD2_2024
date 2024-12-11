-- Inserção de dados para a tabela Marca
INSERT INTO Marca (Nome, IsActive) VALUES
('BMW', TRUE),
('Peugeot', TRUE),
('Audi', TRUE),
('Mercedes', FALSE);

-- Inserção de dados para a tabela Modelo
INSERT INTO Modelo (Nome, Marca_ID, IsActive) VALUES
('307', 2, TRUE),
('I8', 1, TRUE),
('A3', 3, TRUE),
('A1', 3, FALSE);

-- Inserção de dados para a tabela Cores
INSERT INTO Cores (Nome, IsActive) VALUES
('Branco', TRUE),
('Preto', TRUE),
('Cinzento', TRUE),
('Azul', FALSE),
('Verde', TRUE);

-- Inserção de dados para a tabela TipoViatura
INSERT INTO TipoViatura (Nome, IsActive) VALUES
('SUV', TRUE),
('Pickup', FALSE),
('Supercar', TRUE),
('Coupe', TRUE);

-- Inserção de dados para a tabela EstadoViatura
INSERT INTO EstadoViatura (Estado, IsActive) VALUES
('Disponível', TRUE),
('Em manutenção', TRUE),
('Alugado', TRUE),
('Indesponível', TRUE);

-- Inserção de dados para a tabela Combustivel
INSERT INTO Combustivel (Nome, IsActive) VALUES
('Disel', TRUE),
('Gasolina', TRUE),
('Eltétrico', TRUE),
('Hibrido', TRUE);

-- Inserção de dados para a tabela Caixa
INSERT INTO TipoCaixa (Nome, IsActive) VALUES
('Manual', TRUE),
('Automático', TRUE),
('Semi-Automático', TRUE);

-- Inserção de dados para a tabela Caixa
INSERT INTO Traccao (Nome, IsActive) VALUES
('Dianteira', TRUE),
('Traseira', TRUE),
('Ás 4', TRUE);

-- Inserção de dados para a tabela Viatura
INSERT INTO Viatura (Matricula, Ano, KM, Cilindrada, Potencia, Portas, Lotacao, NumeroMudancas, Inspecao, IUC, Preco, Traccao_ID, Tipocaixa_ID, Combustivel_ID, Tipo_Viatura_ID, Marca_ID, Modelo_ID, Cor_ID, Estado_Viatura_ID) VALUES
('18-06-PS', 2003, 150000, '1.6 HDI', 110, 5, 5, 5, '2024-11-24', 22.44,90.51, 1, 1, 1, 1, 2, 1, 5, 1);

-- Inserção de dados para a tabela EstadoReserva
INSERT INTO EstadoReserva (Estado, IsActive) VALUES
('Pendente', TRUE),
('Confirmada', TRUE),
('Em progresso', TRUE),
('Finalizada', TRUE),
('Cancelada', TRUE);


-- Inserção de dados para a tabela TipoUtilizador
INSERT INTO TipoUtilizador (Tipo, IsActive) VALUES
('Admin', TRUE),
('Cliente', TRUE),
('Fornecedor', TRUE);

-- Inserção de dados para a tabela Utilizador
INSERT INTO Utilizador (Nome, Password, IsActive, TipoUtilizador_ID) VALUES
('João Silva', 'password1', TRUE, 1),
('Maria Costa', 'password2', TRUE, 2),
('Carlos Rocha', 'password3', TRUE, 3);

-- Inserção de dados para a tabela Reserva
INSERT INTO Reserva (Data_Inicio, Data_Fim, Danos, DanosTexto, KMPercorridos, Viatura_ID, Utilizador_ID, EstadoReserva_ID) VALUES
('2024-11-01', '2024-11-10', FALSE, '', 200, 1, 1, 4),
('2024-10-01', '2024-10-10', TRUE, 'Danos no volante', 1000, 1, 1, 4),
('2024-09-01', '2024-09-10', FALSE, '', 100, 1, 1, 4),
('2024-08-01', '2024-08-10', FALSE, '', 500, 1, 1, 4);


-- Inserção de dados para a tabela Fornecedor
INSERT INTO Fornecedor (Nome, Valor, IsActive) VALUES
('Auto Peças Ltda', 1500.00, TRUE),
('Peças Rápidas', 2000.00, TRUE),
('Mecânica Geral', 500.00, TRUE);

-- Inserção de dados para a tabela Pecas
INSERT INTO Pecas (Nome, Stock, Marca_ID, Modelo_ID) VALUES
('Filtro de óleo - Universal', 100, 1, 1),  -- Ajuste Marca_ID e Modelo_ID para valores válidos
('Manipulo Mudanças', 50, 2, 1),
('Amortecedores dianteiros', 30, 2, 1);

-- Inserção de dados para a tabela Manutencao
INSERT INTO Manutencao (Valor, Descricao, Data, Viatura_ID) VALUES
(250.00, 'Troca de óleo', '2024-11-01', 1),
(500.00, 'Substituição de pastilhas', '2024-10-15', 1),
(750.00, 'Troca de amortecedores', '2024-09-20', 1);

-- Inserção de dados para a tabela Pecas_Manutencao
INSERT INTO Pecas_Manutencao (ID_Peca, ID_Manutencao, Quantidade) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 1, 2);


-- Inserir os estados
INSERT INTO EstadoEncomendaFornecedor (Estado) VALUES
('Em análise'),
('Em trânsito'),
('Entregue');


-- Inserção de dados para a tabela EncomendaFornecedor
INSERT INTO EncomendaFornecedor (Quantidade, Valor, Peca_ID, Fornecedor_ID, EstadoEncomenda_ID) VALUES
(10, 100.00, 1, 1, 1), -- Em análise
(5, 50.00, 2, 2, 2),   -- Em trânsito
(20, 200.00, 3, 3, 3); -- Entregue


-- Seleciona todos os registros das tabelas
SELECT * FROM Marca;
SELECT * FROM Modelo;
SELECT * FROM Cores;
SELECT * FROM Traccao;
SELECT * FROM TipoViatura;
SELECT * FROM EstadoViatura;
SELECT * FROM Viatura;
SELECT * FROM EstadoReserva;
SELECT * FROM TipoUtilizador;
SELECT * FROM Utilizador;
SELECT * FROM Reserva;
SELECT * FROM Fornecedor;
SELECT * FROM Pecas;
SELECT * FROM Manutencao;
SELECT * FROM Pecas_Manutencao;
SELECT * FROM EstadoEncomendaFornecedor;
SELECT * FROM EncomendaFornecedor;

GRANT ALL
ON ALL TABLES IN SCHEMA public
TO ChefeStand;