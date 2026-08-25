from dataclasses import dataclass


@dataclass
class NLSECoefs:
    kinetic: float
    potential: float
    absorption: float