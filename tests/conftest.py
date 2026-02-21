import pytest

EXPECTED_ROADMAP_VERSION = "2c1367e2"


@pytest.fixture(autouse=True)
def inject_roadmap_version(request):
    """Make the expected roadmap version available as self.version_existing_roadmap."""
    if request.instance is not None:
        request.instance.version_existing_roadmap = EXPECTED_ROADMAP_VERSION
