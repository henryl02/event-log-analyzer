from Evtx.Evtx import Evtx

file_path = "data2.evtx"  # Replace with the actual file name

def inspect_raw_xml(file_name):
    """
    Print the raw XML for each record in the .evtx file to inspect the structure.
    """
    with Evtx(file_name) as log:
        for record in log.records():
            print(record.xml())  # Print raw XML for analysis
            break  # Limit to the first record for debugging

inspect_raw_xml(file_path)