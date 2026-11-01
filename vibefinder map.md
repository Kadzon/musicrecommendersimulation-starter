# VibeFinder Data Flow Map

```
INPUT: User Prefs
  { genre: "lofi", mood: "chill", energy: 0.4, tempo_bpm: 80,
    valence: 0.6, danceability: 0.6, acousticness: 0.7 }
  + K (how many results to return, e.g. 5)
        |
        v
PROCESS: The Loop (one pass over songs.csv)
  for each song in songs.csv:
      score = 0
      if song.genre == prefs.genre:            score += 3
      if song.mood  == prefs.mood:             score += 2
      score += 2 * (1 - |song.energy - prefs.energy|)
      score += 0.5 * (1 - |(song.tempo_bpm - 60)/120 - (prefs.tempo_bpm - 60)/120|)
      score += 0.5 * (1 - |song.valence - prefs.valence|)
      score += 0.5 * (1 - |song.danceability - prefs.danceability|)
      score += 0.5 * (1 - |song.acousticness - prefs.acousticness|)
      store (song, score)
        |
        v
OUTPUT: The Ranking
  sort all (song, score) pairs by score, descending
  return the top K songs (title, artist, score)
```

## Notes before coding

- **Parsing:** Convert numeric columns to floats and `tempo_bpm` to a number. Keep `id` as-is.
- **Tempo normalization:** Scale BPM with `(bpm - 60) / 120`, so the 60 to 180 BPM range maps to 0 to 1, matching the README.
- **Tie-breaking:** If two songs have the same score, decide on a rule (such as keeping file order) so the output is stable.
- **Edge case:** If `K` is larger than the number of songs, return all of them.
- **Independent scoring:** Each song is scored on its own, so the loop doesn't need to know about other songs. That keeps the logic easy to test.
