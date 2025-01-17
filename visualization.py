import logging
from tabulate import tabulate  # For better tabular formatting

def generate_human_readable_report(analyzed_data):
    """
    Generate a user-friendly report for the log analysis and write it to the log file.
    """
    # Define the structure of the report
    table_data = []

    for category, logs in analyzed_data.items():
        for log in logs:
            table_data.append([
                category,
                log.get("EventID", "Unknown"),
                log.get("Source", "Unknown"),
                log.get("Time", "Unknown"),
                log.get("UserSID", "Unknown"),
                summarize_data(log.get("Data", {}))
            ])

    # Generate the table
    table = tabulate(table_data, headers=["Category", "EventID", "Source", "Time", "UserSID", "Details"], tablefmt="grid")

    # Log the table into the cybersecurity.log file
    logging.info("\n" + table)

    # Optionally, print the table to the console (if you want both outputs)
    print(table)


def summarize_data(data):
    """
    Summarize the 'Data' field for concise output.
    """
    if not data:
        return "No additional details"
    
    # Limit the details to the most relevant fields
    summarized_data = []
    for key, value in data.items():
        summarized_data.append(f"{key}: {value}")
    
    # Combine into a single string
    return "; ".join(summarized_data[:5])  # Include only the first 5 fields to avoid clutter
