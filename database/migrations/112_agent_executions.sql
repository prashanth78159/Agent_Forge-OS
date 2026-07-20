
CREATE TABLE IF NOT EXISTS agent_executions (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    agent_id UUID NOT NULL,

    input_text TEXT,

    output_text TEXT,

    provider VARCHAR(50),

    model VARCHAR(100),

    tokens_used INTEGER,

    execution_status VARCHAR(50),

    created_at TIMESTAMP DEFAULT NOW()
);
