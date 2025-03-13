# Initial Unemployment Claims

A project to capture some fields from the Department of Labor's weekly report on Initial Unemployment Claims. This is especially timely right now, since it classifies federal worker as its own category. I am not going to capture every field, but ones that seem useful for watching things unfold.

## Notes on Working With This Data
To understand the utility of this data as well as some caveats, please read this [short explainer from FRED](https://fredblog.stlouisfed.org/2020/04/things-to-know-about-initial-claims-data/). To summarize, one of the best things about the data is that it is updated weekly (as opposed to monthly) and is only 5 days behind the end of the week (meaning it's released every Thursday). The downside of this data is that it is highly volatile compared to a monthly release (or later corrections to unemployment), so a rolling average is often recommended. In addition, it tracks people who have filed claims for unemployment. This isn't the same as people who are receiving unemployment. Just be aware of the data and its limitations.

The source for this data are [press releases on the Department of Labor website](https://www.dol.gov/newsroom/releases?agency=All&state=All&topic=132&year=all) and the latest one is always at [https://www.dol.gov/ui/data.pdf](https://www.dol.gov/ui/data.pdf)

There is an API, but it unfortunately does not seem to include the breakadown of federal staff, so I update this once a week based on the press releases. Also, I decided to start back in early 2024, just to allow if anybody wants to do Year-over-Year (YoY) comparisons.

## Delay in the Unemployment Compensation for Federal Employees (UCFE) Numbers
Even though there were mass layoffs of probationary employees in mid-February, those numbers have still not been reflected in early March. [This report by the Century Foundation](https://tcf.org/content/report/mass-federal-layoffs-present-unprecedented-unemployment-insurance-challenges/) offers some explanations:
1. Many of the workers laid off in the probationary employee purge were put on 30 days of administrative leave, meaning their last paychecks are in early March
2. UCFE is a separate system from the standard state UI and requires manual steps. Typical claims processing can take 14-21 days and the system is expected to be under extraordinary strain in the months ahead
3. Many of the fired probationary employees were accused of being poor performers as a justification. This normally would not qualify them for unemployment insurance and is likely complicating the reporting (besides being inhumane and cruel)
4. People who are forced to quit/resign because of harrassment like being forced to return to office on short notice would not be counted, since that would be considered a voluntary separation
5. Many of the laid-off employees are navigating this system for the first time and may not realize they can file for UI even if appealing their status

## The Columns in the CSV
- Week Ending: this data is for the week ending on this date
- Initial Claims (SA): seasonally-adjusted initial claims from state unemployment data
- Initial Claims (NSA): non-seasonally-adjusted initial claims from state unemployment data
- 4-wk Moving Avg Initial (SA): a 4-week rolling average of the seasonally-adjuted initial claims from state data
- Initial Fed: Initial claims for Federal Employees (UCFE)
- New Discharge Vet: Newly discharged veterans for the week (UCX)
- Cont Regular State: Continued Weeks Claimed Filed for Regular State UI (this usually gets adjusted the following week)
- Cont Fed: Continued Weeks Claimed Filed for Federal Employees
- Cont Vet: Continued Weeks Claimed Filed for Newly Discharged Veterans
- Cont Total: All continued weeks claimed (this is not a sum of the prior 2 column, because I don't record some other programs)

Be aware that the continued week's claims are updated a week after the initial claims for a week, and they may then also be slightly adjusted for the following week as the state total gets corrected (the federal and discharged vet totals are accurate when recorded)

## The Triangular Shape
This data is updated at different cadences, so you will see a triangular shape at the top of the CSV:
- Initial claim numbers: 5 days after
- New federal / military discharge claims: 12 days after
- Continuing claims: 19 days after

You also will usually some adjustments to numbers in following weeks as data is corrected. It's usually pretty small (+/- 100 or less for total continuing claims), but just noting for completeness.