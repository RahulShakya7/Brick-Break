import pytest


def score_obtained(score):
    return score


def testing_highscore():
    high_score = 20
    assert (score_obtained(10) < high_score) is True == True


def testing_highscore1():
    high_score = 40
    assert (score_obtained(50) < high_score) is True == True


def testing_highscore2():
    high_score = 60
    assert (score_obtained(50) < high_score) is True == True


def testing_highscore3():
    high_score = 70
    assert (score_obtained(50) < high_score) is True == True


@pytest.fixture
def score0():
    score1 = 99
    return str(score1)


@pytest.mark.skip(str(99))
def test_score(score0):
    print('skipped')

