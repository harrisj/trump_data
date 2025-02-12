# Gitmo Camp

A small hand-curated CSV tracking the population of the [concentration
camp](https://en.wikipedia.org/wiki/Concentration_camp) established by the Trump
administration in Guantanamo Bay.

## Context

This data is being sourced from different news sources and press releases and
there is no official data source for it yet. This means there will likely be
errors and distortion. Do not confuse any accidental precision in these numbers for
accuracy!

To be extremely clear on this point, if I read an article that says "Over the last 
week, the United States government has sent more than 80 men to Guantánamo Bay",
then I will record it as 80.

## Data
This is a simple CSV that I will update manually over time with the following columns:
- date (in ISO format)
- population (int)
- quote (string)
- source (a link to a source URL)
