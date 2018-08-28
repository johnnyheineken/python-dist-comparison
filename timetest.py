import numpy as np
import pandas as pd
import sklearn
import timeit



def test(test_cases, setup, name, REP, NUM, array_length):
    results = pd.DataFrame()
    counter = 0
    for case, code in test_cases.items():
        
        timing=timeit.Timer(code, setup=setup)
        result = timing.repeat(repeat=REP, number=NUM)

        mean = np.mean(result)
        best = np.min(result)
        best_single_run  = int((best * 1e9)/ NUM)
        avg_single_run  = int((mean * 1e9)/ NUM)

        result_string  = f'Case: {case} | array length: {array_length} | best run out of {REP} runs: {best_single_run} usec/loop '
        print(result_string)
        results[case] = [name, array_length, NUM, mean, best, best_single_run, avg_single_run]
        counter += 1
    return results


for counter, array_length in enumerate([10 ** (10-i) for i in range(4, 8)]):
    setup_intel = """
import numpy as np
import math
array_a = np.random.randn({0})
array_b = np.random.randn({0})
scalar = np.random.random(1)
scalar_number = np.asscalar(scalar)
    """.format(array_length)


    cases_intel = {'array-array': 'array_a - array_b', 
            'array-scalar': 'array_a - scalar', 
            'array*array': 'array_a * array_b',
            'array*scalar': 'array_a * scalar',
            'array+array': 'array_a + array_b',
            'array+scalar': 'array_a + scalar', 
            'erf': 'math.erf(scalar)',
            'erf_number': 'math.erf(scalar_number)', 
            'exp': 'np.exp(scalar)',
            'exp_number': 'np.exp(scalar_number)',
            'invsqrt': 'scalar ** -.05',
            'invsqrt_number': 'scalar_number ** -.05',
            'log10': 'np.log10(scalar)',
            'log10_number': 'np.log10(scalar_number)'}


    intel_res = test(cases_intel, setup_intel, 'intel', REP=(counter+1), NUM=(10 ** (counter + 2)), array_length=array_length)


    setup_pandas = """
import pandas as pd
import numpy as np
array_a = pd.DataFrame(np.random.randn({0}))
array_b = pd.DataFrame(np.random.randn({0}))
a_bool = array_a < 0
b_bool = array_b > 0
fn = lambda x: x < 0
df = pd.concat([array_a, array_b, a_bool, b_bool], axis=1)
df.columns = ['a', 'b', 'c', 'd']
    """.format(array_length)

    cases_pandas = {
        'array+array': 'array_a + array_b',
        'array-array': 'array_a - array_b',
        'array*array': 'array_a * array_b',
        'array < 0': 'array_a < 0', 
        'array > 0': 'array_b > 0',
        'array or array': 'a_bool | b_bool',
        'array and array': 'a_bool & b_bool',
        'array apply': 'array_a.apply(fn)',
        'subseries+subseries': 'df["a"] + df["b"]',
        'subseries*subseries': 'df["a"] * df["b"]',
        'subseries-subseries': 'df["a"] - df["b"]',
        'concat arrays': 'pd.concat([array_a, array_b, a_bool, b_bool], axis=1)', 
        'df groupby max': "df.groupby(['c', 'd']).max()"
            }

    pandas_res = test(cases_pandas, setup_pandas, 'pandas', REP=(counter+1), NUM=(5 ** (counter + 2)), array_length=array_length)


    setup_sklearn = """
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import LinearSVC, SVC

x1 = pd.Series((np.random.randn({0}) + 3) * 2)
x2 = pd.Series((np.random.randn({0}) - 2) / 3)
x3 = pd.Series((np.random.randn({0}) - 1) * 3)
y = -x1 + 5 * x2 + x3 + x1 * x3 * x2
target = y  < 0

X = pd.DataFrame()
X['x1']=x1
X['x2']=x2
X['x3']=x3
clf1 = LogisticRegression().fit(X=X, y=target)
clf2 = AdaBoostClassifier().fit(X=X, y=target)
    """.format(array_length)

    cases_sklearn = {
                'LogReg': 'LogisticRegression(n_jobs=-1).fit(X=X, y=target)',
                'AdaBoost': 'AdaBoostClassifier().fit(X=X, y=target)',
                'RandomForest': 'RandomForestClassifier(n_jobs=-1).fit(X=X, y=target)',
                'GBM': 'GradientBoostingClassifier().fit(X=X, y=target)',
                # 'LinearSVC': 'LinearSVC().fit(X=X, y=target)',
                # 'SVC': 'SVC().fit(X=X, y=target)',
                'predictionLR': 'clf1.predict(X)',
                'predictionAda': 'clf2.predict(X)'
                }


    sklearn_res = test(cases_sklearn, setup_sklearn, 'sklearn', REP=(counter+1), NUM=(2 ** (counter + 2)), array_length=array_length)
    result_temp=pd.concat([intel_res, pandas_res, sklearn_res], axis=1)
    result_temp.to_csv(f"result{array_length}.csv")
    if counter == 0:
        result = result_temp
    else:
        result = pd.concat([result, result_temp], axis=1)

result.to_csv('result_all.csv')
