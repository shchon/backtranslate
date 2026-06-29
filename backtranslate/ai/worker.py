from queue import Queue
from PySide6.QtCore import QThread, Signal, QObject

from .client import call_ai

MAX_RETRIES = 3


class EvaluationWorker(QObject):
    evaluation_done = Signal(int, object)   # eval_id, result_dict
    evaluation_failed = Signal(int)         # eval_id

    def __init__(self, base_url: str, api_key: str, model: str, prompt_template: str):
        super().__init__()
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.prompt_template = prompt_template
        self.queue: Queue = Queue()
        self._retries: dict[int, int] = {}

    def add_task(self, eval_id: int, translation_id: int,
                 user_input: str, official: str, context: str) -> None:
        task = {
            "eval_id": eval_id,
            "translation_id": translation_id,
            "user_input": user_input,
            "official": official,
            "context": context,
        }
        self.queue.put(task)

    def process_next(self) -> None:
        if self.queue.empty():
            return
        task = self.queue.get()

        result = call_ai(
            self.base_url, self.api_key, self.model,
            self.prompt_template, task["context"],
            task["user_input"], task["official"],
        )

        if result is not None:
            self.evaluation_done.emit(task["eval_id"], result)
            self._retries.pop(task["eval_id"], None)
        else:
            retries = self._retries.get(task["eval_id"], 0) + 1
            if retries <= MAX_RETRIES:
                self._retries[task["eval_id"]] = retries
                self.queue.put(task)
            else:
                self._retries.pop(task["eval_id"], None)
                self.evaluation_failed.emit(task["eval_id"])


class EvaluationThread(QThread):
    def __init__(self, worker: EvaluationWorker):
        super().__init__()
        self.worker = worker
        self._running = False

    def run(self) -> None:
        """Process queue items directly on this worker thread, blocking call_ai won't freeze UI."""
        self._running = True
        while self._running:
            self.worker.process_next()
            self.msleep(100)

    def stop(self) -> None:
        self._running = False
