# IT Modernization

A manually updated YAML file that tracks the "IT modernization" efforts of the DOGE Team across various agencies. In the Executive Order establishing DOGE, they are given the following mandate:

> The USDS Administrator shall commence a Software Modernization Initiative to improve the quality and efficiency of government-wide software, network infrastructure, and information technology (IT) systems.  Among other things, the USDS Administrator shall work with Agency Heads to promote inter-operability between agency networks and systems, ensure data integrity, and facilitate responsible data collection and synchronization.

The file modernization.yaml will track the modernization work of the DOGE crew as they steamroll across various agencies. This work will be using only reported sources, which will be linked from the record. Hopefully, it will present a more comprehensive picture of events. You might begin to notice that none of it seems to involve actual IT modernization...

# The Data
A record might look something like this:

```yaml
    - agency: Internal Revenue Service
      acronym: IRS
      people:
        - Gavin Kliger
      events:
        - date: 2025-02-13
          event: Gavin Kliger arrives at the IRS to begin onboarding
          source: https://www.wsj.com/politics/policy/doge-internal-revenue-service-9697cb99
        - date: 2025-02-18
          event: White House pressures the IRS to sign a MOU granting DOGE expanded access to internal systems
          source: https://www.washingtonpost.com/business/2025/02/16/doge-irs-access-taxpayer-data/
      systems:
        - name: Integrated Data Retrieval System
          acronym: IDRS
          link: https://www.irs.gov/irm/part2/irm_02-009-001r
          pia: https://www.irs.gov/pub/irs-pia/idrs-pia.pdf
          sorn: https://www.federalregister.gov/documents/2015/09/08/2015-21980/privacy-act-of-1974-as-amended-system-of-records-notice
          description: The IDRS contains some of the most sensitive financial information on American taxpayers.
          risk: Access to PII and financial data of American taxpayers, including names, SSNs, tax returns, bank account numbers, etc.
      sources:
        - https://thehill.com/homenews/administration/5149835-stephen-miller-doge-irs/
        - https://www.cnn.com/2025/02/17/politics/doge-irs-taxpayer-data/index.html
```

With the following fields:
- agency: the name of the agency
- acronym: if the agency has an acronym, it will be here
- people: a list of known DOGE participants linked to the agency
- events: a list of key events in DOGE's efforts at the agency
- systems: a list of systems that DOGE is likely looking to access, based on either direct reporting or by the class of systems they are (eg, budgeting, HR)
- sources: a list of other sources for things like participants that aren't necessarily linked to specific events
- vandalism: a list of specific acts of vandalism or sabotage against the agency's IT resources

For a given system, there will be the following fields
- name: the name of the system
- acronym: if the system has an acronym, here it is
- link: if there is a page on an agency website for the system
- pia: a link to the Privacy Impact Assessment for the system, if available
- sorn: a link to the System of Records Notice for the system, if available
- description: a short description of the system
- risk: a description of the risks from letting DOGE have full access to the system

# Can You Tell Me More About These Names?
No. I am mainly just trying to track who is at each agency, the types of systems they might be accessing (mentioned in news coverage as well as the general notion they are looking at HR/Contracting/Procurement systems) and a timeline of events for their action. Other news organizations like ProPublica and Wired already have excellent resources on who these people are and where they have come from.

# PIAs and SORNs?
Unlike a private business, the US Government is not allowed to just wantonly collect data on citizens without notification and legal review. There are two main types of documents that can provide insight into what data is in various systems that DOGE is accessing:
- **Privacy Impact Assessments** [(examples)](https://www.ed.gov/about/ed-overview/required-notices/privacy/privacy-impact-assessments-pia) are required to assess the privacy impact of any new system that stores and/or processess the private information of individuals (as mandated in the [E-Government Act of 2002](https://en.wikipedia.org/wiki/E-Government_Act_of_2002)).
- **Systems of Records Notices** [(examples)](https://www.ed.gov/about/ed-overview/required-notices/privacy/privacy-act-system-of-record-notice-issuances) identify the purpose for which a record about an individual is collected, from whom and what type of information is collected and how the information is shared with individuals and organizations outside/external to the agency (as mandated in the [Privacy Act of 1974](https://en.wikipedia.org/wiki/Privacy_Act_of_1974)). 

In some cases, both of these documents might describe the same system, but it's not necessarily guaranteed. For instance, OPM might have a SORN describing the general structure of personnel records and PIAs for one or more systems that operate on that data. You can loosely think of the SORN as describing what information is collected on a form coming into the agency, while a PIA describes systems that act on that data after it has been ingested. In the OPM example, there is a [SORN for race/national origin/disability of staff](https://www.opm.gov/information-management/privacy-policy/sorn/opm-sorn-govt-7-applicant-race-sex-national-origin-and-disability-status-records.pdf) because those are collected on a form as part of the onboarding process and the data collected from those records is available in the [EHRI system as described in its PIA](https://www.opm.gov/information-management/privacy-policy/privacy-policy/ehridw.pdf). I have made my best attempt to link to relevant SORNs and PIAs when I can, but it is an inexact science because they describe two related but different concepts.

# Disclaimer
I am doing my best to fill in the gaps and collect information on a purposefully murky organization designed to avoid transparency and oversight. Mistakes are inevitable; please be aware of the risks and point out any issues to me by filing an Issue on this repo. Also, I am not a reporter. I only put things in here that have been presented publicly in the media.
