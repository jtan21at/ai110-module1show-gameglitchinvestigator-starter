def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Refactored from app.py into logic_utils.py using Copilot Agent mode.
    # FIXME: Logic breaks here — Hard was mapped to 1–50, which is easier than Normal (1–100).
    # FIX: Hard now correctly uses a wider range (1–200) to make it genuinely harder.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIX: Refactored from app.py into logic_utils.py using Copilot Agent mode.
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIXME: Logic breaks here — hints were inverted.
    # The original code returned "Go HIGHER!" when the guess was too high,
    # and "Go LOWER!" when it was too low — the opposite of correct.
    # FIX: Refactored into logic_utils.py; corrected hint directions so
    # "Too High" → "Go LOWER!" and "Too Low" → "Go HIGHER!".
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIX: Refactored from app.py into logic_utils.py using Copilot Agent mode.
    # FIXME: Logic breaks here — the original code rewarded +5 points for a
    # "Too High" wrong guess on even-numbered attempts, which makes no sense.
    # FIX: All wrong guesses (Too High or Too Low) now consistently subtract 5 points.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
