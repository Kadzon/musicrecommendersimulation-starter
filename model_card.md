# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

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

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
