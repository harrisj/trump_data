# IT Modernization

A manually updated YAML file that tracks the "IT modernization" efforts of the DOGE Team across various agencies. In the Executive Order establishing DOGE, they are given the following mandate:

> The USDS Administrator shall commence a Software Modernization Initiative to improve the quality and efficiency of government-wide software, network infrastructure, and information technology (IT) systems.  Among other things, the USDS Administrator shall work with Agency Heads to promote inter-operability between agency networks and systems, ensure data integrity, and facilitate responsible data collection and synchronization.

The file modernization.yaml will track the "modernization" work of the DOGE crew as they steamroll across various agencies. This work will be using only reported sources, which will be linked from the record. Hopefully, it will present a more comprehensive picture of events. You might begin to notice that none of it seems to involve actual IT modernization...

This file will **not** track contracts being cancelled by DOGE, except if that has ramifications for DOGE actions and activities.

## The Data

A record might look something like this:

```yaml
- name: Department of Labor
  acronym: DOL
  roundups:
  - source: https://www.nytimes.com/interactive/2025/02/27/us/politics/doge-staff-list.html
    organization: The New York Times
    named:
    - Adam Ramada
  - source: https://projects.propublica.org/elon-musk-doge-tracker/
    organization: ProPublica
    named:
    - Aram Moghaddassi
  - source: https://www.businessinsider.com/doge-staffer-fertility-clinic-pronatalist-department-of-labor
    organization: Business Insider
    date: 2025-03-05
    context: Business Insider reports Marko Elez, Aram Moghaddassi, and Miles B. Collins are new DOGE arrivals at Department of Labor
    named:
    - Marko Elez
    - Aram Moghaddassi
    - Miles Collins
  events:
  - date: 2025-01-24
    event: Trump fires the Inspector General for the Department of Labor in a late-night purge
    source: https://www.nytimes.com/interactive/2025/02/11/us/politics/trump-musk-doge-federal-workers.html
  - date: 2025-02-04
    event: DOL staff reportedly ordered "to give DOGE access to whatever they ask for-or risk termination"
    source: https://bsky.app/profile/kimkelly.bsky.social/post/3lhf2owbxc22b
  - date: 2025-02-05
    event: DOGE staff are given access to the Department of Labor IT systems
    source: https://www.theguardian.com/us-news/2025/feb/05/elon-musk-doge-labor-department-protest
  - date: 2025-02-13
    event: DOGE is granted authorization to use file transfer software
    named:
    - Sam Beyda
    - Derek Geissler
    - Cole Killian
    - Adam Ramada
    - Jordan Wick
    source: https://www.nbcnews.com/tech/security/doge-software-approval-alarms-labor-department-employees-data-security-rcna191583
  - date: 2025-03-14
    event: Thomas Shedd apparently starts working at the CIO at Department of Labor while also serving as the TTS Commissioner at GSA (experts are unclear if this is legal)
    named:
    - Thomas Shedd
    source: https://www.nextgov.com/people/2025/03/tts-director-tapped-serve-labor-cio/403855/?oref=ng-home-top-story
  - date: 2025-03-18
    event: Keith Sonderling is sworn in as the Deputy Secretary of labor
    named:
    - Keith Sonderling
    source: https://news.artnet.com/art-world/doge-imls-institute-museum-library-services-2623286
  - date: 2025-03-20
    event: Trump issues an executive order which explicitly includes an instruction that "the Secretary of Labor and the Secretary's designees shall receive, to the maximum extent consistent with law, unfettered access to all unemployment data and related payment records, including all such data and records currently available to the Department of Labor's Office of Inspector General."
    source: https://www.whitehouse.gov/presidential-actions/2025/03/stopping-waste-fraud-and-abuse-by-eliminating-information-silos/
  cases:
  - name: AFL-CIO v. Dep't of Labor (D.D.C.)
    description: A coalition of labor unions sued the Department of Labor ("DOL"), the Department of Government Efficiency ("DOGE"), and others seeking to block DOGE's access to internal DOL information systems on the basis that such access violates the Administrative Procedure Act, the Privacy Act, the Economy Act, and other federal laws. A federal court denied requests to temporarily block DOGE's access while the case proceeds, but indicated further analysis was needed in particular on the Economy Act claims.
    case_no: 1:25-cv-00339
    date_filed: 2025-02-05
    link: https://www.courtlistener.com/docket/69613359/american-federation-of-labor-and-congress-of-industrial-organizations-v/
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

## Can You Tell Me More About These Names?

No. I am mainly just trying to track who is at each agency, the types of systems they might be accessing (mentioned in news coverage as well as the general notion they are looking at HR/Contracting/Procurement systems) and a timeline of events for their action. Other news organizations like ProPublica and Wired already have excellent resources on who these people are and where they have come from.

## I See an Error!
Great, please go to the [Issues](https://github.com/harrisj/trump_data/issues) tab and let me know. I especially want to know if:

- You see an error in the data
- You have an idea for a new feature
- There are some media reports or court filings I've missed that include DOGE activities

## Other Useful Fields

Okay, this is where it gets cool. I have some automations going for this file that make if helpful. First, I have JSON schemas defined for these files in the schemas directory. This includes a file with a master list of DOGE names so I don't misspell them in multiple places (Mike Russo here, Michael Russo there, etc.)

I also have a pre-commit hook that makes the following files and keeps them up-to-date:

- events.csv = a CSV dump of the events
- people.yaml = a dump of the DOGE people with a listing of agencies they've been linked to and events they've been named

## PIAs and SORNs?

Unlike a private business, the US Government is not allowed to just wantonly collect data on citizens without notification and legal review. There are two main types of documents that can provide insight into what data is in various systems that DOGE is accessing:

- **Privacy Impact Assessments** [(examples)](https://www.ed.gov/about/ed-overview/required-notices/privacy/privacy-impact-assessments-pia) are required to assess the privacy impact of any new system that stores and/or processess the private information of individuals (as mandated in the [E-Government Act of 2002](https://en.wikipedia.org/wiki/E-Government_Act_of_2002)).
- **Systems of Records Notices** [(examples)](https://www.ed.gov/about/ed-overview/required-notices/privacy/privacy-act-system-of-record-notice-issuances) identify the purpose for which a record about an individual is collected, from whom and what type of information is collected and how the information is shared with individuals and organizations outside/external to the agency (as mandated in the [Privacy Act of 1974](https://en.wikipedia.org/wiki/Privacy_Act_of_1974)).

In some cases, both of these documents might describe the same system, but it's not necessarily guaranteed. For instance, OPM might have a SORN describing the general structure of personnel records and PIAs for one or more systems that operate on that data. You can loosely think of the SORN as describing what information is collected on a form coming into the agency, while a PIA describes systems that act on that data after it has been ingested. In the OPM example, there is a [SORN for race/national origin/disability of staff](https://www.opm.gov/information-management/privacy-policy/sorn/opm-sorn-govt-7-applicant-race-sex-national-origin-and-disability-status-records.pdf) because those are collected on a form as part of the onboarding process and the data collected from those records is available in the [EHRI system as described in its PIA](https://www.opm.gov/information-management/privacy-policy/privacy-policy/ehridw.pdf). I have made my best attempt to link to relevant SORNs and PIAs when I can, but it is an inexact science because they describe two related but different concepts.

## Why You Should Really Look at SORNs

Government agencies are required to provide some standard fields in SORNs that can tell you about the purpose of the system, the type of data being stored, the individuals whose data will be in the system and where data might be sourced from that goes into those systems. For instance, let's look at the SORN for the Department of Education's [Common Origination and Disbursement (COD) System](https://www.federalregister.gov/documents/2023/06/28/2023-13698/privacy-act-of-1974-system-of-records). Whenever a Privacyt Impact Assessment uses or creates a new System of Records, **it is required to reference the associated SORN**

Looking at this specific SORN, we can see for instance the individuals included in the system:
_This system contains records of aid applicants, aid applicants' parents, spouses of aid applicants, and where applicable, endorsers, who apply for title IV, HEA programs including, but not limited to, the_:

1. _Federal Pell Grant Program;_
2. _Federal Perkins Loans Program;_
3. _Academic Competitiveness Grant (ACG) Program;_
4. _National Science and Mathematics Access to Retain Talent (National SMART) Grant Program;_
5. _TEACH Grant Program;_
6. _Iraq and Afghanistan Service Grant (IASG) Program;_
7. _Direct Loan Program, which includes Federal Direct Stafford/Ford Loans, Federal Direct Unsubsidized Stafford/Ford Loans, Federal Direct PLUS Loans, and Federal Direct Consolidation Loans;_
8. _FFEL Program;_
9. _Federal Insured Student Loan (FISL) Program;_
10. _FWS Program; and_
11. _FSEOG Program._

_The COD System also contains records of aid recipients under title IV of the HEA, parents of dependent aid applicants or recipients and the spouse of independent applicant or recipient. The COD System also maintains records on a PSLF qualifying employer's authorizing official who has certified an aid recipient's employment_

And it has this information about the type of information in the COD system:
_Records in the COD System include, but are not limited to, the following data about aid applicants and recipients, endorsers, aid applicants' and recipients' parents, and spouses of aid applicants and recipients who are part of an aid applicant's title IV, HEA aid application or receive title IV, HEA aid:_

1. _Identifier information, including name, Social Security number (SSN), date of birth (DOB), mailing address, email address, driver's license number, and telephone number;_
2. _Aid applicant and recipient demographic information, including demographic information of the aid applicant's and recipient's parent(s) and aid applicant's and recipient's spouse (if applicable), incarcerated student indicator flag, expected student enrollment, list of participating title IV, HEA institutions of higher education designated by the aid applicant to receive the Free Application For Federal Student Aid (FAFSA®) form data along with residency plans, and the financial profile of an aid applicant, an aid applicant's parent(s), or an aid applicant's spouse, as reported and calculated through the FAFSA form, and to also include processing flags, indicators, rejections, and overrides; and the consent/affirmative approval to disclose personally identifiable information to the IRS and to obtain FTI in order to determine eligibility for, or repayment obligations under, IDR plans pursuant to subsection 494 (a) of the HEA (20 U.S.C. 1098h(a));_
3. _Aid recipient's loan information including information about Direct Loans, FFEL program loans, Perkins loans, and FISL program loans. This includes information about the period from the origination of the loan through final payment, and milestones, including, but not limited to: discharge, consolidation, or other final disposition including details such as loan amount, date of disbursement, disbursement amounts, balances, loan status, repayment plan and related information, collections, claims, deferments, forbearances, refunds, and guaranty agencies, lender(s), holder(s), and servicer(s) of an aid recipient's FFEL program loan(s);_
4. _Information about Federal grant aid recipients, including recipients of Pell Grants, ACG, National SMART Grants, TEACH Grants, Iraq and Afghanistan Service Grants, and FSEOGs, including grant amounts, grant awards, verification status, lifetime eligibility used (LEU), IASG eligible veteran's dependent indicator, Children of Fallen Heroes Scholarship eligibility indicator, Pell Grant additional eligibility indicator, approved Prison Education programs (PEPs) (the FAFSA Simplification Act allows for expanding access to Federal Pell Grants to include Federal and State penal facilities' approved PEPS; and information about the FWS program, including the amount of FWS earnings and category/type of FWS employment;_
5. _Pell Grant collection status indicator and overpayment collection information;_
6. _Promissory notes including promissory note identification numbers, loan type, current servicer, principal balance, and the accrued interest for Direct Loans, Federal Direct PLUS Loans, or Department-held FFEL program loans;_
7. _TEACH Agreements to Serve;_
8. _Direct Loan Entrance Counseling forms, Federal Student Loan Exit Counseling forms, Federal Direct PLUS Loan Counseling forms, the Annual School Loan Acknowledgement (ASLA), Federal Direct PLUS Loan Requests, endorser addendums, and counseling in the Direct Loan and TEACH Grant programs, such as the date that the aid applicant completed counseling;_
9. _Credit report information for Federal Direct PLUS Loan applicants, recipients, and endorsers and if applicable, documents related to a Federal Direct PLUS Loan applicant's request for a credit appeal including credit check details, adverse credit history, credit bureau information, and applicant provided appeal support documentation and the Department's appeal decision,_
...

and so on. You can see why these might be useful to figure out in the event of a privacy breach both what kind of information could be leaked and who would be affected. I attempt to summarize it in in the `risk` field, but that is largely limited.

I will generally try to include systems in the `systems` section for which any of the following criteria are true:

- They are named directly in a news report or court filing
- They are described indirectly and I am able to identify based on that
- They are used for HR or contracting/procurement or making payments (those seem to be the systems that DOGE goes after first)

## Validation

I have created a JSON schema for the document that can be used to validate edits if you are using a plugin like the RedHat YAML one in an IDE.

## Disclaimer

I am doing my best to fill in the gaps and collect information on a purposefully murky organization designed to avoid transparency and oversight. Mistakes are inevitable; please be aware of the risks and point out any issues to me by filing an Issue on this repo. Also, I am not a reporter. I only put things in here that have been presented publicly in the media.
