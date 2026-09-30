**Build 1: your first app, done properly (35 min)**

You will build a small Python app with a visual page, the way Anthropic recommends using Claude Code: interview, spec, plan, build with tests, commit.

**Before you start**
- Pick an idea you can say in one sentence. No idea? Pick one:
  - Software: a study-session log that charts hours per course per week.
  - Engineering: a projectile motion calculator that plots the path for a given speed and angle.
  - Any major: a shared-expenses splitter for roommates with a chart of who owes what.
- Stuck at any point? Download `course-planner.zip` from this folder, unzip it, and continue from step 5 with it.

**1. Make a folder and start Claude**
```
mkdir my-app
cd my-app
git init
claude
```

**2. Let Claude interview you** (paste, replacing the bracket)
```
I want to build [your one-sentence idea] as a Python app with a Streamlit page. Interview me using the AskUserQuestion tool. Ask about what the page shows, the inputs, edge cases, and what "done" looks like. Skip obvious questions. Ask at most 6 questions, then write a complete spec to SPEC.md, including how to test the logic with python -m unittest.
```

**3. Start clean**
Type `/clear`. The spec is saved in SPEC.md, so a fresh session loses nothing and focuses only on building.

**4. Plan before code**
Press Shift+Tab until the bottom bar shows `⏸ plan mode on`, then paste:
```
Read @SPEC.md and make a plan. Keep the logic in logic.py and the Streamlit page in app.py, so the logic can be tested without the page.
```
Press Ctrl+G if you want to edit the plan yourself. Approve the plan when it looks right.

**5. Build, with a check Claude can run**
```
Implement the plan. Write unittest tests for logic.py in tests/, run python -m unittest, and fix failures until every test passes. Show me the test output.
```

**6. See it**
Open a second terminal in the same folder and run:
```
streamlit run app.py
```
Your browser opens the page. Ask Claude for a change and refresh the page to see it.

**7. Give the project a memory**
```
/init
```
Then:
```
Keep CLAUDE.md under 15 lines: how to run the app, how to run the tests, and the rule that logic stays out of app.py.
```

**8. Commit** (you need this for Build 2)
```
Commit everything with a clear message.
```

**Keys you will use**
- Esc: stop Claude now. You keep the conversation.
- Esc Esc: rewind to an earlier point, code included.
- Shift+Tab: switch modes (plan mode, accept edits, auto).
- @file: point Claude at a file.
- /clear: start fresh between tasks.
- Corrected Claude twice on the same thing? Type /clear and write a better first prompt.

**Done looks like:** tests pass, the page opens, and `git log` shows your commit.
