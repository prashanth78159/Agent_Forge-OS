
CREATE TABLE IF NOT EXISTS prompt_versions (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    prompt_id UUID NOT NULL,

    version INTEGER NOT NULL,

    prompt TEXT NOT NULL,

    change_notes TEXT,

    created_by UUID,

    created_at TIMESTAMP DEFAULT NOW()
);
