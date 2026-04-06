
import os
import json
import time
from pathlib import Path

from dotenv import load_dotenv
from azure.eventhub import EventHubProducerClient, EventData

load_dotenv()

CONNECTION_STRING = os.getenv("FABRIC_EVENTHUB_CONNECTION_STRING")
EVENTHUB_NAME = os.getenv("FABRIC_EVENTHUB_NAME")
LOG_FILE = Path("logs/ids.log")

producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STRING,
    eventhub_name=EVENTHUB_NAME
)

def follow(file_obj):
    file_obj.seek(0, 2)
    while True:
        line = file_obj.readline()
        if not line:
            time.sleep(0.2)
            continue
        yield line

def parse_ids_line(line):
    line = line.strip()

    parts = line.split(" - ", 4)
    if len(parts) < 5:
        return {
            "log_type": "ids",
            "parse_status": "raw_only",
            "severity": None,
            "protocol": None,
            "src_ip": None,
            "src_port": None,
            "dst_ip": None,
            "dst_port": None,
            "raw_message": line,
            "ingest_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

    event_time, logger_name, severity, protocol, network = parts
    src_ip = src_port = dst_ip = dst_port = None

    if " --> " in network:
        left, right = network.split(" --> ", 1)

        if ":" in left:
            src_ip, src_port = left.rsplit(":", 1)
        else:
            src_ip = left

        if ":" in right:
            dst_ip, dst_port = right.rsplit(":", 1)
        else:
            dst_ip = right

    payload = {
        "event_time": event_time,
        "logger_name": logger_name.strip(),
        "severity": severity.strip(),
        "protocol": protocol.strip(),
        "src_ip": src_ip.strip() if src_ip else None,
        "src_port": int(src_port) if src_port and src_port.isdigit() else None,
        "dst_ip": dst_ip.strip() if dst_ip else None,
        "dst_port": int(dst_port) if dst_port and dst_port.isdigit() else None,
        "log_type": "ids",
        "parse_status": "parsed" if src_ip or dst_ip else "partial",
        "raw_message": line,
        "ingest_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    return payload

with LOG_FILE.open("r", encoding="utf-8", errors="ignore") as f:
    print("Listening on logs/ids.log ...")
    for line in follow(f):
        if not line.strip():
            continue

        payload = parse_ids_line(line)

        try:
            batch = producer.create_batch()
            batch.add(EventData(json.dumps(payload)))
            producer.send_batch(batch)

            sev = payload.get("severity", "unknown")
            proto = payload.get("protocol", "unknown")
            src = payload.get("src_ip", "NA")
            dst = payload.get("dst_ip", "NA")
            status = payload.get("parse_status", "unknown")

            print(f"[SENT] status={status} severity={sev} protocol={proto} {src} -> {dst}")
        except Exception as e:
            print("Error while sending:", e)
            time.sleep(1)

producer.close()