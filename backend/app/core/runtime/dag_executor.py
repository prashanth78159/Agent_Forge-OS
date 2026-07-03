
class DAGExecutor:

    def __init__(
        self,
        nodes,
        edges
    ):

        self.nodes = nodes
        self.edges = edges

    def get_dependencies(
        self,
        node_id
    ):

        return [

            edge["source"]

            for edge in self.edges

            if edge["target"] == node_id

        ]

    def get_ready_nodes(
        self,
        completed
    ):

        ready = []

        for node in self.nodes:

            deps = self.get_dependencies(
                node["id"]
            )

            if all(
                dep in completed
                for dep in deps
            ):

                if (
                    node["id"]
                    not in completed
                ):

                    ready.append(node)

        return ready
