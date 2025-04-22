from datetime import date
from util import read_processed_events, dump_generated_file

FILE_VERSION = "1.0.0"
SCHEMA_PATH = "schemas/generated-systems-file.json"

def get_systems_postings_yaml():
    events = read_processed_events()

    open_access = {}
    closed_access = []

    for event in events:
        for name in event.get("named", []):
            if event['type'] == 'access_granted':
                for system_id in event.get("access_systems", []):
                    key = f"{name}|{system_id}"
                    if key in open_access:
                        raise ValueError(f"Grant access {name} to {system_id} on {event['date']}, but has access")
                    
                    open_access[key] = {"id": system_id,
                                        "name": name,
                                        "agency": event["agency"],
                                        "access_type": event.get("access_type", "unknown"),
                                        "start_date": event["date"]}
            elif event['type'] == 'access_changed':
                for system_id in event.get("access_systems", []):
                    key = f"{name}|{system_id}"
                    if key not in open_access:
                        raise ValueError(f"Change access of {name} to {system_id} on {event['date']}, but doesn't have access")
                    
                    system_record = open_access[key]
                    system_record["end_date"] = event["date"]
                    closed_access.append(system_record)
                    del open_access[key]

                    open_access[key] = {"id": system_id,
                                        "name": name,
                                        "agency": event["agency"],
                                        "access_type": event.get("access_type", "unknown"),
                                        "start_date": event["date"]}
            elif event['type'] == 'access_revoked':
                for system_id in event.get("access_systems", []):
                    key = f"{name}|{system_id}"
                    if key not in open_access:
                        print(closed_access)
                        raise ValueError(f"Revoke access of {name} to {system_id} on {event['date']}, but doesn't have access")
                    
                    system_record = open_access[key]
                    system_record["end_date"] = event["date"]
                    closed_access.append(system_record)
                    del open_access[key]
            elif event['type'] == 'offboarded':
                open_records = [o for o in open_access.values() if o["name"] == name]
                for system_record in open_records:
                    system_id = system_record["id"]
                    print(f"Auto-closing system access of {name} to system {system_id} on {event['date']}")
                    key = f"{name}|{system_id}"
                    system_record["end_date"] = event["date"]
                    closed_access.append(system_record)
                    del open_access[key]

    for item in open_access.values():
        closed_access.append(item)

    return sorted(closed_access, key=lambda x: x['start_date'])

meta = {
    "title": "Systems",
    "version": FILE_VERSION,
    "generated": date.today()
}

systems = get_systems_postings_yaml()
dump_generated_file(meta, {"systems_access": systems}, 'system_postings.yaml', SCHEMA_PATH, line_break_indent=2)