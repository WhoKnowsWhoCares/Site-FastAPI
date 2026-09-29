"""Quick debug for reorder endpoint."""
import asyncio
from fastapi import FastAPI
from backend.api.router import api_router
from httpx import ASGITransport, AsyncClient

async def main():
    app = FastAPI()
    app.include_router(api_router, prefix='/api')
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        r = await client.post('/api/admin/content/reorder', json={
            'section': 'aboutme',
            'content_orders': [{'content_id': 1, 'order': 10}]
        })
        print(f'Status: {r.status_code}')
        print(f'Body: {r.text}')

asyncio.run(main())