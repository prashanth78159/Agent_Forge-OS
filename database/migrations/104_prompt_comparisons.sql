
CREATE TABLE IF NOT EXISTS prompt_comparisons (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID,

    prompt_a UUID,

    prompt_b UUID,

    provider VARCHAR(50),

    model VARCHAR(100),

    result JSONB,

    created_at TIMESTAMP DEFAULT NOW()
);
