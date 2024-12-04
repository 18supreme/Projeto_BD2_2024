-- selecionar Viatura
CREATE OR REPLACE FUNCTION selecionar_Viatura(p_ID_Viatura INTEGER)
RETURNS TABLE (
    ID_Viatura INTEGER,
    ID_Tipo_Viatura INTEGER,
    ID_Marca INTEGER,
    ID_Modelo INTEGER,
    ID_Cor INTEGER,
    ID_Estado_Viatura INTEGER,
    KM INTEGER,
    Ano INTEGER,
    Matricula VARCHAR
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar a viatura correspondente ao ID fornecido
    RETURN QUERY
    SELECT ID_Viatura, ID_Tipo_Viatura, ID_Marca, ID_Modelo, ID_Cor, ID_Estado_Viatura, KM, Ano, Matricula
    FROM Viatura
    WHERE ID_Viatura = p_ID_Viatura;
    
    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhum viatura encontrada com o ID %.', p_ID_Viatura;
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
SELECT * FROM selecionar_Viatura(1); -- Substitua '1' pelo ID desejado

-------------------------------------------------------
-- selecionar Fornecedor
CREATE OR REPLACE FUNCTION selecionar_Fornecedor(p_ID_Fornecedor INTEGER)
RETURNS TABLE (
    ID_Fornecedor INTEGER,
    Nome VARCHAR,
    Valor DECIMAL,
    IsActive BOOLEAN
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar o fornecedor correspondente ao ID fornecido
    RETURN QUERY
    SELECT ID_Fornecedor, Nome, Valor, IsActive
    FROM Fornecedor
    WHERE ID_Fornecedor = p_ID_Fornecedor;
    
    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhum fornecedor encontrado com o ID %.', p_ID_Fornecedor;
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
SELECT * FROM selecionar_Fornecedor(1); -- Substitua '1' pelo ID desejado

-------------------------------------------------------
-- selecionar Manutenção
CREATE OR REPLACE FUNCTION selecionar_Manutencao(p_ID_Manutencao INTEGER)
RETURNS TABLE (
    ID_Manutencao INTEGER,
    ID_Viatura INTEGER,
    Valor DECIMAL,
    Descricao TEXT,
    Data DATE,
    ID_Peca INTEGER
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar a manutenção correspondente ao ID fornecido
    RETURN QUERY
    SELECT ID_Manutencao, ID_Viatura, Valor, Descricao, Data, ID_Peca
    FROM Manutencao
    WHERE ID_Manutencao = p_ID_Manutencao;
    
    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhum Manutenção encontrada com o ID %.', p_ID_Manutencao;
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
SELECT * FROM selecionar_Manutencao(1); -- Substitua '1' pelo ID desejado

-------------------------------------------------------
-- selecionar Reserva
CREATE OR REPLACE FUNCTION selecionar_Reserva(p_ID_Reserva INTEGER)
RETURNS TABLE (
    ID_Reserva INTEGER,
    ID_Viatura INTEGER,
    ID_Utilizador INTEGER,
    Estado_Reserva INTEGER,
    Data_Inicio DATE,
    Data_Fim DATE,
    Danos TEXT
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar a Reserva correspondente ao ID fornecido
    RETURN QUERY
    SELECT ID_Reserva, ID_Viatura INTEGER, ID_Utilizador, Estado_Reserva, Data_Inicio, Data_Fim, Danos
    FROM Reserva
    WHERE ID_Reserva = p_ID_Reserva;
    
    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhum Reserva encontrada com o ID %.', p_ID_Reserva;
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
SELECT * FROM selecionar_Reserva(1); -- Substitua '1' pelo ID desejado

-------------------------------------------------------
-- selecionar Peça
CREATE OR REPLACE FUNCTION selecionar_Peca(p_ID_Peca INTEGER)
RETURNS TABLE (
    ID_Peca INTEGER,
    Nome VARCHAR,
    Stock INTEGER,
    Modelo VARCHAR,
    ID_Marca INTEGER,
    ID_Modelo INTEGER
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar a Peça correspondente ao ID fornecido
    RETURN QUERY
    SELECT ID_Peca, Nome, Stock, Modelo, ID_Marca, ID_Modelo
    FROM Pecas
    WHERE ID_Peca = p_ID_Peca;
    
    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma peça encontrada com o ID %.', p_ID_Peca;
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
SELECT * FROM selecionar_Peca(1); -- Substitua '1' pelo ID desejado

-------------------------------------------------------
-- selecionar Marca 
CREATE OR REPLACE FUNCTION selecionar_Marca (p_ID_Marca INTEGER)
RETURNS TABLE (
    ID_Marca INTEGER,
    Nome VARCHAR,
    IsActive BOOLEAN
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar a Peça correspondente ao ID fornecido
    RETURN QUERY
    SELECT ID_Marca, Nome, IsActive
    FROM Marca
    WHERE ID_Marca = p_ID_Marca;
    
    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma marca encontrada com o ID %.', p_ID_Marca;
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
SELECT * FROM selecionar_Marca(1); -- Substitua '1' pelo ID desejado

-------------------------------------------------------
-- selecionar Modelo 
CREATE OR REPLACE FUNCTION selecionar_Modelo (p_ID_Modelo INTEGER)
RETURNS TABLE (
    ID_Modelo INTEGER,
    Nome VARCHAR,
    ID_Marca INTEGER,
    IsActive BOOLEAN
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar a Peça correspondente ao ID fornecido
    RETURN QUERY
    SELECT ID_Modelo, Nome, ID_Marca, IsActive
    FROM Modelo
    WHERE ID_Modelo = p_ID_Modelo;
    
    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhum modelo encontrado com o ID %.', p_ID_Modelo;
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
SELECT * FROM selecionar_Modelo(1); -- Substitua '1' pelo ID desejado

-------------------------------------------------------
-- selecionar Fornecedor 
CREATE OR REPLACE FUNCTION selecionar_Fornecedor (p_ID_Fornecedor INTEGER)
RETURNS TABLE (
    ID_Fornecedor INTEGER,
    Nome VARCHAR,
    Valor DECIMAL, 
    IsActive BOOLEAN
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar a Peça correspondente ao ID fornecido
    RETURN QUERY
    SELECT ID_Fornecedor, Nome, Valor, IsActive
    FROM Fornecedor
    WHERE ID_Fornecedor = p_ID_Fornecedor;
    
    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhum fornecedor encontrado com o ID %.', p_ID_Fornecedor;
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
SELECT * FROM selecionar_Fornecedor(1); -- Substitua '1' pelo ID desejado