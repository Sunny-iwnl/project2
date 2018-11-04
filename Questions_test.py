import unittest
from Questions import Questions # from Questions file, import Questions class
 
class test_Questions(unittest.TestCase):
    
    def test_getQuestion(self):
        test_question = Questions() # creates object from Questions class named test question

        test_question.getSpecificQuestion(1)
        self.assertEqual(test_question.getQuestion(), "In which Asian country \
is the city of Chiang Mai located?\n a. China\n b. Thailand\n c. Cambodia\n d. Japan\n")
        # test to see if fixNewLine adds new \n characters
        self.assertNotEqual(test_question.getQuestion(), "In which Asian country \
is the city of Chiang Mai located?\n a. China\n b. Thailand\n c. Cambodia\n d. Japan")

    def test_solution(self):
        test_question = Questions()

        test_question.getSpecificQuestion(1) # question is question 1 from csv
        self.assertEqual(test_question.trySolution("b"), True)
        self.assertEqual(test_question.trySolution("a"), False)
        #self.assertEqual(test_question.trySolution("B"), True) # test if uppercase is okay
        
        test_question.getSpecificQuestion(2) # question is question 2 from csv
        self.assertEqual(test_question.trySolution("c"), True)
        self.assertEqual(test_question.trySolution("d"), False)


if __name__ == '__main__':
    unittest.main()
