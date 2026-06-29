from unittest.mock import patch
from backtranslate.ai.worker import EvaluationWorker


def test_worker_process_queue_success(qtbot):
    worker = EvaluationWorker(
        base_url="http://test/v1",
        api_key="sk-test",
        model="test-model",
        prompt_template="Rate: {user_input}",
    )

    fake_result = {
        "meaning_score": 90,
        "grammar_score": 85,
        "naturalness_score": 80,
        "subtitle_style_score": 75,
        "analysis": "ok",
        "suggested_expressions": ["test"],
    }

    with patch("backtranslate.ai.worker.call_ai", return_value=fake_result):
        worker.add_task(1, 10, "hello", "hi", "context text")
        assert worker.queue.qsize() == 1

        eval_received = {}

        def on_done(eval_id, result):
            eval_received["id"] = eval_id
            eval_received["result"] = result

        worker.evaluation_done.connect(on_done)
        worker.process_next()

        assert eval_received["id"] == 1
        assert eval_received["result"]["meaning_score"] == 90


def test_worker_retry_on_failure(qtbot):
    worker = EvaluationWorker(
        base_url="http://test/v1",
        api_key="sk-test",
        model="test-model",
        prompt_template="Rate: {user_input}",
    )

    with patch("backtranslate.ai.worker.call_ai", return_value=None):
        worker.add_task(1, 20, "hello", "hi", "")

        fail_received = {}

        def on_fail(eval_id):
            fail_received["id"] = eval_id

        worker.evaluation_failed.connect(on_fail)

        # Process 4 times (1 initial + 3 retries = 4 attempts, all fail -> emit failed)
        for _ in range(4):
            worker.process_next()

    assert fail_received.get("id") == 1
