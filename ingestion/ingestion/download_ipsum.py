import requests
import redis

IPSUM_URL = "https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt"

def load_ipsum_to_redis():
    print("Downloading IPsum feed...")
    response = requests.get(IPSUM_URL)

    if response.status_code != 200:
        print("Failed to download IPsum")
        return

    lines = response.text.splitlines()

    r = redis.Redis(host="redis", port=6379, decode_responses=True)

    print("Storing malicious IPs in Redis...")

    for line in lines:
        if line.startswith("#"):
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        ip = parts[0]
        confidence = parts[1]

        r.hset(f"malicious:{ip}", mapping={"confidence": confidence})

    print("IPsum feed loaded into Redis successfully!")

if __name__ == "__main__":
    load_ipsum_to_redis()
