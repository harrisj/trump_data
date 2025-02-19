# IT Modernization

A manually updated YAML file that tracks the "IT modernization" efforts of the DOGE Team across various agencies. In the Executive Order establishing DOGE, they are given the following mandate:

> The USDS Administrator shall commence a Software Modernization Initiative to improve the quality and efficiency of government-wide software, network infrastructure, and information technology (IT) systems.  Among other things, the USDS Administrator shall work with Agency Heads to promote inter-operability between agency networks and systems, ensure data integrity, and facilitate responsible data collection and synchronization.

The file modernization.yaml will track the modernization work of the DOGE crew as they steamroll across various agencies. This work will be using only reported sources, which will be linked from the record. Hopefully, it will present a more comprehensive picture of events. You might begin to notice that none of it seems to involve actual IT modernization...

# The Data

A record might look something like this:

```yaml
    - agency: Internal Revenue Service
      acronym: IRS
      participants:
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


