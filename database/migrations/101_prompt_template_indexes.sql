
CREATE INDEX IF NOT EXISTS idx_prompt_templates_user
ON prompt_templates(user_id);

CREATE INDEX IF NOT EXISTS idx_prompt_templates_status
ON prompt_templates(status);

CREATE INDEX IF NOT EXISTS idx_prompt_templates_category
ON prompt_templates(category);
