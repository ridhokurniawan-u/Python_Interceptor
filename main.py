from fastapi import FastAPI, Request
import httpx

app = FastAPI()

TARGET_URL = "http://127.0.0.1:1337"  # <--- Target url : port

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def intercept(request: Request, full_path: str):
    body = await request.body()

    async with httpx.AsyncClient() as client:
        url = f"{TARGET_URL}/{full_path}"
        response = await client.request(
            method=request.method,
            url=url,
            headers=request.headers,
            content=body
        )

    print("==== CLIENT REQUEST ====")
    print("Headers:", dict(request.headers))
    print("Body:", body.decode("utf-8") if body else "No body")
    print("==== SERVER RESPONSE ====")
    print("Status Code:", response.status_code)
    print("Response Headers:", dict(response.headers))
    print("Response Body:", response.text)

    return response.text, response.status_code, dict(response.headers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
