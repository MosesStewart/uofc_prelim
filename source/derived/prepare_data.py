import numpy as np, pandas as pd

def main():
    indir, outdir = 'source/raw', 'output/derived'
    col_rename = {'share_cat1': 'Essential - Pro', 'share_cat2': 'Nonessential - Pro', 'share_cat3': 'Science', 
                    'share_cat4': 'Legal', 'share_cat5': 'Health Practice', 'share_cat6': 'Health Other',
                    'share_cat7': 'Firefighters', 'share_cat8': 'Law Enforcement', 'share_cat9': 'Essential - Service', 
                    'share_cat10': 'Nonessential - Service', 'share_cat11': 'Industrial', 'share_cat12': 'Essential - Tech',
                    'share_cat13': 'Transportation'}
    init_keep = {'log_density': 'Log Density', 'log_commute_time': 'Log Commute Time', 'log_household_size': 'Log Household Size', 'share_male': 'Share Male'}
    trans_keep = {'share_hispanic': 'Share Hispanic', 'share_black': 'Share Black', 'share_asian': 'Share Asian', 'share_20_40': 'Share 20-40', 'share_40_60': 'Share 40-60', 'share_above_60': 'Share $>$60'}
    weeks = [(404, 410), (516, 522)]
    # postive_per_capita, share_positive
    data = pd.read_stata(f'source/raw/metricsgame2.dta')
    data = data.dropna()

    loc_data = pd.DataFrame({'lat': data['lat'].values, 'lon': data['lng'].values})
    loc_data.to_csv(f'{outdir}/lat_lon.csv', index = False)
    
    init_data = pd.DataFrame({'bias': np.ones((data.shape[0]))})
    for col in init_keep:
        init_data[init_keep[col]] = data[col].values
    for col in trans_keep:
        init_data[trans_keep[col]] = data[col].values/100
    init_data['Log Mean Income'] = np.log(data['mean_income'].values)
    init_data['Share Pub. Trans.'] = data['public'].values
    init_data['Uninsured'] = data['uninsured'].values
    init_data.to_csv(f'{outdir}/first_specification.csv', index = False)

    all_data = init_data
    for col in col_rename:
        all_data[col_rename[col]] = data[col].values
    all_data.to_csv(f'{outdir}/second_specification.csv', index = False)

    dependent_vars = pd.DataFrame(columns = ['week0_ppc', 'week0_sp', 'week1_ppc', 'week1_sp'])
    for i in range(len(weeks)):
        week = weeks[i]
        week_ppc = data[f'positive_per_capita_0{week[0]}'].values
        week_share_pos = data[f'share_positive_0{week[0]}'].values
        for day in range(week[0] + 1, week[1] + 1):
            if day == 406 or day == 520:
                pass
            else:
                week_ppc = np.column_stack([week_ppc, data[f'positive_per_capita_0{day}'].values])
                week_share_pos = np.column_stack([week_share_pos, data[f'share_positive_0{day}'].values])
        dependent_vars[f'week{i}_ppc'] = np.mean(week_ppc, axis = 1)
        dependent_vars[f'week{i}_sp'] = np.mean(week_share_pos, axis = 1)

    dependent_vars.to_csv(f'{outdir}/dependent_vars.csv', index = False)

if __name__ == '__main__':
    main()
