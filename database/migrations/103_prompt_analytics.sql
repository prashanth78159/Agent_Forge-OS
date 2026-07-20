
CREATE TABLE IF NOT EXISTS prompt_analytics (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    prompt_id UUID,

    executions INTEGER DEFAULT 0,

    total_tokens BIGINT DEFAULT 0,

    total_cost NUMERIC(12,6) DEFAULT 0,

    avg_latency_ms INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT NOW(),

    updated_at TIMESTAMP DEFAULT NOW()
);
