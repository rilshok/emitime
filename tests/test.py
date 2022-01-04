from emitime.date import Day
from emitime.time import Atomic, Days, Hours, Minutes, Seconds, Time, asatomic
import unittest
from datetime import timedelta as py_timedelta

# AnyTime = Union[float, str, py_timedelta, 'Atomic', 'Days', 'Hours', 'Minutes', 'Seconds']

class TestAtomic(unittest.TestCase):

    def test_init(self):
        # """[D-]HH:MM[:SS][.MS]"""
        t1 = Atomic('00:01:00')
        t2 = Atomic('01:00:00')
        t3 = Atomic('1-00:00:00')

        a1 = Atomic(60000)
        a2 = Atomic(3600000)
        a3 = Atomic(86400000)

        dt1 = py_timedelta(minutes=1)
        dt2 = py_timedelta(hours=1)
        dt3 = py_timedelta(days=1)

        v1 = Atomic(Minutes(1))
        v2 = Atomic(Hours(1))
        v3 = Atomic(Days(1))

        self.assertEqual(t1, a1)
        self.assertEqual(t2, a2)
        self.assertEqual(t3, a3)

        self.assertEqual(dt1, a1)
        self.assertEqual(dt2, a2)
        self.assertEqual(dt3, a3)


        self.assertEqual(v1, a1)
        self.assertEqual(v2, a2)
        self.assertEqual(v3, a3)

    def test_operation(self):
        v1 = Atomic('1-00:01')
        v2 = Atomic('01:00')
        self.assertEqual(v1 - v2, Atomic('23:01'))
        self.assertEqual(v1 + v2, Atomic('1-01:01'))
        self.assertEqual(v2 * 2,  7200000)
        self.assertEqual(v2 / 2, 1800000)
    
    def test_asatomic(self):
        a = asatomic(Hours(1), Minutes(1))
        b = Atomic('01:01')
        self.assertEqual(a,b)

        a = asatomic(Hours(1), Minutes(1), Seconds(1))
        b = Atomic('01:01:01')
        self.assertEqual(a,b)

class TestTime(unittest.TestCase):
    def test_init(self):
        t1 = Time('23:01:01')
        t2 = Time(Atomic((23*3600+1*60+1)*1000))
        self.assertEqual(t1,t2)
        
    def test_operation(self):
        t1 = Time('01:30:00')
        t2 = Time('02:23:59')
        t3 = t2 - t1
        self.assertEqual(t3, Atomic('00:53:59'))
        
if __name__ == '__main__':
    unittest.main()