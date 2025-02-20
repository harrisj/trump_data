# Gitmo Camp

A small hand-curated CSV tracking the population of the [concentration
camp](https://en.wikipedia.org/wiki/Concentration_camp) established by the Trump
administration in Guantanamo Bay.

## Context

This data is being sourced from different news sources and press releases and
there is no official data source for it yet. This means there will likely be
errors and distortion. Do not confuse any accidental precision in these numbers for
accuracy! In general, news organizations will probably use round numbers like 180 to 
suggest approximate values (unlike 187, which suggests precision), but I can't guarantee it!

To be extremely clear on this point, if I read an article that says "Over the last 
week, the United States government has sent more than 80 men to Guantánamo Bay",
then I will record it as 80. I will also record an expression like ">80" in another column
to indicate the way the number is framed, as well as the source quote and source URL

## Data
This is a simple CSV that I will update manually over time with the following columns:
- date (in ISO format): the date of the population count (might be off by a day or so)
- population (int): the population on the given date
- expression (string, e.g. "=10", ">80", "~100"): a representation of the qualifiers in news articles
- quote (string): the quote from the article containing the population number
- source (a link to a source URL): a link to the source of the number

