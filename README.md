# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the fixed app: `python -m streamlit run app.py`
3. Run tests: `pytest tests/`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game purpose:** A number-guessing game where the player tries to identify a secret number within a limited number of attempts. The game gives "Too High" or "Too Low" hints after each guess and tracks a running score.
- [x] **Bugs found:**
  - **Inverted hints** — `check_guess` returned "Go HIGHER!" when the guess was above the secret and "Go LOWER!" when it was below, the opposite of what is correct.
  - **Secret type-switching** — on every even-numbered attempt, `app.py` cast the secret number to a string before passing it to `check_guess`, making numeric equality impossible on those turns.
  - **Hard difficulty too easy** — the Hard range was `1–50`, a narrower range than Normal (`1–100`), which is the wrong direction for a harder mode.
  - **Score rewards wrong guesses** — "Too High" on even attempts gave `+5` points instead of subtracting them.
  - **Hardcoded UI message** — the info bar always said "Guess a number between 1 and 100" even on Easy or Hard.
  - **Attempt counter off-by-one** — the initial attempt count was set to `1` on first load but `0` on New Game, making the counter inconsistent.
- [x] **Fixes applied:**
  - Refactored all four logic functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) from `app.py` into `logic_utils.py`.
  - Corrected hint direction in `check_guess`: "Too High" → "Go LOWER!", "Too Low" → "Go HIGHER!".
  - Removed the `str()` cast on even attempts; the secret is now always compared as an integer.
  - Fixed Hard difficulty range to `1–200`.
  - Simplified scoring so all wrong guesses consistently subtract 5 points.
  - Updated the UI info bar to use the actual `low`/`high` values from `get_range_for_difficulty`.
  - Unified the initial attempt count to `0`.

## 📸 Demo

> Take a screenshot of your running, fixed game and insert it here.
> Example: `![Fixed Game Screenshot](demo_screenshot.png)`

- [ ] <img width="1649" height="787" alt="image" src="https://github.com/user-attachments/assets/d7a32ec1-0ebf-4125-8f95-986feb924401" />


## ✅ Tests

Run `pytest tests/` from the project root. All tests should pass:

```
tests/test_game_logic.py ..............                   [100%]
```

Tests cover:
- Correct win detection
- Correct "Too High" and "Too Low" outcomes
- Hint direction (the word "LOWER" / "HIGHER" in the message)
- Input parsing (valid integers, floats, empty input, non-numeric)
- Difficulty ranges (Hard wider than Normal)
- Score behavior (wrong guesses always decrease score)

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]

