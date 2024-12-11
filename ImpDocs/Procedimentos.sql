-- registar Modelo
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

-- Exemplo de chamada da PROCEDURE
CALL registar_Modelo('Corolla', 1, TRUE); -- Este já existe
CALL registar_Modelo('A3', 4, TRUE);      -- Novo registro

-------------------------------------------------------
-- registar Fornecedor
CREATE OR REPLACE PROCEDURE registar_Fornecedor (
    p_Nome VARCHAR,
    p_Valor DECIMAL,
    p_IsActive BOOLEAN DEFAULT TRUE
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe um registro com o mesmo Nome
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

-- Exemplo de chamadas da PROCEDURE
CALL registar_Fornecedor('Auto Peças Ltda', 1500.00, TRUE); -- Já existe
CALL registar_Fornecedor('Peças Rápidas', 2000.00, TRUE);   -- Já existe
CALL registar_Fornecedor('Peças Novas', 1800.00, TRUE);     -- Novo registro

-------------------------------------------------------
-- registar Peças
CREATE OR REPLACE PROCEDURE registar_Peca (
    p_Nome VARCHAR,
    p_Stock INTEGER,
    p_Modelo VARCHAR,
    p_ID_Marca INTEGER,
    p_ID_Modelo INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe um registro com o mesmo Nome
    IF NOT EXISTS (
        SELECT 1 FROM Pecas WHERE Nome = p_Nome AND Modelo = p_Modelo AND ID_Marca = p_ID_Marca
    ) THEN
        -- Inserir o novo registro caso não exista
        INSERT INTO Pecas (Nome, Stock, Modelo, ID_Marca, ID_Modelo) 
        VALUES (p_Nome, p_Stock, p_Modelo, p_ID_Marca, p_ID_Modelo);
    ELSE
        RAISE NOTICE 'A peça "%" já existe na tabela e não será inserida.', p_Nome;
    END IF;
END;
$$;

-- Exemplo de chamada da PROCEDURE
CALL registar_Peca('Amortecedor', 20, 'SUV', 3, 3); -- Este já existe
CALL registar_Peca('Catalisador', 30, 'Universal', 1, 2); -- Novo registro