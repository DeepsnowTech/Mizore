class Chromosome:
    """
    Chromosome for GA
    """

    def __init__(self, genes):
        self.genes = genes
        self.fitness = -(0xFFFFFFF)