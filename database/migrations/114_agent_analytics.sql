
CREATE TABLE IF NOT EXISTS agent_analytics (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    agent_id UUID,

    total_runs INTEGER DEFAULT 0,

    total_tokens BIGINT DEFAULT 0,

    total_cost NUMERIC(12,6) DEFAULT 0,

    avg_latency_ms INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT NOW()
);
