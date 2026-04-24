-- =============================================================
-- Extensión del modelo de datos — Servicio de Me Gusta
-- Habi · Prueba Técnica Backend
-- =============================================================
-- Tablas nuevas: user, like
-- No se modifica ninguna tabla existente.
-- =============================================================

CREATE TABLE user (
    id         INT          NOT NULL AUTO_INCREMENT,
    email      VARCHAR(255) NOT NULL,
    full_name  VARCHAR(120) NOT NULL,
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_user PRIMARY KEY (id),
    CONSTRAINT uq_user_email UNIQUE (email)
);

-- "like" es palabra reservada en MySQL; se usa backticks.
CREATE TABLE `like` (
    id          INT      NOT NULL AUTO_INCREMENT,
    user_id     INT      NOT NULL,
    property_id INT      NOT NULL,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_like PRIMARY KEY (id),

    -- Garantiza que un usuario no puede dar like dos veces al mismo inmueble.
    -- Este UNIQUE crea implícitamente un índice compuesto (user_id, property_id),
    -- que también acelera la consulta "todos los likes de un usuario".
    CONSTRAINT uq_like_user_property UNIQUE (user_id, property_id),

    CONSTRAINT fk_like_user
        FOREIGN KEY (user_id)     REFERENCES user(id)     ON DELETE CASCADE,
    CONSTRAINT fk_like_property
        FOREIGN KEY (property_id) REFERENCES property(id) ON DELETE CASCADE
);

-- Índice adicional en property_id para el ranking de popularidad.
-- El UNIQUE de arriba ya cubre (user_id, property_id); este cubre (property_id)
-- solo, que es lo que necesita: GROUP BY property_id ORDER BY COUNT(*).
CREATE INDEX idx_like_property_id ON `like` (property_id);

-- =============================================================
-- Consultas derivadas (referencia)
-- =============================================================

-- Histórico completo de likes de un usuario:
--   SELECT l.property_id, p.address, p.city, l.created_at
--   FROM `like` l
--   INNER JOIN property p ON p.id = l.property_id
--   WHERE l.user_id = ?
--   ORDER BY l.created_at DESC;

-- Ranking de popularidad (inmuebles con más likes):
--   SELECT l.property_id, p.address, COUNT(*) AS total_likes
--   FROM `like` l
--   INNER JOIN property p ON p.id = l.property_id
--   GROUP BY l.property_id, p.address
--   ORDER BY total_likes DESC;
