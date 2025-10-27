from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

# Load .env only if not already set (so it doesn’t override GitHub Secrets)
if not os.getenv("GEMINI_API_KEY"):
    load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API key not found in environment or .env file.")

client = genai.Client(api_key=api_key)

# --- System Instruction: Defines the AI's role, rules, and reference template ---
system_instruction = """
You are a network topology assistant. Your task is to generate a new network topology in JSON format. This JSON file will be parsed by a custom Python script that defines a specific schema.

You must follow the schema rules outlined below. You must also use the "Full Schema Template" as a reference for the structure. You must only output the raw JSON, with no other text, comments, or explanations.

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
"""

user_prompt = input("Enter your prompt here: ")

response = client.models.generate_content(
        model="gemini-2.5-flash", 
        config=types.GenerateContentConfig(
            system_instruction=system_instruction),
        contents=user_prompt
        )

print(response.text)
