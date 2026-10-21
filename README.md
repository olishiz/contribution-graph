# Contribution graph

Every Kuala Lumpur day, this repository rolls a number from 1 to 5 and pushes that many empty commits. The author is **olishiz** `<zhuen1101@hotmail.com>`, the public email on that GitHub account. Each commit is dated **12:00 in Asia/Kuala_Lumpur** (`+0800`), which is the calendar day GitHub uses for the square.

## Schedule

Both times are Kuala Lumpur (UTC+8, no daylight saving):

- **09:15** records today, if today does not already have a commit.
- **21:15** records today only when the morning run did not.

GitHub starts the job from the UTC clock (`01:15` and `13:15` UTC). The schedule keeps running from the default branch, which for this account is `master`.

A second run on a Kuala Lumpur day that already has a commit does nothing, so the evening pass cannot add a second roll.

## Fill older days

Open **Actions → Daily contribution → Run workflow** and set **days** to `365`. That fills each of the past 365 Kuala Lumpur days that does not already have a commit, with its own roll of 1 to 5. Days that already have a commit stay as they are.

Squares can take up to 24 hours to appear. The author email has to stay on the account, and the commit has to be on the default branch. If a square is missing, open the commit URL and add `.patch`. The `From:` line should show `zhuen1101@hotmail.com` and a `+0800` time.

## Private repository

This repository is public, so the commits show on the profile. If you later make it private, turn on **Private contributions** from **Contribution settings** above the calendar on your profile.

## Stop

Delete `.github/workflows/daily-contribution.yml`, or delete the repository. Deleting the repository removes the squares that came from it.
