# napolean

Basic Django API service for managing a mobile phone farm with pluggable
hardware-as-a-service providers.

## Stack

- Django 5.2.13
- Django REST Framework 3.15.2
- requests 2.32.3

## Setup

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Configuration

Set provider credentials via environment variables:

- `DEVICEFARM_API_KEY`: API key for `https://devicefarm.io/api/v1`

## API surface

Base path: `/api/`

- `GET /api/providers/` — list supported providers
- `GET /api/providers/{provider}/phones` — list phones (`limit` query supported)
- `POST /api/providers/{provider}/phones` — create phone
- `POST /api/providers/{provider}/phones/{phone_id}/start` — start phone
- `POST /api/providers/{provider}/phones/{phone_id}/stop` — stop phone
- `POST /api/providers/{provider}/phones/{phone_id}/prepare` — install automation library
- `POST /api/providers/{provider}/phones/{phone_id}/shell` — run shell command
- `POST /api/providers/{provider}/phones/{phone_id}/script` — run detached script
- `GET /api/providers/{provider}/phones/{phone_id}/script?run_id=...` — poll run status
- `DELETE /api/providers/{provider}/phones/{phone_id}` — delete phone permanently

## DeviceFarm notes encoded in the client/API layer

- Uses bearer token authentication with your DeviceFarm API key
- Supports the full documented endpoint set
- Preserves provider error envelope (`data` / `error`) for API consumers
- Includes `stop_when_done` support for detached script runs
