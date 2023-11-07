from base_binding import BaseBinding, UnexpectedBindingType
import pytest


def test_bind():
    # Test binding two objects
    obj1 = BaseBinding()
    obj2 = BaseBinding()
    obj1.bind(obj2)
    assert obj1.bindings[obj2.bindname][0] == obj2
    assert obj1.bindings[obj2.bindname][1] == obj1.bindname
    assert obj2.bindings[obj1.bindname][0] == obj1
    assert obj2.bindings[obj1.bindname][1] == obj2.bindname

    # Test check is_bound
    assert obj1.is_bound(obj2)
    assert obj2.is_bound(obj1)
    objx = BaseBinding()
    assert not obj1.is_bound(objx)
    assert not obj2.is_bound(objx)

    # Test binding a list of objects to another object
    obj3 = BaseBinding()
    obj4 = BaseBinding()
    obj5 = BaseBinding()
    obj6 = BaseBinding()
    obj3.bind([obj4, obj5, obj6])
    assert obj3.is_bound(obj4)
    assert obj3.is_bound(obj5)
    assert obj3.is_bound(obj6)
    assert obj4.is_bound(obj3)
    assert obj5.is_bound(obj3)
    assert obj6.is_bound(obj3)

    # Test binding an object to a specific key
    obj7 = BaseBinding()
    obj8 = BaseBinding()
    obj7.bind(obj8, obj_key="key1")
    assert obj7.bindings["key1"][0] == obj8
    assert obj7.bindings["key1"][1] == obj7.bindname
    assert obj7.is_bound(obj8, obj_key="key1")
    assert obj8.bindings[obj7.bindname][0] == obj7
    assert obj8.bindings[obj7.bindname][1] == "key1"
    assert obj8.is_bound(obj7)

def test_unbind():
    # Test unbinding two objects
    obj1 = BaseBinding()
    obj2 = BaseBinding()
    obj1.bind(obj2)
    obj1.unbind(obj2)
    assert obj1.bindings[obj2.bindname] is None
    assert obj2.bindings[obj1.bindname] is None

    # Test unbinding a list of objects from another object
    obj3 = BaseBinding()
    obj4 = BaseBinding()
    obj5 = BaseBinding()
    obj6 = BaseBinding()
    obj3.bind([obj4, obj5, obj6])
    obj3.unbind([obj4, obj5])
    assert obj3.is_bound(obj6)
    assert obj3.bindings[obj6.bindname] == [(obj6, obj3.bindname)]
    assert obj4.bindings[obj3.bindname] is None
    assert obj5.bindings[obj3.bindname] is None
    assert obj6.bindings[obj3.bindname][0] == obj3
    assert obj6.bindings[obj3.bindname][1] == obj6.bindname

    # Test unbinding an object from a specific key
    obj7 = BaseBinding()
    obj8 = BaseBinding()
    obj7.bind(obj8, obj_key="key1")
    obj7.unbind(obj_key="key1")
    assert obj7.bindings["key1"] is None
    assert obj8.bindings[obj7.bindname] is None

def test_bind_errors():
    # Test binding an unexpected type
    obj1 = BaseBinding()
    with pytest.raises(UnexpectedBindingType):
        obj1.bind("not a BaseBinding object")

    # Test binding a list with no BaseBinding objects
    obj2 = BaseBinding()
    obj3 = BaseBinding()
    with pytest.raises(Exception):
        obj2.bind([1, 2, 3])
    with pytest.raises(Exception):
        obj2.bind([obj3, 1, 2, 3])

def test_unbind_errors():
    # Test unbinding an object that is not bound
    obj1 = BaseBinding()
    obj2 = BaseBinding()
    with pytest.raises(Exception):
        obj1.unbind(obj2)

    # Test unbinding a key that does not exist
    obj3 = BaseBinding()
    with pytest.raises(Exception):
        obj3.unbind(obj_key="key1")



if __name__ == "__main__":
    test_bind()
    test_unbind()
    test_bind_errors()
    test_unbind_errors()
    print("All tests passed!")