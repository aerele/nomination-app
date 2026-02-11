# Copyright (c) 2026, Aerele Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

# Multiplication table
D_TABLE = [
	[0,1,2,3,4,5,6,7,8,9],
	[1,2,3,4,0,6,7,8,9,5],
	[2,3,4,0,1,7,8,9,5,6],
	[3,4,0,1,2,8,9,5,6,7],
	[4,0,1,2,3,9,5,6,7,8],
	[5,9,8,7,6,0,4,3,2,1],
	[6,5,9,8,7,1,0,4,3,2],
	[7,6,5,9,8,2,1,0,4,3],
	[8,7,6,5,9,3,2,1,0,4],
	[9,8,7,6,5,4,3,2,1,0]
]

# Permutation table
P_TABLE = [
	[0,1,2,3,4,5,6,7,8,9],
	[1,5,7,6,2,8,3,0,9,4],
	[5,8,0,3,7,9,6,1,4,2],
	[8,9,1,6,0,4,3,5,2,7],
	[9,4,5,3,1,2,6,8,7,0],
	[4,2,8,6,5,7,3,9,0,1],
	[2,7,9,3,8,0,6,4,1,5],
	[7,0,4,6,9,1,3,2,5,8]
]

class NominationForm(Document):
	def validate(self):
		self.validate_aadhaar_number()
		self.validate_pan_number()

	def validate_aadhaar_number(self):
		if not self.aadhaar_number.isdigit() or len(self.aadhaar_number) != 12:
			frappe.throw("Aadhaar Number must be a 12-digit numeric value")
		
		c = 0
		for i, digit in enumerate(reversed(self.aadhaar_number)):
			c = D_TABLE[c][P_TABLE[i % 8][int(digit)]]

		if c != 0:
			frappe.throw("Aadhaar Number is invalid")
	
	def validate_pan_number(self):
		pan_no = self.pan_number.strip().upper()
		name = self.full_name.strip().upper()

		pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
		valid_types = ['A','B','C','F','G','H','L','J','P','T']

		if len(pan_no) != 10:
			frappe.throw( "Invalid PAN Number")

		if not pan_no[3] in  valid_types:
			frappe.throw("Invalid PAN Holder type") 

		if not re.match(pattern, pan_no):
			frappe.throw( "Invalid PAN format")

		if pan_no[4] != name[0]:
			frappe.throw ( "PAN number's 5th character must match the first letter of the full name")
