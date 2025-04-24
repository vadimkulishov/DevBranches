import unittest
from frontend.models.quiz_model import QuizModel

class QuizModelTestCase(unittest.TestCase):

    def setUp(self):
        self.model = QuizModel()
        self.model.questions = [
            {"question": "Question 1", "options": ["A", "B", "C", "D"], "correct_answer": 0},
            {"question": "Question 2", "options": ["A", "B", "C", "D"], "correct_answer": 1}
        ]

    def test_get_current_question(self):
        question = self.model.get_current_question()
        self.assertEqual(question["question"], "Question 1")

    def test_check_answer_correct(self):
        result = self.model.check_answer(0)
        self.assertTrue(result)
        self.assertEqual(self.model.get_score(), 500)

    def test_check_answer_incorrect(self):
        result = self.model.check_answer(1)
        self.assertFalse(result)
        self.assertEqual(self.model.score, 0)

    def test_next_question(self):
        self.model.next_question()
        question = self.model.get_current_question()
        self.assertEqual(question["question"], "Question 2")

    def test_is_finished(self):
        self.model.next_question()
        self.assertFalse(self.model.is_finished())
        self.model.next_question()
        self.assertTrue(self.model.is_finished())

if __name__ == '__main__':
    unittest.main()