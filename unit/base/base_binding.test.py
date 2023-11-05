import unittest
from base_binding import BaseBinding

class TestBaseBinding(unittest.TestCase):
    def setUp(self):
        self.obj1 = BaseBinding()
        self.obj2 = BaseBinding()
        self.obj3 = BaseBinding()
        self.obj4 = BaseBinding()
        self.obj5 = BaseBinding()
        self.obj6 = BaseBinding()
        self.obj7 = BaseBinding()
        self.obj8 = BaseBinding()
        self.obj9 = BaseBinding()
        self.obj10 = BaseBinding()
        self.obj11 = BaseBinding()
        self.obj12 = BaseBinding()
        self.obj13 = BaseBinding()
        self.obj14 = BaseBinding()
        self.obj15 = BaseBinding()
        self.obj16 = BaseBinding()
        self.obj17 = BaseBinding()
        self.obj18 = BaseBinding()
        self.obj19 = BaseBinding()
        self.obj20 = BaseBinding()

    def test_bind(self):
        # Test binding two objects
        self.obj1.bind(obj=self.obj2)
        self.assertEqual(self.obj1.bindings['bindname'], self.obj2)
        self.assertEqual(self.obj2.bindings['bindname'], self.obj1)

        # Test binding a list of objects
        self.obj3.bind(obj=[self.obj4, self.obj5])
        self.assertEqual(self.obj3.bindings['bindname'], [self.obj4, self.obj5])
        self.assertEqual(self.obj4.bindings['bindname'], self.obj3)
        self.assertEqual(self.obj5.bindings['bindname'], self.obj3)

        # Test binding an object with a key
        self.obj6.bind(obj=self.obj7, key='key1')
        self.assertEqual(self.obj6.bindings['key1'], self.obj7)
        self.assertEqual(self.obj7.bindings['bindname'], self.obj6)

        # Test binding a list of objects with a key
        self.obj8.bind(obj=[self.obj9, self.obj10], key='key2')
        self.assertEqual(self.obj8.bindings['key2'], [self.obj9, self.obj10])
        self.assertEqual(self.obj9.bindings['bindname'], self.obj8)
        self.assertEqual(self.obj10.bindings['bindname'], self.obj8)

        # Test binding an object with a key that already exists that will be replaced
        self.obj11.bind(obj=self.obj12, key='key3')
        self.obj11.bind(obj=self.obj13, key='key3')
        self.assertEqual(self.obj11.bindings['key3'], self.obj13)
        self.assertEqual(self.obj13.bindings['bindname'], self.obj11)
        self.assertIsNone(self.obj12.bindings['bindname'])

        # Test binding a list of objects with a key list that already exists
        self.obj14.bind(obj=[self.obj15, self.obj16], key='key4')
        self.obj14.bind(obj=[self.obj17, self.obj18], key='key4')
        self.assertEqual(self.obj14.bindings['key4'], [self.obj15, self.obj16, self.obj17, self.obj18])

        # Test binding a list of objects with a key not list that already exists
        self.obj19.bind(obj=self.obj20, key='key5')
        self.obj19.bind(obj=[self.obj20], key='key5')
        self.assertEqual(self.obj19.bindings['key5'], [self.obj20])

        # Test binding an object with an unexpected type
        with self.assertRaises(Exception):
            self.obj16.bind(obj='not a BaseBinding object')

        # Test binding a list with an unexpected type
        with self.assertRaises(Exception):
            self.obj17.bind(obj=['not a BaseBinding object'])

    def test_unbind(self):
        # Test unbinding two objects
        self.obj1.bind(obj=self.obj2)
        self.obj1.unbind()
        self.assertIsNone(self.obj1.bindings['bindname'])
        self.assertIsNone(self.obj2.bindings['bindname'])

        # Test unbinding a list of objects
        self.obj3.bind(obj=[self.obj4, self.obj5])
        self.obj3.unbind()
        self.assertIsNone(self.obj3.bindings['bindname'])
        self.assertIsNone(self.obj4.bindings['bindname'])
        self.assertIsNone(self.obj5.bindings['bindname'])

        # Test unbinding an object with a key
        self.obj6.bind(obj=self.obj7, key='key1')
        self.obj6.unbind(key='key1')
        self.assertIsNone(self.obj6.bindings['key1'])
        self.assertIsNone(self.obj7.bindings['bindname'])

        # Test unbinding a list of objects with a key
        self.obj8.bind(obj=[self.obj9, self.obj10], key='key2')
        self.obj8.unbind(key='key2')
        self.assertIsNone(self.obj8.bindings['key2'])
        self.assertIsNone(self.obj9.bindings['bindname'])
        self.assertIsNone(self.obj10.bindings['bindname'])

        # Test unbinding an object with an unexpected type
        with self.assertRaises(Exception):
            self.obj16.unbind(obj='not a BaseBinding object')

        # Test unbinding a list with an unexpected type
        with self.assertRaises(Exception):
            self.obj17.unbind(obj=['not a BaseBinding object'])

    def test_reverse_unbind(self):
        # Test reverse unbinding an object
        self.obj1.bind(obj=self.obj2)
        self.obj1.reverse_unbind(key='bindname', obj=self.obj2)
        self.assertIsNone(self.obj1.bindings['bindname'])
        self.assertEqual(self.obj2.bindings['bindname'], self.obj1)
        self.obj2.reverse_unbind(key='bindname', obj=self.obj1) # Unbind the object again to prevent errors in other tests

        # Test reverse unbinding an object from a list
        self.obj3.bind(obj=[self.obj4, self.obj5])
        self.obj3.reverse_unbind(key='bindname', obj=self.obj4)
        self.assertEqual(self.obj3.bindings['bindname'], [self.obj5])
        self.assertEqual(self.obj4.bindings['bindname'], self.obj3)
        self.assertEqual(self.obj5.bindings['bindname'], self.obj3)
        self.obj4.reverse_unbind(key='bindname', obj=self.obj3) # Unbind the object again to prevent errors in other tests

        # Test reverse unbinding an object with an unexpected type
        with self.assertRaises(Exception):
            self.obj16.reverse_unbind(obj='not a BaseBinding object')

    def test_del(self):
        # Test deleting an object
        print(self.obj2.bindings)
        self.obj1.bind(obj=self.obj2)
        self.obj1.unbind()
        print(self.obj2.bindings)
        del self.obj1
        print(self.obj2.bindings)
        self.assertIsNone(self.obj2.bindings['bindname'])

        # Test deleting an object with a key
        self.obj6.bind(obj=self.obj7, key='key1')
        del self.obj6
        self.assertIsNone(self.obj7.bindings['bindname'])

        # Test deleting an object with a list of objects
        self.obj8.bind(obj=[self.obj9, self.obj10], key='key2')
        del self.obj8
        self.assertIsNone(self.obj9.bindings['bindname'])
        self.assertIsNone(self.obj10.bindings['bindname'])


if __name__ == '__main__':
    unittest.main()