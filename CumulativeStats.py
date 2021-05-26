from datetime import datetime
import pandas as pd

def get_cumulative_offensive_stats_df(Team_dataframe):
    """get a dataframe that represent the cumulative offensive statistics for the team 

    Args:
        Team_dataframe ([type]): [description]

    Notes:

    """
        

    kept_columns_name =['extra_points_attempted',
                            'extra_points_made',
                            'field_goals_attempted',
                            'field_goals_made',
                            'fourth_down_attempts',
                            'fourth_down_conversions',
                            'interceptions',
                            'pass_attempts',
                            'pass_completion_rate',
                            'pass_completions',
                            'pass_touchdowns',
                            'pass_yards',
                            'pass_yards_per_attempt',
                            'points_allowed',
                            'points_scored',
                            'punt_yards',
                            'punts',
                            'quarterback_rating',
                            'result',
                            'rush_attempts',
                            'rush_touchdowns',
                            'rush_yards',
                            'rush_yards_per_attempt',
                            'third_down_attempts',
                            'third_down_conversions',
                            'time_of_possession',
                            'times_sacked',
                            'yards_lost_from_sacks']

    cumulative_columns_name = [ 'cummean_extra_points_attempted',
                                    'cummean_extra_points_made',
                                    'cummean_field_goals_attempted',
                                    'cummean_field_goals_made',
                                    'cummean_fourth_down_attempts',
                                    'cummean_fourth_down_conversions',
                                    'cummean_interceptions',
                                    'cummean_pass_attempts',
                                    'cummean_pass_completion_rate',
                                    'cummean_pass_completions',
                                    'cummean_pass_touchdowns',
                                    'cummean_pass_yards',
                                    'cummean_pass_yards_per_attempt',
                                    'cummean_points_allowed',
                                    'cummean_points_scored',
                                    'cummean_punt_yards',
                                    'cummean_punts',
                                    'cummean_quarterback_rating',
                                    'cummean_result',
                                    'cummean_rush_attempts',
                                    'cummean_rush_touchdowns',
                                    'cummean_rush_yards',
                                    'cummean_rush_yards_per_attempt',
                                    'cummean_third_down_attempts',
                                    'cummean_third_down_conversions',
                                    'cummean_pct_of_possession',
                                    'cummean_times_sacked',
                                    'cummean_yards_lost_from_sacks']

    temp_df = Team_dataframe[kept_columns_name]
    temp_df.columns =cumulative_columns_name

    temp_df.loc[:,'cummean_pct_of_possession'] = temp_df['cummean_pct_of_possession'].apply(lambda x: datetime.strptime(x,'%M:%S').second + datetime.strptime(x,'%M:%S').minute * 60 )


    cumulative_stats_dataframe = temp_df.expanding().mean()
    cumulative_stats_dataframe['cummean_pass_completion_rate'] = cumulative_stats_dataframe['cummean_pass_completions']/cumulative_stats_dataframe['cummean_pass_attempts']
    cumulative_stats_dataframe['cummean_pass_yards_per_attempt'] = cumulative_stats_dataframe['cummean_pass_yards']/cumulative_stats_dataframe['cummean_pass_attempts']
    cumulative_stats_dataframe['cummean_rush_yards_per_attempt'] = cumulative_stats_dataframe['cummean_rush_yards']/cumulative_stats_dataframe['cummean_rush_attempts']

    cumulative_stats_dataframe.loc[:,'cummean_pct_of_possession'] = cumulative_stats_dataframe['cummean_pct_of_possession'].apply(lambda x: round(x/3600, 2) )
    cumulative_stats_dataframe["week"] = Team_dataframe["week"]
    cumulative_stats_dataframe["opponent_abbr"] = Team_dataframe["opponent_abbr"]
    
    return cumulative_stats_dataframe


def get_cumulative_defensive_stats_df(Team_schedule):
    """get a dataframe that represent the cumulative defensive statistics for the team

    Args:
        Team_dataframe_extended ([type]): [description]

    Notes:

    """

    kept_columns_name = ['first_downs',
        'fourth_down_attempts',
        'fourth_down_conversions',
        'fumbles', 
        'fumbles_lost',
        'interceptions', 
        'net_pass_yards', 
        'pass_attempts',
        'pass_completions',
        'pass_touchdowns',
        'pass_yards',
        'penalties',
        'points',
        'rush_attempts',
        'rush_touchdowns',
        'rush_yards',
        'third_down_attempts',
        'third_down_conversions',
        'times_sacked', 
        'total_yards', 
        'turnovers',
        'yards_from_penalties', 
        'yards_lost_from_sacks']

    
    defensive_cumulative_columns_name = ['cummean_first_downs_against',
        'cummean_fourth_down_attempts_against',
        'cummean_fourth_down_conversions_against',
        'cummean_fumbles_against', 
        'cummean_fumbles_lost_against',
        'cummean_interceptions_against', 
        'cummean_net_pass_yards_against', 
        'cummean_pass_attempts_against',
        'cummean_pass_completions_against',
        'cummean_pass_touchdowns_against',
        'cummean_pass_yards_against',
        'cummean_penalties_against',
        'cummean_points_against',
        'cummean_rush_attempts_against',
        'cummean_rush_touchdowns_against',
        'cummean_rush_yards_against',
        'cummean_third_down_attempts_against',
        'cummean_third_down_conversions_against',
        'cummean_times_sacked_against', 
        'cummean_total_yards_against', 
        'cummean_turnovers_against',
        'cummean_yards_from_penalties_against', 
        'cummean_yards_lost_from_sacks_against']


    dataframe = Team_schedule.dataframe
    dataframe_extended = Team_schedule.dataframe_extended
    

    df_location_enemy = dataframe.location.apply(lambda x: "home" if x == "Away" else "away")

    column_name_list = []
    for location in df_location_enemy:
        temp_colnames = [] 
        for colname_iter in kept_columns_name:
            temp_colnames.append(location + "_" + colname_iter)
        column_name_list.append(temp_colnames)

    list_of_defensive_stats = []
    for row, colnames in zip(dataframe_extended.iterrows(), column_name_list):
        temps_df = pd.DataFrame(row[1][colnames]).transpose()
        temps_df.columns = defensive_cumulative_columns_name
        list_of_defensive_stats.append(temps_df)

    merged_df = pd.concat(list_of_defensive_stats)

    cumulative_stats_dataframe = merged_df.expanding().mean()
    cumulative_stats_dataframe['cummean_pass_completion_rate_against'] = cumulative_stats_dataframe['cummean_pass_completions_against']/cumulative_stats_dataframe['cummean_pass_attempts_against']
    cumulative_stats_dataframe['cummean_pass_yards_per_attempt_against'] = cumulative_stats_dataframe['cummean_pass_yards_against']/cumulative_stats_dataframe['cummean_pass_attempts_against']
    cumulative_stats_dataframe['cummean_rush_yards_per_attempt_against'] = cumulative_stats_dataframe['cummean_rush_yards_against']/cumulative_stats_dataframe['cummean_rush_attempts_against']

    return cumulative_stats_dataframe

if __name__ == '__main__':
    from sportsipy.nfl.teams import Teams
    teams = Teams()
    lions = teams('DET')
    lions_schedule = lions.schedule
    lions_df = lions_schedule.dataframe


    test_offensive = get_cumulative_offensive_stats_df(lions_df)
    test_defensive = get_cumulative_defensive_stats_df(lions_schedule)

    cumul_df = test_offensive.merge(test_defensive, left_index=True, right_index=True)

    




