# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

VibeFinder is a small music recommender. It scores each song in a 20-song catalog against a listener's favorite genre, mood, and target levels. It adds up points and shows the top 5 songs with reasons. The project is a classroom simulation of how simple scoring can act like a real recommender.

---

## How The System Works

The system compares each song in `songs.csv` to a user's taste profile, gives every song a score from 0 to 9 points, and recommends the highest-scoring songs.

**Song features.** Each song is one row of `songs.csv`. The catalog has 20 songs: ids 1 to 10 are the starter songs, and ids 11 to 20 were added with hand-estimated feature values. The system uses these features:

- `genre` and `mood`: text labels. A song gets credit when its label matches the user's preferred genre or mood.
- `energy`, `valence`, `danceability`, and `acousticness`: numbers from 0 to 1. The system compares each one to the user's target value.
- `tempo_bpm`: scaled to 0 to 1 using a fixed range of 60 to 180 BPM, so it can be compared with the other numbers.

The `id`, `title`, and `artist` columns are not used for scoring. `title` and `artist` are only shown in the output.

**User profile.** A `UserProfile` stores:

- a target value for each numeric feature (for example, energy 0.4), which is the level the user likes
- a preferred genre and mood
- the ids of songs the user has already heard or liked, so they are not recommended again

**Scoring each song.** The system adds up points. There is no averaging or blending, and the feature weights are fixed for all users.

| Feature | Max points | Rule |
|---|---|---|
| `genre` | 3 | 3 if the song's genre equals the preferred genre, otherwise 0 |
| `mood` | 2 | 2 if the song's mood equals the preferred mood (exact match only), otherwise 0 |
| `energy` | 2 | `2 × closeness` |
| `tempo_bpm` | 0.5 | `0.5 × closeness`, using the normalized tempo |
| `valence` | 0.5 | `0.5 × closeness` |
| `danceability` | 0.5 | `0.5 × closeness` |
| `acousticness` | 0.5 | `0.5 × closeness` |
| **Total** | **9** | Final score, from 0 to 9 |

For numeric features, `closeness = 1 - |song value - target|`, which is between 0 and 1. Tempo is first normalized to 0 to 1 with `(bpm - 60) / 120`, and the target is normalized the same way.

**Example user profile: "Late-night studier"**
- genre: lofi
- mood: chill
- targets: energy 0.40, tempo_bpm 80, valence 0.60, danceability 0.60, acousticness 0.75
- skip list: song id 2 (Midnight Coding, already heard)

**Worked example: song 4, Library Rain** (lofi, chill, energy 0.35, tempo 72, valence 0.60, danceability 0.58, acousticness 0.86)
- genre: 3 (lofi matches)
- mood: 2 (chill matches)
- energy: 2 × (1 − 0.05) = 1.90
- tempo: normalized song 0.10, normalized target 0.17, closeness 0.93 → 0.47
- valence: 0.5 × 1.00 = 0.50
- danceability: 0.5 × 0.98 = 0.49
- acousticness: 0.5 × 0.89 = 0.45
- **Total: about 8.80**

```
songs.csv ──► normalize numbers ──► closeness to target ──┐
                                                          ├──► final score ──► sort ──► top k
UserProfile (targets, weights, genre, mood) ──────────────┘          ▲
                                                 genre/mood match ───┘
```

**Choosing songs.** The system:

1. Skips songs the user has already heard or liked.
2. Sorts the remaining songs by final score, highest first. Ties are broken by `id` so results are the same each time.
3. Planned: limit each artist to a set number of songs, so one artist cannot fill the whole list. This is not in the code yet.
4. Returns the top k songs (the starting value is 5).



---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output from `python src/main.py` for the default pop/happy profile (genre=pop, mood=happy, energy=0.8):

```
Loading songs from data/songs.csv...
Loaded songs: 20

Rank  Title                  Score
----------------------------------
1     Sunrise City            6.96
      - genre match (+3.0)
      - mood match (+2.0)
      - energy closeness (+1.96)

2     Gym Hero                4.74
      - genre match (+3.0)
      - energy closeness (+1.74)

3     Rooftop Lights          3.92
      - mood match (+2.0)
      - energy closeness (+1.92)

4     Salt and Sirens         2.00
      - energy closeness (+2.00)

5     Concrete Dreams         1.96
      - energy closeness (+1.96)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## How Real Recommenders Work

Apps like Spotify and YouTube follow the same basic steps as this project: data, preferences, and ranking.

- **Input data:** features of each song or video, such as genre, mood, and tempo, plus behavior like plays, skips, likes, and watch time.
- **User preferences:** taste learned from what the person does, not only from a form they fill out. Real apps update this as the person listens or watches.
- **Ranking and selection:** the app scores many candidates, sorts them, and picks the top results. Many apps also mix in new songs or videos to explore what the person might like.

This project is content-based, because it scores songs only on their own features. Collaborative systems instead use what similar users liked, so they need lots of user data. Real apps usually combine both, along with many more signals than this project uses.

---

## Algorithm Recipe

1. **Input.** Load `songs.csv` and the `UserProfile` (numeric targets, preferred genre and mood, and a list of song ids to skip).
2. **Skip.** Drop any song whose id is in the user's already-heard or liked list.
3. **Normalize.** Scale `tempo_bpm` to 0 to 1 using `(bpm - 60) / 120`, so the 60 to 180 BPM range maps to 0 to 1. The other numeric features are already 0 to 1.
4. **Genre and mood points.** Add 3 if the genre matches exactly, and add 2 if the mood matches exactly.
5. **Numeric points.** For energy, add `2 × closeness`. For tempo, valence, danceability, and acousticness, add `0.5 × closeness`. Closeness is `1 - |song value - target|`.
6. **Total.** The final score is the sum of all points, from 0 to 9.
7. **Rank.** Sort by final score, highest first. Break ties by `id`.
8. **Diversify (planned).** Cap the number of songs from any one artist. Not implemented yet.
9. **Output.** Return the top k songs (default k = 5).

---

## Experiments You Tried

**Run 1: default pop/happy profile** (genre pop, mood happy, energy 0.8).
- The top result was Sunrise City (6.96), which matches on genre, mood, and energy.
- Songs with no genre or mood match, such as Salt and Sirens, still reached the top five. Energy alone can add up to 2 points, so a close energy match can beat a song with a genre match but a poor energy match.

**Run 2: "Late-night studier" profile** (lofi, chill, all five targets).
- Song 4, Library Rain, scored 8.80. This matched the hand calculation in the How The System Works section.

**Design change: blend to additive points.** The first plan combined the numeric and category scores with a 0.7/0.3 blend. We switched to additive points (genre 3, mood 2, energy 2, others 0.5). This was a design decision, not a tested result.

**Run 3: three user profiles** (each run through `recommend_songs`, top 5 shown).

Hip-hop fan (genre hip hop, mood confident, energy 0.85, tempo 95, valence 0.6, danceability 0.85, acousticness 0.1):

```
Rank  Title                  Score
----------------------------------
1     Concrete Dreams         8.83
      - genre match (+3.0)
      - mood match (+2.0)
      - energy closeness (+1.86)
      - tempo_bpm closeness (+0.49)
      - valence closeness (+0.49)
      - danceability closeness (+0.50)
      - acousticness closeness (+0.49)

2     Salt and Sirens         3.71
      - energy closeness (+1.90)
      - tempo_bpm closeness (+0.50)
      - valence closeness (+0.36)
      - danceability closeness (+0.47)
      - acousticness closeness (+0.48)

3     Afterglow Protocol      3.68
      - energy closeness (+1.94)
      - tempo_bpm closeness (+0.38)
      - valence closeness (+0.40)
      - danceability closeness (+0.47)
      - acousticness closeness (+0.48)

4     Sunrise City            3.65
      - energy closeness (+1.94)
      - tempo_bpm closeness (+0.40)
      - valence closeness (+0.38)
      - danceability closeness (+0.47)
      - acousticness closeness (+0.46)

5     Night Drive Loop        3.56
      - energy closeness (+1.80)
      - tempo_bpm closeness (+0.44)
      - valence closeness (+0.45)
      - danceability closeness (+0.44)
      - acousticness closeness (+0.44)
```

Acoustic low-energy listener (genre folk, mood melancholic, energy 0.3, tempo 90, valence 0.35, danceability 0.45, acousticness 0.9):

```
Rank  Title                  Score
----------------------------------
1     Stone and Thread        8.94
      - genre match (+3.0)
      - mood match (+2.0)
      - energy closeness (+1.96)
      - tempo_bpm closeness (+0.49)
      - valence closeness (+0.49)
      - danceability closeness (+0.49)
      - acousticness closeness (+0.49)

2     Clockwork Waltz         3.78
      - energy closeness (+2.00)
      - tempo_bpm closeness (+0.47)
      - valence closeness (+0.41)
      - danceability closeness (+0.42)
      - acousticness closeness (+0.48)

3     Spacewalk Thoughts      3.66
      - energy closeness (+1.96)
      - tempo_bpm closeness (+0.38)
      - valence closeness (+0.35)
      - danceability closeness (+0.48)
      - acousticness closeness (+0.49)

4     Coffee Shop Stories     3.63
      - energy closeness (+1.86)
      - tempo_bpm closeness (+0.50)
      - valence closeness (+0.32)
      - danceability closeness (+0.45)
      - acousticness closeness (+0.49)

5     Library Rain            3.61
      - energy closeness (+1.90)
      - tempo_bpm closeness (+0.42)
      - valence closeness (+0.38)
      - danceability closeness (+0.44)
      - acousticness closeness (+0.48)
```

High-tempo house listener (genre house, mood euphoric, energy 0.9, tempo 124, valence 0.8, danceability 0.9, acousticness 0.05):

```
Rank  Title                  Score
----------------------------------
1     Afterglow Protocol      8.95
      - genre match (+3.0)
      - mood match (+2.0)
      - energy closeness (+1.96)
      - tempo_bpm closeness (+0.50)
      - valence closeness (+0.49)
      - danceability closeness (+0.50)
      - acousticness closeness (+0.49)

2     Gym Hero                3.88
      - energy closeness (+1.94)
      - tempo_bpm closeness (+0.47)
      - valence closeness (+0.48)
      - danceability closeness (+0.49)
      - acousticness closeness (+0.50)

3     Sunrise City            3.67
      - energy closeness (+1.84)
      - tempo_bpm closeness (+0.47)
      - valence closeness (+0.48)
      - danceability closeness (+0.45)
      - acousticness closeness (+0.43)

4     Salt and Sirens         3.59
      - energy closeness (+1.80)
      - tempo_bpm closeness (+0.38)
      - valence closeness (+0.46)
      - danceability closeness (+0.49)
      - acousticness closeness (+0.46)

5     Storm Runner            3.56
      - energy closeness (+1.98)
      - tempo_bpm closeness (+0.38)
      - valence closeness (+0.34)
      - danceability closeness (+0.38)
      - acousticness closeness (+0.47)
```

**What the profiles show:**
- **Hip-hop fan:** Only one song matches genre and mood (Concrete Dreams, 8.83). Second place drops to 3.71, so the rest of the list is filled by songs that match only on energy and the other numbers. The catalog has one hip-hop song, so this is the main limit for this listener.
- **Acoustic low-energy listener:** Stone and Thread (folk, melancholic) wins clearly. The next four are quiet songs from other genres: classical, ambient, jazz, and lofi. Low energy and high acousticness pull the list toward calm songs, even without a genre match.
- **High-tempo house listener:** Afterglow Protocol wins at 8.95. Gym Hero and Sunrise City come next because their energy and tempo are close to the target, even though neither is house.
- **Pattern across all three:** The top song always matches genre and mood when one exists. Ranks 2 to 5 have close scores, and energy does most of the work there.

**Not run yet:**
- Changing the genre weight (for example, from 3 to 0.5) to see how the top results move.
- Running the pytest suite.

---

## Limitations and Risks

The main limits of this recommender are below.

- The catalog has only 20 songs, and most genres have one or two songs.
- It does not understand lyrics, language, or release year.
- It might favor one genre or mood, since genre is worth more points than mood.

### Expected biases

- **Label matching is exact.** "Chill" and "relaxed" get no credit for each other, and genre and mood labels were chosen by the catalog's curator, so users whose tastes fall between labels are served worse.
- **Catalog imbalance.** Genres with one or two songs (for example hip hop or metal) can only be recommended to users who ask for them, and a user with rare tastes gets thin results.
- **Hand-entered features.** The numeric values were set by hand, not measured from audio. The 10 songs added in this project were also estimated by hand, so the rankings reflect those estimates.
- **Profile-author taste.** The default target values reflect whoever wrote the profile. Users who prefer extreme energy or tempo are pulled toward the middle.
- **Filter bubble.** Skipped and liked songs are excluded, but nothing introduces new genres or moods, so the list can narrow over time.
- **Artist cap (planned).** Once added, limiting songs per artist will protect variety, but it may push out a closer match.

You will go deeper on this in your model card.

---

## Reflection

It was great learning the difference between content-based and collaborative recommendations. This project is content-based, because it scores songs on their own features. I also wondered whether movie recommenders use the same kind of scoring, or whether they rely on other non-numerical features, such as cast or reviews.

We changed the scoring from a 0.7/0.3 blend to additive points. When I set the profile to only energy, songs from other genres made the top five, which I did not expect. I also used AI tools to write much of the coding logic, which saved time. I still checked the numbers by hand, because the README and my scoring plan first disagreed, and an AI tool can sound confident and still be wrong. What surprised me most is that simple addition of points, like 3 for a genre match and 2 for a mood match, can feel like a real recommendation. If I kept building this, I would add the artist limit from the README, give partial credit for similar moods like chill and relaxed, and ask a few real listeners to rate the results.


