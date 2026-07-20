
CREATE TABLE IF NOT EXISTS agent_templates (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    name VARCHAR(255) NOT NULL,

    description TEXT,

    system_prompt TEXT NOT NULL,

    provider VARCHAR(50),

    model VARCHAR(100),

    tools JSONB,

    memory_enabled BOOLEAN DEFAULT FALSE,

    knowledge_enabled BOOLEAN DEFAULT FALSE,

    status VARCHAR(50) DEFAULT 'DRAFT',

    version INTEGER DEFAULT 1,

    created_at TIMESTAMP DEFAULT NOW(),

    updated_at TIMESTAMP DEFAULT NOW()
);
