import yaml
from datetime import date
from edtf import parse_edtf
from util import read_processed_events, read_raw_cases_dict, read_raw_details_dict, read_raw_agencies, read_postings, as_list
def generate_agency_page(agency, base_path:str):
    pass

def generate_agencies_mermaid():
    agencies = read_raw_agencies()
    events = read_processed_events()
    cases = read_raw_cases_dict()
    details = read_raw_details_dict()
    postings = read_postings()

    for agency in agencies:
        agency['events'] = [e for e in events if agency['id'] in as_list(e['agency'])]
        #agency['cases'] = [c for c in cases if agency['id'] in as_list(c['agency'])]
        agency['postings'] = [p for p in postings if p["agency_id"] == agency["id"] and p['name'] != 'Elon Musk']

    agencies = sorted([a for a in agencies if len(a['postings']) > 0], key=lambda x: x['postings'][0]['first_date'])
    outfile = "agencies_chart.md"

    with open(outfile, 'w') as file:
        file.write(f"# DOGE Staff by Agency\n\n")

        file.write('''```mermaid
gantt
    title DOGE staff
    todayMarker off
    axisFormat %m/%d
    dateFormat YYYY-MM-DD
''')
        for agency in agencies:
            if len(agency['postings']) == 0 or agency['id'] == 'DOGE':
                continue

            file.write(f"    SECTION {agency['id']}\n")
            for posting in agency['postings']:
                if posting['first_date'] < parse_edtf('2025-01-20'):
                    start = '2025-01-20'
                else:
                    start = str(posting['first_date']).strip('~')

                if 'offboard_date' in posting:
                    end = posting['offboard_date']
                else:
                    end = posting['doge_agency_last']

                file.write(f"        {posting['name']} : {start}, {end}\n")
        file.write("```")

generate_agencies_mermaid()