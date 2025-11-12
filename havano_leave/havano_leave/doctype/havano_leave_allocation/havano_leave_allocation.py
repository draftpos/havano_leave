# Copyright (c) 2025, chirovemunyaradzi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class HavanoLeaveAllocation(Document):
	def before_save(self):
		# ✅ Convert string dates to date objects
		from_date = getdate(self.from_date)
		to_date = getdate(self.to_date)

		# ✅ Validate that To Date is not before From Date
		if to_date < from_date:
			frappe.throw("To Date cannot be before From Date.")

		# ✅ Calculate total number of leave days (include both start & end)
		days = (to_date - from_date).days + 1
		# days=2
		# ✅ Fetch leave type details
		leave_types = frappe.get_all(
		"Havano Leave Type",
		fields=["leave_type_name", "max_leaves_allowed"]
		)

		# Example: iterate through them
		for leave in leave_types:
			if  leave.leave_type_name == self.leave_type:
				self.update_leave_balance(self.employee,self.employee_name, leave.leave_type_name, days,leave.max_leaves_allowed)
			else:
				self.update_leave_balance(self.employee,self.employee_name, leave.leave_type_name, 0,leave.max_leaves_allowed)

	@frappe.whitelist()
	def update_leave_balance(self, name,employee_name, leave_type, days,max_days):
		# ✅ Get existing leave balance record
		existing_record = frappe.db.get_value(
			"Havano Leave Balances",
			{"employee_name": employee_name, "havano_leave_type": leave_type},
			["name", "leave_balance"],
			as_dict=True
		)

		if existing_record:
			# ✅ Update the balance
			new_balance = float(existing_record.leave_balance) - float(days)
			frappe.db.set_value("Havano Leave Balances", existing_record.name, "leave_balance", new_balance)
			if leave_type == "Annual Leave":
				# 1️⃣ Get current total leave taken for this employee (default 0)
				current_taken = frappe.db.get_value("havano_employee", name, "total_leave_taken") or 0

				# 2️⃣ Add the new leave days
				new_total = float(current_taken) + float(days)

				# 3️⃣ Update the employee record with the new total
				frappe.db.set_value("havano_employee", name, "total_leave_taken", new_total)
				frappe.db.commit()

		else:
			# ✅ Create new balance record
			new_doc = frappe.get_doc({
				"doctype": "Havano Leave Balances",
				"employee":name,
				"employee_name": employee_name,
				"havano_leave_type": leave_type,
				"leave_balance": float(max_days)
			})
			new_doc.insert(ignore_permissions=True)
			frappe.msgprint(f"Leave balance record created for {employee_name} with {days} days.")
