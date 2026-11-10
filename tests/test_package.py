import shooter


def test_package_exports_main():
    assert callable(shooter.main)
    assert hasattr(shooter, "App")
