
class Parser:

    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):

        nodes = []
        edges = []

        agent_name = "workflow"

        for i in range(len(self.tokens)):

            token = self.tokens[i]

            if (
                token["type"] == "IDENT"
                and token["value"] == "agent"
            ):

                if i + 1 < len(self.tokens):
                    agent_name = self.tokens[i + 1]["value"]

        return {
            "name": agent_name,
            "nodes": nodes,
            "edges": edges
        }
