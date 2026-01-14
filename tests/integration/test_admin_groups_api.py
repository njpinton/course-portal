import requests
import json

# Test the groups submission status API
url = "http://127.0.0.1:8788/api/admin/groups/submission-status"

try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse Headers:")
    print(json.dumps(dict(response.headers), indent=2))

    if response.status_code == 200:
        data = response.json()
        print(f"\nNumber of groups returned: {len(data)}")

        if len(data) > 0:
            print(f"\nFirst group structure:")
            print(json.dumps(data[0], indent=2))

            print(f"\nAll group names:")
            for group in data:
                print(f"  - {group.get('group_name', 'N/A')} (ID: {group.get('id', 'N/A')[:8]}...)")
        else:
            print("\n⚠️  No groups returned from API!")
    else:
        print(f"\n❌ Error: {response.text}")

except Exception as e:
    print(f"❌ Exception: {e}")
