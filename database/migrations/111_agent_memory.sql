
CREATE TABLE IF NOT EXISTS agent_memory (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    agent_id UUID NOT NULL,

    execution_id UUID,

    memory_type VARCHAR(50),

    memory TEXT,

    importance_score NUMERIC(5,2),

    metadata JSONB,

    created_at TIMESTAMP DEFAULT NOW()
);
