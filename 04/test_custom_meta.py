import pytest

from custom_meta import CustomMeta


@pytest.fixture(name='test_class')
def fixture_test_class():
    class CustomClass(
        metaclass=CustomMeta):  # pylint: disable=redefined-outer-name
        x = 50

        def __init__(self, val=99):
            self.val = val

        def line(self):
            return 100

        def __str__(self):
            return "Custom_by_metaclass"

        @classmethod
        def get_cls_name(cls):
            return cls.__name__

    return CustomClass


def test_get_cls_attr(test_class):
    assert test_class.custom_x == 50
    with pytest.raises(AttributeError):
        test_class.x # pylint: disable=pointless-statement

    assert test_class.custom_get_cls_name() == 'CustomClass'
    with pytest.raises(AttributeError):
        test_class.get_cls_name()


def test_set_cls_attr(test_class):
    test_class.dinamic = 10
    assert test_class.custom_dinamic == 10
    with pytest.raises(AttributeError):
        test_class.dinamic # pylint: disable=pointless-statement


def test_get_inst_attr(test_class):
    inst = test_class()
    assert inst.custom_x == 50
    assert inst.custom_val == 99
    assert inst.custom_line() == 100
    assert str(inst) == "Custom_by_metaclass"
    with pytest.raises(AttributeError):
        inst.x # pylint: disable=pointless-statement
    with pytest.raises(AttributeError):
        inst.val # pylint: disable=pointless-statement
    with pytest.raises(AttributeError):
        inst.line()
    with pytest.raises(AttributeError):
        inst.yyy # pylint: disable=pointless-statement


def test_set_inst_attr(test_class):
    inst = test_class()
    inst.dynamic = "added later"  # pylint: disable=attribute-defined-outside-init
    assert inst.custom_dynamic == "added later"
    with pytest.raises(AttributeError):
        inst.dynamic # pylint: disable=pointless-statement


def test_change_cls_attr(test_class):
    test_class.custom_x = 100
    assert test_class.custom_x == 100

    with pytest.raises(AttributeError):
        test_class.x = 99


def test_change_inst_attr(test_class):
    inst = test_class()
    inst.custom_val = 100  # pylint: disable=attribute-defined-outside-init
    assert inst.custom_val == 100

    with pytest.raises(AttributeError):
        inst.val = 99  # pylint: disable=attribute-defined-outside-init
