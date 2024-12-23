-- Registar Modelo
CREATE OR REPLACE PROCEDURE registar_Modelo (
    p_Nome VARCHAR,
    p_ID_Marca INTEGER,
    p_IsActive BOOLEAN DEFAULT TRUE
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe um registro com o mesmo Nome
    IF NOT EXISTS (
        SELECT 1 FROM Modelo WHERE Nome = p_Nome AND ID_Marca = p_ID_Marca
    ) THEN
        -- Inserir o novo registro caso não exista
        INSERT INTO Modelo (Nome, ID_Marca, IsActive) 
        VALUES (p_Nome, p_ID_Marca, p_IsActive);
    ELSE
        RAISE NOTICE 'O modelo "%" já existe na tabela e não será inserido.', p_Nome;
    END IF;
END;
$$;

-- Exemplo de chamada do PROCEDURE
-- CALL registar_Modelo('A3', 3, TRUE);      -- Este já existe
-- CALL registar_Modelo('Corolla', 1, TRUE); -- Novo registro

------------------------------------------------------------------------------------------------------------------------------------------------

-- Registar Fornecedor
CREATE OR REPLACE PROCEDURE registar_Fornecedor (
    p_Nome VARCHAR,
    p_Valor DECIMAL,
    p_IsActive BOOLEAN DEFAULT TRUE
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe um registro com o mesmo nome
    IF NOT EXISTS (
        SELECT 1 FROM Fornecedor WHERE Nome = p_Nome
    ) THEN
        -- Inserir o novo registro caso não exista
        INSERT INTO Fornecedor (Nome, Valor, IsActive) 
        VALUES (p_Nome, p_Valor, p_IsActive);
    ELSE
        RAISE NOTICE 'O fornecedor "%" já existe na tabela e não será inserido.', p_Nome;
    END IF;
END;
$$;

-- Exemplo de chamadas do PROCEDURE
-- CALL registar_Fornecedor('Auto Peças Ltda', 1500.00, TRUE); -- Já existe
-- CALL registar_Fornecedor('Peças Rápidas', 2000.00, TRUE);   -- Já existe
-- CALL registar_Fornecedor('Peças Novas', 1800.00, TRUE);     -- Novo registro

------------------------------------------------------------------------------------------------------------------------------------------------

-- Registar Peças
CREATE OR REPLACE PROCEDURE registar_Peca (
    p_Nome VARCHAR,
    p_Stock INTEGER,
    p_ID_Marca INTEGER,
    p_ID_Modelo INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe um registro com o mesmo Nome
    IF NOT EXISTS (
        SELECT 1 FROM Pecas WHERE Nome = p_Nome AND ID_Marca = p_ID_Marca
    ) THEN
        -- Inserir o novo registro caso não exista
        INSERT INTO Pecas (Nome, Stock, ID_Marca, ID_Modelo) 
        VALUES (p_Nome, p_Stock, p_ID_Marca, p_ID_Modelo);
    ELSE
        RAISE NOTICE 'A peça "%" já existe na tabela e não será inserida.', p_Nome;
    END IF;
END;
$$;

SELECT * FROM pecas

-- Exemplo de chamada do PROCEDURE
-- CALL registar_Peca('Filtro de óleo - Universal', 100, 1, 1); -- Este já existe
-- CALL registar_Peca('Catalisador', 30, 1, 2);                 -- Novo registro

------------------------------------------------------------------------------------------------------------------------------------------------

-- Eliminar Marca pelo Id
CREATE OR REPLACE PROCEDURE deleteMarcaById(p_marcaid INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Deletar o usuário com o ID fornecido
    DELETE FROM Marca WHERE ID_Marca = p_marcaid;

    -- Opcional: Verificar se algo foi deletado
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma Marca encontrado com o ID %', p_marcaid;
    END IF;
END;
$$;

-- Exemplo de chamada do PROCEDURE
-- CALL deleteMarcaById(1);

------------------------------------------------------------------------------------------------------------------------------------------------

-- Registar Reserva
CREATE OR REPLACE PROCEDURE registar_Reserva (
    p_Data_Inicio DATE,
    p_Data_Fim DATE, 
    p_Danos BOOLEAN,
    p_DanosTexto VARCHAR,
    p_KMPercorridos INTEGER,
    p_ID_Viatura INTEGER,
    p_ID_Utilizador INTEGER,
    p_ID_EstadoReserva INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Inserir o novo registro caso não exista
    INSERT INTO Reserva (Data_Inicio, Data_Fim, Danos, DanosTexto, KMPercorridos, ID_Viatura, ID_Utilizador, ID_EstadoReserva)
    VALUES (p_Data_Inicio, p_Data_Fim, p_Danos, p_DanosTexto, p_KMPercorridos, p_ID_Viatura, p_ID_Utilizador, p_ID_EstadoReserva);
END;
$$;

-- Exemplo de chamadas do PROCEDURE
-- CALL registar_Reserva('20-12-2023', '23-12-2023', False, '', 0, 1, 1 , 1);

------------------------------------------------------------------------------------------------------------------------------------------------

-- Uptade Reserva
CREATE OR REPLACE PROCEDURE update_Reserva (
    p_reserva_id INTEGER,
    p_ID_EstadoReserva INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Atualiza o estado da reserva para cancelada 
    UPDATE Reserva
        SET ID_EstadoReserva = p_ID_EstadoReserva
        WHERE id_reserva = p_reserva_id
END;
$$;

-- Exemplo de chamadas do PROCEDURE
-- CALL update_Reserva('20-12-2023', '23-12-2023', False, '', 0, 1, 1 , 1);
