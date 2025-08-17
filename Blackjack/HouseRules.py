class HouseRules:
    def __init__(self, standS17: bool, DASoffered: bool, 
                 LSoffered: bool, NBJpayout: float, penetration: int,
                 minBet: int, numDecks: int):
        self.standS17: str = standS17
        self.DASoffered: bool = DASoffered
        self.LSoffered: bool = LSoffered
        self.NBJpayout: float = NBJpayout
        self.penetration: int = penetration
        self.minBet: int = minBet
        self.numDecks = numDecks