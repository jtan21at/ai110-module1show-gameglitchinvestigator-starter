# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

When I first ran the app, the game was completely unplayable. The most glaring issue was that the hints were backwards: guessing a number that was too high would tell me to "Go HIGHER!", which pushed me further away from the answer instead of closer. A second bug caused the secret number to be converted to a string on every even-numbered attempt, which broke numeric comparison entirely — the guess `50` would never equal the string `"50"`, so winning was impossible on those turns. Together, these two bugs made it feel like the game was actively working against the player.

---

## 2. How did you use AI as a teammate?

I used GitHub Copilot (via Copilot Chat and Agent mode) throughout this project. For a correct suggestion, I asked Copilot to refactor all four logic functions out of `app.py` and into `logic_utils.py`. Its multi-file diff was accurate: it moved the functions cleanly, updated the import in `app.py`, and left the UI code untouched. I verified this by reading the diff carefully and then running `pytest` — all tests that relied on the refactored functions passed immediately. For a misleading suggestion, when I asked Copilot to "fix the scoring logic," it initially suggested changing the `update_score` function so that any guess on an odd attempt added points. This would have rewarded wrong guesses, which still made no sense. I caught this by writing a targeted test (`test_too_high_subtracts_points`) that proved the new score was still going up — so I rejected the suggestion and simplified the logic myself to always subtract 5 points for a wrong guess.

---

## 3. Debugging and testing your fixes

I treated each bug as fixed only when both a pytest assertion and a manual in-app test confirmed correct behavior. For the inverted-hint bug, I wrote `test_too_high_hint_says_go_lower()` and `test_too_low_hint_says_go_higher()`, which check that the word "LOWER" or "HIGHER" appears in the returned message. Before my fix, both tests failed; after the fix, both passed. I then ran the live app with `streamlit run app.py`, opened "Developer Debug Info" to see the secret, and verified that guessing a number above the secret displayed "Go LOWER!" — confirming the fix worked end-to-end. Copilot helped me understand how to assert on specific parts of a tuple return value (`result[0]` vs `result`), which made the tests much more readable.

---

## 4. What did you learn about Streamlit and state?

The secret number kept changing because Streamlit re-executes the entire Python script from top to bottom every time the user interacts with the page (clicks a button, types in a box, etc.). Each re-run hit the line `random.randint(low, high)` again and generated a fresh secret. The fix is `st.session_state`: a dictionary that persists across re-runs for a given user session. By writing `if "secret" not in st.session_state: st.session_state.secret = random.randint(low, high)`, the secret is only generated once and then stored safely between re-runs. I'd explain it to a friend like this: imagine Streamlit tears up and reprints the whole recipe card every time you stir the batter. `session_state` is a sticky note on the fridge that survives the reprint, so you don't forget ingredients you already added.

---

## 5. Looking ahead: your developer habits

One habit I want to carry forward is writing a failing test first, before fixing the bug. Seeing the test fail confirmed I understood the bug correctly, and seeing it pass confirmed the fix was real — not just a feeling. I also found it valuable to use separate, focused Copilot chat sessions for each bug rather than one long conversation; this kept the AI's context clean and its suggestions more relevant. Next time I work with AI on a coding task, I would ask for smaller, more targeted changes instead of broad rewrites, because large Agent-mode diffs are harder to review and easier to accept blindly. This project changed how I think about AI-generated code: I now treat it the same way I'd treat code written by a fast but careless intern — useful as a first draft, but always requiring a human to verify correctness before trusting it.
