import collections
import json
'''
Test Data
'''
#with open("C:\\Users\\Moritz\\Documents\\biglist.txt") as f:
database = [[1,2],[3,8]]

fetch = [[1,2], [2,3]]

def l2set(lst_lst):
	'''
	This method is a helper to convert a list of lists into 
	a set of tuples since these are more efficient to compare.
	'''
	n_set = set()
	for entry in lst_lst:
		n_set.add(tuple(entry))
	return n_set

def set2l(set_tpl):
	'''
	This method is a helper to convert a set of tuples 'set_tpl' to a list of
	lists. It then returns the converted list.
	'''
	n_lst = []
	for entry in set_tpl:
		n_lst.append(list(entry))
	return n_lst

def unify_fetch1(dbl, fl):
	'''
	INEFFICIENT
	This method returns all the items	of lst1 which are not present in
	lst2. Thus lst1 represents the fetched data of a response and lst2
	represents the data objects stored in the database. The result is
	returned as a list of lists.
	'''
	dupe_free_fl, dupe_free_all = [],[]
	dupe_free_set_fl, dupe_free_set_all = set(), set()
	dupes_fetch, dupes_db = [],[]
	for x in fl:
		if tuple(x) not in dupe_free_set_fl:
			dupe_free_fl.append(x)
			dupe_free_set_fl.add(tuple(x))
		else:
			dupes_fetch.append(x)
	for x in dupe_free_fl + dbl:
		if tuple(x) not in dupe_free_set_all:
			dupe_free_all.append(x)
			dupe_free_set_all.add(tuple(x))
		else:
			dupes_db.append(x)
	s = set()
	for x in database:
		s.add(tuple(x))
	differences = dupe_free_set_all - s
	return set2l(differences)

def unify_fetch2(lst1, lst2):
	'''
	This method returns all the items	of lst1 which are not present in
	lst2. Thus lst1 represents the fetched data of a response and lst2
	represents the data objects stored in the database. The result is
	returned as a list of lists.
	'''
	differences = l2set(lst1).difference(l2set(lst2))
	return set2l(differences)

testdata1 = (unify_fetch2(fetch, database))