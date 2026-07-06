
class WorkflowDiffService:

    @staticmethod
    def compare(
        version_a,
        version_b
    ):

        nodes_a = {

            n["id"]

            for n in
            version_a.get(
                "nodes",
                []
            )

        }

        nodes_b = {

            n["id"]

            for n in
            version_b.get(
                "nodes",
                []
            )

        }

        edges_a = {

            (
                e["source"],
                e["target"]
            )

            for e in
            version_a.get(
                "edges",
                []
            )

        }

        edges_b = {

            (
                e["source"],
                e["target"]
            )

            for e in
            version_b.get(
                "edges",
                []
            )

        }

        return {

            "added_nodes":
                list(
                    nodes_b - nodes_a
                ),

            "removed_nodes":
                list(
                    nodes_a - nodes_b
                ),

            "added_edges":
                list(
                    edges_b - edges_a
                ),

            "removed_edges":
                list(
                    edges_a - edges_b
                )

        }
