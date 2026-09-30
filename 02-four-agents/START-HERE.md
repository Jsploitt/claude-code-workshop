**Build 2: four agents at once (27 min)**

Four Claude sessions work on the same project at the same time. Each one gets its own git worktree: a separate copy of the project on its own branch, so their edits never collide. Then you merge the four branches.

**Which project?**
- Your Build 1 app, if it has at least one commit. Open a terminal in its folder.
- Or the starter: download `course-planner.zip`, unzip it, open a terminal in the `course-planner` folder, run `claude` once, accept the trust prompt, and type `/exit`.

**1. Open four terminals in the project folder**
Windows Terminal: Ctrl+Shift+T opens a new tab. In each tab, `cd` into the project folder.

**2. Start one agent per terminal**
```
claude -w feature
claude -w tests
claude -w docs
claude -w review
```
In each one, type `/model sonnet` first. Four agents at once use your plan's limits fast, and Sonnet stretches them.

**3. Give each agent its job** (starter users: the tasks are also in TASKS.md)

Terminal 1, feature:
```
Add [one feature to the app; starter: a weekly load bar chart of credit hours per day]. Put the logic in logic.py with a unittest for it, add the chart to app.py, run python -m unittest until it passes, then commit.
```
Terminal 2, tests:
```
Read logic.py and add unittest tests for edge cases that are not covered yet: empty input, zero values, very large values, invalid grades. Do not change any code outside tests/. Run python -m unittest and commit.
```
Terminal 3, docs:
```
Write README.md: what the app does, how to install it (pip install streamlit), how to run it, and how to run the tests. Change no other file. Commit.
```
Terminal 4, review:
```
Review this codebase for bugs and missing edge cases. Report only issues that affect correctness, not style. Write them to REVIEW.md with file and line for each, change no other file, and commit.
```

**4. Merge the four branches**
When all four have committed, type `/exit` in each and choose **Keep** when asked about the worktree. Then, in a fifth terminal in the main project folder:
```
claude
```
```
Merge the branches worktree-feature, worktree-tests, worktree-docs and worktree-review into the current branch. Resolve any conflicts, run python -m unittest, and show me the output.
```
Time left? Ask:
```
Fix the issues in REVIEW.md that affect correctness, run the tests, and commit.
```

**Why four separate agents?**
- Each has a clean context focused on one job.
- The reviewer never saw the code being written, so it judges the result, not its own reasoning.
- Worktrees keep their files apart until you decide to merge.

**Done looks like:** `git log` shows the merge, the tests pass, and `streamlit run app.py` shows the new feature.
