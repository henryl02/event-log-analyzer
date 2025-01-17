def analyze_logs(logs):
    """Analyze logs and categorize them."""
    categorized_logs = {"Critical": [], "Confidential": [], "Informal": []}

    for log in logs:
        # Ensure EventID is treated as an integer
        try:
            event_id = int(log["EventID"])
        except ValueError:
            event_id = 0  # Default to 0 if EventID is invalid

        # Categorize logs based on predefined rules
        if event_id in [4625, 7031, 7032]:  # Critical event IDs
            categorized_logs["Critical"].append(log)
        elif log["Source"] in ["Security", "Application"]:  # Confidential sources
            categorized_logs["Confidential"].append(log)
        else:
            categorized_logs["Informal"].append(log)

    return categorized_logs
