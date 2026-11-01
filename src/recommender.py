import csv
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    # Optional targets for the other numeric features. None means "no preference",
    # so that feature is left out of the score.
    target_valence: Optional[float] = None
    target_danceability: Optional[float] = None
    target_tempo_bpm: Optional[float] = None
    target_acousticness: Optional[float] = None
    # How much each numeric feature counts in the score. Keys match Song field names.
    weights: Dict[str, float] = field(default_factory=lambda: {
        "energy": 1.0,
        "valence": 1.0,
        "danceability": 1.0,
        "acousticness": 1.0,
        "tempo_bpm": 1.0,
    })
    # Songs the user has already heard or liked. These are not recommended again.
    seen_song_ids: Set[int] = field(default_factory=set)

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file, converting numeric columns to int or float."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

NUMERIC_MAX_POINTS = {
    "energy": 2.0,
    "tempo_bpm": 0.5,
    "valence": 0.5,
    "danceability": 0.5,
    "acousticness": 0.5,
}

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return the score with its reasons."""
    score = 0.0
    reasons = []

    if user_prefs.get("genre") == song["genre"]:
        score += 3.0
        reasons.append("genre match (+3.0)")

    if user_prefs.get("mood") == song["mood"]:
        score += 2.0
        reasons.append("mood match (+2.0)")

    for feature, max_points in NUMERIC_MAX_POINTS.items():
        target = user_prefs.get(feature)
        if target is None:
            continue
        song_value = song[feature]
        if feature == "tempo_bpm":
            song_value = (song_value - 60) / 120
            target = (target - 60) / 120
        closeness = max(0.0, 1 - abs(song_value - target))
        points = max_points * closeness
        score += points
        reasons.append(f"{feature} closeness (+{points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, skip seen ones, and return the top k as (song, score, explanation)."""
    seen = user_prefs.get("seen_song_ids", set())
    scored = []
    for song in songs:
        if song["id"] in seen:
            continue
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    scored.sort(key=lambda item: (-item[1], item[0]["id"]))
    return scored[:k]
