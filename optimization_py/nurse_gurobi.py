# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import gurobipy as gb
import xlrd
from urllib.request import urlopen

# Use pandas to read the file, one tab for each table.
data_url = "https://github.com/IBMDecisionOptimization/docplex-examples/blob/master/examples/mp/jupyter/nurses_data.xls?raw=true"
nurse_xls_file = pd.ExcelFile(urlopen(data_url))

df_skills = nurse_xls_file.parse('Skills')
df_depts  = nurse_xls_file.parse('Departments')
df_shifts = nurse_xls_file.parse('Shifts')
# Rename df_shifts index
df_shifts.index.name = 'shiftId'

# Index is column 0: name
df_nurses = nurse_xls_file.parse('Nurses', header=0, index_col=0)
df_nurse_skilles = nurse_xls_file.parse('NurseSkills')
df_vacations = nurse_xls_file.parse('NurseVacations')
df_associations = nurse_xls_file.parse('NurseAssociations')
df_incompatibilities = nurse_xls_file.parse('NurseIncompatibilities')

# Display the nurses dataframe
print("#nurses = {}".format(len(df_nurses)))
print("#shifts = {}".format(len(df_shifts)))
print("#vacations = {}".format(len(df_vacations)))

# maximum work time (in hours)
max_work_time = 40
# maximum number of shifts worked in a week.
max_nb_shifts = 5

days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
day_of_weeks = dict(zip(days, range(7)))

# utility to convert a day string e.g. "Monday" to an integer in 0..6
def day_to_day_of_week(day):
    return day_of_weeks[day.strip().lower()]

df_shifts["dow"] = df_shifts.day.apply(day_to_day_of_week)
df_shifts["wstart"] = df_shifts.start_time + 24 * df_shifts.dow

# an auxiliary function to calculate absolute end time of a shift
def calculate_absolute_endtime(start, end, dow):
    return 24*dow + end + (24 if start>=end else 0)

# store the results in a new column
df_shifts["wend"] = df_shifts.apply(lambda row: calculate_absolute_endtime(
        row.start_time, row.end_time, row.dow), axis=1, raw=True)

df_shifts["duration"] = df_shifts.wend - df_shifts.wstart
# also compute minimum demand in nurse-hours
df_shifts["min_demand"] = df_shifts.min_req * df_shifts.duration

### Model
mod = gb.Model()
# first global collections to iterate upon
all_nurses = df_nurses.index.values
all_shifts = df_shifts.index.values

var_assigned = mod.addVars(all_nurses, all_shifts, vtype="B")
# Organize decision variables in a DataFrame
vdf_assigned = pd.DataFrame({"assigned": var_assigned})
vdf_assigned.index.names=['all_nurses', 'all_shifts']

# Re-organize the Data Frame as a pivot table with nurses as row index and shifts as columns:
vdf_assigned_pivot = vdf_assigned.unstack(level='all_shifts')

# Create a pivot using nurses and shifts index as dimensions
# vdf_assigned_pivot = vdf_assigned.reset_index().pivot(index='all_nurses', columns='all_shifts', values='assigned')

# Display first rows of the pivot table
vdf_assigned_pivot.head()

# Create a Data Frame representing a list of shifts sorted by wstart and duration.
# One keeps only the three relevant columns: 'shiftId', 'wstart' and 'wend' in the resulting Data Frame 
df_sorted_shifts = df_shifts.sort_values(['wstart','duration']).reset_index()[['shiftId', 'wstart', 'wend']]

# Display the first rows of the newly created Data Frame
df_sorted_shifts.head()

number_of_incompatible_shift_constraints = 0
for shift in df_sorted_shifts.itertuples():
    for shift_2 in df_sorted_shifts.loc[shift[0]+1:].itertuples():
        if shift_2.wstart <shift.wend:
            for nurse_assignments in vdf_assigned_pivot.iloc[:, [shift.shiftId, shift_2.shiftId]].itertuples():
                mod.addConstr( nurse_assignments[1] + nurse_assignments[2] <= 1 ) 
                number_of_incompatible_shift_constraints += 1
        else:
            break
print("#incompatible shift constraints: {}".format(number_of_incompatible_shift_constraints))

# Add 'day of week' column to vacations Data Frame
df_vacations['dow'] = df_vacations.day.apply(day_to_day_of_week)

df_assigned_reindexed = vdf_assigned.reset_index()
df_vacation_forbidden_assignments = df_vacations.merge(df_shifts.reset_index()[['dow', 'shiftId']]).merge(
    df_assigned_reindexed, left_on=['nurse', 'shiftId'], right_on=['all_nurses', 'all_shifts'])

mod.addConstrs(forbidden_assignment.assigned == 0 
              for forbidden_assignment in df_vacation_forbidden_assignments.itertuples() )

df_preferred_assign = df_associations.merge(
    df_assigned_reindexed, left_on='nurse1', right_on='all_nurses').merge(
    df_assigned_reindexed, left_on=['nurse2', 'all_shifts'], right_on=['all_nurses', 'all_shifts'], suffixes=('_1','_2'))

mod.addConstrs(preferred_assign.assigned_1 == preferred_assign.assigned_2 
               for preferred_assign in df_preferred_assign.itertuples() )

df_incompatible_assign = df_incompatibilities.merge(
    df_assigned_reindexed, left_on='nurse1', right_on='all_nurses').merge(
    df_assigned_reindexed, left_on=['nurse2', 'all_shifts'], right_on=['all_nurses', 'all_shifts'], suffixes=('_1','_2'))

mod.addConstrs(incompatible_assign.assigned_1 + incompatible_assign.assigned_2 <= 1
               for incompatible_assign in df_incompatible_assign.itertuples() ) 

# auxiliary function to create worktime variable from a row
def make_var(row, varname_fmt):
    return mod.addVar(name=varname_fmt % row.name, lb=0)

# apply the function over nurse rows and store result in a new column
df_nurses["worktime"] = df_nurses.apply(lambda r: make_var(r, "worktime_%s"), axis=1)
mod.update()

for nurse, nurse_assignments in vdf_assigned.groupby(level='all_nurses'):
    mod.addConstr(df_nurses.worktime[nurse] == np.dot(nurse_assignments.assigned, df_shifts.duration))
                       
# print model information and check we now have 32 extra continuous variables
#mdl.print_information()
    
def set_max_work_time(v):
    v.ub = max_work_time # JU: setting inside the function
    # Optionally: return a string for fancy display of the constraint in the Output cell
    # return str(v) + ' <= ' + str(v.ub)

df_nurses["worktime"].apply(convert_dtype=False, func=set_max_work_time)

for shift, shift_nurses in vdf_assigned.groupby(level='all_shifts'):
    mod.addConstr(gb.quicksum(shift_nurses.assigned) >= df_shifts.min_req[shift])
    mod.addConstr(gb.quicksum(shift_nurses.assigned) <= df_shifts.max_req[shift])


# again leverage pandas to create a series of expressions: costs of each nurse
total_salary_series = df_nurses.worktime * df_nurses.pay_rate

# compute global salary cost using pandas sum()
# Note that the result is a DOcplex expression: DOcplex if fully compatible with pandas
total_salary_cost = total_salary_series.sum()
mod.setObjective(total_salary_cost)


mod.printStats()
mod.optimize()

