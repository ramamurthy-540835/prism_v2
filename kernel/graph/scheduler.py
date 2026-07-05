class GraphScheduler:
    def ordered(self, graph):
        completed = set()
        remaining = list(graph)
        ordered = []
        while remaining:
            ready = [node for node in remaining if all(dep in completed for dep in node.depends_on)]
            if not ready:
                raise RuntimeError("DAG contains unsatisfied dependencies")
            for node in ready:
                ordered.append(node)
                completed.add(node.id)
                remaining.remove(node)
        return ordered
