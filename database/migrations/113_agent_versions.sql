
CREATE TABLE IF NOT EXISTS agent_versions (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    agent_id UUID NOT NULL,

    version INTEGER NOT NULL,

    configuration JSONB,

    created_at TIMESTAMP DEFAULT NOW()
);
