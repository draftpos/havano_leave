import frappe
def test():
    print('FOUND:', frappe.get_all('DocType', filters={'name': ['like', '%Leave Application%']}, fields=['name']))
