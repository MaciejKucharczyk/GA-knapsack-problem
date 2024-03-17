import unittest
from unittest.mock import patch
from alghoritm import Alghoritm 
from chromosome import Chromosome

class TestAlghoritm(unittest.TestCase):
    
    @patch('random.randint')
    @patch('random.random')
    def test_CrossOver(self, mock_random, mock_randint):
        mock_random.return_value = 0.1
        fixed_cut_point = 3  # Example fixed value
        mock_randint.return_value = fixed_cut_point
        
        # Initialize algorithm and create dummy parents
        algo = Alghoritm()
        algo.base.weights = [10, 20, 30, 40]  # Assuming some weights
        parent1_content = [1, 1, 1, 1]
        parent2_content = [0, 0, 0, 0]
        parent1 = Chromosome(parent1_content)  # Assuming a Chromosome class exists
        parent2 = Chromosome(parent2_content)

        # Perform the crossover
        algo.CrossOver([parent1, parent2])

        # Assertions to verify the crossover occurred as expected with the fixed cut_point
        expected_content_after_crossover_parent1 = [0, 0, 0, 1]  # Assuming how crossover modifies the content
        expected_content_after_crossover_parent2 = [1, 1, 1, 0]

        self.assertEqual(parent1.content, expected_content_after_crossover_parent1)
        self.assertEqual(parent2.content, expected_content_after_crossover_parent2)

    @patch('random.random')
    @patch('random.randint')
    def test_Mutation(self, mock_randint, mock_random):
        # Setup to ensure mutation always occurs
        mock_random.return_value = 0  # Assuming mutation_rate is > 0, to ensure mutation happens

        # Configure mock_randint to return different values for each call
        mock_randint.side_effect = [2, 3]  # First call to randint returns 2, second call returns 3

        # Initialize algorithm and create a dummy chromosome
        algo = Alghoritm()
        algo.content_len = 5  # Assuming content length
        chromosome = Chromosome([0, 1, 1, 0, 1])  # Assuming a Chromosome class exists and initial content

        # Perform the mutation
        algo.Mutation(chromosome)

        # Assertions to verify the mutation occurred as expected with the predetermined indexes
        # Expected result is based on swapping the elements at indexes 2 and 3
        expected_content_after_mutation = [0, 1, 0, 1, 1]  # Assuming how mutation modifies the content

        self.assertEqual(chromosome.content, expected_content_after_mutation)
            
            
            
if __name__ == '__main__':
    unittest.main()
