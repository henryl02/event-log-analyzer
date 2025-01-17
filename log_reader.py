from Evtx.Evtx import Evtx
import xml.etree.ElementTree as ET
import win32evtlog

def read_system_logs(log_type="Application"):
    """
    Fetch logs from the Windows Event Viewer.
    """
    server = "localhost"  # Local machine
    hand = win32evtlog.OpenEventLog(server, log_type)
    logs = []

    # Fetch events from the specified log type
    events = win32evtlog.ReadEventLog(
        hand, win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ, 0
    )

    for event in events:
        logs.append({
            "EventID": event.EventID,
            "Source": event.SourceName,
            "Time": event.TimeGenerated,
            "Message": event.StringInserts or "No message",
        })

    win32evtlog.CloseEventLog(hand)
    return logs

def parse_event_details(xml_data):
    """
    Parse detailed information from an event's XML data, accounting for namespaces.
    """
    # Define the namespace
    namespace = {"ns": "http://schemas.microsoft.com/win/2004/08/events/event"}

    # Parse the XML
    event = ET.fromstring(xml_data)

    # Extract EventID
    event_id_elem = event.find(".//ns:EventID", namespace)
    event_id = event_id_elem.text if event_id_elem is not None else "Unknown"

    # Extract Provider Name
    provider_elem = event.find(".//ns:Provider", namespace)
    provider_name = provider_elem.attrib.get("Name", "Unknown") if provider_elem is not None else "Unknown"

    # Extract TimeCreated
    time_elem = event.find(".//ns:TimeCreated", namespace)
    time_generated = time_elem.attrib.get("SystemTime", "Unknown") if time_elem is not None else "Unknown"

    # Extract UserSID
    user_elem = event.find(".//ns:Security", namespace)
    user_sid = user_elem.attrib.get("UserID", "Unknown") if user_elem is not None else "Unknown"

    # Extract Level, Task, Opcode, etc.
    level_elem = event.find(".//ns:Level", namespace)
    level = level_elem.text if level_elem is not None else "Unknown"

    task_elem = event.find(".//ns:Task", namespace)
    task = task_elem.text if task_elem is not None else "Unknown"

    opcode_elem = event.find(".//ns:Opcode", namespace)
    opcode = opcode_elem.text if opcode_elem is not None else "Unknown"

    # Extract Data elements
    data_elems = event.findall(".//ns:Data", namespace)
    data = {data_elem.attrib.get("Name", f"Field-{i}"): (data_elem.text or "No data")
            for i, data_elem in enumerate(data_elems)}

    return {
        "EventID": event_id,
        "Source": provider_name,
        "Time": time_generated,
        "Level": level,
        "Task": task,
        "Opcode": opcode,
        "UserSID": user_sid,
        "Data": data,
    }

def read_evtx_file(file_name):
    """
    Read and parse logs from an .evtx file.
    """
    logs = []

    with Evtx(file_name) as log:
        for record in log.records():
            try:
                xml_data = record.xml()
                parsed_event = parse_event_details(xml_data)
                logs.append(parsed_event)
            except Exception as e:
                print(f"Error parsing record: {e}")
                continue

    return logs
