# coding: utf-8
from openerp.tests.common import TransactionCase


class TestPartnerMerge(TransactionCase):
    def setUp(self):
        super(TestPartnerMerge, self).setUp()
        self.partner1 = self.env.ref('base.res_partner_6')
        self.partner2 = self.env.ref('base.res_partner_6').copy()
        self.user = self.env.ref('base.user_demo')

    def _do_merge(self):
        # Switch to old API due to guessing mismatch
        wizard_obj = self.registry['base.partner.merge.automatic.wizard']
        wizard_obj._merge(
            self.env.cr, self.user.id, [self.partner1.id, self.partner2.id],
            self.partner2, context=self.env.context)

    def test_partner_merge(self):
        self._do_merge()

    def test_partner_merge_protected_field(self):
        """ Protecting a field with a specific group does not break merging """
        column = self.env['res.partner']._columns['birthdate']
        groups_orig = getattr(column, 'groups', None)
        column.groups = 'base.group_system'
        try:
            self._do_merge()
        finally:
            column.groups = groups_orig
