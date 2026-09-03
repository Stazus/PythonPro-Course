from app import get_version, health_check


def test_get_version():
    assert get_version() == "Lesson 17 - CI/CD VERSION 1"


def test_health_check():
    assert health_check() is True
