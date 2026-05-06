"""
Fichier contenant la classe Tile

Auteur: Adrien Buschbeck
"""

import dataclasses as dc
from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Tile:
    """
    Classe représentant les différents types de terrains
    Name --> Nom
    Colour --> couleur par laquelle le terrain va être représenté (systèem RGB)
    wfc_delete --> terrain qui ne peuvent pas être à côté (conectivité 4)
    """

    Name: str
    Color: tuple[int, int, int] = dc.field(default_factory=tuple[int, int, int])
    wfc_delete: list[str] = dc.field(default_factory=list[str])
    # wealth: float will add if time and if Albert
    # wildness: float will add if time and if Albert

    def __repr__(self):
        return self.Name[0]


Placeholer = Tile(
    "Placeholer",
    (255, 255, 255),
    [],
)  # (0, 0,)
