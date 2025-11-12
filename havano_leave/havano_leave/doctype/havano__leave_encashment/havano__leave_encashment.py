# Copyright (c) 2025, chirovemunyaradzi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class havano__leave_encashment(Document):

    def before_save(self):
        # Ensure days is set
        if not self.encashment_days:
            frappe.throw("Please enter the number of days to encash.")

        # Fetch the leave balance record
        balance_record = frappe.db.get_value(
            "havano_leave_balances",
            {
                "employee_name": self.employee_name,
                "havano_leave_type": self.leave_type
            },
            ["leave_balance"],
            as_dict=True
        )
        print(balance_record)

        if not balance_record:
            frappe.throw(f"No leave balance record found for {self.employee_name} and leave type {self.leave_type}.")

        # Check if days to encash exceed available balance
        if self.encashment_days > float(balance_record.leave_balance):
            frappe.throw(
                f"You cannot encash {self.encashment_days} days. Available balance is {balance_record['leave_balance']} days."
            )
        self.add_component()

    @frappe.whitelist()
    def add_component(self):
        emp_doc = frappe.get_doc("havano_employee", self.employee)

        # Append a new row to employee_earnings table
        emp_doc.append("employee_earnings", {
            "components": "Leave Encashment",
        })

        emp_doc.save()
        frappe.msgprint(f"Leave Encashment added to {emp_doc.employee_name}'s earnings.")