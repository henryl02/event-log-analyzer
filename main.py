import log_reader
import log_analyzer
import visualization
import logging


def main():
    logging.basicConfig(filename="cybersecurity.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info("Starting EventLogAnalyzer...")

    print("Choose an option:")
    print("1. Analyze system logs")
    print("2. Analyze an .evtx file")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        logging.info("Fetching and analyzing system logs...")
        logs = log_reader.read_system_logs("Application")  # Change log type as needed
    elif choice == "2":
        file_name = input("Enter the name of the .evtx file (e.g., logs.evtx): ")
        logging.info(f"Analyzing .evtx file: {file_name}")
        logs = log_reader.read_evtx_file(file_name)
    else:
        logging.error("Invalid choice. Exiting.")
        return

    # Analyze logs
    categorized_data = log_analyzer.analyze_logs(logs)

    # Generate a human-readable report
    visualization.generate_human_readable_report(categorized_data)


if __name__ == "__main__":
    main()
