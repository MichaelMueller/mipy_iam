import os
import pytest
import asyncio
import mipy_iam.interactive as interactive
import mipy_iam.db as db
import mipy_aiofiles
from mipy_users import create, by_id, by_email, all, update, delete_user

@pytest.fixture(scope="module")
async def setup_temp_db():
    """
    Fixture to set up a temporary database for testing.
    Cleans up the temporary folder after the test.
    """
    temp_dir = await mipy_aiofiles.create_temp_folder()
    db_path = os.path.join(temp_dir, "test.db")
    interactive.set_param("SQLITE_PATH", db_path)
    print(f"Using test database at: {db_path}")

    yield  # Yield control to the test

    # Cleanup after the test
    await db.close()
    await mipy_aiofiles.delete_folder(temp_dir)
    print(f"Cleaned up temporary directory: {temp_dir}")

@pytest.mark.asyncio
async def test_create_and_fetch_user(setup_temp_db):
    
    # Create a user
    user = await create(
        name="John Doe",
        email="john.doe@example.com",
        hashed_password="hashed_password123"
    )
    assert user is not None
    assert user.name == "John Doe"
    assert user.email == "john.doe@example.com"

    # Fetch the user by ID
    fetched_user = await by_id(user_id=user.id)
    assert fetched_user is not None
    assert fetched_user.id == user.id


# @pytest.mark.asyncio
# async def test_get_user_by_email(setup_temp_db):
#     # Create a user
#     await create_user(
#         name="Jane Doe",
#         email="jane.doe@example.com",
#         hashed_password="hashed_password456"
#     )

#     # Fetch the user by email
#     fetched_user = await get_user_by_email(email="jane.doe@example.com")
#     assert fetched_user is not None
#     assert fetched_user.email == "jane.doe@example.com"


# @pytest.mark.asyncio
# async def test_update_user(setup_temp_db):
#     # Create a user
#     user = await create_user(
#         name="John Doe",
#         email="john.doe@example.com",
#         hashed_password="hashed_password123"
#     )

#     # Update the user
#     updated_user = await update_user(user_id=user.id, name="John Updated")
#     assert updated_user is not None
#     assert updated_user.name == "John Updated"


# @pytest.mark.asyncio
# async def test_delete_user(setup_temp_db):
#     # Create a user
#     user = await create_user(
#         name="John Doe",
#         email="john.doe@example.com",
#         hashed_password="hashed_password123"
#     )

#     # Delete the user
#     is_deleted = await delete_user(user_id=user.id)
#     assert is_deleted

#     # Verify the user is deleted
#     deleted_user = await get_user(user_id=user.id)
#     assert deleted_user is None


# @pytest.mark.asyncio
# async def test_get_all_users(setup_temp_db):
#     # Create multiple users
#     await create_user(
#         name="John Doe",
#         email="john.doe@example.com",
#         hashed_password="hashed_password123"
#     )
#     await create_user(
#         name="Jane Doe",
#         email="jane.doe@example.com",
#         hashed_password="hashed_password456"
#     )

#     # Fetch all users
#     all_users = await get_all_users()
#     assert len(all_users) == 2
#     assert any(user.name == "John Doe" for user in all_users)
#     assert any(user.name == "Jane Doe" for user in all_users)

if __name__ == "__main__":
    import sys
    # Run pytest programmatically
    sys.exit(pytest.main(["-v", __file__]))