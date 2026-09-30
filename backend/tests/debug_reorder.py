"""Quick debug for reorder endpoint."""
import asyncio

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from backend.api.router import api_router


async def main():
    app = FastAPI()
    app.include_router(api_router, prefix='/api')

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        r = await client.post('/api/admin/content/reorder', params=[('section', 'aboutme'), ('content_orders', '1,10'), ('content_orders', '2,5')])
        print(f'Status: {r.status_code}')
        print(f'Body: {r.text}')

asyncio.run(main())
