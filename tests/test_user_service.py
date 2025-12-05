import asyncio
import nats
import json

async def test_user_service():
    nc = await nats.connect("nats://localhost:4222")
    
    print("Test 1: Creating user...")
    response = await nc.request(
        "users.create",
        json.dumps({
            "keycloak_id": "test-123",
            "username": "testuser"
        }).encode(),
        timeout=5
    )
    result = json.loads(response.data.decode())
    print("Created:", result)
    
    print("\nTest 2: Getting user...")
    response = await nc.request(
        "users.get",
        json.dumps({
            "keycloak_id": "test-123"
        }).encode(),
        timeout=5
    )
    result = json.loads(response.data.decode())
    print("Retrieved:", result)
    
    print("\nTest 3: Listing all users...")
    response = await nc.request(
        "users.list",
        json.dumps({}).encode(),
        timeout=5
    )
    result = json.loads(response.data.decode())
    print("All users:", result)
    
    await nc.close()

if __name__ == "__main__":
    asyncio.run(test_user_service())