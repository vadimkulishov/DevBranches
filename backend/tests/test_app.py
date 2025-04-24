import unittest
from backend.quiz import Quiz


class QuizTestCase(unittest.TestCase):

    def setUp(self):
        self.quiz = Quiz()

    def test_initial_score(self):
        self.assertEqual(self.quiz.score, 0)

    def test_add_question(self):
        self.quiz.add_question("What is 2+2?", ["3", "4", "5"], 1)
        self.assertEqual(len(self.quiz.questions), 1)


if __name__ == '__main__':
    unittest.main()
