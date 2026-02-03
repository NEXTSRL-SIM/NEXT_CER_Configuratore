from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    RESA_NORD = 1200
    RID_RATE = 0.137
    CER_RATE = 0.06
    QUOTA_CONDIVISA = 0.50
    DETRAZIONE = 0.50
    ANNI_DETRAZIONE = 10

CFG = Config()
