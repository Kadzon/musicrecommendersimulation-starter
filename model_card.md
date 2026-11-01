# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Task

VibeFinder tries to suggest songs a listener will enjoy right now.

It scores each song in the catalog. The score shows how well the song fits the listener's favorite genre, favorite mood, and target levels. The top 5 songs are shown, with reasons for each one.

---

## 3. Intended Use

VibeFinder suggests songs from a small catalog. It is a classroom project, not a real app.

It assumes the listener can tell us a favorite genre, a favorite mood, and a rough energy level. It does not learn from what people click or skip.

Do not use it for real users. The catalog is too small, and the weights were chosen by hand.

---

## 4. How the Model Works

The recommender goes through every song in the catalog and asks one question: how well does this song fit what the listener wants right now? Each song earns points for how well it matches, the points are added up, and the highest-scoring songs are shown first.

**What it looks at in each song.** Every song has a genre and a mood, which are simple labels like "lofi" or "chill." Every song also has five numbers: energy (how intense it feels), valence (how upbeat or positive it sounds), danceability, acousticness (how acoustic versus electronic it sounds), and tempo (how fast it is, in beats per minute). The song's title and artist are shown in the results but do not affect the score.

**What it knows about the listener.** The listener gives a favorite genre and a favorite mood. They can also give a target level for any of the five numbers, such as "I want energy around 0.4." The system can also skip songs the listener has already heard.

**How points are given.**
- A genre match earns 3 points, and a mood match earns 2 points. Only exact matches count.
- Energy can earn up to 2 points. The closer a song's energy is to the listener's target, the more points it gets.
- Tempo, valence, danceability, and acousticness can each earn up to half a point, using the same closeness idea.
- Adding all of this up gives a total out of 9. Tempo is first put on a 0-to-1 scale so it can be compared fairly with the other numbers.

If the listener does not give a target for one of the numbers, that number simply does not add any points. That means a listener who only sets energy is ranked almost entirely by energy and genre.

**How the results are chosen.** Songs are sorted from highest total to lowest. If two songs tie, the one with the lower id comes first. The top results are shown with a short list of reasons, such as "genre match" or "energy close to target," so the listener can see why each song was picked.

**What changed from the starter logic.** The starter code returned placeholder results. The points system above was built from scratch, with each feature's influence chosen on purpose. The tempo scaling, the skip list, and the reasons shown with each result were added to make the recommendations easier to check.

---

## 5. Data

The catalog has 20 songs.

- Songs 1 to 10 came with the starter file.
- Songs 11 to 20 we added ourselves.
- The numbers for songs 11 to 20 are estimates. We did not measure them from real audio.

**Genres:** pop, indie pop, lofi, rock, ambient, jazz, synthwave, hip hop, r&b, metal, classical, country, gospel, latin, house, blues, and folk.

**Moods:** happy, chill, intense, relaxed, moody, focused, confident, romantic, angry, peaceful, nostalgic, uplifting, playful, euphoric, sad, and melancholic.

Most genres have only one song. Lofi has three. That means a listener who likes jazz gets one jazz song at most.

**What is missing:** reggae, K-pop, world music, and most kinds of electronic music. There are also no sad or angry songs in most genres. The catalog is too small to show real taste.

---

## 6. Strengths

- A pop/happy listener gets sensible results. "Sunrise City" comes first, since it matches both genre and mood.
- Songs that match both genre and mood always rank above songs that match only one.
- Every result shows its reasons, so it is easy to see why a song was picked.
- The scoring is simple enough to check by hand. We checked the top results for the pop/happy profile and they matched what we expected.

---

## 7. Limitations and Bias

- **Exact matches only.** "Chill" and "relaxed" get no credit for each other, even though they feel similar.
- **Energy can pull in the wrong genres.** If a listener only sets energy, songs from other genres can rank high. For example, "Salt and Sirens" (latin) and "Concrete Dreams" (hip hop) show up in the top five for the pop/happy profile.
- **Genre counts more than mood.** An intense pop song can beat a happy indie-pop song. That may not match how people think about mood.
- **Missing features.** The system ignores lyrics, language, release year, and popularity.
- **Uneven catalog.** Genres with more songs have more chances to show up. Genres with one song are hard to reach.
- **Hand-set numbers.** Songs 11 to 20 use guessed values, so their rankings are only as good as those guesses.
- **Weights are our choice.** We picked 3, 2, 2, and 0.5 by reasoning, not by testing with listeners.
- **No artist limit yet.** The README plans to cap songs per artist, but the code does not do it yet. One artist can fill several slots.
- **Possible bias toward pop.** The default profile is pop/happy, and pop has the most songs. The system may work better for listeners who like pop.

---

## 8. Evaluation

**Profiles we tested:**
- The default pop/happy profile (genre pop, mood happy, energy 0.8).
- A "Late-night studier" profile (lofi, chill, with targets for all five numbers). We checked song 4, "Library Rain," and got 8.80, which matched our hand calculation.
- A hip-hop fan (hip hop, confident, high energy and danceability).
- An acoustic low-energy listener (folk, melancholic, low energy, high acousticness).
- A high-tempo house listener (house, euphoric, high energy and tempo).

The three new profiles show that the top song matches genre and mood when one exists. The hip-hop profile has only one matching song, so its list drops off fast.

**What we looked for:** whether the top results matched the genre and mood we asked for, and whether the reasons matched the points.

**What surprised us:** songs with no genre or mood match still made the top five. This happened because energy alone can add up to 2 points.

**What we did not do:** we did not run the pytest suite as part of this evaluation. We also did not test with real listeners, and we did not try lowering the genre weight.

---

## 9. Future Work

- **Partial credit for similar moods.** "Chill" and "relaxed" could earn some points.
- **Artist limit.** Cap how many songs one artist can take in the top results.
- **More songs.** Add more genres and moods, especially the ones we are missing.
- **Let the listener set every feature.** Right now, a profile with only energy is ranked mostly by energy.
- **Better explanations.** Show how close each number was to the target, not just the points.
- **Test with real people.** Ask listeners whether the results feel right.

---

## 10. Personal Reflection

Small choices change the results a lot. Changing one weight can move a song from first place to fifth.

The data matters as much as the code. Most of the bias came from which songs and labels we picked, not from the scoring math.

A points system is easy to explain. We could say exactly why each song was picked. Real apps probably work the same way underneath, but with far more data and more signals.
