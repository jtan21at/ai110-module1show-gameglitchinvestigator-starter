from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score

# ---------------------------------------------------------------------------
# check_guess — outcome and hint direction
# Note: check_guess returns a tuple (outcome, message); we check result[0].
# ---------------------------------------------------------------------------

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result[0] == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome should be "Too High"
    result = check_guess(60, 50)
    assert result[0] == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome should be "Too Low"
    result = check_guess(40, 50)
    assert result[0] == "Too Low"

# FIX: New tests that specifically target the inverted-hint bug.
# Before the fix, "Too High" returned "Go HIGHER!" — the wrong direction.
def test_too_high_hint_says_go_lower():
    # When the guess is too high the hint must tell the player to go LOWER
    _, message = check_guess(60, 50)
    assert "LOWER" in message, f"Expected 'LOWER' in hint, got: {message}"

def test_too_low_hint_says_go_higher():
    # When the guess is too low the hint must tell the player to go HIGHER
    _, message = check_guess(40, 50)
    assert "HIGHER" in message, f"Expected 'HIGHER' in hint, got: {message}"

# ---------------------------------------------------------------------------
# parse_guess — input validation
# ---------------------------------------------------------------------------

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_float_rounds_down():
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None

# ---------------------------------------------------------------------------
# get_range_for_difficulty — correct ranges
# ---------------------------------------------------------------------------

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1 and high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1 and high == 100

def test_hard_range_is_harder_than_normal():
    # FIX: Hard difficulty must have a wider range than Normal (bug was 1–50).
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, (
        f"Hard range ({hard_high}) should be wider than Normal range ({normal_high})"
    )

# ---------------------------------------------------------------------------
# update_score — consistent penalty for wrong guesses
# ---------------------------------------------------------------------------

def test_win_adds_points():
    new_score = update_score(0, "Win", 1)
    assert new_score > 0

def test_too_high_subtracts_points():
    # FIX: "Too High" must always subtract points, not reward on even attempts.
    score_after = update_score(50, "Too High", 2)  # attempt 2 was the problematic even case
    assert score_after < 50, "Wrong guess should decrease the score"

def test_too_low_subtracts_points():
    score_after = update_score(50, "Too Low", 1)
    assert score_after < 50

# ---------------------------------------------------------------------------
# parse_guess — None input
# ---------------------------------------------------------------------------

def test_parse_none_input():
    # None should be treated the same as an empty/missing guess
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None

# ---------------------------------------------------------------------------
# get_range_for_difficulty — unknown / fallback difficulty
# ---------------------------------------------------------------------------

def test_unknown_difficulty_returns_default_range():
    # Any unrecognised difficulty string must fall back to Normal (1–100)
    low, high = get_range_for_difficulty("Expert")
    assert low == 1 and high == 100

# ---------------------------------------------------------------------------
# update_score — minimum-points cap and unknown outcome
# ---------------------------------------------------------------------------

def test_win_score_is_at_least_10():
    # Late-game win: attempt_number=10 → 100 - 10*(10+1) = -10, clamped to 10
    new_score = update_score(0, "Win", 10)
    assert new_score == 10

def test_unknown_outcome_leaves_score_unchanged():
    # An unrecognised outcome string must not change the score
    score_after = update_score(50, "Draw", 1)
    assert score_after == 50
