-- Selecionar Viatura
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
    SELECT v.ID_Viatura, v.ID_Tipo_Viatura, v.ID_Marca, v.ID_Modelo, v.ID_Cor, v.ID_Estado_Viatura, v.KM, v.Ano, v.Matricula
    FROM Viatura v
    WHERE v.ID_Viatura = p_ID_Viatura;
    
    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma viatura encontrada com o ID %.', p_ID_Viatura;
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_Viatura(1); -- Substitua '1' pelo ID desejado

------------------------------------------------------------------------------------------------------------------------------------------------

-- Selecionar Fornecedor
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
    SELECT f.ID_Fornecedor, f.Nome, f.Valor, f.IsActive
    FROM Fornecedor f
    WHERE f.ID_Fornecedor = p_ID_Fornecedor;
    
    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhum fornecedor encontrado com o ID %.', p_ID_Fornecedor;
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_Fornecedor(1); -- Substitua '1' pelo ID desejado

------------------------------------------------------------------------------------------------------------------------------------------------

-- Selecionar Manutenção
CREATE OR REPLACE FUNCTION selecionar_Manutencao(p_ID_Manutencao INTEGER)
RETURNS TABLE (
    ID_Manutencao INTEGER,
    ID_Viatura INTEGER,
    Valor DECIMAL,
    Descricao TEXT,
    Data DATE
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar a manutenção correspondente ao ID fornecido
    RETURN QUERY
    SELECT m.ID_Manutencao, m.ID_Viatura, m.Valor, m.Descricao, m.Data
    FROM Manutencao m
    WHERE m.ID_Manutencao = p_ID_Manutencao;
    
    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma manutenção encontrada com o ID %.', p_ID_Manutencao;
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_Manutencao(1); -- Substitua '1' pelo ID desejado

------------------------------------------------------------------------------------------------------------------------------------------------

-- Selecionar Reserva
CREATE OR REPLACE FUNCTION selecionar_Reserva(p_ID_Reserva INTEGER)
RETURNS TABLE (
    ID_Reserva INTEGER,
    ID_Viatura INTEGER,
    ID_Utilizador INTEGER,
    Estado_Reserva INTEGER,
    Data_Inicio DATE,
    Data_Fim DATE,
    Danos BOOLEAN
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar a Reserva correspondente ao ID fornecido
    RETURN QUERY
    SELECT r.ID_Reserva, r.ID_Viatura, r.ID_Utilizador, r.ID_EstadoReserva, r.Data_Inicio, r.Data_Fim, r.Danos
    FROM Reserva r
    WHERE r.ID_Reserva = p_ID_Reserva;
    
    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma reserva encontrada com o ID %.', p_ID_Reserva;
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_Reserva(1); -- Substitua '1' pelo ID desejado

------------------------------------------------------------------------------------------------------------------------------------------------

-- Selecionar Peça
CREATE OR REPLACE FUNCTION selecionar_Peca(p_ID_Peca INTEGER)
RETURNS TABLE (
    ID_Peca INTEGER,
    Nome VARCHAR,
    Stock INTEGER,
    ID_Marca INTEGER,
    ID_Modelo INTEGER
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar a Peça correspondente ao ID fornecido
    RETURN QUERY
    SELECT p.ID_Peca, p.Nome, p.Stock, p.ID_Marca, p.ID_Modelo
    FROM Pecas p
    WHERE p.ID_Peca = p_ID_Peca;
    
    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma peça encontrada com o ID %.', p_ID_Peca;
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_Peca(1); -- Substitua '1' pelo ID desejado

------------------------------------------------------------------------------------------------------------------------------------------------

-- Selecionar Marca 
CREATE OR REPLACE FUNCTION selecionar_Marca(p_id_marca INTEGER)
RETURNS TABLE (
    ID_Marca INTEGER,
    Nome VARCHAR,
    IsActive BOOLEAN
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar a Marca correspondente ao ID fornecido
    RETURN QUERY
    SELECT m.ID_Marca, m.Nome, m.IsActive
    FROM Marca m
    WHERE m.ID_Marca = p_id_marca;
    
    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma marca encontrada com o ID %.', p_id_marca;
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_Marca(1); -- Substitua '1' pelo ID desejado

------------------------------------------------------------------------------------------------------------------------------------------------

-- Selecionar Modelo 
CREATE OR REPLACE FUNCTION selecionar_Modelo(p_id_modelo INTEGER)
RETURNS TABLE (
    ID_Modelo INTEGER,
    Nome VARCHAR,
    ID_Marca INTEGER,
    IsActive BOOLEAN
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar o Modelo correspondente ao ID fornecido
    RETURN QUERY
    SELECT m.ID_Modelo, m.Nome, m.ID_Marca, m.IsActive
    FROM Modelo m
    WHERE m.ID_Modelo = p_id_modelo;
    
    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhum modelo encontrado com o ID %.', p_id_modelo;
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_Modelo(1); -- Substitua '1' pelo ID desejado

------------------------------------------------------------------------------------------------------------------------------------------------

-- Selecionar Fornecedor 
CREATE OR REPLACE FUNCTION selecionar_Fornecedor(p_id_fornecedor INTEGER)
RETURNS TABLE (
    ID_Fornecedor INTEGER,
    Nome VARCHAR,
    Valor DECIMAL, 
    IsActive BOOLEAN
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar o Fornecedor correspondente ao ID fornecido
    RETURN QUERY
    SELECT f.ID_Fornecedor, f.Nome, f.Valor, f.IsActive
    FROM Fornecedor f
    WHERE f.ID_Fornecedor = p_id_fornecedor;
    
    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhum fornecedor encontrado com o ID %.', p_id_fornecedor;
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_Fornecedor(1); -- Substitua '1' pelo ID desejado

------------------------------------------------------------------------------------------------------------------------------------------------

-- Selecionar Utilizador pelo nome e senha
CREATE OR REPLACE FUNCTION selecionar_UtilizadorByUsernameAndPassword(p_username VARCHAR, p_password VARCHAR)
RETURNS TABLE (
    ID_Utilizador INTEGER,
    Nome VARCHAR,
    Tipo VARCHAR
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar o utilizador correspondente ao nome e senha fornecidos
    RETURN QUERY
    SELECT u.id_utilizador, u.nome, tu.tipo
    FROM utilizador u
    JOIN tipoutilizador tu ON u.id_tipoutilizador = tu.id_tipoutilizador
    WHERE u.nome = p_username AND u.password = p_password;

    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhum utilizador encontrado com essa combinação de Utilizador e Senha.';
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_UtilizadorByUsernameAndPassword("João Silva", "password1");

------------------------------------------------------------------------------------------------------------------------------------------------

-- Seleciona o numero total de reservas de um determinado utilizador
CREATE OR REPLACE FUNCTION selecionar_TotalReservasByUser(p_ID_user VARCHAR)
RETURNS TABLE (
    Reservas_Totais INTEGER
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar o total das reservas do utilizador fornecido
    RETURN QUERY
    SELECT COUNT(id_reserva) AS Reservas_Totais
    FROM reserva 
    WHERE ID_utilizador = p_ID_user;

    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma reserva encontrada desse Utilizador.';
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_TotalReservasByUser(1);