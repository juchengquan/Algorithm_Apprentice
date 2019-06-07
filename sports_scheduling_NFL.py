import pandas as pd
import numpy as np
import docplex.mp.model as cpmodel
from collections import namedtuple

# Teams in 1st division
team_div1 = ["Baltimore Ravens","Cincinnati Bengals", "Cleveland Browns","Pittsburgh Steelers","Houston Texans",
                "Indianapolis Colts","Jacksonville Jaguars","Tennessee Titans","Buffalo Bills","Miami Dolphins",
                "New England Patriots","New York Jets","Denver Broncos","Kansas City Chiefs","Oakland Raiders",
                "San Diego Chargers"]
# Teams in 2nd division
team_div2 = ["Chicago Bears","Detroit Lions","Green Bay Packers","Minnesota Vikings","Atlanta Falcons",
                "Carolina Panthers","New Orleans Saints","Tampa Bay Buccaneers","Dallas Cowboys","New York Giants",
                "Philadelphia Eagles","Washington Redskins","Arizona Cardinals","San Francisco 49ers",
                "Seattle Seahawks","St. Louis Rams"]
teams = pd.DataFrame(np.array([team_div1,team_div2]).T)
teams.columns = ["AFC", "NFC"]

if len(team_div1) != len(team_div2):
    raise Exception("Not equal team members.")

nb_teams = len(team_div1) + len(team_div2)
rg_teams = np.arange(nb_teams)

nb_weeks = 31
rg_weeks= np.arange(nb_weeks)

match = namedtuple("match",["team1","team2","is_divisional"])

matches = {match(t1, t2, 1 if (t2 < nb_teams/2 or t1 >= nb_teams/2) else 0) 
            for t1 in rg_teams 
            for t2 in rg_teams 
            if t1<t2 }

nb_inside_division = 1
nb_outside_division = 1

nb_play = { m : nb_inside_division if m.is_divisional==1 else nb_outside_division 
           for m in matches }

mdl = cpmodel.Model()

v_b_plays = mdl.binary_var_matrix(matches, rg_weeks, ) 

#df_v = pd.DataFrame({"v_b_plays": v_b_plays})
#df_v.index.names=['matches', 'weeks']
#df_v_pivot = df_v.unstack(level='weeks')

### Each pair of teams must play the correct number of games.
mdl.add_constraints( mdl.sum(v_b_plays[m,w]  for w in rg_weeks) == nb_play[m] for m in matches)
#mdl.print_information()

### Each team must play exactly once in a week.
mdl.add_constraints( mdl.sum(v_b_plays[m,w] for m in matches if (m.team1 == t or m.team2 == t) )  == 1
                   for w in rg_weeks for t in rg_teams)
#mdl.print_information()

### Games between the same teams cannot be on successive weeks.
mdl.add_constraints( v_b_plays[m,w] + v_b_plays[m,w+1] <= 1 
                   for w in rg_weeks[0:-1]
                   for m in matches )
#mdl.print_information()

# Season is split into two halves
first_half_weeks = np.arange(nb_weeks // 2)
nb_first_half_games = nb_weeks // 3
mdl.add_constraints( mdl.sum(v_b_plays[m,w]  for w in first_half_weeks for m in matches 
                            if (((m.team1 == t or m.team2 == t) and m.is_divisional == 1 ))) >= nb_first_half_games
                   for t in rg_teams )
mdl.print_information()


gain = { w : w*w for w in rg_weeks}

# If an intradivisional pair plays in week w, Gain[w] is added to the objective.
mdl.maximize( mdl.sum(m.is_divisional * w * v_b_plays[m,w] for m in matches for w in rg_weeks) )
mdl.add_kpi( mdl.sum(m.is_divisional * gain[w] * v_b_plays[m,w] for m in matches for w in rg_weeks) )


mdl.print_information()

assert mdl.solve(log_output=True), "!!! Solve of the model fails"
mdl.report()

df_v = pd.DataFrame({"v_b_plays": v_b_plays})
df_v.index.names=['matches', 'weeks']
df_result = df_v.v_b_plays.apply(lambda v: v.solution_value)
df_result_pivot = df_result.unstack(level='weeks')

res = df_result_pivot.idxmax(axis=1)
res = res.reset_index()
res.index = pd.MultiIndex.from_tuples(res.matches, names=["team1", "team2", "is_divisional"])
res.drop("matches", axis=1, inplace=True)
res[0] +=1

q_g = res.reindex(level="is_divisional").unstack(level="team2").groupby(level="team1").sum()

q_arr = q_g.to_numpy()

q_arr = np.insert(q_arr, [0], np.zeros((q_arr.shape[0], 1)), axis=1 )
q_arr = np.append(q_arr, np.zeros((1, q_arr.shape[1])), axis=0)

q_arr += q_arr.T

df_res = pd.DataFrame(data=q_arr, index=team_div1+team_div2, columns=team_div1+team_div2)
## process the result