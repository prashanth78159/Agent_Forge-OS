
ALTER TABLE prompt_templates
ENABLE ROW LEVEL SECURITY;


CREATE POLICY prompt_select_policy
ON prompt_templates
FOR SELECT
USING (
    auth.uid() = user_id
);


CREATE POLICY prompt_insert_policy
ON prompt_templates
FOR INSERT
WITH CHECK (
    auth.uid() = user_id
);


CREATE POLICY prompt_update_policy
ON prompt_templates
FOR UPDATE
USING (
    auth.uid() = user_id
);


CREATE POLICY prompt_delete_policy
ON prompt_templates
FOR DELETE
USING (
    auth.uid() = user_id
);
