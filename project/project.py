# project.py
import json
import os
import random
import subprocess
import sys
import time


# ─────────────────────────────────────────────
#  ANSI COLOURS
# ─────────────────────────────────────────────
class C:
    HEADER = '\033[95m'
    BLUE   = '\033[94m'
    CYAN   = '\033[96m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    RED    = '\033[91m'
    BOLD   = '\033[1m'
    END    = '\033[0m'


# ─────────────────────────────────────────────
#  QUESTION BANK  (NumPy · Pandas · SQL)
# ─────────────────────────────────────────────
QUESTION_BANK = {
    "NumPy": [
        {
            "q": "Which NumPy function creates an array of evenly spaced values over a specified interval?",
            "opts": {"A": "np.arange()", "B": "np.linspace()", "C": "np.logspace()", "D": "np.spacing()"},
            "ans": "B",
            "exp": "np.linspace(start, stop, num) returns 'num' evenly spaced values between start and stop (inclusive)."
        },
        {
            "q": "What is the output of np.array([1,2,3]).reshape(3,1).shape?",
            "opts": {"A": "(1, 3)", "B": "(3,)", "C": "(3, 1)", "D": "(1, 3, 1)"},
            "ans": "C",
            "exp": "reshape(3,1) turns the 1-D array of 3 elements into a 2-D column vector of shape (3, 1)."
        },
        {
            "q": "What does np.dot(A, B) compute when A and B are 2-D arrays?",
            "opts": {"A": "Element-wise product", "B": "Matrix multiplication", "C": "Dot product of flattened arrays", "D": "Kronecker product"},
            "ans": "B",
            "exp": "For 2-D arrays np.dot() performs matrix multiplication, equivalent to A @ B."
        },
        {
            "q": "Which attribute gives the total number of elements in a NumPy array?",
            "opts": {"A": ".shape", "B": ".size", "C": ".ndim", "D": ".length"},
            "ans": "B",
            "exp": "arr.size returns the total number of elements (product of all dimension sizes)."
        },
        {
            "q": "What does np.where(condition, x, y) return?",
            "opts": {"A": "Indices where condition is True", "B": "x where condition is True, y elsewhere", "C": "Boolean mask", "D": "Count of True values"},
            "ans": "B",
            "exp": "np.where(cond, x, y) returns elements from x where cond is True, from y otherwise."
        },
        {
            "q": "What is broadcasting in NumPy?",
            "opts": {
                "A": "Sending arrays over a network",
                "B": "Duplicating an array in memory",
                "C": "Automatic expansion of arrays with smaller shapes to match larger shapes in operations",
                "D": "Printing array values to stdout"
            },
            "ans": "C",
            "exp": "Broadcasting allows NumPy to work with arrays of different shapes during arithmetic operations without copying data."
        },
        {
            "q": "Which function stacks arrays vertically (row-wise)?",
            "opts": {"A": "np.hstack()", "B": "np.vstack()", "C": "np.dstack()", "D": "np.concatenate(axis=1)"},
            "ans": "B",
            "exp": "np.vstack() stacks arrays along the first axis (rows). np.hstack() stacks along the second axis (columns)."
        },
        {
            "q": "What is the default dtype of np.zeros((3, 3))?",
            "opts": {"A": "int32", "B": "int64", "C": "float64", "D": "float32"},
            "ans": "C",
            "exp": "np.zeros() and np.ones() default to float64 unless dtype is specified."
        },
        {
            "q": "What does np.linalg.inv(A) compute?",
            "opts": {"A": "Eigenvalues of A", "B": "Transpose of A", "C": "Inverse of matrix A", "D": "Determinant of A"},
            "ans": "C",
            "exp": "np.linalg.inv(A) returns the multiplicative inverse of the square matrix A."
        },
        {
            "q": "How do you select elements of arr that are greater than 5?",
            "opts": {"A": "arr.filter(arr > 5)", "B": "arr[arr > 5]", "C": "arr.where(arr > 5)", "D": "np.select(arr, 5)"},
            "ans": "B",
            "exp": "Boolean indexing: arr[arr > 5] returns a 1-D array of elements satisfying the condition."
        },
        {
            "q": "What is the result of np.arange(10).reshape(2, 5)[1, ::2]?",
            "opts": {"A": "array([0, 2, 4])", "B": "array([5, 7, 9])", "C": "array([1, 3, 5])", "D": "array([6, 8])"},
            "ans": "B",
            "exp": "Row index 1 gives [5,6,7,8,9]; ::2 slices every other element → [5, 7, 9]."
        },
        {
            "q": "Which function returns the indices that would sort an array?",
            "opts": {"A": "np.sort()", "B": "np.argsort()", "C": "np.sortindex()", "D": "np.order()"},
            "ans": "B",
            "exp": "np.argsort() returns the indices that would sort the array. np.sort() returns the sorted array itself."
        },
        {
            "q": "What does the axis parameter do in np.sum(arr, axis=0)?",
            "opts": {
                "A": "Sums all elements ignoring shape",
                "B": "Sums along rows, collapsing columns",
                "C": "Sums along columns, collapsing rows",
                "D": "Sums only the first row"
            },
            "ans": "C",
            "exp": "axis=0 collapses along the first dimension (rows), so each column is summed independently."
        },
        {
            "q": "What is a NumPy structured array?",
            "opts": {
                "A": "An array with only integer dtype",
                "B": "An array that can hold multiple dtypes per element (like a table row)",
                "C": "A multi-dimensional array with more than 3 axes",
                "D": "An immutable NumPy array"
            },
            "ans": "B",
            "exp": "Structured arrays use a compound dtype, allowing each element to contain multiple fields of different types."
        },
        {
            "q": "Which method makes a deep copy of a NumPy array?",
            "opts": {"A": "arr.view()", "B": "arr.copy()", "C": "arr.clone()", "D": "np.duplicate(arr)"},
            "ans": "B",
            "exp": "arr.copy() creates a deep copy. arr.view() creates a view sharing the same data buffer."
        },
    ],

    "Pandas": [
        {
            "q": "What is the difference between loc[] and iloc[] in Pandas?",
            "opts": {
                "A": "loc uses integer positions; iloc uses labels",
                "B": "loc uses labels; iloc uses integer positions",
                "C": "They are identical",
                "D": "loc is faster than iloc"
            },
            "ans": "B",
            "exp": "loc is label-based indexing; iloc is positional (integer-based) indexing."
        },
        {
            "q": "What does df.groupby('col').agg({'val': 'sum'}) do?",
            "opts": {
                "A": "Filters rows where col equals sum",
                "B": "Groups rows by 'col' and returns the sum of 'val' per group",
                "C": "Sorts by 'col' then sums 'val'",
                "D": "Creates a new column named 'sum'"
            },
            "ans": "B",
            "exp": "groupby + agg splits the DataFrame by unique values in 'col', then applies the specified aggregation."
        },
        {
            "q": "Which Pandas method removes duplicate rows?",
            "opts": {"A": "df.unique()", "B": "df.drop_duplicates()", "C": "df.deduplicate()", "D": "df.distinct()"},
            "ans": "B",
            "exp": "df.drop_duplicates() returns a DataFrame with duplicate rows removed."
        },
        {
            "q": "What does df.pivot_table(values='sales', index='region', columns='year', aggfunc='mean') produce?",
            "opts": {
                "A": "A flat list of mean sales",
                "B": "A 2-D table with regions as rows, years as columns, and mean sales as values",
                "C": "A grouped series indexed by year",
                "D": "A new column 'mean' added to df"
            },
            "ans": "B",
            "exp": "pivot_table reshapes the DataFrame into a 2-D summary table, computing the specified aggregation."
        },
        {
            "q": "What is the output dtype of a Pandas Series containing [1, 2, None]?",
            "opts": {"A": "int64", "B": "object", "C": "float64", "D": "Int64 (nullable integer)"},
            "ans": "C",
            "exp": "None/NaN in an int Series promotes the dtype to float64 because NaN is a float."
        },
        {
            "q": "How do you efficiently apply a function element-wise to a Pandas Series?",
            "opts": {"A": "series.apply(func)", "B": "series.map(func)", "C": "series.applymap(func)", "D": "Both A and B"},
            "ans": "D",
            "exp": "Both .apply() and .map() work element-wise on a Series."
        },
        {
            "q": "What does pd.merge(df1, df2, how='left', on='id') do?",
            "opts": {
                "A": "Returns only rows common to both DataFrames",
                "B": "Returns all rows from df1 and matching rows from df2; NaN for non-matches",
                "C": "Returns all rows from both DataFrames",
                "D": "Returns all rows from df2 with matching rows from df1"
            },
            "ans": "B",
            "exp": "A left join keeps all rows from df1 and fills NaN where there is no matching key in df2."
        },
        {
            "q": "What is the purpose of df.melt()?",
            "opts": {
                "A": "Converts wide-format DataFrame to long-format",
                "B": "Melts all NaN values",
                "C": "Converts long-format DataFrame to wide-format",
                "D": "Flattens a MultiIndex"
            },
            "ans": "A",
            "exp": "melt() unpivots columns into rows, converting a wide DataFrame to a long (tidy) format."
        },
        {
            "q": "Which method fills missing values with the previous valid observation?",
            "opts": {"A": "df.fillna(method='pad')", "B": "df.ffill()", "C": "df.bfill()", "D": "Both A and B"},
            "ans": "D",
            "exp": "Both df.fillna(method='ffill') / method='pad' and df.ffill() forward-fill missing values."
        },
        {
            "q": "What does df.resample('M').sum() require?",
            "opts": {
                "A": "A numeric index",
                "B": "A DatetimeIndex",
                "C": "A MultiIndex",
                "D": "A RangeIndex"
            },
            "ans": "B",
            "exp": "resample() is a time-series function that requires the DataFrame index to be a DatetimeIndex."
        },
        {
            "q": "How do you select all columns except one named 'drop_me'?",
            "opts": {
                "A": "df.drop('drop_me')",
                "B": "df.drop(columns=['drop_me'])",
                "C": "df.remove('drop_me', axis=1)",
                "D": "df[df.columns != 'drop_me']"
            },
            "ans": "B",
            "exp": "df.drop(columns=['drop_me']) is the idiomatic way to remove a column."
        },
        {
            "q": "What is a Pandas MultiIndex?",
            "opts": {
                "A": "An index with duplicate labels",
                "B": "A hierarchical index with multiple levels, enabling advanced grouping",
                "C": "An index referencing multiple DataFrames",
                "D": "An integer index larger than int32"
            },
            "ans": "B",
            "exp": "MultiIndex allows multiple levels of row/column labels for complex data organisation."
        },
        {
            "q": "What does df.explode('list_col') do?",
            "opts": {
                "A": "Raises an error on list columns",
                "B": "Transforms each element of a list-like column into a separate row",
                "C": "Converts a list column to a string",
                "D": "Counts list lengths per row"
            },
            "ans": "B",
            "exp": "explode() unnests list-like elements, creating one row per element."
        },
        {
            "q": "Which statement about df.copy(deep=False) is correct?",
            "opts": {
                "A": "Creates a completely independent copy",
                "B": "Creates a new DataFrame object but shares the underlying data",
                "C": "Is identical to df.copy()",
                "D": "Only copies the index, not the data"
            },
            "ans": "B",
            "exp": "A shallow copy creates a new object but does not copy the data buffer."
        },
        {
            "q": "What does pd.cut(series, bins=4) do?",
            "opts": {
                "A": "Removes the top 4 rows",
                "B": "Splits series into 4 equal-width intervals and returns categorical codes",
                "C": "Rounds values to 4 decimal places",
                "D": "Samples 4 elements"
            },
            "ans": "B",
            "exp": "pd.cut() bins continuous data into discrete intervals."
        },
    ],

    "SQL": [
        {
            "q": "What is the difference between HAVING and WHERE?",
            "opts": {
                "A": "WHERE filters after aggregation; HAVING filters before",
                "B": "HAVING filters after aggregation; WHERE filters before",
                "C": "They are interchangeable",
                "D": "WHERE works only on numeric columns"
            },
            "ans": "B",
            "exp": "WHERE filters rows before grouping; HAVING filters groups after GROUP BY."
        },
        {
            "q": "Which SQL join returns all rows from both tables, with NULLs where there is no match?",
            "opts": {"A": "INNER JOIN", "B": "LEFT JOIN", "C": "RIGHT JOIN", "D": "FULL OUTER JOIN"},
            "ans": "D",
            "exp": "FULL OUTER JOIN returns all rows from both tables; unmatched rows get NULLs."
        },
        {
            "q": "What does the COALESCE function do?",
            "opts": {
                "A": "Concatenates two strings",
                "B": "Returns the first non-NULL value in a list",
                "C": "Counts non-NULL values",
                "D": "Converts NULL to zero"
            },
            "ans": "B",
            "exp": "COALESCE(val1, val2, ...) returns the first argument that is not NULL."
        },
        {
            "q": "What is a CTE (Common Table Expression)?",
            "opts": {
                "A": "A permanent view stored in the database",
                "B": "A temporary named result set defined with WITH and usable in the main query",
                "C": "A type of index",
                "D": "A stored procedure with parameters"
            },
            "ans": "B",
            "exp": "A CTE (WITH clause) defines a temporary named result set for use within a single query."
        },
        {
            "q": "Which window function assigns a unique rank with no gaps when values are equal?",
            "opts": {"A": "RANK()", "B": "ROW_NUMBER()", "C": "DENSE_RANK()", "D": "NTILE()"},
            "ans": "C",
            "exp": "DENSE_RANK() assigns consecutive ranks with no gaps. RANK() skips ranks after ties."
        },
        {
            "q": "What is the correct order of SQL clauses in a SELECT statement?",
            "opts": {
                "A": "SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY",
                "B": "FROM → SELECT → WHERE → GROUP BY → HAVING → ORDER BY",
                "C": "SELECT → WHERE → FROM → GROUP BY → ORDER BY → HAVING",
                "D": "FROM → WHERE → GROUP BY → SELECT → HAVING → ORDER BY"
            },
            "ans": "A",
            "exp": "Written order: SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY."
        },
        {
            "q": "What does SELECT * FROM orders WHERE id IN (SELECT order_id FROM returns) do?",
            "opts": {
                "A": "Returns orders not in returns",
                "B": "Returns orders whose id appears in the returns subquery",
                "C": "Raises a syntax error",
                "D": "Returns only the order_id column"
            },
            "ans": "B",
            "exp": "IN with a subquery filters rows whose column value matches any value in the inner SELECT."
        },
        {
            "q": "What is the difference between TRUNCATE and DELETE?",
            "opts": {
                "A": "DELETE removes all rows; TRUNCATE removes specific rows",
                "B": "TRUNCATE is DDL, removes all rows faster without logging individual rows; DELETE is DML and can use WHERE",
                "C": "They are identical",
                "D": "TRUNCATE can be rolled back; DELETE cannot"
            },
            "ans": "B",
            "exp": "TRUNCATE is DDL and fast; DELETE is DML, can filter rows, and logs each deletion."
        },
        {
            "q": "Which normal form eliminates transitive dependencies?",
            "opts": {"A": "1NF", "B": "2NF", "C": "3NF", "D": "BCNF"},
            "ans": "C",
            "exp": "3NF requires no non-key attribute depends on another non-key attribute."
        },
        {
            "q": "What does LAG(salary, 1) OVER (ORDER BY hire_date) return?",
            "opts": {
                "A": "Next row's salary",
                "B": "Previous row's salary in hire_date order",
                "C": "Maximum salary so far",
                "D": "Salary 1% lower"
            },
            "ans": "B",
            "exp": "LAG(col, n) returns the value of col from n rows before the current row."
        },
        {
            "q": "What is an index in SQL, and what is a trade-off of using one?",
            "opts": {
                "A": "A constraint that ensures uniqueness; trade-off is slower reads",
                "B": "A data structure that speeds up reads; trade-off is slower writes and extra storage",
                "C": "A backup copy of a table; trade-off is extra storage",
                "D": "A foreign key; trade-off is referential overhead"
            },
            "ans": "B",
            "exp": "Indexes speed up SELECT queries but add overhead to INSERT/UPDATE/DELETE."
        },
        {
            "q": "Which SQL statement is used to grant permissions to a user?",
            "opts": {"A": "PERMIT", "B": "ALLOW", "C": "GRANT", "D": "ASSIGN"},
            "ans": "C",
            "exp": "GRANT privilege ON object TO user; is the standard SQL command for assigning permissions."
        },
        {
            "q": "What does the EXPLAIN keyword do in most SQL databases?",
            "opts": {
                "A": "Runs the query and explains errors",
                "B": "Shows the query execution plan without running the query",
                "C": "Adds comments to the query",
                "D": "Converts SQL to Python code"
            },
            "ans": "B",
            "exp": "EXPLAIN shows the query plan so you can optimise performance."
        },
        {
            "q": "What is the purpose of ACID properties in databases?",
            "opts": {
                "A": "To speed up queries",
                "B": "To ensure reliable processing of database transactions",
                "C": "To enforce referential integrity",
                "D": "To compress stored data"
            },
            "ans": "B",
            "exp": "ACID (Atomicity, Consistency, Isolation, Durability) guarantees reliable transaction processing."
        },
        {
            "q": "What does a self-join accomplish?",
            "opts": {
                "A": "Joins a table to a view with the same name",
                "B": "Joins a table to itself to compare rows within the same table",
                "C": "Creates a recursive CTE",
                "D": "Joins two tables with identical schemas"
            },
            "ans": "B",
            "exp": "A self-join uses aliases to join a table to itself, useful for hierarchies like employee-manager."
        },
    ],
}


# ─────────────────────────────────────────────
#  GIT AUTO-PUSH
# ─────────────────────────────────────────────
def git_auto_push(filepath: str, score: int, total: int, grade: str) -> None:
    """
    Automatically stage, commit, and push quiz_history.json to GitHub.
    Works silently — prints a friendly status either way.
    """
    print(f"\n{C.CYAN}{C.BOLD}🚀 Auto-pushing results to GitHub…{C.END}")

    # ── make sure we are inside a git repo ────────────────────────────
    repo_root = _find_git_root()
    if repo_root is None:
        print(f"{C.YELLOW}⚠️  Not inside a Git repository. Skipping push.{C.END}")
        return

    timestamp  = time.strftime("%Y-%m-%d %H:%M:%S")
    pct        = round(score / total * 100, 1) if total else 0
    commit_msg = (
        f"quiz result [{timestamp}] "
        f"score={score}/{total} ({pct}%) grade={grade}"
    )

    steps = [
        # configure safe directory (needed in some CI / codespaces)
        ["git", "-C", repo_root, "config", "--global",
         "--add", "safe.directory", repo_root],
        # stage only the history file
        ["git", "-C", repo_root, "add", filepath],
        # commit  (--allow-empty skips error when nothing new to commit)
        ["git", "-C", repo_root, "commit", "--allow-empty",
         "-m", commit_msg],
        # push to the tracking remote/branch
        ["git", "-C", repo_root, "push"],
    ]

    for cmd in steps:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            # commit "nothing to commit" is not a real error
            if "nothing to commit" in result.stdout + result.stderr:
                continue
            print(f"{C.YELLOW}⚠️  Git warning on step {cmd[2]}:{C.END}")
            print(f"   {result.stderr.strip()}")
            # don't abort — try the remaining steps

    print(f"{C.GREEN}✅ Results pushed to GitHub!{C.END}")
    print(f"{C.CYAN}   Commit: {commit_msg}{C.END}")


def _find_git_root() -> str | None:
    """Walk up from CWD to find the nearest .git directory."""
    current = os.path.abspath(os.getcwd())
    while True:
        if os.path.isdir(os.path.join(current, ".git")):
            return current
        parent = os.path.dirname(current)
        if parent == current:          # reached filesystem root
            return None
        current = parent


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def print_banner() -> None:
    print(f"""
{C.CYAN}{C.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🧠  NumPy  •  Pandas  •  SQL  Quiz  🧠               ║
║                                                              ║
║        CS50   |  45 Expert Questions                         ║
║        Results auto-pushed to GitHub after each quiz         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{C.END}""")


def choose_topic() -> str:
    topics = {
        "1": "NumPy",
        "2": "Pandas",
        "3": "SQL",
        "4": "Mixed (All Topics)",
    }
    print(f"\n{C.BOLD}{C.BLUE}📚 Choose a Topic:{C.END}")
    print(f"{C.CYAN}{'─'*40}{C.END}")
    for k, v in topics.items():
        print(f"  {C.YELLOW}[{k}]{C.END}  {v}")
    print(f"{C.CYAN}{'─'*40}{C.END}")
    while True:
        ch = input(f"\n{C.BOLD}Enter choice (1-4): {C.END}").strip()
        if ch in topics:
            print(f"{C.GREEN}✓ Selected: {topics[ch]}{C.END}")
            return topics[ch]
        print(f"{C.RED}Invalid. Enter 1-4.{C.END}")


def choose_difficulty() -> str:
    levels   = {"1": "easy", "2": "medium", "3": "hard", "4": "any"}
    display  = {
        "1": "🟢 Easy   (Q 1-5)",
        "2": "🟡 Medium (Q 6-10)",
        "3": "🔴 Hard   (Q 11-15)",
        "4": "🌈 Any",
    }
    print(f"\n{C.BOLD}{C.BLUE}💪 Choose Difficulty:{C.END}")
    print(f"{C.CYAN}{'─'*40}{C.END}")
    for k, v in display.items():
        print(f"  {C.YELLOW}[{k}]{C.END}  {v}")
    print(f"{C.CYAN}{'─'*40}{C.END}")
    while True:
        ch = input(f"\n{C.BOLD}Enter choice (1-4): {C.END}").strip()
        if ch in levels:
            print(f"{C.GREEN}✓ Selected: {display[ch]}{C.END}")
            return levels[ch]
        print(f"{C.RED}Invalid. Enter 1-4.{C.END}")


def choose_num_questions(max_q: int) -> int:
    print(f"\n{C.BOLD}{C.BLUE}🔢 How many questions? (1 – {max_q}){C.END}")
    while True:
        try:
            n = int(input(f"{C.BOLD}Enter number: {C.END}").strip())
            if 1 <= n <= max_q:
                print(f"{C.GREEN}✓ {n} questions selected!{C.END}")
                return n
            print(f"{C.RED}Enter a number between 1 and {max_q}.{C.END}")
        except ValueError:
            print(f"{C.RED}Please enter a valid number.{C.END}")


def build_question_pool(topic: str, difficulty: str) -> list:
    """
    Return a shuffled list of questions filtered by topic and difficulty.

    Difficulty slices per-topic (15 questions each):
        easy   → indices  0-4
        medium → indices  5-9
        hard   → indices 10-14
        any    → all 15
    """
    if topic == "Mixed (All Topics)":
        raw = (
            QUESTION_BANK["NumPy"]
            + QUESTION_BANK["Pandas"]
            + QUESTION_BANK["SQL"]
        )
    else:
        raw = QUESTION_BANK[topic]

    if difficulty == "easy":
        pool = [q for i, q in enumerate(raw) if i % 15 < 5]
    elif difficulty == "medium":
        pool = [q for i, q in enumerate(raw) if 5 <= i % 15 < 10]
    elif difficulty == "hard":
        pool = [q for i, q in enumerate(raw) if i % 15 >= 10]
    else:
        pool = raw[:]

    random.shuffle(pool)
    return pool


def get_grade(pct: float) -> tuple[str, str]:
    if pct >= 93: return "A+", "🏆"
    if pct >= 90: return "A",  "🌟"
    if pct >= 87: return "A-", "⭐"
    if pct >= 83: return "B+", "👏"
    if pct >= 80: return "B",  "👍"
    if pct >= 77: return "B-", "😊"
    if pct >= 73: return "C+", "📚"
    if pct >= 70: return "C",  "📖"
    if pct >= 67: return "C-", "✏️"
    if pct >= 60: return "D",  "⚠️"
    return "F", "📕"


def save_results(
    score: int,
    total: int,
    pct:   float,
    grade: str,
    log:   list,
) -> str:
    """
    Append quiz result to quiz_history.json.
    Returns the absolute path to the file.
    """
    record = {
        "timestamp":  time.strftime("%Y-%m-%d %H:%M:%S"),
        "score":      score,
        "total":      total,
        "percentage": round(pct, 1),
        "grade":      grade,
        "log":        log,
    }

    # Always save next to project.py so git can find it
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "quiz_history.json")
    try:
        with open(fname, "r") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    history.append(record)

    with open(fname, "w") as f:
        json.dump(history, f, indent=2)

    print(f"{C.GREEN}💾 Results saved → {fname}{C.END}")
    return fname


def format_question_check(q: dict) -> bool:
    """Utility used by tests to validate a question's structure."""
    required = {"q", "opts", "ans", "exp"}
    return (
        required.issubset(q.keys())
        and q["ans"] in q["opts"]
        and len(q["opts"]) == 4
    )


# ─────────────────────────────────────────────
#  PRESENT A SINGLE QUESTION
# ─────────────────────────────────────────────
def present_question(question: dict, current: int, total: int) -> str:
    """
    Display question and collect answer.
    Returns 'CORRECT' | 'WRONG' | 'SKIPPED' | 'QUIT'
    """
    opt_colors = {"A": C.YELLOW, "B": C.GREEN, "C": C.BLUE, "D": C.RED}

    print(f"\n{C.BOLD}{C.BLUE}┌{'─'*58}┐{C.END}")
    print(f"{C.BOLD}{C.BLUE}│  Question {current:>2} / {total}  {C.END}")
    print(f"{C.BOLD}{C.BLUE}└{'─'*58}┘{C.END}")
    print(f"\n  {C.BOLD}{C.CYAN}{question['q']}{C.END}\n")

    for lbl in ("A", "B", "C", "D"):
        col = opt_colors[lbl]
        print(f"    {col}{C.BOLD}[{lbl}]{C.END} {question['opts'][lbl]}")

    print()

    while True:
        raw = input(
            f"  {C.BOLD}Answer (A/B/C/D) | 'next' skip | 'quit' exit: {C.END}"
        ).strip().upper()

        if raw == "QUIT":
            return "QUIT"

        if raw == "NEXT":
            correct_lbl = question["ans"]
            print(f"  {C.YELLOW}⏭️  Skipped!  Correct → "
                  f"{correct_lbl}) {question['opts'][correct_lbl]}{C.END}")
            print(f"  {C.CYAN}💡 {question['exp']}{C.END}")
            return "SKIPPED"

        if raw in ("A", "B", "C", "D"):
            if raw == question["ans"]:
                print(f"\n  {C.GREEN}{C.BOLD}✅  CORRECT! 🎉{C.END}")
                print(f"  {C.CYAN}💡 {question['exp']}{C.END}")
                return "CORRECT"
            else:
                correct_lbl = question["ans"]
                print(f"\n  {C.RED}{C.BOLD}❌  WRONG!{C.END}")
                print(f"  {C.YELLOW}Correct → "
                      f"{correct_lbl}) {question['opts'][correct_lbl]}{C.END}")
                print(f"  {C.CYAN}💡 {question['exp']}{C.END}")
                return "WRONG"

        print(f"  {C.RED}Type A, B, C, D, 'next', or 'quit'.{C.END}")


# ─────────────────────────────────────────────
#  WAIT FOR 'NEXT'
# ─────────────────────────────────────────────
def wait_for_next() -> None:
    print(f"\n{C.CYAN}{'─'*60}{C.END}")
    while True:
        cmd = input(
            f"  {C.BOLD}{C.YELLOW}Type 'next' to continue ➡️   : {C.END}"
        ).strip().lower()
        if cmd == "next":
            print(f"{C.CYAN}{'─'*60}{C.END}\n")
            return
        if cmd == "quit":
            print(f"\n{C.YELLOW}👋 Goodbye!{C.END}")
            sys.exit(0)
        print(f"  {C.RED}Type 'next' or 'quit'.{C.END}")


# ─────────────────────────────────────────────
#  SHOW FINAL RESULTS
# ─────────────────────────────────────────────
def show_results(
    score:     int,
    total:     int,
    log:       list,
    questions: list,
) -> None:
    if total == 0:
        print(f"\n{C.RED}No questions attempted.{C.END}")
        return

    pct          = (score / total) * 100
    grade, emoji = get_grade(pct)

    print(f"\n\n{C.BOLD}{C.CYAN}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    📊  FINAL RESULTS  📊                    ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║   Score      : {score:>3} / {total:<3}                      ║")
    print(f"║   Percentage : {pct:>6.1f}%                                 ║")
    print(f"║   Grade      : {grade:<4}  {emoji}                          ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║              Question-by-Question Breakdown                  ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(C.END)

    for i, status in enumerate(log):
        if i >= len(questions):
            break
        icon  = (f"{C.GREEN}✅{C.END}" if status == "CORRECT"
                 else f"{C.RED}❌{C.END}" if status == "WRONG"
                 else f"{C.YELLOW}⏭️ {C.END}")
        short = questions[i]["q"][:50]
        print(f"  Q{i+1:>2}:  {icon}  {short}")

    print(f"\n{C.CYAN}{C.BOLD}", end="")
    msg = (
        "🏆  OUTSTANDING! You're a data genius!"  if pct >= 90 else
        "🌟  Great job! Strong fundamentals!"      if pct >= 70 else
        "👍  Decent. Revise the explanations!"     if pct >= 50 else
        "📖  Study more — read the explanations!"  if pct >= 30 else
        "💪  Don't quit! Review and retry!"
    )
    print(f"\n  {msg}")
    print(f"{'═'*64}{C.END}\n")

    # ── save then AUTO-PUSH ────────────────────────────────────────────
    history_file = save_results(score, total, pct, grade, log)
    git_auto_push(history_file, score, total, grade)


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main() -> None:
    print_banner()

    topic      = choose_topic()
    difficulty = choose_difficulty()
    pool       = build_question_pool(topic, difficulty)
    max_q      = len(pool)

    if max_q == 0:
        print(f"{C.RED}No questions match that filter. Try 'Any' difficulty.{C.END}")
        sys.exit(1)

    num_q     = choose_num_questions(max_q)
    questions = pool[:num_q]

    print(f"\n{C.GREEN}✅  {len(questions)} questions ready!{C.END}")
    print(f"{C.YELLOW}A/B/C/D → answer  |  'next' → skip  |  'quit' → exit{C.END}")
    print(f"{C.CYAN}{'─'*60}{C.END}\n")

    score = 0
    log   = []

    for idx, q in enumerate(questions):
        result = present_question(q, idx + 1, len(questions))

        if result == "QUIT":
            questions = questions[:idx]
            break
        if result == "CORRECT":
            score += 1

        log.append(result)

        if idx < len(questions) - 1:
            wait_for_next()

    show_results(score, len(log), log, questions)


if __name__ == "__main__":
    main()