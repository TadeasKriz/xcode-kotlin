from .KonanStep import KonanStep


class KonanStepOver(KonanStep):
    def __init__(self, thread_plan, dict, *args):
        KonanStep.__init__(self, thread_plan)

    def do_queue_thread_plan(self, address, offset):
        return self.thread_plan.QueueThreadPlanForStepOverRange(address, offset)
