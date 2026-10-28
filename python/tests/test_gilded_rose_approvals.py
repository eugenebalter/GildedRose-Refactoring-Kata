import io
import sys
from contextlib import redirect_stdout
from unittest.mock import patch

from approvaltests import verify
from approvaltests.reporters.python_native_reporter import PythonNativeReporter
from texttest_fixture import main

def test_gilded_rose_approvals():
    fake_stdout = io.StringIO()
    with patch.object(sys, "argv", ["texttest_fixture.py", "30"]), redirect_stdout(fake_stdout):
        main()

    verify(fake_stdout.getvalue().rstrip() + "\n", reporter=PythonNativeReporter())

if __name__ == "__main__":
    test_gilded_rose_approvals()
