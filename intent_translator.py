from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json
import re

TOPOLOGY_DIR = "topologies"

def slugify(name):
    """
    Converts a string like "My Test Net" into "my_test_net".
    """
    name = name.lower()
    name = re.sub(r'[\s\W]+', '_', name)
    name = name.strip('_')
    return name

def get_next_topology_num(directory):
    """
    Checks the directory for files like 01_...json, 02_...json
    and returns the next available number.
    """
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    files = os.listdir(directory)
    pattern = re.compile(r'^(\d{2})_.*\.json$')
    max_num = 0

    for f in files:
        match = pattern.match(f)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num

    return max_num + 1


if not os.getenv("GEMINI_API_KEY"):
    load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API key not found in environment or .env file.")

client = genai.Client(api_key=api_key)

system_instruction = """
CRITICAL RULE: You MUST output *only* the raw JSON. Your entire response must be valid JSON parsable by Python's json.loads(). Do NOT include ```json, comments, or any other text.

You are a network topology assistant. Your task is to generate a new network topology in JSON format based on the user's request, following the schema below.

You must follow the schema rules outlined below. You must also use the "Full Schema Template" as a reference for the structure.

### Schema Rules

1.  **Top-Level Keys:**
    * `ID`: (String) A unique, simple identifier for the topology (e.g., "MyTestNet").
    * `VERSION`: (String) The topology version (e.g., "1.0").
    * `DESCRIPTION`: (String) A brief description of the topology.

2.  **`MONITORING` Block (Optional):**
    * This block controls the `IntentMonitor`.
    * `enabled`: (Boolean) `true` to run the monitor, `false` to disable.
    * `interval`: (Number) The time in seconds between monitoring checks.
    * `recovery_enabled`: (Boolean) `true` to allow the monitor to attempt recovery actions, `false` to only report issues.

3.  **`COMPONENTS` Block:**
    * This block defines all network devices.
    * **`HOSTS`:** (List)
        * `ID`: (String) Host identifier (e.g., "h1").
        * `IP`: (String, Optional) IP address with subnet (e.g., "10.0.0.1/24").
        * `MAC`: (String, Optional) MAC address.
        * `MAX_CPU`: (Number, Optional) Creates a CPU Intent. A float from 0.0 to 1.0 (e.g., 0.8 for 80%).
        * `MAX_RAM`: (Number, Optional) Creates a Memory Intent. An integer for max RAM in MB (e.g., 512).
    * **`SWITCHES`:** (List)
        * `ID`: (String) Switch identifier (e.g., "s1").
        * `TYPE`: (String, Optional) The class to use (e.g., "OVSSwitch", "OVSKernelSwitch").
        * `PARAMS`: (Object, Optional) Parameters for the switch (e.g., `{"PROTOCOLS": "OpenFlow13"}`).
    * **`CONTROLLERS`:** (List)
        * `ID`: (String) Controller identifier (e.g., "c0").
        * `TYPE`: (String, Optional) The class to use (e.g., "Controller").
        * `PARAMS`: (Object, Optional) Parameters (e.g., `{"IP": "127.0.0.1", "PORT": 6653}`).

4.  **`CONNECTIONS` Block:**
    * This block defines the links between components.
    * `ENDPOINTS`: (List) A list of two `ID` strings to link (e.g., `["h1", "s1"]`).
    * `PARAMS` (Optional): This object creates Link Intents.
        * `BANDWIDTH`: (Number) Link speed limit in Mbps (e.g., 100).
        * `DELAY`: (String) Link delay (e.g., "5ms", "100us").
        * `LOSS`: (Number) Packet loss percentage (e.g., 1 for 1%).

---
### Full Schema Template JSON (for reference)
```json
{
        "ID": "my_new_topology",
        "VERSION": "1.0",
        "DESCRIPTION": "A description of the new topology.",
        "MONITORING": {
            "enabled": true,
            "interval": 10,
            "recovery_enabled": true
            },
        "COMPONENTS": {
            "HOSTS": [
                {
                    "ID": "h1",
                    "IP": "10.0.0.1/24",
                    "MAC": "00:00:00:00:00:01",
                    "MAX_CPU": 0.5,
                    "MAX_RAM": 256
                    },
                {
                    "ID": "h2",
                    "IP": "10.0.0.2/24"
                    }
                ],
            "SWITCHES": [
                {
                    "ID": "s1",
                    "TYPE": "OVSSwitch",
                    "PARAMS": {
                        "PROTOCOLS": "OpenFlow13"
                        }
                    }
                ],
            "CONTROLLERS": [
                {
                    "ID": "c0",
                    "TYPE": "Controller",
                    "PARAMS": {
                        "IP": "127.0.0.1",
                        "PORT": 6653
                        }
                    }
                ]
            },
        "CONNECTIONS": [
            {
                "ENDPOINTS": ["h1", "s1"],
                "PARAMS": {
                    "BANDWIDTH": 100,
                    "DELAY": "5ms",
                    "LOSS": 1
                    }
                },
            {
                "ENDPOINTS": ["h2", "s1"],
                "PARAMS": {
                    "BANDWIDTH": 50
                    }
                }
            ]
}
FINAL REMINDER: Your entire output must be only the raw JSON. Do not write any other text, comments, or markdown.
"""

user_prompt = input("Enter your prompt here: ")

response = client.models.generate_content(
        model="gemini-2.5-pro", 
        config=types.GenerateContentConfig(
            system_instruction=system_instruction),
        contents=user_prompt
        )

json_output = response.text

try:
    start_index = json_output.index("{")
    end_index = json_output.rindex("}") + 1
    cleaned_json = json_output[start_index:end_index]
except ValueError:
    cleaned_json = json_output

try:
    data = json.loads(cleaned_json)
    
    topology_id = data.get("ID", "untitled")
    
    slug_name = slugify(topology_id)
    
    next_num = get_next_topology_num(TOPOLOGY_DIR)
    
    filename = f"{next_num:02d}_{slug_name}.json"
    filepath = os.path.join(TOPOLOGY_DIR, filename)
    
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
        
    print(f"\n✅ Success! Topology saved to: {filepath}")

except json.JSONDecodeError:
    print("\n--- ❌ ERROR: AI did not return valid JSON. ---")
    print("Raw output from AI (after cleaning):")
    print
