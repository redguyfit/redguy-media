# RedGuy daily pipeline (Phase 1)

Runbook for the daily scheduled task. Phase 1 = 1 carousel a day at 07:00 Tahiti + 2 stories (07:00 and 12:00) + 1 Reel at 18:00.
Owner: Henere. Every carousel needs his approval before it publishes.

## Fixed facts
- Instagram: Windsor.ai for Social Media, connector `instagram`, account `17841447489554216` (@redguy.fit).
  Actions: `create_carousel_post` (image_urls 2–10 JPEG, caption), `create_story` (image_url),
  `create_video_post` (video_url MP4, caption, share_to_feed) for Reels.
- Image hosting: this repo, public. URL pattern:
  `https://raw.githubusercontent.com/redguyfit/redguy-media/main/post-NNN/NN.jpg`
- Brand: background #F5F3EE, red #EF2020, black #111111, cyan #06B6D4. Headlines Archivo Black, body Inter.
- Timezone: Pacific/Tahiti (UTC-10). 07:00 Tahiti = 17:00 UTC.

## Repo layout
- `templates/` 7 slide templates (01-hook, 02-problem, 03-bignumber, 04-point, 05-list, 06-takeaway, 07-cta).
- `assets/poses/` crossed, point, thumbsdown, thumbsup, flex, dumbbell, eating (transparent PNG). `assets/avatar.png`.
- `post-NNN/` one folder per post: `slides/NN-name.dc.html`, rendered `01.jpg…`, `story.jpg`, `story2.jpg`, `caption.txt`.
- `content/queue.md` topics in order. `content/log.md` what was made, approved, published.
- `tools/render.py` renderer (see its docstring).
- `tools/reel.py` Reel renderer (1080x1920 MP4, 16 s) with `tools/reel_audio.py` (original synthesized beat + synced effects, no licensing issues). Example: `post-002/reel/reel.html`.

## Evening run (daily, ~16:45 Tahiti): make tomorrow's post
1. Read `content/log.md` and `content/queue.md`. Take the first queue topic not in the log. Next number = last post + 1.
2. Research before writing. Open the study's PubMed page (or the full text) with WebFetch and confirm every number you will use.
   A number you cannot confirm from a page you opened does not go on a slide. Note established vs uncertain evidence.
3. Write the slides: copy `templates/` into `post-NNN/slides/`, change only text, counters and poses.
   - Hook ≤ 8 words. Every other slide ≤ 10 words, one idea. 5–8 slides total (drop or duplicate the point/list templates as needed).
   - One small source line (Author et al., Journal, Year) on the slide that states the finding.
   - Counters `N/total` must match. Watermark (avatar + REDGUY) stays bottom-left.
   - Poses: hook = crossed, problem/myth = thumbsdown, research = dumbbell or point, nutrition = eating, takeaway = thumbsup, CTA = flex.
     If a topic really needs a pose that does not exist, use the closest one and tell Henere which pose to generate.
   - Never copy BlueBro's posts, wording or product names.
4. Render: `pip install --break-system-packages playwright` if missing (and `python3 -m playwright install chromium` if no Chrome).
   `python3 -I tools/render.py post-NNN/slides post-NNN`
   Stories: `python3 -I tools/render.py --story post-NNN/01.jpg post-NNN/story.jpg "New post" "Tap my profile to see it"`
   and the same with the takeaway slide → `story2.jpg` ("Save this rule", "Full post on my profile").
5. Look at every rendered JPEG (Read it). Fix any text touching the mascot, cut-off art or overflow; re-render.
5b. Reel: copy `post-002/reel/reel.html` to `post-NNN/reel/reel.html`, change only text, numbers, source and poses
   (same claims as the slides, nothing new). Keep text clear of the mascot and of the bottom 300 px and right 120 px (Instagram UI).
   `python3 -I tools/reel.py post-NNN/reel/reel.html post-NNN/reel.mp4 16 30`. Check frames at ~1.8, 5, 8.8, 12.2, 15 s
   (ffmpeg -ss … -frames:v 1) and fix overlaps.
6. Write `post-NNN/caption.txt`: hook line · one sentence naming the study (authors, journal, year) and the finding ·
   the rule in one line · a question that invites a one-word comment · "Save this. Follow @redguy.fit for gym science, drawn simple." ·
   5 hashtags. Under 2,200 characters.
7. Commit and push (`git -c user.name=redguyfit -c user.email=redguyfit@users.noreply.github.com`), then check each image URL returns 200 image/jpeg.
8. Send Henere a contact sheet of the slides and reel.mp4 (SendUserFile) and the caption (SendUserMessage). Ask (in French):
   "Réponds **post** (carrousel + Reel avec mon son), **post manuel** (carrousel seulement, tu postes le Reel avec un son tendance),
   ou dis-moi quoi changer."
9. On "post": schedule with send_later, in this session:
   - 07:00 Tahiti next day: `create_carousel_post` with the URLs in order and caption.txt, then `create_story` with story.jpg. Message Henere the result.
   - 12:00 Tahiti same day: `create_story` with story2.jpg.
   - 18:00 Tahiti same day, only on "post" (not "post manuel"): `create_video_post` with
     video_url `https://raw.githubusercontent.com/redguyfit/redguy-media/main/post-NNN/reel.mp4`, caption.txt, share_to_feed true.
     raw.githubusercontent serves MP4 as application/octet-stream; if Instagram rejects it, tell Henere and send him the MP4 to post by hand.
   - On "post manuel": schedule only the carousel and stories; remind Henere the Reel MP4 is in the chat for him to post with a trending sound.
   Add the post to `content/log.md` (number, topic, date, status "scheduled") and push.
   On changes: edit, re-render, push, send the new sheet, ask again. No reply = nothing is published.
10. Sundays: also pull the last 7 days of post stats through Windsor (`get_fields` then `get_data`, connector instagram):
    reach, saves, shares, follows per post. Send a 5-line summary and whether to keep, raise or lower volume.

## Never
- Publish without Henere's "post" for that specific carousel.
- Publish more than one carousel and one Reel a day in Phase 1.
- Reply to comments or DMs as Henere.
