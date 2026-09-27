WIP

T.R.A.C.E. or Text Repair & Angeles Crime Evaluation

Note: This is just simulating a client-developer vibe/scenario and the names are just fictional.

Project Request

From: Ligaya Torres, Data & Records Officer — Angeles City Community Safety Watch To: [Developer] Re: Making sense of our crime records export

Hi,

Thanks for agreeing to look at this. Some background first, then what we're hoping you can build.

Background

As part of our neighborhood reporting initiative, we requested crime records covering our city going back several years. What came back is a CSV export — a little under 28,000 rows, 18 columns. The problem is the file is a mess. A lot of the text fields look like they went through some scanning or extraction process on the source end, and it shows: words come out broken with random spaces stuck in the middle. We've seen things like "Investigatio n" where it should say "Investigation," and it's all over the categorical columns — offense type, location type, case status, all of it. Right now we can't even get a reliable count of anything because the same value gets split into two or three "different" values depending on how it got mangled.

Nobody on our side can code, so we're hoping to hand this off entirely.

What we need

1. A cleaning step. Take the raw export and produce a cleaned version where the broken text is fixed and values are consistent. Doesn't need to be a perfect general-purpose fix — this file's corruption follows a small number of patterns, so something tuned to what's actually in there is fine.

2. A per-barangay lookup. Our board members keep asking "what's actually happening in [barangay]" and right now the only answer is someone opening the spreadsheet and eyeballing it, which nobody trusts. We'd like to type in a barangay name and get back: how many incidents on record, the most common types of incidents there, what time of day trouble tends to cluster (we think of it as three chunks of the day — night, morning, evening), and what kind of place it tends to happen in (residential, street, etc).

3. Something we can run more than once. We'll get updated exports periodically. Ideally the tool just points at whatever file we give it next time, and there's an option to save the output somewhere instead of only printing it to the screen — a few of us want to bring printouts to meetings.

4. Something we can trust. The whole point of this is data quality. We've been burned before by a "quick script" nobody could vouch for. Please build in some way to actually verify the cleaning and the lookup logic are correct, not just eyeballed as looking right.

5. Graceful handling of bad input. If someone mistypes a barangay name, or a row in the file is broken somehow, we'd rather see a clear message than have the whole thing crash.

Nice to have — later phase, not required now

We've seen other groups use "AI" to turn raw numbers into a plain-language summary. If the core tool is solid and there's time left over, a small add-on that takes a barangay's stats and drafts a short plain-English blurb we could paste into a newsletter would be great. Not a priority. Only if everything above is done and working first.

What "done" looks like

Cleaned file produces consistent, de-duplicated category values

Typing any real barangay name returns a sensible profile

A bad barangay name or a bad row doesn't crash the program

You can point it at a different file later without changing the code

There's something in place that proves the core logic is actually correct, not just tested by hand

No hard deadline on our end, but sooner is better — we've been sitting on this data for a while. Let us know if anything above is unclear.

Thanks, Ligaya

Personal tracking notes (not part of the brief — for your own use)

Rough map of where each ask pulls in something from the course, so you can check these off as you go instead of guessing what's "covered":

Client ask What it forces you to use #1 Cleaning step File I/O (reading the raw CSV), Regular Expressions (fixing the broken text) #5 Bad input handling Exceptions (bad rows, bad barangay names) #2 Per-barangay lookup Object-Oriented Programming (a profile class), dictionaries/Counter for aggregation, Conditionals (shift bucketing logic) #3 Run it more than once / save to file Libraries (argparse or sys.argv for the file path and save flag), Loops (re-prompt for another barangay without restarting) #4 Trust the logic Unit Tests with pytest Everywhere, quietly Functions & Variables (baseline), and reach for "Et Cetera" week stuff — f-strings, comprehensions, unpacking — instead of the clunkiest version of the same code AI blurb (phase 2) Not a course concept — deliberately kept out of the graded core

If you finish the core tool and every row in that table except the last has something checked off, you've built exactly what the brief above is asking for — no more, no less.