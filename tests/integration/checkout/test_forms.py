# coding=utf-8
from django.test import TestCase
from django.test.utils import override_settings

from oscar.apps.address.models import Country
from oscar.apps.checkout.forms import ShippingAddressForm
from oscar.test.factories import CountryFactory


class TestShippingAddressForm(TestCase):
    minimal_data = {
        'first_name': 'Bärry',
        'last_name': 'Chuckle',
        'line1': '1 King St',
        'line4': 'Gothám',
        'postcode': 'N1 7RR'
    }

    def setUp(self):
        CountryFactory(iso_3166_1_a2='GB', is_shipping_country=True)

    def test_removes_country_field(self):
        self.assertTrue('country' not in ShippingAddressForm().fields)

    def test_keeps_country_field(self):
        CountryFactory(iso_3166_1_a2='DE', is_shipping_country=True)
        self.assertTrue('country' in ShippingAddressForm().fields)

    @override_settings(OSCAR_REQUIRED_ADDRESS_FIELDS=('last_name', 'postcode'))
    def test_required_fields_validated(self):
        form = ShippingAddressForm()
        self.assertTrue(form.fields['last_name'].required)
        self.assertTrue(form.fields['postcode'].required)
        self.assertFalse(form.fields['first_name'].required)
        self.assertFalse(form.fields['line2'].required)
        self.assertFalse(form.fields['line3'].required)
        self.assertFalse(form.fields['line4'].required)

    @override_settings(OSCAR_REQUIRED_ADDRESS_FIELDS=('phone_number',))
    def test_required_phone_number_validated(self):
        # This needs a separate test because of the logic in PhoneNumberMixin
        form = ShippingAddressForm()
        self.assertTrue(form.fields['phone_number'].required)

    # Tests where the country field is hidden

    def test_is_valid_without_phone_number(self):
        self.assertTrue(ShippingAddressForm(self.minimal_data).is_valid())

    def test_only_accepts_british_local_phone_number(self):
        data = self.minimal_data.copy()
        data['phone_number'] = '07 914721389'  # local UK number
        self.assertTrue(ShippingAddressForm(data).is_valid())

        data['phone_number'] = '0176 968 426 71'  # local German number
        self.assertFalse(ShippingAddressForm(data).is_valid())

    def test_is_valid_with_international_phone_number(self):
        data = self.minimal_data.copy()
        data['phone_number'] = '+49 176 968426 71'
        form = ShippingAddressForm(data)
        self.assertTrue(form.is_valid())

    # Tests where the country field exists

    def test_needs_country_data(self):
        CountryFactory(iso_3166_1_a2='DE', is_shipping_country=True)

        self.assertFalse(ShippingAddressForm(self.minimal_data).is_valid())

        data = self.minimal_data.copy()
        data['country'] = Country.objects.get(iso_3166_1_a2='GB').pk
        self.assertTrue(ShippingAddressForm(data).is_valid())

    def test_only_accepts_local_phone_number_when_country_matches(self):
        CountryFactory(iso_3166_1_a2='DE', is_shipping_country=True)

        data = self.minimal_data.copy()
        data['phone_number'] = '07 914721389'  # local UK number

        data['country'] = Country.objects.get(iso_3166_1_a2='DE').pk
        self.assertFalse(ShippingAddressForm(data).is_valid())

        data['country'] = Country.objects.get(iso_3166_1_a2='GB').pk
        self.assertTrue(ShippingAddressForm(data).is_valid())

    @override_settings(OSCAR_REQUIRED_ADDRESS_FIELDS=('phone_number',))
    def test_local_phonenumber_invalid_without_country(self):
        # Add another country, so we have two.
        CountryFactory(iso_3166_1_a2='DE', is_shipping_country=True)
        data = self.minimal_data.copy()
        data['phone_number'] = '07 914721389'
        # User hasn't selected a country. Because there are multiple country
        # choices we should not accept the local number.
        form = ShippingAddressForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
