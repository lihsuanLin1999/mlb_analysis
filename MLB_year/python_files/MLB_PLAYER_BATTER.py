from mlb_player_scrape import mlb_scrape_player_stat

# batter
if __name__ == '__main__':
    url = "https://www.mlb.com/stats/"
    position_exist = True
    col_name = ["player", "position", "team", "G", "AB", "R", "H", "2B", "3B", "HR", "RBI", "BB", "SO",
                "SB", "CS", "AVG", "OBP", "SLG", "OPS", "url"]
    col_num_specific = 19
    file_path = "/Users/leechilin/Desktop/python scrape/data_MLB_PLAYER_BATTER/"

    mlb_scrape_player_stat(url, position_exist, col_name, col_num_specific, file_path)