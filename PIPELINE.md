# RedGuy daily pipeline (Phase 1)

Runbook for the daily scheduled task. Phase 1 = 1 carousel a day at 07:00 Tahiti + 2 stories (07:00 and 12:00) + 1 Reel at 18:00.
Owner: Henere. Every carousel needs his approval before it publishes.
Since 15 Nov 2026 Henere posts himself in the app (to add trending sounds to carousels and Reels): send him the slides (zip), stories, silent reel.mp4,
both captions and 2–3 trending sounds; do not schedule anything through Windsor unless he asks for it for that post.

## Fixed facts
- Instagram: Windsor.ai for Social Media, connector `instagram`, account `17841447489554216` (@redguy.fit).
  Actions: `create_carousel_post` (image_urls 2–10 JPEG, caption), `create_story` (image_url),
  `create_video_post` (video_url MP4, caption, share_to_feed) for Reels.
- Image hosting: this repo, public. URL pattern:
  `https://raw.githubusercontent.com/redguyfit/redguy-media/main/post-NNN/NN.jpg`
- Brand: background #F5F3EE, red #EF2020, black #111111, cyan #06B6D4. Headlines Archivo Black, body Inter.
- Timezone: Pacific/Tahiti (UTC-10). 07:00 Tahiti = 17:00 UTC.
- Audience: men 18–40. Every post opens on something they physically feel in the gym or in their body
  (sore for days, shoulder pinch on bench, can't feel the chest, no pump, elbow pain, strength stuck…) and gives a simple, practical fix.
  No study hunt per post (Henere, 15 Nov 2026). See "Content rules" and "Variety rules" below.
- Two topic families, alternate them: (1) what they feel in the gym; (2) male insecurities and how to fix them
  (skinny arms, narrow shoulders, flat chest, belly/love handles, looking small in a T-shirt, skinny legs, posture, gym anxiety, face fat).
  Insecurity posts: name the feeling, then fix it. Encouraging, never mocking or shaming bodies. No crash diets, no extreme cuts,
  no "you're worthless until…" framing. Anything medical (e.g. gynecomastia) → "see a doctor" line, no diagnosis.
- Reels first (Henere, 15 Nov 2026): the Reel is the main reach tool for non-followers. See "Reels" below.

## Content rules (Henere, 15 Nov 2026)
- Topic = a recurring sensation or frustration, from `content/queue.md`. Answer = 2–4 concrete fixes (technique, setup, rest, food, sleep).
- Plain, well-known coaching advice. No study per post, no study slide, no source line by default.
- Only put a number or "research shows" on a slide if it is common, settled knowledge you can state safely
  (e.g. "48–72 h" soreness window) — otherwise say it without a number. Never invent a figure or a citation.
- Pain topics: technique and setup tips only, plus one line "Sharp or lasting pain → see a physio." No diagnosis.

## Variety rules (Henere, 15 Nov 2026) — it must not look automated
- Rotate the format; never the same format two posts in a row. Formats:
  A. Problem → fixes (hook, problem, 2–3 fix slides, takeaway, CTA)
  B. Do this / Not this (each slide: ❌ wrong vs ✅ right)
  C. Quick checklist (hook, one slide listing 3–5 checks, one slide per check, CTA)
  D. Myth vs truth (hook, myth, truth, why, fix, CTA)
  E. "Try this next set" (hook, one drill or cue, step slides, CTA)
- Change the layout, not only the words: move the headline (top/middle/bottom), switch light/dark slides, change box styles, slide count 5–8.
- RedGuy: never the same pose on the same slide type as the previous post. Mirror (`transform: scaleX(-1)`), move him left/right,
  change size and crop between posts. Use the exercise poses (incline-press and any new ones in `assets/poses/`) whenever they fit.
- Hook wording, caption opening line, CTA line and question must differ from the last 3 posts (check their caption.txt).
- Log the format and the poses used per slide in `content/log.md` so the next run can avoid repeats.
- When a pose that would fit is missing, use the closest one and add it to `assets/poses/POSES-TODO.md` for Henere.
- Inspiration: `content/inspiration/` holds Henere's screenshots of BlueBro posts and `content/inspiration/notes.md` the patterns
  taken from them (hook types, formats, pacing, layouts, Reel structures). Use them to pick formats and structures.
  Never copy BlueBro's wording, drawings, character, layouts one-to-one or product names; take the idea, not the execution.

## Reels (main reach tool)
- Every post gets a Reel. Built to carry a trending sound Henere adds in the Instagram app (the API cannot attach Instagram music,
  and we never put copyrighted songs in our MP4s).
- Render silent: `python3 -I tools/reel.py --silent post-NNN/reel/reel.html post-NNN/reel.mp4 <seconds> 30`.
  Also keep the original-beat version (`reel-beat.mp4`, same command without --silent) as a fallback.
- Structure: 7–12 s. Hook text readable in the first 0.5 s (≤ 6 words, insecurity or feeling). One cut every ~1 s so any beat fits.
  Payoff (the fix) before 6 s. Last frame loops cleanly into the first. Text big, centered, clear of the bottom 300 px and right 120 px.
- Sound: each evening search the web for this week's trending Instagram Reels audio lists, and propose 2–3 sounds that fit the mood
  (name + artist + why). Henere picks one in the app. Never claim a sound is trending without a page you opened that says so.
- Reel caption: first line = hook (searchable words, e.g. "skinny arms fix"), 3–5 hashtags, "Follow for more" CTA.

## Repo layout
- `templates/` 7 slide templates (01-hook, 02-problem, 03-bignumber, 04-point, 05-list, 06-takeaway, 07-cta).
- `assets/poses/` crossed, point, thumbsdown, thumbsup, flex, dumbbell, eating (transparent PNG). `assets/avatar.png`.
- `post-NNN/` one folder per post: `slides/NN-name.dc.html`, rendered `01.jpg…`, `story.jpg`, `story2.jpg`, `caption.txt`.
- `content/queue.md` topics in order. `content/log.md` what was made, approved, published.
- `tools/render.py` renderer (see its docstring).
- `tools/reel.py` Reel renderer (1080x1920 MP4, 16 s) with `tools/reel_audio.py` (original synthesized beat + synced effects, no licensing issues). Example: `post-002/reel/reel.html`.

## Evening run (daily, ~16:45 Tahiti): make tomorrow's post
1. Read `content/log.md` and `content/queue.md`. Take the first queue topic not in the log. Next number = last post + 1.
2. No study research (see Content rules). Pick 2–4 practical fixes for the sensation. Read the last 3 posts' caption.txt and log rows to avoid repeating format, poses and wording.
3. Write the slides: copy `templates/` into `post-NNN/slides/`, change only text, counters and poses.
   - Hook ≤ 8 words. Every other slide ≤ 10 words, one idea. 5–8 slides total (drop or duplicate the point/list templates as needed).
   - No source line unless a slide states a research finding (rare; see Content rules).
   - Counters `N/total` must match. Watermark (avatar + REDGUY) stays bottom-left.
   - Poses: follow the Variety rules (no fixed pose per slide type). Pick poses that match the slide's meaning; vary mirror, side and size.
     If a topic really needs a pose that does not exist, use the closest one and tell Henere which pose to generate.
   - Never copy BlueBro's posts, wording or product names.
4. Render: `pip install --break-system-packages playwright` if missing (and `python3 -m playwright install chromium` if no Chrome).
   `python3 -I tools/render.py post-NNN/slides post-NNN`
   Stories: `python3 -I tools/render.py --story post-NNN/01.jpg post-NNN/story.jpg "New post" "Tap my profile to see it"`
   and the same with the takeaway slide → `story2.jpg` ("Save this rule", "Full post on my profile").
5. Look at every rendered JPEG (Read it). Fix any text touching the mascot, cut-off art or overflow; re-render.
5b. Reel: start from `post-002/reel/reel.html` (or `tools/workout_reel.py` for exercise lists) into `post-NNN/reel/reel.html`.
   Follow "Reels" above (silent, 7–12 s, ~1 s cuts). Same claims as the slides, nothing new.
   Check a frame every ~1.5 s (ffmpeg -ss … -frames:v 1) and fix overlaps. Write `post-NNN/reel-caption.txt`.
6. Write `post-NNN/caption.txt`: hook line (new wording) · 1–2 sentences on why it happens ·
   the rule in one line · a question that invites a one-word comment · "Save this. Follow @redguy.fit for gym science, drawn simple." ·
   5 hashtags. Under 2,200 characters.
7. Commit and push (`git -c user.name=redguyfit -c user.email=redguyfit@users.noreply.github.com`), then check each image URL returns 200 image/jpeg.
8. Send Henere a contact sheet of the slides and reel.mp4 (SendUserFile) and the caption (SendUserMessage). Ask (in French):
   "Réponds **post** (je programme le carrousel ; je t'envoie le Reel muet à 18:00 pour que tu le postes avec le son tendance),
   **post son RedGuy** (je publie aussi le Reel moi-même avec le son maison), ou dis-moi quoi changer."
   Include the 2–3 trending sound suggestions with the Reel.
9. On "post": schedule with send_later, in this session:
   - 07:00 Tahiti next day: `create_carousel_post` with the URLs in order and caption.txt, then `create_story` with story.jpg. Message Henere the result.
   - 12:00 Tahiti same day: `create_story` with story2.jpg.
   - 18:00 Tahiti same day, on "post" (default): remind Henere to post the silent reel.mp4 with the chosen trending sound
     and reel-caption.txt (send the MP4 again with SendUserFile and the sound suggestions).
   - Only on "post son RedGuy": `create_video_post` with
     video_url `https://raw.githubusercontent.com/redguyfit/redguy-media/main/post-NNN/reel-beat.mp4`, reel-caption.txt, share_to_feed true.
     raw.githubusercontent serves MP4 as application/octet-stream; if Instagram rejects it, tell Henere and send him the MP4 to post by hand.
   Add the post to `content/log.md` (number, topic, date, status "scheduled") and push.
   On changes: edit, re-render, push, send the new sheet, ask again. No reply = nothing is published.
10. Sundays: also pull the last 7 days of post stats through Windsor (`get_fields` then `get_data`, connector instagram):
    reach, saves, shares, follows per post. Compare Reels vs carousels and insecurity vs gym-feeling topics.
    Send a 5-line summary and whether to keep, raise or lower volume.

## Never
- Publish without Henere's "post" for that specific carousel.
- Publish more than one carousel and one Reel a day in Phase 1.
- Reply to comments or DMs as Henere.
