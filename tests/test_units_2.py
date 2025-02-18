import unittest
from dotenv import load_dotenv
from os import getenv
from random import randint, choice, random
from string import ascii_letters, digits
from sys import path as sys_path
from time import sleep

sys_path.append('../')
from src.client import PyRedis

load_dotenv('../src/redis.env')  # Load environment variables from redis.env file
redis_psw: str = getenv('REDIS_PSW')
redis_db: int = int(getenv('REDIS_DB') or 0)
redis_host: str = getenv('REDIS_HOST') or 'localhost'
redis_port: int = int(getenv('REDIS_PORT') or 6379)
redis_username: str = getenv('REDIS_USERNAME') or 'default'


class TtlTests(unittest.TestCase):
	"""
	Tests to check the service life of keys, the sleep() function will be used,
	so the tests are run in parallel on all processor cores

	!!! Warning: Timings for the sleep function are always greater than the key lifetime -
	this is done to eliminate errors when calculating the key lifetime when
	writing to Redis and the start of the sleep() function count in Python
	"""
	# def setUp(self):
	# 	self.maxDiff = None

	r = PyRedis(
		host=redis_host,
		port=redis_port,
		password=redis_psw,
		username=redis_username,
		db=redis_db
	)

	@staticmethod
	def get_random_integer(_min: int = 0, _max: int = 100):
		return randint(0, 100)

	@staticmethod
	def get_random_string(length: int = randint(5, 10)):
		return ''.join(choice(ascii_letters + digits) for _ in range(length))

	def test_ping(self):
		""" Service is available """
		self.assertTrue(TtlTests.r.r_ping())

	# set_get_ttl  #####################################################################################################

	def test_set_get_ttl_str_001(self):
		key: str = 'set_get_str_001'
		value: str = TtlTests.get_random_string()
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=5))
		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(res_1, value)
		sleep(10)
		res_2: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_2, f'res = {res_2}')

	def test_set_get_ttl_str_002(self):
		key: str = 'set_get_str_002'
		value: str = TtlTests.get_random_string()
		self.assertIsNone(TtlTests.r.r_set(key, value, time_ms=10_000))
		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(res_1, value)
		sleep(20)
		res_2: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_2, f'res = {res_2}')

	def test_set_get_ttl_str_003(self):
		key: str = 'set_get_str_003'
		value: str = TtlTests.get_random_string()
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=3, time_ms=100_000))
		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(res_1, value)
		sleep(5)
		res_2: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_2, f'res = {res_2}')

	def test_set_get_ttl_str_004(self):
		key: str = 'set_get_str_004'
		value: str = TtlTests.get_random_string()
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=10000, time_ms=5_000))
		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(res_1, value)
		sleep(10)
		res_2: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_2, f'res = {res_2}')

	def test_set_get_ttl_str_005(self):
		key: str = 'set_get_str_005'
		value: str = TtlTests.get_random_string()
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=1, time_ms=1_000_000))
		sleep(3)
		res: None = TtlTests.r.r_get(key)
		self.assertIsNone(res, f'res = {res}')

	def test_set_get_ttl_int_001(self):
		key: str = 'set_get_int_001'
		value: int = TtlTests.get_random_integer()
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=10, time_ms=100))
		sleep(1)
		res: None = TtlTests.r.r_get(key)
		self.assertIsNone(res, f'res = {res}')

	def test_set_get_ttl_int_002(self):
		key: str = 'set_get_int_002'
		value: int = TtlTests.get_random_integer()
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=15))
		res_1: str = TtlTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res_1, value)
		sleep(5)
		res_2: str = TtlTests.r.r_get(key, convert_to_type='integer')
		self.assertEqual(res_2, value)
		sleep(15)
		res_3: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_3, f'res = {res_2}')

	def test_set_get_ttl_float_001(self):
		key: str = 'set_get_float_001'
		value: float = random()
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=5))
		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(res_1, str(value))
		sleep(10)
		res_2: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_2, f'res = {res_2}')

	def test_set_get_ttl_float_002(self):
		key: str = 'set_get_float_002'
		value: float = random()
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=20))
		res_1: str = TtlTests.r.r_get(key, convert_to_type='numeric')
		self.assertEqual(res_1, value)
		sleep(10)
		res_2: str = TtlTests.r.r_get(key, convert_to_type='double')
		self.assertEqual(res_2, value)
		sleep(15)
		res_3: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_3, f'res = {res_2}')

	def test_set_get_ttl_bool_001(self):
		key: str = 'set_get_bool_001'
		value: bool = bool(randint(0, 1))
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=10))
		res_1: str = TtlTests.r.r_get(key, convert_to_type='boolean')
		self.assertEqual(res_1, value)
		sleep(15)
		res_2: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_2, f'res = {res_2}')

	def test_set_get_ttl_bool_002(self):
		key: str = 'set_get_bool_002'
		value: bool = bool(randint(0, 1))
		self.assertIsNone(TtlTests.r.r_set(key, value, time_ms=10))
		sleep(1)
		res: None = TtlTests.r.r_get(key)
		self.assertIsNone(res, f'res = {res}')

	def test_set_get_ttl_list_001(self):
		key: str = 'set_get_list_001'
		value: list[str] = [TtlTests.get_random_string() for _ in range(randint(10, 20))]
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=10))
		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(res_1, value)
		sleep(15)
		res_2: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_2, f'res = {res_2}')

	def test_set_get_ttl_list_002(self):
		key: str = 'set_get_list_002'
		value: list[str] = [TtlTests.get_random_string() for _ in range(randint(10, 20))]
		self.assertIsNone(TtlTests.r.r_set(key, value, time_ms=10))
		sleep(1)
		res: None = TtlTests.r.r_get(key)
		self.assertIsNone(res, f'res = {res}')

	def test_set_get_ttl_tuple_001(self):
		key: str = 'set_get_tuple_001'
		value: tuple[str, ...] = tuple([TtlTests.get_random_string() for _ in range(randint(10, 20))])
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=15, time_ms=50_000))

		sleep(1)
		res_1: tuple[str, ...] = tuple(TtlTests.r.r_get(key))
		self.assertEqual(res_1, value)

		sleep(20)
		res_2: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_2, f'res = {res_2}')

	def test_set_get_ttl_tuple_002(self):
		key: str = 'set_get_tuple_002'
		value: tuple[float, ...] = tuple([random() for _ in range(randint(10, 20))])
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=5))

		sleep(10)
		res: None = TtlTests.r.r_get(key, convert_to_type='float')
		self.assertIsNone(res, f'res = {res}')

	def test_set_get_ttl_set_001(self):
		key: str = 'set_get_set_001'
		value: set[float] = {random() for _ in range(randint(10, 20))}
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=15, time_ms=5_000_000))

		sleep(5)
		res_1: set[float] = set(TtlTests.r.r_get(key, convert_to_type='float'))
		self.assertEqual(res_1, value)

		sleep(15)
		res_2: None = TtlTests.r.r_get(key)  # without convert_to_type
		self.assertIsNone(res_2, f'res = {res_2}')
		res_3: None = TtlTests.r.r_get(key, convert_to_type='float')
		self.assertIsNone(res_3, f'res = {res_3}')

	def test_set_get_ttl_set_002(self):
		key: str = 'set_get_set_001'
		value: set[str] = {TtlTests.get_random_string() for _ in range(randint(10, 20))}
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=1))

		sleep(5)
		res_1: None = TtlTests.r.r_get(key)  # without convert_to_type
		self.assertIsNone(res_1, f'res = {res_1}')
		res_2: None = TtlTests.r.r_get(key, convert_to_type='integer')  # wrong type
		self.assertIsNone(res_2, f'res = {res_2}')

	# set_key_ttl ##################################################################################################

	def test_set_key_ttl_001(self):
		key: str = 'set_key_ttl_001'
		value: str = TtlTests.get_random_string()
		TtlTests.r.r_set(key, value)

		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(value, res_1)

		TtlTests.r.set_key_ttl(key, ttl_sec=5)
		res_2: str = TtlTests.r.r_get(key)
		self.assertEqual(value, res_2)

		sleep(10)
		self.assertIsNone(TtlTests.r.r_get(key))

	def test_set_key_ttl_002(self):
		key: str = 'set_key_ttl_002'
		value: str = TtlTests.get_random_string()
		TtlTests.r.r_set(key, value)

		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(value, res_1)

		TtlTests.r.set_key_ttl(key, ttl_ms=10_000)
		res_2: str = TtlTests.r.r_get(key)
		self.assertEqual(value, res_2)

		sleep(15)
		self.assertIsNone(TtlTests.r.r_get(key))

	def test_set_key_ttl_003(self):
		key: str = 'set_key_ttl_003'
		value: str = TtlTests.get_random_string()
		TtlTests.r.r_set(key, value)

		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(value, res_1)

		TtlTests.r.set_key_ttl(key, ttl_ms=50_000, ttl_sec=5)
		res_2: str = TtlTests.r.r_get(key)
		self.assertEqual(value, res_2)

		sleep(10)
		self.assertIsNone(TtlTests.r.r_get(key))

	# set_keys_ttl #####################################################################################################

	def test_set_keys_ttl_001(self):
		""" List - 001 - 009 """
		keys: list = [f'set_keys_ttl_00{i}' for i in range(1, 10)]
		for key in keys:
			TtlTests.r.r_set(key, key)

		for key in keys:
			self.assertEqual(TtlTests.r.r_get(key), key)

		TtlTests.r.set_keys_ttl(keys, ttl_sec=1)

		sleep(3)

		for key in keys:
			self.assertIsNone(TtlTests.r.r_get(key))

	def test_set_keys_ttl_002(self):
		""" List - 011 - 019 """
		keys: list = [f'set_keys_ttl_01{i}' for i in range(1, 10)]
		for key in keys:
			TtlTests.r.r_set(key, key)

		for key in keys:
			self.assertEqual(TtlTests.r.r_get(key), key)

		TtlTests.r.set_keys_ttl(keys, ttl_ms=5_000)

		sleep(10)

		for key in keys:
			self.assertIsNone(TtlTests.r.r_get(key))

	def test_set_keys_ttl_003(self):
		""" List - 021 - 029 """
		keys: list = [f'set_keys_ttl_02{i}' for i in range(1, 10)]
		for key in keys:
			TtlTests.r.r_set(key, key)

		for key in keys:
			self.assertEqual(TtlTests.r.r_get(key), key)

		TtlTests.r.set_keys_ttl(keys, ttl_ms=5_000, ttl_sec=1_000)

		sleep(10)

		for key in keys:
			self.assertIsNone(TtlTests.r.r_get(key))

	def test_set_keys_ttl_004(self):
		""" Tuple - 031 - 039 """
		keys: tuple = tuple([f'set_keys_ttl_03{i}' for i in range(1, 10)])
		for key in keys:
			TtlTests.r.r_set(key, key)

		for key in keys:
			self.assertEqual(TtlTests.r.r_get(key), key)

		TtlTests.r.set_keys_ttl(keys, ttl_ms=5_000)

		sleep(10)

		for key in keys:
			self.assertIsNone(TtlTests.r.r_get(key))

	def test_set_keys_ttl_005(self):
		""" Set - 041 - 049 """
		keys: set = set([f'set_keys_ttl_04{i}' for i in range(1, 10)])
		for key in keys:
			TtlTests.r.r_set(key, key)

		for key in keys:
			self.assertEqual(TtlTests.r.r_get(key), key)

		TtlTests.r.set_keys_ttl(keys, ttl_ms=5_000)

		sleep(10)

		for key in keys:
			self.assertIsNone(TtlTests.r.r_get(key))

	def test_set_keys_ttl_006(self):
		""" Frozenset - 051 - 059 """
		keys: frozenset = frozenset([f'set_keys_ttl_05{i}' for i in range(1, 10)])
		for key in keys:
			TtlTests.r.r_set(key, key)

		for key in keys:
			self.assertEqual(TtlTests.r.r_get(key), key)

		TtlTests.r.set_keys_ttl(keys, ttl_ms=5_000)

		sleep(10)

		for key in keys:
			self.assertIsNone(TtlTests.r.r_get(key))

	def test_set_keys_ttl_007(self):
		""" List - 061 - 069 """
		keys: list = [f'set_keys_ttl_06{i}' for i in range(1, 10)]
		for key in keys:
			TtlTests.r.r_set(key, key)

		for key in keys:
			self.assertEqual(TtlTests.r.r_get(key), key)

		TtlTests.r.set_keys_ttl(keys)

		sleep(15)

		for key in keys:
			self.assertEqual(TtlTests.r.r_get(key), key)

	def test_set_keys_ttl_008(self):
		""" List - 071 - 079 """
		keys: list = [f'set_keys_ttl_07{i}' for i in range(1, 10)]
		for key in keys:
			if int(key[-1]) % 2 == 0:
				TtlTests.r.r_set(key, key)
			else:
				TtlTests.r.r_set(key, [key])

		for key in keys:
			if int(key[-1]) % 2 == 0:
				self.assertEqual(TtlTests.r.r_get(key), key)
			else:
				self.assertEqual(TtlTests.r.r_get(key), [key])

		TtlTests.r.set_keys_ttl(keys, ttl_ms=None, ttl_sec=1)

		sleep(5)

		for key in keys:
			self.assertIsNone(TtlTests.r.r_get(key))

	def test_set_keys_ttl_009(self):
		""" List - 081 - 089 + unknown keys """
		keys: list = [f'set_keys_ttl_08{i}' for i in range(1, 10)]
		for key in keys:
			TtlTests.r.r_set(key, key)

		for key in keys:
			self.assertEqual(TtlTests.r.r_get(key), key)

		keys.extend([TtlTests.get_random_string() for _ in range(randint(5, 10))])
		TtlTests.r.set_keys_ttl(keys, ttl_ms=5_000, ttl_sec=None)

		sleep(10)

		for key in keys:
			self.assertIsNone(TtlTests.r.r_get(key))

	# get_key_ttl ######################################################################################################

	# TODO

	# drop_key_ttl #####################################################################################################

	def test_drop_key_ttl_001(self):
		key: str = 'drop_key_ttl_001'
		value: str = TtlTests.get_random_string()
		TtlTests.r.r_set(key, value)

		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(value, res_1)

		TtlTests.r.set_key_ttl(key, ttl_ms=15_000)
		res_2: str = TtlTests.r.r_get(key)
		self.assertEqual(value, res_2)

		TtlTests.r.drop_key_ttl(key)
		sleep(20)
		res_3: str = TtlTests.r.r_get(key)
		self.assertEqual(value, res_3)

	def test_drop_key_ttl_002(self):
		key: str = 'drop_key_ttl_002'
		value: str = TtlTests.get_random_string()
		TtlTests.r.r_set(key, value)

		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(value, res_1)

		TtlTests.r.set_key_ttl(key, ttl_sec=10)
		res_2: str = TtlTests.r.r_get(key)
		self.assertEqual(value, res_2)

		TtlTests.r.drop_key_ttl(key)
		sleep(15)
		res_3: str = TtlTests.r.r_get(key)
		self.assertEqual(value, res_3)

	def test_drop_key_ttl_003(self):
		key: str = 'drop_key_ttl_003'
		value: str = TtlTests.get_random_string()
		TtlTests.r.r_set(key, value)

		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(value, res_1)

		TtlTests.r.set_key_ttl(key, ttl_sec=10)
		res_2: str = TtlTests.r.r_get(key)
		self.assertEqual(value, res_2)

		TtlTests.r.drop_key_ttl('')  # unknown key
		sleep(20)
		self.assertIsNone(TtlTests.r.r_get(key))

	def test_drop_key_ttl_004(self):
		""" drop ttl without ttl for key """
		key: str = 'drop_key_ttl_004'
		value: str = TtlTests.get_random_string()
		TtlTests.r.r_set(key, value)

		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(value, res_1)

		TtlTests.r.set_key_ttl(key)
		res_2: str = TtlTests.r.r_get(key)
		self.assertEqual(value, res_2)

		TtlTests.r.drop_key_ttl(key)
		sleep(10)
		res_3: str = TtlTests.r.r_get(key)
		self.assertEqual(value, res_3)

	# drop_keys_ttl ####################################################################################################

	# TODO


if __name__ == '__main__':
	from redis import Redis, ConnectionPool
	_redis = Redis(connection_pool=ConnectionPool(
		host=redis_host,port=redis_port,db=0,password=redis_psw, username=redis_username
	))
	_redis.flushall()  # clear the database before tests
