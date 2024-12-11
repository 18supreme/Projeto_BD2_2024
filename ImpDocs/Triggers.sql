
--Atualizar Stock de Peça Usada----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION atualizar_stock_peca()
RETURNS TRIGGER AS $$
BEGIN
    -- Atualiza o estoque da peça
    UPDATE Pecas
    SET Stock = Stock - NEW.Quantidade
    WHERE ID_Peca = NEW.ID_Peca;

    -- Verifica se o estoque ficou negativo
    IF (SELECT Stock FROM Pecas WHERE ID_Peca = NEW.ID_Peca) < 0 THEN
        RAISE EXCEPTION 'Estoque insuficiente para a peça %', NEW.ID_Peca;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trigger_atualizar_stock
AFTER INSERT ON Pecas_Manutencao
FOR EACH ROW
EXECUTE FUNCTION atualizar_stock_peca();

--Adicionar Stock quando uma encomenda chega!----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION atualizar_stock_apos_entrega()
RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se o estado mudou para "Entregue" (ID = 3)
    IF NEW.EstadoEncomenda_ID = 3 THEN
        -- Atualiza o stock da peça
        UPDATE Pecas
        SET Stock = Stock + NEW.Quantidade
        WHERE ID_Peca = NEW.Peca_ID;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
   
CREATE TRIGGER trigger_atualizar_stock
AFTER UPDATE OF EstadoEncomenda_ID
ON EncomendaFornecedor
FOR EACH ROW
EXECUTE FUNCTION atualizar_stock_apos_entrega();

--Quando se cria uma reserva, a viatura passar para reservada----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION atualizar_estado_viatura_para_alugado()
RETURNS TRIGGER AS $$
BEGIN
    -- Atualiza o estado da viatura para o ID correspondente ao estado "Alugado"
    UPDATE Viatura
    SET Estado_Viatura_ID = (
        SELECT ID_EstadoViatura
        FROM EstadoViatura
        WHERE Estado = 'Alugado'
        LIMIT 1
    )
    WHERE ID_Viatura = NEW.Viatura_ID;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trigger_reserva_viatura
AFTER INSERT
ON Reserva
FOR EACH ROW
EXECUTE FUNCTION atualizar_estado_viatura_para_alugado();

-- Quando se termina a reserva, a viatura passar para disponível----------------------------------------------------------------------

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
    IF NEW.EstadoReserva_ID = (
        SELECT ID_Estado_Reserva
        FROM EstadoReserva
        WHERE Estado = 'Finalizada'
    ) THEN
        UPDATE Viatura
        SET Estado_Viatura_ID = estado_disponivel_id
        WHERE ID_Viatura = NEW.Viatura_ID;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_reserva_terminada_viatura_disponivel
AFTER UPDATE OF EstadoReserva_ID
ON Reserva
FOR EACH ROW
EXECUTE FUNCTION atualizar_estado_viatura_para_disponivel();

--Após criar manutenção para uma viatura a mesma fica em manutenção----------------------------------------------------------------------

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
    SET Estado_Viatura_ID = estado_em_manutencao_id
    WHERE ID_Viatura = NEW.Viatura_ID;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Cria o trigger
CREATE TRIGGER trigger_manutencao_viatura_em_manutencao
AFTER INSERT ON Manutencao
FOR EACH ROW
EXECUTE FUNCTION atualizar_estado_viatura_para_em_manutencao();
