import os
import httpx
import asyncio

token = "eyJraWQiOiJaTUtjVXciLCJhbGciOiJFUzI1NiJ9.eyJleHAiOjI1NjI3NjQwMTMsImlhdCI6MTc3NDM2NDAxMywibmJmIjoxNzc0MzY0MDEzLCJzdWIiOiJ7XCJ0b2tlblJlZklkXCI6XCJiZjAxMTE4NS03ZjE0LTQ1MDItODk1MC0yMTgyNDU4MzZmMGFcIixcInZlbmRvckludGVncmF0aW9uS2V5XCI6XCJlMzFmZjIzYjA4NmI0MDZjODg3NGIyZjZkODQ5NTMxM1wiLFwidXNlckFjY291bnRJZFwiOlwiMzRjMjQzYjItNDhkZS00MGMzLWI0ODctN2E5ZTY1YjM3MWM5XCIsXCJkZXZpY2VJZFwiOlwiNWMxM2I3MDQtZmJmZS01MGI3LWJjODktNzgyZTJjYTYyZWE5XCIsXCJzZXNzaW9uSWRcIjpcImQ1M2ZhM2YwLTlhMmYtNDg1Ni04ZTM3LWNmMDlkZDI1YzBlOVwiLFwiYWRkaXRpb25hbERhdGFcIjpcIno1NC9NZzltdjE2WXdmb0gvS0EwYkVuN0lYZmJ0LzUrelNpMkVXR0s1VzFSTkczdTlLa2pWZDNoWjU1ZStNZERhWXBOVi9UOUxIRmtQejFFQisybTdRPT1cIixcInJvbGVcIjpcImF1dGgtdG90cFwiLFwic291cmNlSXBBZGRyZXNzXCI6XCIxMjIuMTY3LjEwMC45MiwxMDQuMjIuNDcuMTM2LDM1LjI0MS4yMy4xMjNcIixcInR3b0ZhRXhwaXJ5VHNcIjoyNTYyNzY0MDEzMjMxLFwidmVuZG9yTmFtZVwiOlwiZ3Jvd3dBcGlcIn0iLCJpc3MiOiJhcGV4LWF1dGgtcHJvZC1hcHAifQ.fiFaLg-1egXw4agAsZUR-uvAHh2YS6EDnSqxHYJps2U4zyx8hDIas8j9FY44FvsxpKAY9A9VLbt9xYig6oKDBA"

async def main():
    symbols = ["NSE_RELIANCE", "NSE_TCS", "NSE_HDFCBANK", "NSE_INFY", "NSE_ICICIBANK", "NSE_BHARTIARTL", "NSE_ITC", "NSE_LT", "NSE_WIPRO", "NSE_ASIANPAINT"]
    url = f"https://api.groww.in/v1/live-data/ltp?segment=CASH&exchange_symbols={','.join(symbols)}"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-API-VERSION": "1.0",
        "Accept": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
            print(f"Status: {resp.status_code}")
            print(f"Response: {resp.text[:500]}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(main())
