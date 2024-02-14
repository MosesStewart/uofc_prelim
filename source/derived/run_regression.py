import numpy as np, pandas as pd
import statsmodels.api as sm

def main():
    outdir = 'output/analysis'
    dvars = pd.read_csv('output/derived/dependent_vars.csv')
    spec1 = pd.read_csv('output/derived/first_specification.csv')
    spec2 = pd.read_csv('output/derived/second_specification.csv')

    dper_capita = dvars.loc[:, ['week0_ppc', 'week1_ppc']]
    drate = dvars.loc[:, ['week0_sp', 'week1_sp']]

    # run per capita regression
    do_regress(dvars, 'ppc', spec1, spec2, outdir)
    do_regress(dvars, 'sp', spec1, spec2, outdir)

def do_regress(dvars, method, spec1, spec2, outdir):
    output = pd.DataFrame({'Dep. Variable': spec2.columns[1:]})
    num_rows = output.shape[0]
    for wk in range(0, 2):
        output = pd.DataFrame({'Dep. Variable': spec2.columns[1:]})
        for spec in range(1, 3):
            reg = sm.OLS(dvars[f'week{wk}_{method}'].values, eval(f'spec{spec}')).fit(cov_type='HAC', cov_kwds = {'maxlags':1})
            formatted_est = np.empty((0, 1))
            formatted_se = np.empty((0, 1))
            for i in range(1, reg.pvalues.values.shape[0]):
                pval = reg.pvalues.values[i]
                est = reg.params.values[i]
                if pval <= 0.05:
                    formatted_est = np.append(formatted_est, f'{est:.3f}***')
                elif pval <= 0.10:
                    formatted_est = np.append(formatted_est, f'{est:.3f}**')
                elif pval <= 0.25:
                    formatted_est = np.append(formatted_est, f'{est:.3f}*')
                else:
                    formatted_est = np.append(formatted_est, f'{est:.3f}')
            fill = ['.' for i in range(num_rows - formatted_est.shape[0])]
            output[f' - Spec. {spec} Coeff - '] = np.concatenate([formatted_est, fill])
            formatted_se = np.array( [f'({se:.3f})' for se in reg.bse.values[1:]])
            fill = ['.' for i in range(num_rows - formatted_se.shape[0])]
            output[f'SE {spec}'] = np.concatenate([formatted_se, fill])
        output.to_latex(f'{outdir}/{method}_{wk}.txt', index = False)

if __name__ == '__main__':
    main()
