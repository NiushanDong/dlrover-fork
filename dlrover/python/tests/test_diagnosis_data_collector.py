import unittest
from dlrover.python.tests.test_utils import start_local_master
from dlrover.python.elastic_agent.master_client import (
    MasterClient,
    build_master_client,
)
from unittest.mock import patch
from dlrover.python.diagnosis.datacollector.training_log_collector import (
    TrainingLogCollector,
)
from dlrover.python.diagnosis.datacollector.xpu_timer_metric_collector import (
    XpuTimerMetricsCollector,
)
import os
from dlrover.python.common import env_utils
from dlrover.python.diagnosis.common.constants import (
    DiagnosisDataType,
    EnvConfigKey,
)
from dlrover.python.common.constants import NodeEnv, NodeType
from dlrover.python.diagnosis.common.diagnosis_data import WorkerTrainingMetric


class TestDiagnosisDataCollector(unittest.TestCase):
    def setUp(self):
        self.master_proc, self.addr = start_local_master()
        MasterClient._instance = build_master_client(self.addr, 1)

    def tearDown(self):
        os.environ.clear()

    @patch(
        "dlrover.python.diagnosis.datacollector.training_log_collector"
        ".read_last_n_lines"
    )
    def test_training_log_collector(self, mock_file_util):
        mock_file_util.return_value = [
            "test0",
            "DLRover agent started with:",
            "test1",
        ]
        training_log_collector = TrainingLogCollector(
            log_file="test", n_line=3
        )
        self.assertTrue(training_log_collector.is_enabled())
        result = training_log_collector.collect_data()
        self.assertTrue("test0" not in result.logs)
        self.assertTrue("test1" in result.logs)

    def test_xpu_timer_metric_collector(self):
        collector = XpuTimerMetricsCollector()
        self.assertFalse(collector.is_enabled())

        env_utils.set_env(EnvConfigKey.XPU_TIMER_PORT, 18889)
        collector = XpuTimerMetricsCollector()
        self.assertTrue(collector.is_enabled())

        self.assertEqual(collector.collect_data(), "")

        file = "data/xpu_timer_metrics"
        file_path = os.path.join(os.path.dirname(__file__), file)
        with open(file_path, "r", encoding="utf-8") as file:
            test_metrics = file.read()
        result = collector._preprocess_metrics(test_metrics)
        self.assertTrue(result)
        if "#" in result or "exposer" in result:
            self.fail()

        env_utils.set_env(NodeEnv.NODE_ID, 1)
        env_utils.set_env(NodeEnv.NODE_TYPE, NodeType.WORKER)
        env_utils.set_env(NodeEnv.NODE_RANK, 1)
        agent_xpu_metric = WorkerTrainingMetric(
            data_type=DiagnosisDataType.XPU_TIMER_METRIC,
            data_content=result,
            node_id=env_utils.get_node_id(),
            node_type=env_utils.get_node_type(),
            node_rank=env_utils.get_node_rank(),
        )
        self.assertEqual(
            agent_xpu_metric.data_type,
            DiagnosisDataType.XPU_TIMER_METRIC,
        )
        self.assertEqual(agent_xpu_metric.data_content, result)
        self.assertEqual(agent_xpu_metric.node_id, 1)
        self.assertEqual(agent_xpu_metric.node_type, NodeType.WORKER)
        self.assertEqual(agent_xpu_metric.node_rank, 1)
        self.assertTrue(agent_xpu_metric.timestamp > 0)