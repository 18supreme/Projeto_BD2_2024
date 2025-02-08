
------------------------------------------------------------------------------------------------------------------------------------------------

-- Quando se cria uma reserva, a viatura passar para reservada
CREATE OR REPLACE FUNCTION atualizar_estado_viatura_para_alugado()
RETURNS TRIGGER AS $$
BEGIN
    -- Atualiza o estado da viatura para o ID correspondente ao estado "Alugado"
    UPDATE Viatura
    SET id_estado_viatura = (
        SELECT ID_EstadoViatura
        FROM EstadoViatura
        WHERE Estado = 'Alugado'
        LIMIT 1
    )
    WHERE ID_Viatura = NEW.ID_Viatura;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_reserva_viatura
AFTER INSERT
ON Reserva
FOR EACH ROW
EXECUTE FUNCTION atualizar_estado_viatura_para_alugado();

------------------------------------------------------------------------------------------------------------------------------------------------

-- Quando se termina a reserva, a viatura passar para disponível
CREATE OR REPLACE FUNCTION atualizar_estado_viatura_para_disponivel()
RETURNS TRIGGER AS $$
DECLARE
    estado_disponivel_id INTEGER;
BEGIN
    -- Obtemos o ID do estado "Disponível" na tabela EstadoViatura
    SELECT ID_EstadoViatura
    INTO estado_disponivel_id
    FROM EstadoViatura
    WHERE Estado = 'Disponível';

    --Se o novo estado da reserva for "Finalizada", atualizamos a viatura
    IF NEW.ID_reserva = (
        SELECT ID_Estado_Reserva
        FROM EstadoReserva
        WHERE Estado = 'Finalizada'
    ) THEN
        UPDATE Viatura
        SET id_estado_viatura = estado_disponivel_id
        WHERE ID_Viatura = NEW.ID_Viatura;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_reserva_terminada_viatura_disponivel
AFTER UPDATE OF ID_EstadoReserva
ON Reserva
FOR EACH ROW
EXECUTE FUNCTION atualizar_estado_viatura_para_disponivel();

------------------------------------------------------------------------------------------------------------------------------------------------

-- Após criar manutenção para uma viatura a mesma fica em manutenção
CREATE OR REPLACE FUNCTION atualizar_estado_viatura_para_em_manutencao()
RETURNS TRIGGER AS $$
DECLARE
    estado_em_manutencao_id INTEGER;
BEGIN
    -- Obtemos o ID do estado "Em manutenção" na tabela EstadoViatura
    SELECT ID_EstadoViatura
    INTO estado_em_manutencao_id
    FROM EstadoViatura
    WHERE Estado = 'Em manutenção';

    -- Atualizamos o estado da viatura associada
    UPDATE Viatura
    SET ID_Estado_Viatura = estado_em_manutencao_id
    WHERE ID_Viatura = NEW.ID_Viatura;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Cria o trigger
CREATE OR REPLACE TRIGGER trigger_manutencao_viatura_em_manutencao
AFTER INSERT ON Manutencao
FOR EACH ROW
EXECUTE FUNCTION atualizar_estado_viatura_para_em_manutencao();

-----------------------------------------------------------------------------------------------
--Atualizar o Valor de fornecedor quando faço uma encomenda entregue

CREATE OR REPLACE FUNCTION atualizar_valor_fornecedor()
RETURNS TRIGGER AS $$
BEGIN
    -- Só atualizar se o estado da nova encomenda for "Entregue"
    IF NEW.ID_EstadoEncomenda = (SELECT ID_EstadoEncomenda FROM EstadoEncomendaFornecedor WHERE Estado = 'Entregue') THEN
        UPDATE Fornecedor
        SET Valor = Valor + NEW.Valor
        WHERE ID_Fornecedor = NEW.ID_Fornecedor;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Criar o trigger para só atualizar o fornecedor quando a encomenda é criada no estado "Entregue"
CREATE TRIGGER trigger_atualizar_valor_fornecedor
AFTER INSERT ON EncomendaFornecedor
FOR EACH ROW
EXECUTE FUNCTION atualizar_valor_fornecedor();

-- Criar a função  para subtrair o valor apenas uma vez ao eliminar a encomenda
CREATE OR REPLACE FUNCTION remover_valor_fornecedor()
RETURNS TRIGGER AS $$
BEGIN
    -- Só remover o valor do fornecedor se a encomenda eliminada estava no estado "Entregue"
    IF OLD.ID_EstadoEncomenda = (SELECT ID_EstadoEncomenda FROM EstadoEncomendaFornecedor WHERE Estado = 'Entregue') THEN
        UPDATE Fornecedor
        SET Valor = Valor - OLD.Valor
        WHERE ID_Fornecedor = OLD.ID_Fornecedor;
    END IF;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Criar o trigger para remover o valor só se a encomenda eliminada estava como "Entregue"
CREATE TRIGGER trigger_remover_valor_fornecedor
AFTER DELETE ON EncomendaFornecedor
FOR EACH ROW
EXECUTE FUNCTION remover_valor_fornecedor();



------------------------------------------------------------------------------------------------------------------------------------

-- Criar função para atualizar o stock quando uma encomenda for criada ou editada
-- Criação da função que será chamada pelo trigger
CREATE OR REPLACE FUNCTION atualizar_stock_apos_entrega()
RETURNS TRIGGER 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Apenas atualizar o stock se o novo estado for "Entregue" (substituir pelo ID correto)
    IF NEW.ID_EstadoEncomenda = (SELECT ID_EstadoEncomenda FROM EstadoEncomendaFornecedor WHERE Estado = 'Entregue') THEN
        UPDATE Pecas 
        SET Stock = Stock + NEW.Quantidade
        WHERE ID_Peca = NEW.ID_Peca;
    END IF;
    
    RETURN NEW;
END;
$$;

-- Criação do trigger
CREATE TRIGGER trigger_atualizar_stock
AFTER UPDATE ON EncomendaFornecedor
FOR EACH ROW
WHEN (OLD.ID_EstadoEncomenda IS DISTINCT FROM NEW.ID_EstadoEncomenda)  -- Apenas quando o estado muda
EXECUTE FUNCTION atualizar_stock_apos_entrega();


-- Criar função para atualizar o stock ao eliminar uma encomenda
CREATE OR REPLACE FUNCTION reduzir_stock_pecas()
RETURNS TRIGGER AS $$
DECLARE
    v_estado_entregue INTEGER;
BEGIN
    -- Buscar o ID do estado "Entregue"
    SELECT ID_EstadoEncomenda INTO v_estado_entregue
    FROM EstadoEncomendaFornecedor
    WHERE Estado = 'Entregue';

    -- Se a encomenda estava "Entregue", reduzir do stock
    IF OLD.ID_EstadoEncomenda = v_estado_entregue THEN
        UPDATE Pecas
        SET Stock = Stock - OLD.Quantidade
        WHERE ID_Peca = OLD.ID_Peca;
    END IF;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Criar o Trigger para chamar a função ao excluir encomendas
CREATE TRIGGER trigger_reduzir_stock_pecas
BEFORE DELETE ON EncomendaFornecedor
FOR EACH ROW
EXECUTE FUNCTION reduzir_stock_pecas();

------------------------------------------------------------------------------------------------------------------------------------------------

----ATENÇAO ISTO APAGA TRIGGERS E FUNÇÕES-----
DO $$ 
DECLARE 
    r RECORD;
BEGIN 
    FOR r IN (
        SELECT tgname, relname 
        FROM pg_trigger 
        JOIN pg_class ON pg_trigger.tgrelid = pg_class.oid
        WHERE NOT tgisinternal
    ) 
    LOOP 
        EXECUTE 'DROP TRIGGER IF EXISTS ' || r.tgname || ' ON ' || r.relname || ' CASCADE;';
    END LOOP;
END $$;
------------------------------------------------------------------------------------------------------------------------------------------------