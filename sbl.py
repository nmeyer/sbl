#!/usr/bin/env python
# encoding: utf-8
"""
sbl.py

Created by Nicholas Meyer on 2004-01-13.
Copyright (c) 2004 __Nicholas Meyer__. All rights reserved.

Simple Brainstorming Language

A simple language designed for brainstorming and
the organization of thoughts. The purpose of 
SBL is to aid in prioritization of goals by 
visualizing their relationships.

The core unit of SBL is the Goal. 
A single goal may have dependencies (Goals that must be
met in order to meet this goal) and results (Goals that are
triggered by the completion of this goal).
"""

import sys
import os

class Goal():
	"""
	Class containing prerequisites and results of a goal
	"""
	def __init__(self, label):
		self.label = label
		self.deps = {}
		self.results = {}
		
	def add_dependency(self, Goal):
		"""Define a pre-requisite for this goal."""
		if not Goal.label in self.deps:
			self.deps[Goal.label] = Goal
		
	def add_result(self, Goal):
		"""Define a result of this Goal"""
		if not Goal.label in self.results:
			self.results[Goal.label] = Goal
	
	def show_state(self, indent_level=0):
		if indent_level == 0:
			print "\t%s (" % self.label,
			for dep in self.deps.values():
				print dep.label,
			print ") :"
		# print results of goal nested
		for res in self.results.values():
			indent = "\t" * (indent_level + 2)
			print "%s-->%s" % (indent, res.label)
			res.show_state(indent_level + 1)
	
	def __str__(self):
		return self.label
			
class Interpreter():
	"""
	Class responsible for parsing and interpretation of SBL
	"""
	def __init__(self, input=None):
		if input is None:
			self.input = []
		else:
			self.input = input
		self.rules  = []
		self.goals = {}
	
	def parse(self, input):
		"""
		Parse input into SBL rule format.
		returns an instance of Rule
		"""
		input = input.lower()
		for verb in ['results in', 'depends on']:
			try:
				sub, pred = input.split(verb)
				return Rule(sub.strip(), verb.strip(), pred.strip())
			except:
				continue
		print "Invalid input: %s" % (input)
		return None

		
	def process_rule(self, rule):
		"""
		Process rule. Create goals as necessary and establishes
		relationships between goals based on properties of rule.
		"""
		if rule is None:
			return
		if not rule.is_valid:
			return
		sub = self.get_goal(rule.subject)
		pred = self.get_goal(rule.predicate)
		if rule.verb == "results in":
			sub.add_result(pred)
		elif rule.verb == "depends on":
			sub.add_dependency(pred)
		else:
			print "Unable to process rule"
			return None
		self.rules.append(rule)
		return rule
			
		
	def get_goal(self, label):
		"""Get Goal corresponding to label. Create Goal if does not exist."""
		try:
			goal = self.goals[label]
		except:
			goal = Goal(label)
			self.goals[label] = goal
		return goal
		
	def run(self):
		while len(self.input) > 0:
			input = self.input.pop(0)
			rule = self.parse(input)
			if rule is None:
				continue
			self.process_rule(rule)
			
	def show_state(self):
		"""Print current state of interpreter"""
		print "--- Interpreter State ---"
		print "Rules:"
		for rule in self.rules:
			print "\t", rule
		print "Goals:"
		# print each goal with dependencies in ()
		for goal in self.goals.values():
			goal.show_state()
			
		
class Rule():
	"""
	Representation of an SBL Rule.
	
	An SBL rule consists of:
	- SUBJECT ( depends on | results in ) (number (more | less)) PREDICATE
	OR
	- SUBJECT as objective
	
	Example:
	In the input "BETTER RECOMMENDATIONS depends on RECOMMENDATION ENGINE"
	"BETTER RECOMMENDATIONS" is the subject, "DEPENDS ON" is the verbal phrase,
	and "RECOMMENDATION ENGINE" is the predicate, accuracy regarding 
	english grammer	not withstanding.
	"""
	def __init__(self, subject, verb, predicate):
		self.subject = subject.lower().strip()
		self.verb = verb.lower().strip()
		self.predicate = predicate.lower().strip()
		
	def is_valid(self):
		"""Tests this rule for validity."""
		if self.subject is None:
			return False
		if self.predicate is None:
			return False
		if self.verb not in ['depends on', 'results in']:
			return False
		return True
		
	def __str__(self):
		return "%s, %s, %s" % (self.subject, self.verb, self.predicate)

def main():
	input = [
		"better recommendations depends on recommendation engine",
		"music sales depends on ecommerce platform",
		"music sales results in revenue",
		"page views results in ad views",
		"ad views results in revenue",
		"users results in page views",
		"better recommendations results in music sales",
		"merchandise sales results in revenue",
		"merchandise sales depends on ecommerce platform",
		"advertise local events results in ticket sales",
		"ticket sales depends on ticketing platform",
		"ticketing platform depends on ecommerce platform",
		"users results in more playlists"
	]
	interpreter = Interpreter(input)
	interpreter.run()
	interpreter.show_state()

if __name__ == '__main__':
	main()

