
CREATE TABLE IF NOT EXISTS prompt_templates (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    name VARCHAR(250) NOT NULL,

    description TEXT,

    category VARCHAR(100),

    prompt TEXT NOT NULL,

    version INTEGER DEFAULT 1,

    status VARCHAR(50) DEFAULT 'DRAFT',

    created_at TIMESTAMP DEFAULT NOW(),

    updated_at TIMESTAMP DEFAULT NOW()
);
