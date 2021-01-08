from mlb_team_scrape import mlb_scrape_team_stats

if __name__ == '__main__':
    year_list = [2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010]
    scenario_list = ["h", "a", "d", "n", "vl", "vr", "sah", "sbh", "sti", "r0", "r1", "r12", "r123", "ron",
                     "ron2", "risp", "risp2", "o0", "o1", "o2", "ac", "bc", "ec", "2s", "fc"]
    url = "https://www.mlb.com/stats/team/"
    col_specific = ["team", "url"]
    col_num_specific = 18
    col_name = ["team", "league", "G", "AB", "R", "H", "2B", "3B", "HR", "RBI", "BB", "SO", "SB", "CS",
                "AVG", "OBP", "SLG", "OPS", "url"]
    file_path = "/Users/leechilin/Desktop/python scrape/data_MLB_TEAM_BATTER/"
    mlb_scrape_team_stats(year_list, scenario_list, url, col_specific, col_num_specific, col_name, file_path)


