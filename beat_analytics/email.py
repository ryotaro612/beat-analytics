import csv
import os
import google.cloud.bigquery as bq


def fetch_raw_events(client: bq.Client, output_filename: str):
    """ """
    job = client.query(
        f"select * from {os.environ['RAW_EMAIL_TABLE']} where timestamp > '2020-01-01'"
    )
    rows = job.result()
    with open(output_filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["event_id", "event", "timestamp"])
        for row in rows:
            writer.writerow([field for field in row])
