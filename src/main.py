"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\n{'Rank':<6}{'Title':<22}{'Score':>6}")
    print("-" * 34)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank:<6}{song['title']:<22}{score:>6.2f}")
        for reason in explanation.split("; "):
            print(f"      - {reason}")
        print()


if __name__ == "__main__":
    main()
