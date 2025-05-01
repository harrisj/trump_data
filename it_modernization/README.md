# IT Modernization

**UPDATE 2025-05-01: I am working to move IT Modernization to a new repo so I can also use it to build out a static website and API, since not everybody loves looking at huge YAML files**

-----------

A manually updated YAML file that tracks the "IT modernization" efforts of the DOGE Team across various agencies. In the Executive Order establishing DOGE, they are given the following mandate:

> The USDS Administrator shall commence a Software Modernization Initiative to improve the quality and efficiency of government-wide software, network infrastructure, and information technology (IT) systems. Among other things, the USDS Administrator shall work with Agency Heads to promote inter-operability between agency networks and systems, ensure data integrity, and facilitate responsible data collection and synchronization.

The file modernization.yaml will track the "modernization" work of the DOGE crew as they steamroll across various agencies. This work will be using only reported sources, which will be linked from the record. Hopefully, it will present a more comprehensive picture of events. You might begin to notice that none of it seems to involve actual IT modernization...

This file will **not** track contracts being canceled by DOGE, except if that has ramifications for DOGE actions and activities. It's not that it's not relevant to the damage DOGE is doing, I just am finding it harder to keep track off and quantify.

## The Data

Currently, the source data is stored in several files located within the `data` directory:

- `agencies.yaml`: a list of agencies currently being affected by DOGE activities
- `cases.yaml`: court cases that either are related to or might provide information about DOGE activities
- `events.yaml`: specific events related to DOGE's destruction across multiple agencies
- `roundups.yaml`: information of media roundups ([example](https://www.nytimes.com/interactive/2025/02/27/us/politics/doge-staff-list.html)) that provide high-level overviews of who is where (in some cases, these list people who haven't been associated with specific events)
- `systems.yaml`: information on government systems that have been accessed by DOGE

Each of these files has associated JSON schemas that can be used to validate the file's contents in an IDE, if you are editing them. But, if you notice an error, the best option is to just file a new Issue to let me know and I'll fix it.

## The Dates

One important thing to note is that I am using the [Extended Datetime Format of ISO 8601](https://www.datafix.com.au/BASHing/2020-02-12.html) to represent exact and imprecise dates. This allows me to represent that certain dates are approximate rather than exact (it's very common for news reports to say something like "late last week"). If you are using Python, you can use the `edtf` package to parse them with your YAML parsing like this:

```python
from edtf import parse_edtf
from edtf.parser.parser_classes import EDTFObject, UncertainOrApproximate

def edtf_representer(dumper, data):
    return dumper.represent_scalar(u'!edtf', u'%s' % data)

yaml.add_representer(UncertainOrApproximate, edtf_representer)

def edtf_constructor(loader, node):
    value = loader.construct_scalar(node)
    return parse_edtf(str(value))

yaml.add_constructor(u'!edtf', edtf_constructor)

pattern = re.compile(r'^(2024|2025)-\d{2}-\d{2}(~?)$')
yaml.add_implicit_resolver(u'!edtf', pattern)
```

It is possible that I might add more complicated date representations going forward (EDTF is amazing), but otherwise you can also make sure to strip a trailing ~ from date strings before parsing and look for the `fuzz:` key in the YAML object.

## Reports

This data is then combined and processed by automated scripts to produce more comprehensive files that can be used as input for web interfaces, read by automated programs or just looked at to get details on what is happening where.

For instance, here is a record from the `agency_comprehensive.json` file which provides info on DOGE activities at each agency

```yaml
DOI:
  name: Department of the Interior
  id: DOI
  associated:
  - Tyler Hassen
  - Stephanie Holmes
  - Bryton Shang
  - Katrine Trampe
  events:
  - date: 2025-01-28
    type: disruption
    event: Two DOGE staffers attempted to force water pumps to be turned on in a large reservoir in California for a photo op
    named:
    - Tyler Hassen
    - Bryton Shang
    source: https://www.cnn.com/2025/03/07/climate/trump-doge-california-water/index.html
    agency: DOI
  - date: 2025-02-24
    type: onboarded
    onboard_type: detailed
    event: Stephanie Holmes is detailed to the Department of the Interior as a Special Advisor and acting Chief Human Capital Officer for the entire agency
    detailed_from: DOGE
    named:
    - Stephanie Holmes
    source: https://subscriber.politicopro.com/article/eenews/2025/03/05/heres-the-people-connected-to-doge-at-interior-00213330
    agency: DOI
  - date: 2025-03-04
    type: disruption
    event: DOGE boasts in a tweet that 27% more water was released in February compared to January (unclear if this adjusts for different lengths of months)
    source: https://xcancel.com/DOGE/status/1896948512975433787
    agency: DOI
  - date: 2025-03-07
    type: promotion
    event: Tyler Hassen is promoted to Acting Assistant Secretary of Policy, Management and Budget
    named:
    - Tyler Hassen
    source: https://www.eenews.net/articles/doge-official-appointed-head-of-policy-at-interior/
    agency: DOI
  - date: 2025-03-28
    type: report
    event: Expressing concerns about DOGE requesting access to FPPS, the CIO and CISO of the Department of the Interior present a memo to the Interior Secretary about the risks for him to acknowledge and sign. He doesn't sign it
    source: https://www.nytimes.com/2025/03/31/us/politics/doge-musk-federal-payroll.html
    agency: DOI
  - date: 2025-03-28
    type: disruption
    event: Tyler Hassen places the CIO and CISO on admininstrative leave under investigation for raising alarm about DOGE access
    named:
    - Tyler Hassen
    source: https://www.nytimes.com/2025/03/31/us/politics/doge-musk-federal-payroll.html
    agency: DOI
  - date: 2025-03-29
    event: Two DOGE staffers are granted admin access to the FPPS payroll system at the Department of the Interior
    type: access_granted
    access_type: admin
    access_systems:
    - FPPS
    named:
    - Stephanie Holmes
    - Katrine Trampe
    source: https://www.nytimes.com/2025/03/31/us/politics/doge-musk-federal-payroll.html
    agency: DOI
  systems:
    FPPS:
      name: Federal Personnel Payroll System
      id: FPPS
      description: A shared service which processes payrolls for the Justice, Treasury and Homeland Security departments, as well as the Air Force, Nuclear Regulatory Commission and the U.S. Customs and Border Protection, among other federal agencies.
      risk: PII and payment info for federal staff at several large agencies, including the ability to interfere with pay
      pia: https://www.doi.gov/sites/doi.gov/files/fpps-pia-revised-04222020_0.pdf
      agency: DOI
  cases:
    1:25-cv-00612:
      name: Center for Biological Diversity v. U.S. Department of Interior (D.D.C.)
      description: Plaintiffs, a nonprofit organization focused on habitat preservation for endangered species, alleges that DOGE and the Department of Interior have violated the Administrative Procedures Act by failing to follow Federal Advisory Committee Act (FACA) requirements
      case_no: 1:25-cv-00612
      date_filed: 2025-03-03
      link: https://www.courtlistener.com/docket/69698261/center-for-biological-diversity-v-us-department-of-interior/
      agency: DOI
    1:25-cv-00643:
      name: Japanese American Citizens League v. Musk (D.D.C.)
      description: Plaintiffs allege that they are harmed by DOGE's cutting of federal funding and firing of federal employees, including in the work of the National Park Service and historic sites, and they are violating the separation of powers, Appointments Clause and Administrative Procedure Act
      case_no: 1:25-cv-00643
      date_filed: 2025-03-05
      link: https://www.courtlistener.com/docket/69706944/japanese-american-citizens-league-v-musk/
      agency:
      - DOGE
      - DOI
```

With the following fields:

- agency: the name of the agency
- acronym: if the agency has an acronym, it will be here
- roundups: if there are any articles, etc. that list staff identified at that agency, I put them here
- events: a list of dated events in DOGE's efforts at the agency, included staff explicitly named where available
- systems: a list of systems that DOGE is likely looking to access, based on either direct reporting or by the class of systems they are (eg, budgeting, HR)
- cases: a list of cases relevant to the agency
- vandalism: a list of specific acts of vandalism or sabotage against the agency's IT resources

For a given system, there will be the following fields

- name: the name of the system
- acronym: if the system has an acronym, here it is
- link: if there is a page on an agency website for the system
- pia: a link to the Privacy Impact Assessment for the system, if available
- sorn: a link to the System of Records Notice for the system, if available
- description: a short description of the system
- risk: a description of the risks from letting DOGE have full access to the system

More formally, there is now a JSON Schema file for the YAML and if you have the appropriate validation tools (like the RedHat YAML plugin in Visual SourceSafe), it can help report any validation errors.

## Event Types

I have defined event types to help supplement what is going on in various systems and which include additional metadata:

First, there are some general event fields you will always see:

- date: the date of the event or a close approximation (journalists, I am begging you to say "last Thursday" instead of "late last week")
- event: a text description of what happened
- source: the source from where the event info was taken
- comment: if I need to put a comment about the record
- named: an array of DOGE staff that were associated with the even

- access_granted: identifying when access has been granted to one or more systems for one or more DOGE staff
  - access_type: read | read-write | admin | unknown
  - access_systems: an array of system IDs if provided
  - named: which DOGE staff were given access
- access_changed: when the access level for a DOGE staffer is changed
  - access_type: (like above, but indicating the new value)
  - access_systems: like above
  - named: which DOGE staff had access changed
- access_revoked: when access for a system might be revoked (might be reported later than when revocation happened)
  - access_systems: like above
  - named: which DOGE staff had access removed
- disruption: the Silicon Valley term for vandalism, looting, destruction
- offboarding: when DOGE staffers leaves an agency
  - named: an array of named
- onboarding: a record of DOGE staff onboarding at a new agency.
  - onboard_type: hired | appointed | detailed | other
  - detailed_from: the agencies where people were detailed from
  - named: the names of the people being onboarded
- legal: a legal development
- official: an official communication or action, usually one of the many executive orders
- other: for things I don't know, but also aren't reports?
- promotion: a record of a DOGE staffers getting a new role at an existing agency (usually to have more power)
  - named: who was affects
- report: a general report of a sighting, something happening, etc.

## Can You Tell Me More About These Names?

No. I am mainly just trying to track who is at each agency, the types of systems they might be accessing (mentioned in news coverage as well as the general notion they are looking at HR/Contracting/Procurement systems) and a timeline of events for their action. Other news organizations like ProPublica and Wired already have excellent resources on who these people are and where they have come from.

## I See an Error!

Great, please go to the [Issues](https://github.com/harrisj/trump_data/issues) tab and let me know. I especially want to know if:

- You see an error in the data
- You have an idea for a new feature
- There are some media reports or court filings I've missed that include DOGE activities

## Other Useful Files

Okay, this is where it gets cool. I have some automations going for this file that make if helpful. First, I have JSON schemas defined for these files in the schemas directory. This includes a file with a master list of DOGE names so I don't misspell them in multiple places (Mike Russo here, Michael Russo there, etc.)

I also have a pre-commit hook that makes the following files and keeps them up-to-date:

- agency_comprehensive.yaml = a grouping of people / events associated with each agency
- aliases.yaml = a processed version of my aliases file that allows me to see likely candidates for unknown aliases
- events.csv = a CSV version of the big events YAML file for people who prefer to work in spreadsheets
- events.yaml = a processed version of my raw events file that merges in some data from other records
- people.yaml = a people-centric view of the DOGE activities that groups them by name
- postings.yaml = an array of what people have been posted at a specific agency with durations
- system_postings.yaml = an array of what system access has been given to people

As well as some silly prototypes that might go away:

- agencies_chart.md = a chart that uses the posting data to give a rough view of who is where in given agencies. This is highly imprecise!
- staffing_chart.md = a person-centric view of where individual people have shown up at various agencies

## What About a Database?

You're in luck! As part of the pre-commit hooks, I also generate a sequence of CSV files for DB tables in `db/import` which includes the following tables:

- events (including foreign key references to cases and details tables)
- agencies
- aliases
- details
- systems

As well as some join tables for representing many-to-many relationships:

- cases_agencies
- details_aliases
- details_names
- events_agencies
- events_aliases
- events_names
- events_systems

For a primary key, I generate an 8-character short UUID as part of the events preprocessing. That can be used to reference the event going forward and for joining against things.

If you want to create the sqlite table, just run the following command `scripts/create_sqlite_db` and it'll completely recreate a database at `doge.sqlite` for you to play with.

## Next Big Steps

- I need to figure out to better represent the system access/grants/etc. since more details of those are coming to light.
  - One interesting wrinkle is that sometimes agencies are Shared Service Providers to multiple agencies
  - DOGE sometimes just has access to a small slice of that (like CFPB's usage of HRConnect), but sometimes they have the whole system (like Grants.gov)
- Providing a relatively clear picture/diagram of staffing/detailing moves as DOGE hopscotches people across agencies
- It's probably time to leverage SQLite as part of my analysis/file-generation
- Auditing/validation to find mismatched / inconsistent data

## PIAs and SORNs?

Unlike a private business, the US Government is not allowed to just wantonly collect data on citizens without notification and legal review. There are two main types of documents that can provide insight into what data is in various systems that DOGE is accessing:

- **Privacy Impact Assessments** [(examples)](https://www.ed.gov/about/ed-overview/required-notices/privacy/privacy-impact-assessments-pia) are required to assess the privacy impact of any new system that stores and/or processess the private information of individuals (as mandated in the [E-Government Act of 2002](https://en.wikipedia.org/wiki/E-Government_Act_of_2002)).
- **Systems of Records Notices** [(examples)](https://www.ed.gov/about/ed-overview/required-notices/privacy/privacy-act-system-of-record-notice-issuances) identify the purpose for which a record about an individual is collected, from whom and what type of information is collected and how the information is shared with individuals and organizations outside/external to the agency (as mandated in the [Privacy Act of 1974](https://en.wikipedia.org/wiki/Privacy_Act_of_1974)).

In some cases, both of these documents might describe the same system, but it's not necessarily guaranteed. For instance, OPM might have a SORN describing the general structure of personnel records and PIAs for one or more systems that operate on that data. You can loosely think of the SORN as describing what information is collected on a form coming into the agency, while a PIA describes systems that act on that data after it has been ingested. In the OPM example, there is a [SORN for race/national origin/disability of staff](https://www.opm.gov/information-management/privacy-policy/sorn/opm-sorn-govt-7-applicant-race-sex-national-origin-and-disability-status-records.pdf) because those are collected on a form as part of the onboarding process and the data collected from those records is available in the [EHRI system as described in its PIA](https://www.opm.gov/information-management/privacy-policy/privacy-policy/ehridw.pdf). I have made my best attempt to link to relevant SORNs and PIAs when I can, but it is an inexact science because they describe two related but different concepts.

## Validation

I have created a JSON schema for the document that can be used to validate edits if you are using a plugin like the RedHat YAML one in an IDE.

## Disclaimer

I am doing my best to fill in the gaps and collect information on a purposefully murky organization designed to avoid transparency and oversight. Mistakes are inevitable; please be aware of the risks and point out any issues to me by filing an Issue on this repo. Also, I am not a reporter. I only put things in here that have been presented publicly in the media.
