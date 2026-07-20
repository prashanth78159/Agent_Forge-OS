
CREATE TABLE IF NOT EXISTS agent_conversations (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    agent_id UUID NOT NULL,

    role VARCHAR(30),

    message TEXT,

    created_at TIMESTAMP DEFAULT NOW()
);
