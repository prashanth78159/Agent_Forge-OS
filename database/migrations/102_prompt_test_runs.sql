
CREATE TABLE IF NOT EXISTS prompt_test_runs (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    prompt_id UUID,

    user_id UUID,

    provider VARCHAR(50),

    model VARCHAR(100),

    input_data JSONB,

    response TEXT,

    latency_ms INTEGER,

    token_usage INTEGER,

    estimated_cost NUMERIC(12,6),

    created_at TIMESTAMP DEFAULT NOW()
);
