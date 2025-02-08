-- Registar Modelo
CREATE OR REPLACE PROCEDURE registar_Modelo(
    p_nome VARCHAR,
    p_id_marca INTEGER,
    p_isactive BOOLEAN DEFAULT TRUE
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe um modelo com o mesmo nome para essa marca
    IF EXISTS (
        SELECT 1 
        FROM Modelo 
        WHERE LOWER(Nome) = LOWER(p_nome) AND ID_Marca = p_id_marca
    ) THEN
        RAISE EXCEPTION 'O modelo "%" já existe para esta marca!', p_nome;
    ELSE
        -- Inserir o modelo se não existir
        INSERT INTO Modelo (Nome, ID_Marca, IsActive) 
        VALUES (p_nome, p_id_marca, p_isactive);
    END IF;
END;
$$;


-- Exemplo de chamada do PROCEDURE
-- CALL registar_Modelo('A3', 3, TRUE);      -- Este já existe
-- CALL registar_Modelo('Corolla', 1, TRUE); -- Novo registro

------------------------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE update_Modelo(
    p_modeloid INTEGER,
    p_nome VARCHAR,
    p_id_marca INTEGER,
    p_isactive BOOLEAN
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe outro modelo com o mesmo nome para essa marca
    IF EXISTS (
        SELECT 1 
        FROM Modelo 
        WHERE LOWER(Nome) = LOWER(p_nome) AND ID_Modelo != p_modeloid AND ID_Marca = p_id_marca
    ) THEN
        RAISE EXCEPTION 'Já existe um outro modelo com este nome para esta marca!';
    ELSE
        -- Atualizar os dados do modelo
        UPDATE Modelo
        SET Nome = p_nome, ID_Marca = p_id_marca, IsActive = p_isactive
        WHERE ID_Modelo = p_modeloid;
    END IF;
END;
$$;
------------------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE delete_Modelo(
    p_modeloid INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM Modelo WHERE ID_Modelo = p_modeloid;
END;
$$;

------------------------------------------------------------------------------------

-- Registar Fornecedor
CREATE OR REPLACE PROCEDURE registar_Fornecedor(
    p_Nome VARCHAR,
    p_Valor DECIMAL,
    p_IsActive BOOLEAN DEFAULT TRUE
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe um fornecedor com o mesmo nome
    IF EXISTS (
        SELECT 1 FROM Fornecedor WHERE LOWER(Nome) = LOWER(p_Nome)
    ) THEN
        RAISE EXCEPTION 'O fornecedor "%" já existe!', p_Nome;
    ELSE
        -- Inserir o novo fornecedor
        INSERT INTO Fornecedor (Nome, Valor, IsActive)
        VALUES (p_Nome, p_Valor, p_IsActive);
    END IF;
END;
$$;

--------------------------------------------------------------------------------------
--Atualizar Fornecedor 
CREATE OR REPLACE PROCEDURE update_Fornecedor(
    p_fornecedorid INTEGER,
    p_Nome VARCHAR,
    p_Valor DECIMAL,
    p_IsActive BOOLEAN
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe outro fornecedor com o mesmo nome
    IF EXISTS (
        SELECT 1 FROM Fornecedor WHERE LOWER(Nome) = LOWER(p_Nome) AND ID_Fornecedor != p_fornecedorid
    ) THEN
        RAISE EXCEPTION 'Já existe outro fornecedor com este nome!';
    ELSE
        -- Atualizar os dados do fornecedor
        UPDATE Fornecedor
        SET Nome = p_Nome, Valor = p_Valor, IsActive = p_IsActive
        WHERE ID_Fornecedor = p_fornecedorid;
    END IF;
END;
$$;

---------------------------------------------------------------------------------------------------------
--Eliminar Fornecedor
CREATE OR REPLACE PROCEDURE delete_Fornecedor(p_fornecedor_id INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se o fornecedor tem encomendas associadas
    IF EXISTS (
        SELECT 1 FROM EncomendaFornecedor WHERE ID_Fornecedor = p_fornecedor_id
    ) THEN
        RAISE EXCEPTION 'O fornecedor tem encomendas associadas e não pode ser eliminado.';
    END IF;

    -- Se não houver encomendas, eliminar o fornecedor
    DELETE FROM Fornecedor WHERE ID_Fornecedor = p_fornecedor_id;

    -- Mensagem opcional para logs
    RAISE NOTICE 'Fornecedor com ID % eliminado com sucesso.', p_fornecedor_id;
END;
$$;



-- Exemplo de chamadas do PROCEDURE
-- CALL registar_Fornecedor('Auto Peças Ltda', 1500.00, TRUE); -- Já existe
-- CALL registar_Fornecedor('Peças Rápidas', 2000.00, TRUE);   -- Já existe
-- CALL registar_Fornecedor('Peças Novas', 1800.00, TRUE);     -- Novo registro

------------------------------------------------------------------------------------

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
    -- Verificar se já existe um registro com o mesmo Nome e Marca
    IF NOT EXISTS (
        SELECT 1 FROM Pecas WHERE LOWER(Nome) = LOWER(p_Nome) AND ID_Marca = p_ID_Marca
    ) THEN
        -- Inserir a peça caso não exista
        INSERT INTO Pecas (Nome, Stock, ID_Marca, ID_Modelo) 
        VALUES (p_Nome, p_Stock, p_ID_Marca, p_ID_Modelo);
    ELSE
        RAISE NOTICE 'A peça "%" já existe na tabela e não será inserida.', p_Nome;
    END IF;
END;
$$;

--Atualizar Peça
CREATE OR REPLACE PROCEDURE update_Peca (
    p_ID_Peca INTEGER,
    p_Nome VARCHAR,
    p_Stock INTEGER,
    p_ID_Marca INTEGER,
    p_ID_Modelo INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Atualizar os dados da peça
    UPDATE Pecas
    SET Nome = p_Nome, Stock = p_Stock, ID_Marca = p_ID_Marca, ID_Modelo = p_ID_Modelo
    WHERE ID_Peca = p_ID_Peca;
END;
$$;

--Eliminar Peça
CREATE OR REPLACE PROCEDURE delete_Peca (
    p_ID_Peca INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verifica se a peça está associada a uma manutenção antes de eliminar
    IF EXISTS (SELECT 1 FROM Pecas_Manutencao WHERE ID_Peca = p_ID_Peca) THEN
        RAISE EXCEPTION 'A peça não pode ser eliminada porque está associada a uma manutenção.';
    ELSE
        DELETE FROM Pecas WHERE ID_Peca = p_ID_Peca;
    END IF;
END;
$$;




-- Exemplo de chamada do PROCEDURE
-- CALL registar_Peca('Filtro de óleo - Universal', 100, 1, 1); -- Este já existe
-- CALL registar_Peca('Catalisador', 30, 1, 2);                 -- Novo registro

------------------------------------------------------------------------------------

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

------------------------------------------------------------------------------------

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

------------------------------------------------------------------------------------

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
        WHERE id_reserva = p_reserva_id;
END;
$$;

-- Exemplo de chamadas do PROCEDURE
-- CALL update_Reserva('20-12-2023', '23-12-2023', False, '', 0, 1, 1 , 1);

------------------------------------------------------------------------------------

-- Criar Manutenção
CREATE OR REPLACE PROCEDURE registar_Manutencao(
    p_valor DECIMAL,
    p_descricao TEXT,
    p_data DATE,
    p_id_viatura INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Manutencao (Valor, Descricao, Data, ID_Viatura)
    VALUES (p_valor, p_descricao, p_data, p_id_viatura);
END;
$$;

------------------------------------------------------------------------------------

-- Registar Uma encomenda ao Fornecedor 
CREATE OR REPLACE PROCEDURE registar_Encomenda(
    p_ID_Fornecedor INTEGER,
    p_ID_Peca INTEGER,
    p_Quantidade INTEGER,
    p_Valor DECIMAL,
    p_ID_EstadoEncomenda INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO EncomendaFornecedor (ID_Fornecedor, ID_Peca, Quantidade, Valor, ID_EstadoEncomenda) 
    VALUES (p_ID_Fornecedor, p_ID_Peca, p_Quantidade, p_Valor, p_ID_EstadoEncomenda);
    
    -- Atualizar o saldo do fornecedor automaticamente ao fazer a encomenda
    UPDATE Fornecedor
    SET Valor = Valor + p_Valor
    WHERE ID_Fornecedor = p_ID_Fornecedor;
END;
$$;

--Atualizar Encomenda
CREATE OR REPLACE PROCEDURE update_Encomenda(
    p_ID_Encomenda INTEGER,
    p_Quantidade INTEGER,
    p_Valor DECIMAL,
    p_ID_EstadoEncomenda INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_FornecedorID INTEGER;
    v_ValorAntigo DECIMAL;
BEGIN
    -- Obter o ID do Fornecedor e o valor antigo da encomenda
    SELECT ID_Fornecedor, Valor INTO v_FornecedorID, v_ValorAntigo
    FROM EncomendaFornecedor
    WHERE ID_Encomenda_Fornecedor = p_ID_Encomenda;

    -- Atualizar os dados da encomenda
    UPDATE EncomendaFornecedor
    SET Quantidade = p_Quantidade, 
        Valor = p_Valor, 
        ID_EstadoEncomenda = p_ID_EstadoEncomenda  -- 📌 Garante que está a atualizar o estado!
    WHERE ID_Encomenda_Fornecedor = p_ID_Encomenda;

    -- Ajustar o saldo do fornecedor
    UPDATE Fornecedor
    SET Valor = Valor - v_ValorAntigo + p_Valor
    WHERE ID_Fornecedor = v_FornecedorID;
END;
$$;

-- Eleminar Encomenda
CREATE OR REPLACE PROCEDURE delete_Encomenda(
    p_ID_Encomenda INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_FornecedorID INTEGER;
    v_Valor DECIMAL;
BEGIN
    -- Obter o ID do Fornecedor e o valor da encomenda
    SELECT ID_Fornecedor, Valor INTO v_FornecedorID, v_Valor
    FROM EncomendaFornecedor
    WHERE ID_Encomenda_Fornecedor = p_ID_Encomenda;

    -- Eliminar a encomenda
    DELETE FROM EncomendaFornecedor WHERE ID_Encomenda_Fornecedor = p_ID_Encomenda;

    -- Atualizar o saldo do fornecedor ao remover a encomenda
    UPDATE Fornecedor
    SET Valor = Valor - v_Valor
    WHERE ID_Fornecedor = v_FornecedorID;
END;
$$;

------------------------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE registar_marca(
    p_nome VARCHAR,
    p_isactive BOOLEAN DEFAULT TRUE
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe uma marca com o mesmo nome (case insensitive)
    IF NOT EXISTS (
        SELECT 1 
        FROM Marca 
        WHERE LOWER(Nome) = LOWER(p_nome)
    ) THEN
        -- Inserir a nova marca caso não exista
        INSERT INTO Marca (Nome, IsActive) 
        VALUES (p_nome, p_isactive);
        RAISE NOTICE 'Marca "%" inserida com sucesso.', p_nome;
    ELSE
        -- Caso o nome já exista
        RAISE EXCEPTION 'A marca "%" já existe.', p_nome;
    END IF;
END;
$$;


------------------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE update_marca(
    p_id_marca INTEGER,
    p_nome VARCHAR,
    p_isactive BOOLEAN
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verifica se já existe outra marca com o mesmo nome
    IF EXISTS (
        SELECT 1
        FROM Marca
        WHERE LOWER(Nome) = LOWER(p_nome) AND ID_Marca != p_id_marca
    ) THEN
        RAISE EXCEPTION 'Já existe uma marca com o nome "%"!', p_nome;
    END IF;

    -- Atualiza a marca no banco de dados
    UPDATE Marca
    SET Nome = p_nome, IsActive = p_isactive
    WHERE ID_Marca = p_id_marca;

    RAISE NOTICE 'Marca "%" atualizada com sucesso.', p_nome;
END;
$$;

------------------------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE registar_Peca_Manutencao(
    p_id_peca INTEGER,
    p_id_manutencao INTEGER,
    p_quantidade INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se a peça existe
    IF NOT EXISTS (
        SELECT 1 FROM Pecas WHERE ID_Peca = p_id_peca
    ) THEN
        RAISE EXCEPTION 'A peça com ID % não existe.', p_id_peca;
    END IF;

    -- Verificar se a manutenção existe
    IF NOT EXISTS (
        SELECT 1 FROM Manutencao WHERE ID_Manutencao = p_id_manutencao
    ) THEN
        RAISE EXCEPTION 'A manutenção com ID % não existe.', p_id_manutencao;
    END IF;

    -- Inserir o registro na tabela Pecas_Manutencao
    INSERT INTO Pecas_Manutencao (ID_Peca, ID_Manutencao, Quantidade)
    VALUES (p_id_peca, p_id_manutencao, p_quantidade);
END;
$$;

------------------------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE registar_TipoViatura(
    p_nome VARCHAR,
    p_isactive BOOLEAN DEFAULT TRUE
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe um registro com o mesmo Nome
    IF NOT EXISTS (
        SELECT 1 FROM TipoViatura WHERE Nome = p_nome
    ) THEN
        -- Inserir o novo registro caso não exista
        INSERT INTO TipoViatura (Nome, IsActive)
        VALUES (p_nome, p_isactive);
    ELSE
        RAISE NOTICE 'O Tipo de Viatura "%" já existe na tabela e não será inserido.', p_nome;
    END IF;
END;
$$;

------------------------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE registar_EstadoViatura(
    p_estado VARCHAR,
    p_isactive BOOLEAN DEFAULT TRUE
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe um registro com o mesmo Estado
    IF NOT EXISTS (
        SELECT 1 FROM EstadoViatura WHERE Estado = p_estado
    ) THEN
        -- Inserir o novo registro caso não exista
        INSERT INTO EstadoViatura (Estado, IsActive)
        VALUES (p_estado, p_isactive);
    ELSE
        RAISE NOTICE 'O Estado de Viatura "%" já existe na tabela e não será inserido.', p_estado;
    END IF;
END;
$$;

------------------------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE registar_Combustivel(
    p_nome VARCHAR,
    p_isactive BOOLEAN DEFAULT TRUE
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe um combustível com o mesmo nome (case insensitive)
    IF EXISTS (
        SELECT 1 FROM Combustivel WHERE LOWER(Nome) = LOWER(p_nome)
    ) THEN
        -- Gera um erro que será capturado no Django
        RAISE EXCEPTION 'O combustível "%" já existe!', p_nome;
    ELSE
        -- Inserir o novo combustível caso não exista
        INSERT INTO Combustivel (Nome, IsActive)
        VALUES (p_nome, p_isactive);
    END IF;
END;
$$;
------------------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE update_Combustivel(
    p_combustivelid INTEGER,
    p_nome VARCHAR,
    p_isactive BOOLEAN
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe outro combustível com o mesmo nome
    IF EXISTS (
        SELECT 1 FROM Combustivel WHERE LOWER(Nome) = LOWER(p_nome) AND ID_Combustivel != p_combustivelid
    ) THEN
        RAISE EXCEPTION 'Já existe outro combustível com este nome!';
    ELSE
        -- Atualizar o combustível
        UPDATE Combustivel
        SET Nome = p_nome, IsActive = p_isactive
        WHERE ID_Combustivel = p_combustivelid;
    END IF;
END;
$$;
------------------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE delete_Combustivel(
    p_combustivelid INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Apagar o combustível pelo ID
    DELETE FROM Combustivel WHERE ID_Combustivel = p_combustivelid;
END;
$$;


------------------------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE registar_TipoCaixa(
    p_nome VARCHAR,
    p_isactive BOOLEAN DEFAULT TRUE
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe um registro com o mesmo Nome
    IF NOT EXISTS (
        SELECT 1 FROM TipoCaixa WHERE Nome = p_nome
    ) THEN
        -- Inserir o novo registro caso não exista
        INSERT INTO TipoCaixa (Nome, IsActive)
        VALUES (p_nome, p_isactive);
    ELSE
        RAISE NOTICE 'O Tipo de Caixa "%" já existe na tabela e não será inserido.', p_nome;
    END IF;
END;
$$;

------------------------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE registar_Traccao(
    p_nome VARCHAR,
    p_isactive BOOLEAN DEFAULT TRUE
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe um registro com o mesmo Nome
    IF NOT EXISTS (
        SELECT 1 FROM Traccao WHERE Nome = p_nome
    ) THEN
        -- Inserir o novo registro caso não exista
        INSERT INTO Traccao (Nome, IsActive)
        VALUES (p_nome, p_isactive);
    ELSE
        RAISE NOTICE 'A Tracção "%" já existe na tabela e não será inserida.', p_nome;
    END IF;
END;
$$;

------------------------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE registar_EstadoReserva(
    p_estado VARCHAR,
    p_isactive BOOLEAN DEFAULT TRUE
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe um registro com o mesmo Estado
    IF NOT EXISTS (
        SELECT 1 FROM EstadoReserva WHERE Estado = p_estado
    ) THEN
        -- Inserir o novo registro caso não exista
        INSERT INTO EstadoReserva (Estado, IsActive)
        VALUES (p_estado, p_isactive);
    ELSE
        RAISE NOTICE 'O Estado de Reserva "%" já existe na tabela e não será inserido.', p_estado;
    END IF;
END;
$$;

------------------------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE registar_Cor(
    p_nome VARCHAR,
    p_isactive BOOLEAN DEFAULT TRUE
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe uma cor com o mesmo nome (case insensitive)
    IF EXISTS (
        SELECT 1 FROM Cores WHERE LOWER(Nome) = LOWER(p_nome)
    ) THEN
        -- Gera um erro que será capturado no Django
        RAISE EXCEPTION 'A cor "%" já existe!', p_nome;
    ELSE
        -- Inserir a nova cor caso não exista
        INSERT INTO Cores (Nome, IsActive)
        VALUES (p_nome, p_isactive);
    END IF;
END;
$$;



------------------------------------------------------------------------------------
-- Dar Update na cor 
CREATE OR REPLACE PROCEDURE update_Cor(
    p_corid INTEGER,
    p_nome VARCHAR,
    p_isactive BOOLEAN
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe outra cor com o mesmo nome
    IF EXISTS (
        SELECT 1 FROM Cores WHERE LOWER(Nome) = LOWER(p_nome) AND ID_Cor != p_corid
    ) THEN
        RAISE EXCEPTION 'Já existe outra cor com este nome!';
    ELSE
        -- Atualizar a cor
        UPDATE Cores
        SET Nome = p_nome, IsActive = p_isactive
        WHERE ID_Cor = p_corid;
    END IF;
END;
$$;

------------------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE delete_Cor(
    p_corid INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM Cores WHERE ID_Cor = p_corid;
END;
$$;

------------------------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE registar_TipoUtilizador(
    p_tipo VARCHAR,
    p_isactive BOOLEAN DEFAULT TRUE
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe um registro com o mesmo Tipo
    IF NOT EXISTS (
        SELECT 1 FROM TipoUtilizador WHERE Tipo = p_tipo
    ) THEN
        -- Inserir o novo registro caso não exista
        INSERT INTO TipoUtilizador (Tipo, IsActive)
        VALUES (p_tipo, p_isactive);
    ELSE
        RAISE NOTICE 'O Tipo de Utilizador "%" já existe na tabela e não será inserido.', p_tipo;
    END IF;
END;
$$;

------------------------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE registar_Viatura(
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
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validar se o ID_Traccao existe
    IF NOT EXISTS (
        SELECT 1 FROM Traccao WHERE ID_Traccao = p_id_traccao
    ) THEN
        RAISE EXCEPTION 'A tracção com ID % não existe.', p_id_traccao;
    END IF;

    -- Validar se o ID_Tipocaixa existe
    IF NOT EXISTS (
        SELECT 1 FROM TipoCaixa WHERE ID_Caixa = p_id_tipocaixa
    ) THEN
        RAISE EXCEPTION 'O tipo de caixa com ID % não existe.', p_id_tipocaixa;
    END IF;

    -- Validar se o ID_Combustivel existe
    IF NOT EXISTS (
        SELECT 1 FROM Combustivel WHERE ID_Combustivel = p_id_combustivel
    ) THEN
        RAISE EXCEPTION 'O combustível com ID % não existe.', p_id_combustivel;
    END IF;

    -- Validar se o ID_TipoViatura existe
    IF NOT EXISTS (
        SELECT 1 FROM TipoViatura WHERE ID_TipoViatura = p_id_tipo_viatura
    ) THEN
        RAISE EXCEPTION 'O tipo de viatura com ID % não existe.', p_id_tipo_viatura;
    END IF;

    -- Validar se o ID_Marca existe
    IF NOT EXISTS (
        SELECT 1 FROM Marca WHERE ID_Marca = p_id_marca
    ) THEN
        RAISE EXCEPTION 'A marca com ID % não existe.', p_id_marca;
    END IF;

    -- Validar se o ID_Modelo existe
    IF NOT EXISTS (
        SELECT 1 FROM Modelo WHERE ID_Modelo = p_id_modelo
    ) THEN
        RAISE EXCEPTION 'O modelo com ID % não existe.', p_id_modelo;
    END IF;

    -- Validar se o ID_Cor existe
    IF NOT EXISTS (
        SELECT 1 FROM Cores WHERE ID_Cor = p_id_cor
    ) THEN
        RAISE EXCEPTION 'A cor com ID % não existe.', p_id_cor;
    END IF;

    -- Validar se o ID_EstadoViatura existe
    IF NOT EXISTS (
        SELECT 1 FROM EstadoViatura WHERE ID_EstadoViatura = p_id_estado_viatura
    ) THEN
        RAISE EXCEPTION 'O estado da viatura com ID % não existe.', p_id_estado_viatura;
    END IF;

    -- Inserir a nova viatura
    INSERT INTO viatura (Matricula, Ano, KM, Cilindrada, Potencia, Portas, Lotacao, NumeroMudancas, Inspecao, IUC, Preco, ID_Traccao, ID_Tipocaixa, ID_Combustivel, ID_Tipo_Viatura, ID_Marca, ID_Modelo, ID_Cor, ID_Estado_Viatura)
  
    VALUES (
        p_matricula, p_ano, p_km, p_cilindrada, p_potencia, p_portas, p_lotacao, p_numero_mudancas, 
        p_inspecao, p_iuc, p_preco, p_id_traccao, p_id_tipocaixa, p_id_combustivel, p_id_tipo_viatura, 
        p_id_marca, p_id_modelo, p_id_cor, p_id_estado_viatura
    );

    -- Exibir mensagem de sucesso
    RAISE NOTICE 'Viatura com matrícula "%" inserida com sucesso.', p_matricula;
END;
$$;

------------------------------------------------------------------------------------

-- Criar um novo utilizador
CREATE OR REPLACE PROCEDURE registar_Utilizador(
    p_Nome VARCHAR,
    p_Password VARCHAR,
    p_ID_TipoUtilizador INTEGER,
    p_IsActive BOOLEAN DEFAULT TRUE
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar se já existe um utilizador com o mesmo nome
    IF NOT EXISTS (SELECT 1 FROM Utilizador WHERE Nome = p_Nome) THEN
        INSERT INTO Utilizador (Nome, Password, ID_TipoUtilizador, IsActive)
        VALUES (p_Nome, p_Password, p_ID_TipoUtilizador, p_IsActive);
    ELSE
        RAISE NOTICE 'O utilizador "%" já existe na tabela e não será inserido.', p_Nome;
    END IF;
END;
$$;


-- Atualizar um utilizador
CREATE OR REPLACE PROCEDURE update_Utilizador(
    p_ID_Utilizador INTEGER,
    p_Nome VARCHAR,
    p_Password VARCHAR,
    p_IsActive BOOLEAN,
    p_ID_TipoUtilizador INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE Utilizador
    SET Nome = p_Nome,
        Password = p_Password,
        IsActive = p_IsActive,
        ID_TipoUtilizador = p_ID_TipoUtilizador
    WHERE ID_Utilizador = p_ID_Utilizador;
END;
$$;

-- Eliminar um utilizador
CREATE OR REPLACE PROCEDURE delete_Utilizador(
    p_ID_Utilizador INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM Utilizador WHERE ID_Utilizador = p_ID_Utilizador;
END;
$$;