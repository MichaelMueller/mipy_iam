import os
import pytest
import asyncio
import mipy_env
import mipy_db
import mipy_aiofiles
import mipy_config

@pytest.fixture(scope="module")
async def setup_temp_db():
    """
    Fixture to set up a temporary database for testing.
    Cleans up the temporary folder after the test.
    """
    temp_dir = await mipy_aiofiles.create_temp_folder()
    db_path = os.path.join(temp_dir, "test.db")
    mipy_env.set_param("SQLITE_PATH", db_path)
    print(f"Using test database at: {db_path}")

    yield  # Yield control to the test

    # Cleanup after the test
    await mipy_db.close()
    await mipy_aiofiles.delete_folder(temp_dir)
    print(f"Cleaned up temporary directory: {temp_dir}")

@pytest.mark.asyncio
async def test_set(setup_temp_db):
    
    # Create a user
    await mipy_config.set(
        key="John Doe pass",
        value="hashed_password123"
    )

if __name__ == "__main__":
    import sys
    # Run pytest programmatically
    sys.exit(pytest.main(["-v", __file__]))