class Agent:
    name = "agent"

    def run(self, node: dict, model: str, **kwargs) -> dict:
        raise NotImplementedError
