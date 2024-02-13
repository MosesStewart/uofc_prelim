addpath('../../source/raw')

dvars = readtable('../../output/derived/dependent_vars.csv');
lat_lon = readtable('../../output/derived/lat_lon.csv');
spec1 = readtable('../../output/derived/first_specification.csv');
spec2 = readtable('../../output/derived/second_specification.csv');
panelvars = ones(height(dvars));
years = 2020 * ones(height(dvars));
output = cell2table(cell(0,width(spec2)), 'VariableNames', spec2.Properties.VariableNames);

loc = table2array(lat_lon);
locCutoff = 65;             % From quoara on furthest distance across NYC
lagCutoff = height(dvars);

for week = 0:1
    for dv = {'ppc', 'sp'}
        dname = sprintf("week%d_%s", week, char(dv));
        dvar = table2array(dvars(:, dname));
        for spec = {'spec1', 'spec2'}
            ivar = table2array(eval(char(spec)));
            estimate = regress_panel_spatial_HAC(dvar, ivar, loc, years, panelvars, locCutoff, lagCutoff, 'yes');
            rname = sprintf("%s_%s", dname, char(spec));
            output(rname, :) = estimate;
        end
    end
end

output
