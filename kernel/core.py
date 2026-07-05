from kernel.boot import BootLoader
from kernel.types import KernelRequest

class PrismKernel:
    def __init__(self):
        self.boot = BootLoader()
        self.boot.initialize()

    def run(self, task: str, operation: str | None = None, context: dict | None = None):
        request = KernelRequest(task=task, operation=operation or "plan", context=context or {})
        return self.boot.execute(request).to_dict()
