# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

The system compares each song in `songs.csv` to a user's taste profile, gives every song a score from 0 to 1, and recommends the highest-scoring songs.

**Song features.** Each song is one row of `songs.csv`. The system uses these features:

- `genre` and `mood`: text labels. A song gets credit when its label matches the user's preferred genre or mood.
- `energy`, `valence`, `danceability`, and `acousticness`: numbers from 0 to 1. The system compares each one to the user's target value.
- `tempo_bpm`: scaled to 0 to 1 using a fixed range of 60 to 180 BPM, so it can be compared with the other numbers.

The `id`, `title`, and `artist` columns are not used for scoring. `title` and `artist` are only shown in the output.

**User profile.** A `UserProfile` stores:

- a target value for each numeric feature (for example, energy 0.4), which is the level the user likes
- a weight for each feature, which sets how much that feature counts
- a preferred genre and mood
- the ids of songs the user has already heard or liked, so they are not recommended again

**Scoring each song.** The score is built in two steps.

1. **Numeric score.** For each numeric feature, the system measures how close the song is to the user's target: `closeness = 1 - |song value - target|`. The closer the value, the higher the closeness. The closeness values are averaged using the feature weights. A song with energy 0.42 scores close to 1.0 for a user who wants energy 0.40, and a song with energy 0.91 scores about 0.5.
2. **Category score.** Each match in genre or mood adds to the score, with genre and mood each worth half.

The two scores are combined: `final = 0.7 × numeric score + 0.3 × category score`. The 0.7 and 0.3 are starting values to be tested.

```
songs.csv ──► normalize numbers ──► closeness to target ──┐
                                                          ├──► final score ──► sort ──► top k
UserProfile (targets, weights, genre, mood) ──────────────┘          ▲
                                                 genre/mood match ───┘
```

**Choosing songs.** The system:

1. Skips songs the user has already heard or liked.
2. Sorts the remaining songs by final score, highest first. Ties are broken by `id` so results are the same each time.
3. Limits each artist to a set number of songs, so one artist cannot fill the whole list.
4. Returns the top k songs (the starting value is 5).

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



