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
CREATE OR REPLACE FUNCTION selecionar_TotalReservasByUser(p_ID_user INTEGER)
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

------------------------------------------------------------------------------------------------------------------------------------------------

-- Seleciona a percentagem de danos de um determinado utilizador
CREATE OR REPLACE FUNCTION selecionar_PercentDanosByUser(p_ID_user INTEGER)
RETURNS TABLE (
    Percentagem_danos NUMERIC(5,2) -- Alterado para suportar decimais
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar a percentagem de danos do utilizador fornecido
    RETURN QUERY
    SELECT 
        COALESCE(
            ROUND(
                (SUM(CASE WHEN Danos = TRUE THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0),
                1
            ),
            0.0
        ) AS Percentagem_danos
    FROM reserva 
    WHERE ID_utilizador = p_ID_user;

    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma reserva encontrada para este utilizador.';
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_PercentDanosByUser(1);

------------------------------------------------------------------------------------------------------------------------------------------------

-- Seleciona a marca mais usada de um determinado utilizador
CREATE OR REPLACE FUNCTION selecionar_MarcaByUser(p_ID_user INTEGER)
RETURNS TABLE (
    marca_preferida VARCHAR
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar a marca mais usada do utilizador fornecido
    RETURN QUERY
    SELECT marca.nome AS marca_preferida
    FROM reserva 
    JOIN viatura ON reserva.id_viatura = viatura.id_viatura
    JOIN marca ON viatura.id_marca = marca.id_marca
    WHERE reserva.id_utilizador = p_ID_user  -- Filtro para o utilizador específico
    GROUP BY marca.nome
    ORDER BY COUNT(*) DESC
    LIMIT 1;

    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma marca encontrada desse Utilizador.';
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_MarcaByUser(1);

------------------------------------------------------------------------------------------------------------------------------------------------

-- Seleciona o modelo mais usado de um determinado utilizador
CREATE OR REPLACE FUNCTION selecionar_ModeloByUser(p_ID_user INTEGER)
RETURNS TABLE (
    marca_preferida VARCHAR
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar o modelo mais usado do utilizador fornecido
    RETURN QUERY
    SELECT modelo.nome AS modelo_preferido
    FROM reserva 
    JOIN viatura ON reserva.id_viatura = viatura.id_viatura
    JOIN modelo ON viatura.id_modelo = modelo.id_modelo
    WHERE reserva.id_utilizador = p_ID_user  -- Filtro para o utilizador específico
    GROUP BY modelo.nome
    ORDER BY COUNT(*) DESC
    LIMIT 1;

    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma modelo encontrado desse Utilizador.';
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_ModeloByUser(1);

------------------------------------------------------------------------------------------------------------------------------------------------

-- Seleciona a média de KM realizados por um determinado utilizador
CREATE OR REPLACE FUNCTION selecionar_MediaKmByUser(p_ID_user INTEGER)
RETURNS TABLE (
    media_km DECIMAL(10, 2) -- Correct data type
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar a média de KM realizados por um utilizador fornecido
    RETURN QUERY
    SELECT 
        COALESCE(ROUND(SUM(KMPercorridos) * 1.0 / COUNT(KMPercorridos), 2), 0)
    FROM reserva 
    WHERE reserva.id_utilizador = p_ID_user; -- Filtro para o utilizador específico

    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma quilometragem encontrada.';
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_MediaKmByUser(1);

------------------------------------------------------------------------------------------------------------------------------------------------

-- Seleciona o total de KM realizados por um determinado utilizador
CREATE OR REPLACE FUNCTION selecionar_TotalKmByUser(p_ID_user INTEGER)
RETURNS TABLE (
    total_km NUMERIC(10,2) -- Define precisão para melhor controle
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar o total de KM percorridos por um utilizador fornecido
    RETURN QUERY
    SELECT COALESCE(SUM(KMPercorridos), 0) AS total_km
    FROM reserva 
    WHERE reserva.id_utilizador = p_ID_user;  -- Filtro para o utilizador específico

    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma quilometragem encontrada.';
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_TotalKmByUser(1);

------------------------------------------------------------------------------------------------------------------------------------------------

-- Seleciona as 3 viaturas mais requisitadas
CREATE OR REPLACE FUNCTION selecionar_getTop3Viaturas()
RETURNS TABLE (
    id_viatura INTEGER,
    marca VARCHAR,
    modelo VARCHAR,
    caixa VARCHAR,
    total_reservas BIGINT
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar as 3 viaturas mais requisitadas
    RETURN QUERY
    SELECT 
        v.id_viatura, 
        m.nome AS marca, 
        mo.nome AS modelo, 
        tc.nome AS caixa, 
        COUNT(r.id_reserva) AS total_reservas
    FROM reserva r
    JOIN viatura v ON r.id_viatura = v.id_viatura
    JOIN marca m ON v.id_marca = m.id_marca
    JOIN modelo mo ON v.id_modelo = mo.id_modelo
    JOIN tipocaixa tc ON tc.id_caixa = v.id_tipocaixa
    GROUP BY v.id_viatura, m.nome, mo.nome, tc.nome
    ORDER BY total_reservas DESC
    LIMIT 3;

    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma viatura encontrado.';
    END IF;
END;
$$;


-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM getTop3Viaturas(1);

------------------------------------------------------------------------------------------------------------------------------------------------

-- Seleciona todas as viaturas
CREATE OR REPLACE FUNCTION selecionar_Viaturas()
RETURNS TABLE (
    id_viatura INTEGER, 
    matricula VARCHAR, 
    modelo VARCHAR, 
    marca VARCHAR, 
    cor VARCHAR, 
    Combustivel VARCHAR, 
    Tipo_Caixa VARCHAR, 
    preco MONEY
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar as 3 viaturas mais requisitadas
    RETURN QUERY
    SELECT 
        vi.id_viatura, vi.matricula, mo.nome AS modelo, ma.nome AS marca, co.nome AS cor, i.Nome AS Combustivel, tc.Nome AS Tipo_Caixa, vi.preco
    FROM viatura vi
    JOIN modelo mo ON vi.id_modelo = mo.id_modelo
    JOIN marca ma ON vi.id_marca = ma.id_marca
    JOIN cores co ON vi.id_cor = co.id_cor
    JOIN Combustivel i ON i.ID_Combustivel = vi.id_Combustivel
    JOIN TipoCaixa tc ON tc.ID_Caixa = vi.id_Tipocaixa;

    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma viatura encontrada.';
    END IF;
END;
$$;


-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_Viaturas(1);

------------------------------------------------------------------------------------------------------------------------------------------------

-- Seleciona todas as viaturas
CREATE OR REPLACE FUNCTION selecionar_DetailViaturaById(p_id_viatura INTEGER)
RETURNS TABLE (
    ID_Viatura INTEGER, 
    Matricula VARCHAR, 
    KM INTEGER, 
    Ano INTEGER, 
    Modelo VARCHAR, 
    Marca VARCHAR, 
    Tipo_Viatura VARCHAR, 
    Cor VARCHAR,
    Estado_Viatura VARCHAR, 
    Combustivel VARCHAR, 
    Tipo_Caixa VARCHAR, 
    Traccao VARCHAR
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar todas as viaturas
    RETURN QUERY
    SELECT 
        v.ID_Viatura, v.Matricula, v.KM, v.Ano, 
        mv.Nome AS Modelo, 
        m.Nome AS Marca, 
        tv.Nome AS Tipo_Viatura, 
        c.Nome AS Cor, 
        ev.Estado AS Estado_Viatura, 
        i.Nome AS Combustivel, 
        tc.Nome AS Tipo_Caixa, 
        tr.Nome AS Traccao
    FROM Viatura v
    JOIN Modelo mv ON mv.ID_Modelo = v.ID_Modelo
    JOIN Marca m ON m.ID_Marca = v.ID_Marca
    JOIN TipoViatura tv ON tv.ID_TipoViatura = v.ID_Tipo_Viatura
    JOIN Cores c ON c.ID_Cor = v.ID_Cor
    JOIN EstadoViatura ev ON ev.ID_EstadoViatura = v.ID_Estado_Viatura
    JOIN Combustivel i ON i.ID_Combustivel = v.ID_Combustivel
    JOIN TipoCaixa tc ON tc.ID_Caixa = v.ID_Tipocaixa
    JOIN Traccao tr ON tr.ID_Traccao = v.ID_Traccao
    WHERE v.ID_Viatura = p_id_viatura;

    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma viatura encontrada com o ID %.', p_id_viatura;
    END IF;
END;
$$;


-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_DetailViaturaById(1);

------------------------------------------------------------------------------------------------------------------------------------------------

-- Seleciona todas as reservas de um determinado utilizador
CREATE OR REPLACE FUNCTION selecionar_ReservaByUser(p_ID_user INTEGER)
RETURNS TABLE (
    id INTEGER,
    marca VARCHAR,
    modelo VARCHAR,
    status VARCHAR,
    data_inicio DATE,
    data_fim DATE,
    danos BOOLEAN
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar todas as reservas de um utilizador fornecido
    RETURN QUERY
    SELECT 
        reserva.id_reserva AS id,
        marca.nome AS marca, 
        modelo.nome AS modelo, 
        estadoreserva.estado AS status, 
        reserva.data_inicio AS data_inicio, 
        reserva.data_fim AS data_fim,
        reserva.danos AS danos
    FROM reserva
    JOIN viatura ON viatura.id_viatura = reserva.id_viatura
    JOIN marca ON viatura.id_marca = marca.id_marca
    JOIN modelo ON viatura.id_modelo = modelo.id_modelo
    JOIN estadoreserva ON reserva.ID_EstadoReserva = estadoreserva.ID_Estado_Reserva
    WHERE id_utilizador = p_ID_user
    ORDER BY reserva.data_inicio DESC;

    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma reserva encontrada';
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_ReservaByUser(1)

------------------------------------------------------------------------------------------------------------------------------------------------

-- Confere se existe alguma reserva para uma determinada viatura, data de inicio e data de fim
CREATE OR REPLACE FUNCTION selecionar_conflitoReserva(p_viatura_id INTEGER, p_data_inicio DATE, p_data_fim DATE)
RETURNS TABLE (
    COUNT BigInt
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar todas as reservas de um utilizador fornecido
    RETURN QUERY
        SELECT COUNT(*) as COUNT
        FROM reserva
        WHERE ID_Viatura = p_viatura_id
            AND (
                (Data_Inicio <= p_data_fim AND Data_Fim >= p_data_inicio)
            )
            AND (reserva.id_estadoreserva != 5)  -- Exclui reservas com estado "Cancelada"
            AND (reserva.id_estadoreserva != 4); -- Exclui reservas com estado "Finalizado"

    -- Caso não encontre, exibir uma mensagem (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Nenhuma reserva encontrada';
    END IF;
END;
$$;

-- Exemplo de chamadas da FUNCTION
-- SELECT * FROM selecionar_conflitoReserva(1,'20-12-2023','23-12-2023')