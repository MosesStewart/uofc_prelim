addpath('../../source/raw')

dvars = readtable('../../output/derived/dependent_vars.csv');
lat_lon = readtable('../../output/derived/lat_lon.csv');
spec1 = readtable('../../output/derived/first_specification.csv');
spec2 = readtable('../../output/derived/second_specification.csv');
panelvars = transpose(1:height(dvars)); %ones([height(dvars), 1]);
years = 2020 * ones([height(dvars), 1]);
output = cell2table(cell(width(spec2), 0), 'RowNames', spec2.Properties.VariableNames);
output(:, 'varnames') = transpose(spec2.Properties.VariableNames);

loc = lat_lon{:,:};
locCutoff = 65;             % From quora on furthest distance across NYC
lagCutoff = 0;

for week = 0:1
    for dv = {'ppc', 'sp'}
        dname = sprintf("week%d_%s", week, char(dv));
        dvar = dvars(:, dname);
        dvar = dvar{:,:};
        for spec = {'spec1', 'spec2'}
            ivar = eval(char(spec));
            ivar = ivar{:,:};
            estimate = regress_panel_spatial_HAC(dvar, ivar, loc, years, panelvars, locCutoff, lagCutoff, 'no');

            cname = sprintf("%s_%s", dname, char(spec));
            fill = zeros(width(spec2) - width(estimate.coeff), 1);
            output(:, sprintf('%s_est', cname)) = array2table(cat(1, transpose(estimate.coeff), fill));
            output(:, sprintf('%s_se', cname)) = array2table(cat(1, transpose(estimate.se), fill));
            output(:, sprintf('%s_pval', cname)) = array2table(cat(1, transpose(estimate.p_val), fill));
        end
    end
end

writetable(output, '../../output/analysis/spatial_raw_results.csv')
