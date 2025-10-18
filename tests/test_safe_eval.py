import ast
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from main import _safe_eval


def test_safe_eval_simple_expression():
    parsed = ast.parse("2 + 3 * 4", mode="eval")
    assert _safe_eval(parsed.body) == 14


def test_safe_eval_disallowed_expression():
    parsed = ast.parse("__import__('os').system('ls')", mode="eval")
    with pytest.raises(ValueError):
        _safe_eval(parsed.body)