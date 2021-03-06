import numpy as np
import pandas as pd

from model import MainClauseModel

class MainClauseExperiment(object):

    def __init__(self, data, seed=25472):
        self._data = data
        self._seed = seed

        np.random.seed(seed)

    def _initialize_models(self):
        self._models = {c: [MainClauseModel()
                            for _ in np.arange(self._niters)]
                        for c in self._data.keys()}

    def run(self, niters=10): #DEFAULT 10
        self._niters = niters
        self._initialize_models()
        
        for c, m in self._models.items():
            for i in np.arange(self._niters):
                print(c, i)
                m[i].fit(self._data[c])

    @property
    def results(self):  # NH: add data about feature probs for validation
        try:
            return self._results_verbreps, self._results_projection, self._featureprobs
        except AttributeError:        
            results_verbreps = []
            results_projection = []
            results_feature_probs = [] # NH: added

            for c, m in self._models.items():
                for i in np.arange(self._niters):        
                    vh = m[i].verbreps_history
                    ph = m[i].projection_history
                    fp = m[i].feature_prob # NH: added
                    

                    vh['child'] = c
                    ph['child'] = c
                    fp['child'] = c # NH: added

                    vh['itr'] = i
                    ph['itr'] = i
                    fp['itr'] = i # NH: added

                    results_verbreps.append(vh)
                    results_projection.append(ph)
                    results_feature_probs.append(fp)

            self._results_verbreps = pd.concat(results_verbreps, sort = True) # ADDED sort = True 
            self._results_projection = pd.concat(results_projection, sort = True) # ADDED sort = True 
            self._results_feature_probs = pd.concat(results_feature_probs, sort = True) # NH: added

            return self._results_verbreps, self._results_projection, self._results_feature_probs

def main():
    import data, datamc
    import argparse
    # Toggle language options. Note that the penalty has to be manually toggled in model.py
    parser = argparse.ArgumentParser(description='Run bootstrapping model.')
    parser.add_argument('-l', '--language', action='store', choices=['en', 'mc'], default='en', help='Set language')
    lg = parser.parse_args().language
    print('Language selected:\t', lg)
    
    if lg == 'en':
        data = data.main()
    elif lg == 'mc':
        data = datamc.main()
    
    exp = MainClauseExperiment(data)
    exp.run()

    verbreps, projection, results_feature_probs = exp.results # NH: added feature probs

    verbs = ['want', 'see', 'know', 'think', 'say', 'like', 'tell', 'try', 'need', 'remember',
             'DECLARATIVE', 'IMPERATIVE', '要', '看', '说', '看看', '讲', '想', '知道', '叫', '喜欢', '告诉', '帮', '让', '觉得','准备']
			 # Chinese:
			 # 'DECLARATIVE', 'IMPERATIVE', 'yao want', 'kan see', 'shuo say', 'kankan see-REDUP' ("look, try looking"), 'jiang say, tell', 'xiang think/want', 'zhidao know', 'jiao call, get', 'xihuan like', 'gaosu tell', 'bang help', 'rang let', 'juede feel',
    
    verbreps[verbreps.verb.isin(verbs)].to_csv('../bin/results/verbreps_results'+lg+'.csv', index=False)
    projection.to_csv('../bin/results/projection_results'+lg+'.csv', index=False)
    results_feature_probs.to_csv('../bin/results/featureprobs_results'+lg+'.csv', index=False) # NH: added feature probs

    return exp

if __name__ == '__main__':
    exp = main()
    
