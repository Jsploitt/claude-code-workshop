---
name: scout
description: Find open opportunities in Saudi Arabia (internships, hackathons, competitions, scholarships) that match profile.md, and return them as a JSON array. Use when asked to scout or check for opportunities.
disable-model-invocation: true
---

# Scout

1. Read profile.md in the current folder.
2. Search the web 6 to 10 times for opportunities in Saudi Arabia, or remote ones open to students in Saudi Arabia, that match the profile. Include the major's usual employers, university and club competitions, hackathons, and scholarship programs.
3. For each candidate, open its official page with WebFetch. Keep it only if the page confirms that it is real, still open, has a deadline after today, and a student in Saudi Arabia can apply. Drop anything you cannot confirm from the page itself.
4. Keep at most 10 items, soonest deadline first.
5. Your final message must be ONLY a JSON array, with no other text and no code fences. Each item:
   {"title": "...", "org": "...", "type": "internship|hackathon|competition|scholarship", "deadline": "YYYY-MM-DD", "url": "https://...", "why": "one sentence on why it fits the profile"}
   If nothing passes step 3, return [].
