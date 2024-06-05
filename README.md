# Saga Treatment Planner Webhook

Discord Webhook handler for Saga Treatment Planner.

## Configuration

Populate `config.json` with the following values:

```json
{
    "url": "Url of treatment planner app",
    "username": "Username for treatment planner app",
    "password": "Password for treatment planner app",
    "webhooks": {        
        "treatment_start_time": "Discord webhook url for treatment start time channel",
        "companion_start_time": "Discord webhook url for companion start time channel"
    }
}
```

Running the script

```bash
python main.py
```
