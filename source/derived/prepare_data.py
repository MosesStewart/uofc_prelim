import numpy as np, pandas as pd

def main():
    indir, outdir = 'source/raw', 'output/derived'
    col_rename = {'share_cat1': 'share_pro_essential', 'share_cat2': 'share_pro_nonessential', 'share_cat3': 'share_science', 
                    'share_cat4': 'share_legal', 'share_cat5': 'share_caregiver', 'share_cat6': 'share_health',
                    'share_cat7': 'share_fire', 'share_cat8': 'share_police', 'share_cat9': 'share_reg_essential', 
                    'share_cat10': 'share_reg_nonessential', 'share_cat11': 'share_industrial', 'share_cat12': 'share_tec_essential',
                    'share_cat13': 'share_transportation'}
    init_keep = ['log_density', 'share_hispanic', 'share_white', 'share_black', 'share_asian', 'share_below_20', 'share_20_40', 'share_40_60', 
            'share_above_60', 'log_commute_time', 'household_size', 'share_male']
    weeks = [(404, 410), (516, 522)]
    # postive_per_capita, share_positive
    data = pd.read_stata(f'{indir}/metricsgame2.dta')

    loc_data = pd.DataFrame({'lat': data['lat'], 'lon': data['lng']})
    loc_data.to_csv(f'{outdir}/lat_lon.csv', index = False)

    init_keep = ['log_density', 'share_hispanic', 'share_white', 'share_black', 'share_asian', 'share_below_20', 'share_20_40', 'share_40_60', 
                'share_above_60', 'log_commute_time', 'household_size', 'share_male']
    init_data = pd.DataFrame({'uninsured': data['uninsured']})
    for col in init_keep:
        init_data[col] = data[col]
    init_data['log_mean_income'] = np.log(data['mean_incomce'].values)
    init_data['share_public_trans'] = data['public']
    init_data.to_csv(f'{outdir}/first_specification.csv', index = False)

    all_data = init_data
    for col in col_rename:
        all_data[col_rename[col]] = data[col]
    all_data.to_csv(f'{outdir}/second_specification.csv', index = False)

    dependent_vars = pd.DataFrame(columns = ['week1_ppc', 'week1_sp', 'week2_ppc', 'week2_sp'])
    for i in range(weeks):
        week = weeks[i]
        week_ppc = data[f'positive_per_capita_0{week[0]}'].values
        week_share_pos = data[f'share_positive_0{week[0]}'].values
        for day in range(week[0] + 1, week[1] + 1):
            if day == 406:
                pass
            else:
                week_ppc = np.concatenate([week_ppc, data[f'positive_per_capita_0{day}'].values], axis = 1)
                week_share_pos = np.concatenate([week_share_pos, data[f'share_positive_0{day}'].values], axis = 1)
        dependent_vars[f'week{i}_ppc'] = np.mean(week_ppc, axis = 1)
        dependent_vars[f'week{i}_sp'] = np.mean(week_share_pos, axis = 1)

    dependent_vars.to_csv(f'{outdir}/dependent_vars.csv', index = False)

if __name__ == '__main__':
    main()