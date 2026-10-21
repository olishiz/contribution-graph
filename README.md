# Contribution graph

This repository uses [bcanseco/github-contribution-graph-action](https://github.com/bcanseco/github-contribution-graph-action) to keep a GitHub contribution graph green. Every day it rolls a number from 1 to 5 and pushes that many empty commits, authored as **olishiz** with `zhuen1101@hotmail.com` (the public email on that GitHub account).

It is a standalone repository that calls the published action. Commits on a fork of someone else's repository stay off the contribution graph, so this is not a fork of that action.

## Schedule

The workflow runs at **01:15 UTC**, which is **09:15 in Malaysia**. Weekdays and weekends are both included. The schedule keeps going on its own once the workflow file is on the repository's default branch. For this account that branch is `master`.

GitHub can take up to about an hour to start a scheduled run, and it can skip a day when Actions is busy. If a morning is missing, open **Actions → Daily contribution → Run workflow** and leave **days** at `1`.

## Fill older days

**Run workflow** and set **days** to `365` to fill the past year with 1–5 commits on each day. Do that once. A second 365-day run adds another year of commits on top of the ones already there.

The graph shows roughly the last year. [Contribution criteria](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference#what-counts-as-a-contribution) also require the author email to stay on the account, and the commits to be on the default branch of a repository you own. Squares can take up to 24 hours to appear. If one is missing, open the commit URL and add `.patch`. The `From:` line should be `zhuen1101@hotmail.com`.

## Private repository

This repository is public, so the commits show on the profile with no extra setting. If you later make it private, the squares stay hidden until you show them: on your profile, above the calendar, open **Contribution settings** and enable **Private contributions**. [How that setting works](https://docs.github.com/en/account-and-profile/how-tos/contribution-settings/manage-visibility-settings-for-private-contributions-and-achievements).

## Stop

Delete `.github/workflows/daily-contribution.yml`, or delete the repository. Deleting the repository removes the squares that came from it.

The noreply address `22555339+olishiz@users.noreply.github.com` is the other address GitHub already ties to this account. Use it as `GIT_EMAIL` if you remove `zhuen1101@hotmail.com` from the account.
