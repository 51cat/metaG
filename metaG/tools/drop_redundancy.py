from metaG.softs.cd_hit import CD_HIT
from metaG.core.minana import MinAna

class RedundancyRemover(MinAna):
    def __init__(
            self, 
            input_fa,
            output_fa,
            outdir, 
            word_size = 9,
            identity_threshold = 0.95,
            shorter_coverage = 0.9,
            config_file = None):
        super().__init__(outdir = outdir)
        self.input_fa  = input_fa
        self.output_fa = output_fa
        self.word_szie = word_size
        self.config_file = config_file
        self.identity_threshold = identity_threshold
        self.shorter_coverage = shorter_coverage

        self.redundancy_remove_use = "cd_hit"
        self.redundancy_remove_soft = {
                 "cd_hit":self.redundancy_remove_cd_hit
            }
        

    def set_redundancy_remove_use(self, use):
        self.predict_use = use

    def redundancy_remove_cd_hit(self):
        runner = CD_HIT(
            in_fa=self.input_fa,
            out_fa=self.output_fa,
            word_size=self.word_szie,
            shorter_coverage=self.shorter_coverage,
            config_file=self.config_file,
            cpu = self.cpu,
            memeory=self.memory
        )
        runner.run()

    def run(self):
          self.redundancy_remove_soft[self.redundancy_remove_use]()

    @property
    def unique_fa(self):
        return self.output_fa