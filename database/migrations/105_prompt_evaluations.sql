
CREATE TABLE IF NOT EXISTS prompt_evaluations (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    prompt_id UUID,

    score NUMERIC(5,2),

    feedback TEXT,

    reviewer VARCHAR(100),

    created_at TIMESTAMP DEFAULT NOW()
);
