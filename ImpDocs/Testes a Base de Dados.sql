-- Teste ao Procedimento Registar Modelo  
CREATE OR REPLACE FUNCTION TEST_registar_Modelo(
    p_nome VARCHAR,
    p_id_marca INTEGER,
    p_isactive BOOLEAN DEFAULT TRUE
)
RETURNS TEXT AS $$
DECLARE
    contador INTEGER;
    resultado TEXT;
BEGIN
    -- Tentar chamar a função de inserção
    BEGIN
        CALL registar_Modelo(p_nome, p_id_marca, p_isactive);
    EXCEPTION
        WHEN OTHERS THEN
            RETURN 'NOK - Erro na função registar_Modelo: ' || SQLERRM;
    END;

    -- Verificar se o modelo foi inserido corretamente
    SELECT COUNT(*)
    INTO contador
    FROM Modelo
    WHERE Nome = p_nome AND ID_Marca = p_id_marca AND IsActive = p_isactive;

    -- Determinar o resultado do teste
    IF contador > 0 THEN
        resultado := 'OK - Modelo inserido com sucesso.';
    ELSE
        resultado := 'NOK - Modelo não foi inserido.';
    END IF;

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

SELECT TEST_registar_Modelo('A4', 1, TRUE);
SELECT TEST_registar_Modelo('A6', 999, TRUE); -- ID inválido para testar

------------------------------------------------------------------------------------

-- Teste ao procedimento Registar Fornecedor 

CREATE OR REPLACE FUNCTION TEST_registar_Fornecedor(
    p_nome VARCHAR,
    p_valor DECIMAL,
    p_isactive BOOLEAN DEFAULT TRUE
)
RETURNS TEXT AS $$
DECLARE
    contador INTEGER;
    resultado TEXT;
BEGIN
    -- Tentar chamar a função de inserção
    BEGIN
        CALL registar_Fornecedor(p_nome, p_valor, p_isactive);
    EXCEPTION
        WHEN OTHERS THEN
            RETURN 'NOK - Erro na função registar_Fornecedor: ' || SQLERRM;
    END;

    -- Verificar se o fornecedor foi inserido corretamente
    SELECT COUNT(*)
    INTO contador
    FROM Fornecedor
    WHERE Nome = p_nome AND Valor = p_valor AND IsActive = p_isactive;

    -- Determinar o resultado do teste
    IF contador > 0 THEN
        resultado := 'OK - Fornecedor inserido com sucesso.';
    ELSE
        resultado := 'NOK - Fornecedor não foi inserido.';
    END IF;

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

SELECT TEST_registar_Fornecedor('Fornecedor X', 1500.00, TRUE);
SELECT TEST_registar_Fornecedor('Fornecedor X', 2000.00, TRUE); -- Deve retornar uma mensagem de duplicado.

------------------------------------------------------------------------------------

--Teste ao procedimento Registar Pecas
CREATE OR REPLACE FUNCTION TEST_registar_Peca(
    p_nome VARCHAR,
    p_stock INTEGER,
    p_id_marca INTEGER,
    p_id_modelo INTEGER
)
RETURNS TEXT AS $$
DECLARE
    contador INTEGER;
    resultado TEXT;
BEGIN
    -- Tentar chamar a função de inserção
    BEGIN
        CALL registar_Peca(p_nome, p_stock, p_id_marca, p_id_modelo);
    EXCEPTION
        WHEN OTHERS THEN
            RETURN 'NOK - Erro na função registar_Peca: ' || SQLERRM;
    END;

    -- Verificar se a peça foi inserida corretamente
    SELECT COUNT(*)
    INTO contador
    FROM Pecas
    WHERE Nome = p_nome AND Stock = p_stock AND ID_Marca = p_id_marca AND ID_Modelo = p_id_modelo;

    -- Determinar o resultado do teste
    IF contador > 0 THEN
        resultado := 'OK - Peça inserida com sucesso.';
    ELSE
        resultado := 'NOK - Peça não foi inserida.';
    END IF;

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

SELECT TEST_registar_Peca('Catalisador', 10, 1, 2);
SELECT TEST_registar_Peca('Catalisador', 10, 999, 2); -- ID inválido para testar

------------------------------------------------------------------------------------

--Teste ao Procedimento Registar Reserva
CREATE OR REPLACE FUNCTION TEST_registar_Reserva(
    p_Data_Inicio DATE,
    p_Data_Fim DATE, 
    p_Danos BOOLEAN,
    p_DanosTexto VARCHAR,
    p_KMPercorridos INTEGER,
    p_ID_Viatura INTEGER,
    p_ID_Utilizador INTEGER,
    p_ID_EstadoReserva INTEGER
)
RETURNS TEXT AS $$
DECLARE
    contador INTEGER;
    resultado TEXT;
BEGIN
    -- Tentar chamar o procedimento de inserção
    BEGIN
        CALL registar_Reserva(p_Data_Inicio, p_Data_Fim, p_Danos, p_DanosTexto, p_KMPercorridos, p_ID_Viatura, p_ID_Utilizador, p_ID_EstadoReserva);
    EXCEPTION
        WHEN OTHERS THEN
            RETURN 'NOK - Erro na função registar_Reserva: ' || SQLERRM;
    END;

    -- Verificar se a reserva foi inserida corretamente
    SELECT COUNT(*)
    INTO contador
    FROM Reserva
    WHERE Data_Inicio = p_Data_Inicio 
      AND Data_Fim = p_Data_Fim
      AND Danos = p_Danos
      AND DanosTexto = p_DanosTexto
      AND KMPercorridos = p_KMPercorridos
      AND ID_Viatura = p_ID_Viatura
      AND ID_Utilizador = p_ID_Utilizador
      AND ID_EstadoReserva = p_ID_EstadoReserva;

    -- Determinar o resultado do teste
    IF contador > 0 THEN
        resultado := 'OK - Reserva inserida com sucesso.';
    ELSE
        resultado := 'NOK - Reserva não foi inserida.';
    END IF;

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

SELECT TEST_registar_Reserva('2025-01-15', '2025-01-20', FALSE, '', 200, 1, 1, 2);
SELECT TEST_registar_Reserva('2025-01-10', '2025-01-12', TRUE, 'Danos na lateral', 150, 1, 2, 3);
SELECT TEST_registar_Reserva('2025-01-05', '2025-01-07', FALSE, '', 0, 999, 1, 1);

------------------------------------------------------------------------------------

-- Teste ao Procediemento Registar Manutencao
CREATE OR REPLACE FUNCTION TEST_registar_Manutencao(
    p_valor DECIMAL,
    p_descricao TEXT,
    p_data DATE,
    p_id_viatura INTEGER
)
RETURNS TEXT AS $$
DECLARE
    contador INTEGER;
    resultado TEXT;
BEGIN
    BEGIN
        CALL registar_Manutencao(p_valor, p_descricao, p_data, p_id_viatura);
    EXCEPTION
        WHEN OTHERS THEN
            RETURN 'NOK - Erro na função registar_Manutencao: ' || SQLERRM;
    END;

    SELECT COUNT(*)
    INTO contador
    FROM Manutencao
    WHERE Valor = p_valor AND Descricao = p_descricao AND Data = p_data AND ID_Viatura = p_id_viatura;

    IF contador > 0 THEN
        resultado := 'OK - Manutenção inserida com sucesso.';
    ELSE
        resultado := 'NOK - Manutenção não foi inserida.';
    END IF;

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

SELECT TEST_registar_Manutencao(250.00, 'Troca de óleo', '2025-01-15', 1);
SELECT TEST_registar_Manutencao(300.00, 'Manutenção geral', '2025-01-25', 999); -- ID de viatura inválido

------------------------------------------------------------------------------------

--Teste a Registar uma encomenda ao Fornecedor 
CREATE OR REPLACE FUNCTION TEST_registar_EncomendaFornecedor(
    p_quantidade INTEGER,
    p_valor DECIMAL,
    p_id_peca INTEGER,
    p_id_fornecedor INTEGER,
    p_id_estado_encomenda INTEGER
)
RETURNS TEXT AS $$
DECLARE
    contador INTEGER;
    resultado TEXT;
BEGIN
    BEGIN
        CALL registar_EncomendaFornecedor(p_quantidade, p_valor, p_id_peca, p_id_fornecedor, p_id_estado_encomenda);
    EXCEPTION
        WHEN OTHERS THEN
            RETURN 'NOK - Erro na função registar_EncomendaFornecedor: ' || SQLERRM;
    END;

    SELECT COUNT(*)
    INTO contador
    FROM EncomendaFornecedor
    WHERE Quantidade = p_quantidade AND Valor = p_valor AND ID_Peca = p_id_peca AND ID_Fornecedor = p_id_fornecedor AND ID_EstadoEncomenda = p_id_estado_encomenda;

    IF contador > 0 THEN
        resultado := 'OK - Encomenda inserida com sucesso.';
    ELSE
        resultado := 'NOK - Encomenda não foi inserida.';
    END IF;

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

SELECT TEST_registar_EncomendaFornecedor(3, 50.00, 3, 3, 2); -- IDs válidos
SELECT TEST_registar_EncomendaFornecedor(20, 200.00, 999, 3, 3); -- ID de peça inválido

------------------------------------------------------------------------------------

-- Teste ao Procedimento Registar Marca
CREATE OR REPLACE FUNCTION TEST_registar_Marca(
    p_nome VARCHAR,
    p_isactive BOOLEAN DEFAULT TRUE
)
RETURNS TEXT AS $$
DECLARE
    contador INTEGER;
    resultado TEXT;
BEGIN
    -- Tentar chamar o procedimento de inserção
    BEGIN

    SELECT COUNT(*)
    INTO contador
    FROM Marca
    WHERE LOWER(Nome) = LOWER(p_nome);

        -- Determinar o resultado do teste
        IF contador = 1 THEN
            resultado := 'NOK - Marca duplicada ou não foi inserida.';
        ELSE
            CALL registar_Marca(p_nome, p_isactive);
            resultado := 'OK- Marca adicionada com sucesso.';
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RETURN 'NOK - Erro na função registar_Marca: ' || SQLERRM;
    END;

    -- Verificar se a marca foi inserida corretamente
    
    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM marca

SELECT TEST_registar_Marca('BMW', TRUE); -- Marca válida
SELECT TEST_registar_Marca('bmw', TRUE); -- Marca duplicado

------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION TEST_registar_TipoViatura(
    p_nome VARCHAR,
    p_isactive BOOLEAN DEFAULT TRUE
)
RETURNS TEXT AS $$
DECLARE
    contador INTEGER;
    resultado TEXT;
BEGIN
    -- Verificar se o registro foi inserido corretamente
    SELECT COUNT(*)
    INTO contador
    FROM TipoViatura
    WHERE Nome = p_nome;

    -- Determinar o resultado do teste
    IF contador = 0 THEN
            -- Tentar chamar o procedimento de inserção
        BEGIN
            CALL registar_TipoViatura(p_nome, p_isactive);
        EXCEPTION
            WHEN OTHERS THEN
                RETURN 'NOK - Erro na função registar_TipoViatura: ' || SQLERRM;
        END;
        resultado := 'OK - TipoViatura inserido com sucesso.';
    ELSE
        resultado := 'NOK - TipoViatura não foi inserido.';
    END IF;

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION TEST_registar_EstadoViatura(
    p_estado VARCHAR,
    p_isactive BOOLEAN DEFAULT TRUE
)
RETURNS TEXT AS $$
DECLARE
    contador INTEGER;
    resultado TEXT;
BEGIN

-- Verificar se o registro foi inserido corretamente
    SELECT COUNT(*)
    INTO contador
    FROM EstadoViatura
    WHERE Estado = p_estado;

    -- Determinar o resultado do teste
    IF contador = 0 THEN
        BEGIN
            CALL registar_EstadoViatura(p_estado, p_isactive);
        EXCEPTION
            WHEN OTHERS THEN
                RETURN 'NOK - Erro na função registar_EstadoViatura: ' || SQLERRM;
        END;
        resultado := 'OK - EstadoViatura inserido com sucesso.';
    ELSE
        resultado := 'NOK - EstadoViatura não foi inserido.';
    END IF;
    -- Tentar chamar o procedimento de inserção
    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION TEST_registar_Combustivel(
    p_nome VARCHAR,
    p_isactive BOOLEAN DEFAULT TRUE
)
RETURNS TEXT AS $$
DECLARE
    contador INTEGER;
    resultado TEXT;
BEGIN
    -- Verificar se o registro foi inserido corretamente
    SELECT COUNT(*)
    INTO contador
    FROM Combustivel
    WHERE Nome = p_nome;
    -- Determinar o resultado do teste
    IF contador = 0 THEN
        BEGIN
            CALL registar_Combustivel(p_nome, p_isactive);
        EXCEPTION
            WHEN OTHERS THEN
                RETURN 'NOK - Erro na função registar_Combustivel: ' || SQLERRM;
        END;
        resultado := 'OK - Combustível inserido com sucesso.';
    ELSE
        resultado := 'NOK - Combustível não foi inserido.';
    END IF;
    -- Tentar chamar o procedimento de inserção

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION TEST_registar_TipoCaixa(
    p_nome VARCHAR,
    p_isactive BOOLEAN DEFAULT TRUE
)
RETURNS TEXT AS $$
DECLARE
    contador INTEGER;
    resultado TEXT;
BEGIN

    -- Verificar se o registro foi inserido corretamente
    SELECT COUNT(*)
    INTO contador
    FROM TipoCaixa
    WHERE Nome = p_nome;

    -- Determinar o resultado do teste
    IF contador = 0 THEN
        BEGIN
            -- Tentar chamar o procedimento de inserção
            CALL registar_TipoCaixa(p_nome, p_isactive);
        EXCEPTION
            WHEN OTHERS THEN
                RETURN 'NOK - Erro na função registar_TipoCaixa: ' || SQLERRM;
        END;
        resultado := 'OK - TipoCaixa inserido com sucesso.';
    ELSE
        resultado := 'NOK - TipoCaixa não foi inserido.';
    END IF;

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION TEST_registar_Traccao(
    p_nome VARCHAR,
    p_isactive BOOLEAN DEFAULT TRUE
)
RETURNS TEXT AS $$
DECLARE
    contador INTEGER;
    resultado TEXT;
BEGIN
    -- Verificar se o registro foi inserido corretamente
    SELECT COUNT(*)
    INTO contador
    FROM Traccao
    WHERE Nome = p_nome;

    -- Determinar o resultado do teste
    IF contador = 0 THEN
        BEGIN
            -- Tentar chamar o procedimento de inserção
            CALL registar_Traccao(p_nome, p_isactive);
        EXCEPTION
            WHEN OTHERS THEN
                RETURN 'NOK - Erro na função registar_Traccao: ' || SQLERRM;
        END;
        resultado := 'OK - Tracção inserida com sucesso.';
    ELSE
        resultado := 'NOK - Tracção não foi inserida.';
    END IF;

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION TEST_registar_EstadoReserva(
    p_estado VARCHAR,
    p_isactive BOOLEAN DEFAULT TRUE
)
RETURNS TEXT AS $$
DECLARE
    contador INTEGER;
    resultado TEXT;
BEGIN
-- Verificar se o registro foi inserido corretamente
    SELECT COUNT(*)
    INTO contador
    FROM EstadoReserva
    WHERE Estado = p_estado;

    -- Determinar o resultado do teste
    IF contador = 0 THEN
        BEGIN
            CALL registar_EstadoReserva(p_estado, p_isactive);
            EXCEPTION
                WHEN OTHERS THEN
            RETURN 'NOK - Erro na função registar_EstadoReserva: ' || SQLERRM;
        END;
        resultado := 'OK - EstadoReserva inserido com sucesso.';
    ELSE
        resultado := 'NOK - EstadoReserva não foi inserido.';
    END IF;
    -- Tentar chamar o procedimento de inserção

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION TEST_registar_Cor(
    p_nome VARCHAR,
    p_isactive BOOLEAN DEFAULT TRUE
)
RETURNS TEXT AS $$
DECLARE
    contador INTEGER;
    resultado TEXT;
BEGIN
    -- Verificar se o registro foi inserido corretamente
    SELECT COUNT(*)
    INTO contador
    FROM Cores
    WHERE Nome = p_nome;

    -- Determinar o resultado do teste
    IF contador = 0 THEN
        BEGIN
            CALL registar_Cor(p_nome, p_isactive);
            EXCEPTION
                WHEN OTHERS THEN
            RETURN 'NOK - Erro na função registar_Cor: ' || SQLERRM;
        END;
        resultado := 'OK - Cor inserida com sucesso.';
    ELSE
        resultado := 'NOK - Cor não foi inserida.';
    END IF;
    -- Tentar chamar o procedimento de inserção

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION TEST_registar_TipoUtilizador(
    p_tipo VARCHAR,
    p_isactive BOOLEAN DEFAULT TRUE
)
RETURNS TEXT AS $$
DECLARE
    contador INTEGER;
    resultado TEXT;
BEGIN

    -- Verificar se o registro foi inserido corretamente
    SELECT COUNT(*)
    INTO contador
    FROM TipoUtilizador
    WHERE Tipo = p_tipo;

    -- Determinar o resultado do teste
    IF contador = 0 THEN
        BEGIN
            CALL registar_TipoUtilizador(p_tipo, p_isactive);
            EXCEPTION
                WHEN OTHERS THEN
            RETURN 'NOK - Erro na função registar_TipoUtilizador: ' || SQLERRM;
        END;
        resultado := 'OK - TipoUtilizador inserido com sucesso.';
    ELSE
        resultado := 'NOK - TipoUtilizador não foi inserido.';
    END IF;
    -- Tentar chamar o procedimento de inserção

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION TEST_registar_Viatura(
    p_matricula VARCHAR,
    p_ano INTEGER,
    p_km INTEGER,
    p_cilindrada VARCHAR,
    p_potencia VARCHAR,
    p_portas INTEGER,
    p_lotacao INTEGER,
    p_numero_mudancas INTEGER,
    p_inspecao DATE,
    p_iuc MONEY,
    p_preco MONEY,
    p_id_traccao INTEGER,
    p_id_tipocaixa INTEGER,
    p_id_combustivel INTEGER,
    p_id_tipo_viatura INTEGER,
    p_id_marca INTEGER,
    p_id_modelo INTEGER,
    p_id_cor INTEGER,
    p_id_estado_viatura INTEGER
)
RETURNS TEXT AS $$
DECLARE
    contador INTEGER;
    resultado TEXT;
BEGIN
    -- Tentar chamar o procedimento de inserção
    BEGIN
        CALL registar_Viatura(
            p_matricula, p_ano, p_km, p_cilindrada, p_potencia, p_portas, p_lotacao, 
            p_numero_mudancas, p_inspecao, p_iuc, p_preco, p_id_traccao, p_id_tipocaixa, 
            p_id_combustivel, p_id_tipo_viatura, p_id_marca, p_id_modelo, p_id_cor, 
            p_id_estado_viatura
        );
    EXCEPTION
        WHEN OTHERS THEN
            RETURN 'NOK - Erro na função registar_Viatura: ' || SQLERRM;
    END;

    -- Verificar se a viatura foi inserida corretamente
    SELECT COUNT(*)
    INTO contador
    FROM Viatura
    WHERE Matricula = p_matricula AND Ano = p_ano AND KM = p_km AND ID_Traccao = p_id_traccao;

    -- Determinar o resultado do teste
    IF contador > 0 THEN
        resultado := 'OK - Viatura inserida com sucesso.';
    ELSE
        resultado := 'NOK - Viatura não foi inserida.';
    END IF;

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

------------------------------------------------------------------------------------

-- TipoViatura
SELECT TEST_registar_TipoViatura('Cross', TRUE);

-- EstadoViatura
SELECT TEST_registar_EstadoViatura('Disponível', TRUE);

-- Combustível
SELECT TEST_registar_Combustivel('Gasolina', TRUE);

-- TipoCaixa
SELECT TEST_registar_TipoCaixa('Automático', TRUE);

-- Tracção
SELECT TEST_registar_Traccao('4x4', TRUE);

-- EstadoReserva
SELECT TEST_registar_EstadoReserva('Pendente', TRUE);

-- Cor
SELECT TEST_registar_Cor('Azul', TRUE);

-- TipoUtilizador
SELECT TEST_registar_TipoUtilizador('Admin', TRUE);

-- Viatura
SELECT TEST_registar_Viatura('AA-00-AA', 2023, 10000, CAST('1600' AS VARCHAR), CAST('120' AS VARCHAR), 1, 1, 1, CAST('2025-01-01' AS DATE), CAST(150.0 AS MONEY), CAST(25000.0 AS MONEY), 1, 1, 1, 1, 1, 1, 1, 1);
SELECT TEST_registar_Viatura('AA-00-AA', 2023, 10000, CAST('1600' AS VARCHAR), CAST('120' AS VARCHAR), 1, 1, 1, CAST('2025-01-01' AS DATE), CAST(150.0 AS MONEY), CAST(25000.0 AS MONEY), 1, 1, 999, 1, 1, 1, 1, 1);