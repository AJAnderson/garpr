from scraper.challonge import ChallongeScraper
from model import *
from config.config import Config
import csv


class Error(Exception):
    pass


class OccupiedError(Error):

    def __init__(self):
        self.msg = 'All setups are occupied'


class MatchAllocator(object):

    def __init__(self, tournids, setups_csv_path=None, teams_csv_path=None):
        '''
            tournids is a list of tournament ids from challonge
            brackets is a dictionary, key=tournid, val=bracket objects.
            bracket object is a dictionary, key=matchid, val=(player1,player2)
        '''
        self.brackets = {}
        for tid in tournids:
            print tid
            matches, name = self.import_matches(tid)
            self.brackets[name] = matches

        self.player_to_match_maps = self.build_player_to_match_map()

        if teams_csv_path:
            self.teams_map = self.import_teams(teams_csv_path)

        if setups_csv_path:
            self.setups = self.import_setups(setups_csv_path)

        self.available_setups = self.setups
        self.occupied_setups = {}

    def choose_next_match(self):
        try:
            self.allocate_setup()
        except OccupiedError:
            return

    def get_bracket_priority(self):
        return

    def allocate_setup(self, matchid):
        # This actually needs to take a match.
        # Perhaps "matches" should be objects which can then be pushed to lists easier.
        # It could just take a match ID though.
        try:
            self.occupied_setups.update(dict(self.available_setups.pop(0), matchid))
        except IndexError:
            print 'All setups are occupied'
            raise OccupiedError()

    def build_player_to_match_map(self):
        p_match_map = {}
        for tournid, brack in self.brackets.iteritems():
            p_match_map[tournid] = {players[0]: match
                                    for match, players in brack.iteritems()}
            temp = {players[1]: match for match, players in brack.iteritems()}
            p_match_map[tournid].update(temp)

        return p_match_map

    def import_matches(self, tourn_id):
        Config()
        scraper = ChallongeScraper(tourn_id)
        matches = scraper.get_unplayed_matches()
        tournname = scraper.get_name()

        return matches, tournname

    def import_teams(self, path):
        f = open(path)
        reader = csv.reader(f)
        teams = {line[0]: (line[1], line[2]) for line in reader}

        return teams

    def import_setups(self, path):
        fs = open(path)
        reader = csv.reader(fs)
        setups = [line[0] for line in reader]

        return setups

    # def build_teamsmatch_to_player_map(self):
    #     match_player_map = {}
    #     for match, players in selfmatches.items():
    #         match_player_map[match] = (teams[players[0]] + teams[players[1]])

    #     return match_player_map

# def build_clash_list(team_tourn_id, singles_tourn_id, teams_csv_path):
#     teams_match_player_map = build_teams_clash_list(
#         team_tourn_id, teams_csv_path)
#     matches, singles_player_map = import_matches(singles_tourn_id)

#     first_pick = teams_match_player_map.popitem()

#     blockedmatch = dict()
#     for player in first_pick[1]:
#         blockedmatch[singles_player_map[player]] = matches[singles_player_map[player]]

#     return blockedmatch, singles_player_map, teams_match_player_map
