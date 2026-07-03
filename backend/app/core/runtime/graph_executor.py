
class GraphExecutor:

    def __init__(self, workflow):

        self.workflow = workflow

    def get_levels(self):

        levels = []

        roots = []

        for node in self.workflow.nodes:

            incoming = [

                e for e in self.workflow.edges

                if e.target == node.id

            ]

            if not incoming:

                roots.append(node.id)

        current = roots

        visited = set()

        while current:

            levels.append(current)

            next_level = []

            for node_id in current:

                visited.add(node_id)

                children = [

                    e.target

                    for e in self.workflow.edges

                    if e.source == node_id

                ]

                for child in children:

                    if child not in visited:

                        next_level.append(child)

            current = next_level

        return levels
