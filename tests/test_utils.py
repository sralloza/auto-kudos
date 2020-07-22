from strava_api.utils import MetaSingleton


def test_meta_singleton():
    class Test1(metaclass=MetaSingleton):
        pass

    class Test2:
        pass

    t1a = Test1()
    t1b = Test1()
    t2a = Test2()
    t2b = Test2()

    assert t1a is t1b
    assert t2a is not t2b
