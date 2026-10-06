base_ELO = 1600
from config import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    atk_elo = db.Column(db.Integer)
    def_elo = db.Column(db.Integer)
    avg_elo = db.Column(db.Integer)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "attackElo": self.atk_elo,
            "defenseElo": self.def_elo,
            "averageElo": self.avg_elo,
        }


class Matchs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    black_atk = db.Column(db.Integer)
    black_def = db.Column(db.Integer)
    white_atk = db.Column(db.Integer)
    white_def = db.Column(db.Integer)
    white_score = db.Column(db.Integer)
    black_score = db.Column(db.Integer)
    E_white = db.Column(db.Integer)
    E_black = db.Column(db.Integer)

    def to_json(self):
        return {
            "id": self.id,
            "blackAttack": self.black_atk,
            "blackDefense": self.black_def,
            "whiteAttack": self.white_atk,
            "whiteDefense": self.white_def,
            "whiteScore": self.white_score,
            "blackScore": self.black_score,
        }


def calculate_ELO(
    black_atk, black_def, white_atk, white_def, white_score, black_score, K=32
):
    # Retrieving the ELO of each player
    player_black_atk = Player.query.get(black_atk)
    player_black_def = Player.query.get(black_def)
    player_white_atk = Player.query.get(white_atk)
    player_white_def = Player.query.get(white_def)

    # Calculate ELO of the match
    R_white = (
        player_white_atk.atk_elo + player_white_def.def_elo
    ) / 2  # Ranking of team white
    R_black = (
        player_black_atk.atk_elo + player_black_def.def_elo
    ) / 2  # Ranking of team black

    E_white = 1 / (1 + 10 ** ((R_white - R_black) / 400))
    E_black = 1 / (1 + 10 ** ((R_black - R_white) / 400))

    S_white = int(white_score > black_score)
    S_black = 1 - S_white

    # Update Elo of each player
    player_white_atk.atk_elo = player_white_atk.atk_elo + K * (S_white - E_white)
    player_white_atk.avg_elo = (player_white_atk.atk_elo + player_white_atk.def_elo) / 2

    player_white_def.def_elo = player_white_def.def_elo + K * (S_white - E_white)
    player_white_def.avg_elo = (player_white_def.def_elo + player_white_def.atk_elo) / 2

    player_black_atk.atk_elo = player_black_atk.atk_elo + K * (S_black - E_black)
    player_black_atk.avg_elo = (player_black_atk.atk_elo + player_black_atk.def_elo) / 2

    player_black_def.def_elo = player_black_def.def_elo + K * (S_black - E_black)
    player_black_def.avg_elo = (player_black_def.def_elo + player_black_def.atk_elo) / 2

    return (E_white, E_black)
