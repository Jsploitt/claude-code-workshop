**Build 3: an agent that works while you don't (27 min)**

Opportunity Scout runs on its own every morning. It reads your profile, searches for internships, hackathons, competitions and scholarships in Saudi Arabia, checks each one on its official page, skips what it already showed you, and opens a one-page digest in your browser.

**1. Get the agent**
Download `opportunity-scout.zip`, unzip it into your Documents folder, and open a terminal in `opportunity-scout`.

**2. Tell it who you are**
```
claude
```
```
Interview me with the AskUserQuestion tool and fill in profile.md: my major, year, interests, skills, and the kinds of opportunities I want. At most 5 questions.
```

**3. Look at the skill**
Open `.claude/skills/scout/SKILL.md`. This is the whole job, written once. Try it here:
```
/scout
```
Type `/exit` when it answers.

**4. Run it with no chat window**
Windows:
```
powershell -ExecutionPolicy Bypass -File run.ps1
```
Mac:
```
bash run.sh
```
Your digest opens in the browser. Run it again: items it already showed you are no longer marked NEW.

**5. Put it on a schedule**
Ask Claude to do it:
```
claude
```
```
Schedule run.ps1 in this folder to run every day at 8:00 am with Windows Task Scheduler. Then show me the task with schtasks /query /tn OpportunityScout.
```
Mac: ask for a crontab entry that runs `bash run.sh --no-open` at 8:00 every day.
Remove it later with `schtasks /delete /tn OpportunityScout /f` (Windows) or `crontab -e` (Mac).
It runs only while your laptop is on and awake.

**Stretch**
- Add a site you trust to the search list in SKILL.md and run it again.
- Ask Claude to add a "days left" filter to render.py.

**How it stays safe**
- `run.ps1` lets the agent search the web, read web pages and read files, and nothing else. It cannot edit files or run commands.
- The Python script, not Claude, writes the page and the memory file.
- Every item must have a link Claude opened itself. Check the ones you act on.
- Your agent, your login, for you. Building something for other people needs an API key from the Claude Console, not your Pro or Max login.
- Never use `--dangerously-skip-permissions` on your own laptop.
