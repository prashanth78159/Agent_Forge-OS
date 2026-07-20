
CREATE TABLE IF NOT EXISTS prompt_audit_log (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    prompt_id UUID,

    user_id UUID,

    event_type VARCHAR(100),

    details JSONB,

    created_at TIMESTAMP DEFAULT NOW()
);
