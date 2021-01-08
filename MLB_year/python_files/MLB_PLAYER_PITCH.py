from mlb_player_scrape import mlb_scrape_player_stat

#pitcher
if __name__ == '__main__':
    url = "https://www.mlb.com/stats/pitching/innings-pitched/"
    position_exist = False
    col_name = ["name", "team", "W", "L", "ERA", "G", "GS", "CG", "SHO", "SV", "SVO", "IP", "H", "R",
                              "ER", "HR", "HB", "BB", "SO", "WHIP", "AVG", "url"]
    col_num_specific = 21
    file_path = "/Users/leechilin/Desktop/python scrape/data_MLB_PLAYER_PITCHER/"

    mlb_scrape_player_stat(url, position_exist, col_name, col_num_specific, file_path)