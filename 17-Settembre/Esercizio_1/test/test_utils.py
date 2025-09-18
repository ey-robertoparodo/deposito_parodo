from utils.calcoli import somma
import pytest


@pytest.mark.parametrize("a, b, ris", [(5, 5, 10),(2, 3, 5)])
def test_somma(a, b, ris):
    assert somma(a, b) == ris
