from datetime import date
from util import read_processed_events, sorted_by_last_name, as_list

def generate_mermaid_chart():
    events = read_processed_events()

    people = {}
    for event in events:
        if 'named' in event:
            for name in event['named']:
                agency = event['agency']
                if not isinstance(agency, str) or agency == 'DOGE':
                    continue

                if name not in people:
                    people[name] = {}

                if event['type'] == 'offboarded':
                    if agency in people[name]:
                        people[name][agency]['end'] = str(event['date'])
                elif agency not in people[name]:
                    sdate = str(event['date']).strip('~')
                    if sdate < '2025-01-20':
                        start = '2025-01-20'
                    else:
                        start = sdate

                    people[name][agency] = {'agency': agency, 'start': start}

    names = sorted_by_last_name(people.keys())

    out = '''```mermaid
gantt
    title DOGE staffing
    dateFormat YYYY-MM-DD
'''

    for name in names:
        out += f"    section {name}\n"
        
        postings = sorted(people[name].values(), key=lambda x: x['start'])
        for posting in postings:
            if 'end' in posting:
                end = posting['end']
            else:
                end = date.today()

            out += f"        {posting['agency']} : {posting['start']}, {end}\n"

    out += "```\n"
    return out

output_md = generate_mermaid_chart()
output_file = './staffing_chart.md'
with open(output_file, 'w') as file:
    file.write(output_md)

