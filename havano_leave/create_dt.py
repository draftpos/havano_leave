import frappe

def create_doctype():
    if frappe.db.exists('DocType', 'Havano Leave Ledger Entry'):
        print('DocType already exists')
        return

    doc = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'Havano Leave Ledger Entry',
        'module': 'Havano Leave',
        'custom': 0,
        'is_submittable': 0,
        'naming_rule': 'Expression',
        'autoname': 'format:LLE-{employee}-{####}',
        'permissions': [{'role': 'System Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1}],
        'fields': [
            {'fieldname': 'employee', 'label': 'Employee', 'fieldtype': 'Link', 'options': 'havano_employee', 'reqd': 1, 'in_list_view': 1, 'in_standard_filter': 1},
            {'fieldname': 'posting_date', 'label': 'Posting Date', 'fieldtype': 'Date', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'transaction_type', 'label': 'Transaction Type', 'fieldtype': 'Select', 'options': '\nLeave Allocation\nLeave Application\nLeave Reversal\nStarting Balance', 'reqd': 1, 'in_list_view': 1, 'in_standard_filter': 1},
            {'fieldname': 'transaction_name', 'label': 'Transaction Name', 'fieldtype': 'Data', 'reqd': 0},
            {'fieldname': 'days_added', 'label': 'Days Added', 'fieldtype': 'Float', 'default': '0', 'in_list_view': 1},
            {'fieldname': 'days_deducted', 'label': 'Days Deducted', 'fieldtype': 'Float', 'default': '0', 'in_list_view': 1},
            {'fieldname': 'balance_after_transaction', 'label': 'Balance After Transaction', 'fieldtype': 'Float', 'in_list_view': 1}
        ]
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print('DocType Havano Leave Ledger Entry created successfully.')
