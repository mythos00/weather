## Usage

Run the API:

```bash
uvicorn main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

Use the endpoint:

```text
GET /weather?city=Baku
```

You can enter any city:

```text
/weather?city=London
/weather?city=Istanbul
/weather?city=Paris
```

The API returns the current temperature, feels-like temperature, humidity, wind speed, and weather condition.
