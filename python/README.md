# Gilded Rose in Python

See the [exercise instructions](../README.md) and [requirements](../GildedRoseRequirements.md).

## Requirements

Python 3.10 or newer is required. Use a virtual environment to keep the project's
test dependencies separate from other projects. Dependency groups require pip
25.1 or newer; the setup commands below upgrade pip before installing them.

Test dependencies are declared in `pyproject.toml`. `requirements.txt` is the
original unpinned dependency list; prefer the test group, which also specifies
minimum versions.

## Setup (Linux / macOS)

From the repository root:

```sh
cd python
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --group test
```

Check that `python3 --version` reports Python 3.10 or newer. If needed, use the
executable for a suitable installed version when creating the environment.

Create the environment and install dependencies once per checkout. In a new
terminal, return to the `python` directory and run `source .venv/bin/activate`
again. Activation makes `python` refer to the virtual environment's interpreter.
Run `deactivate` to leave it. `.venv` is local and must not be committed.

## Tests

From the `python` directory with the environment activated:

```sh
python -m pytest -q
```

Run only the unit tests (no third-party dependencies required):

```sh
python -m unittest discover -s tests -p test_gilded_rose.py -v
```

Unit tests describe existing rules and boundaries. The approval test compares a
30-day simulation, including day zero, with the reviewed text file under
`tests/approved_files`. The baseline includes Conjured items under the new rules.

Conjured items lose 2 quality per day before their sell-by date and 4 when
`sell_in <= 0` at the start of the update. Quality stops at zero; `sell_in`
decreases by one even when quality is already zero.

Assumption: names beginning with the case-sensitive prefix `Conjured ` (including
the space) identify this category. This supports different conjured products;
names such as `ConjuredMana Cake` and `conjured Mana Cake` remain ordinary items.
No combined special-item rules are introduced for names such as `Conjured Aged Brie`;
they follow the Conjured rule. Existing categories retain their behavior.

If an approval test fails, compare the `.received.txt` and `.approved.txt` files.
Update the baseline only for an intentional, reviewed behavior change.

## Coverage

```sh
python -m coverage run -m pytest -q
python -m coverage report -m
```

Generated coverage files and Python caches are ignored by Git.

## Simulation

```sh
python texttest_fixture.py 10
```

For the separate TextTest application, see the [TextTest README](../texttests/README.md).

## Windows (PowerShell)

From the repository root, check the selected Python version and create the
environment. `py -3 --version` must report Python 3.10 or newer. If it selects an
older version, select a suitable installed version explicitly (for example,
`py -3.14 -m venv .venv` if Python 3.14 is installed).

```powershell
cd python
py -3 --version
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install --group test
```

If the Windows Python launcher (`py`) is unavailable, use `python` instead after
checking `python --version`. If an environment already exists, check
`.\.venv\Scripts\python.exe --version` before reusing it.

Use the environment's executable directly; activation and PowerShell execution
policy changes are unnecessary. From the `python` directory:

```powershell
# All tests
.\.venv\Scripts\python.exe -m pytest -q

# Unit tests only
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_gilded_rose.py -v

# Coverage
.\.venv\Scripts\python.exe -m coverage run -m pytest -q
.\.venv\Scripts\python.exe -m coverage report -m

# Simulation
.\.venv\Scripts\python.exe texttest_fixture.py 10
```
