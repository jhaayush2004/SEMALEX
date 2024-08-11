import unittest
from evaluator import EnhancedEvaluator

class TestRAGEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = EnhancedEvaluator()

    def test_evaluate_all(self):
        response = "There is a huge impact of human activities on climate. Some of these activities are burning fossil fuels, mining and so on."
        reference = "Human activities such as burning fossil fuels cause climate change."
        metrics = self.evaluator.evaluate_all(reference, response)
        for metric_name, metric_value in metrics.items():
            print(f"{metric_name}: {metric_value}")
        self.assertIsInstance(metrics, dict)
        self.assertIn("SemaLex", metrics)

if __name__ == '__main__':
    unittest.main()