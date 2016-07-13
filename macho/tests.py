import json
from django.test import TestCase

from .models import Macho, MachoDetail


def create_Macho(macho_data):
    macho = Macho.objects.create(
        macho_id = macho_data['id'][:-2],
        periodicity = macho_data['periodicity'],
        period = macho_data['period']
    )
    mag = macho_data['Mag']
    mjd = macho_data['MJD']
    for time, magnitude in zip(mjd,mag):
        MachoDetail.objects.create(
            macho = macho,
            mag = magnitude,
            mjd = time
        )

    return macho

# Test Model
class MachoModelTestCase(TestCase):

    def setUp(self):
        with open('macho/test_periodic.json', 'r') as test_periodic:
            self.macho_data = json.load(test_periodic)

    def test_macho_table_created(self):
        macho = create_Macho(self.macho_data)

        self.assertEqual(macho.macho_id, '1.3441.15')
        self.assertTrue(macho.periodicity)

    def test_macho_detail_match(self):
        macho = create_Macho(self.macho_data)

        timeseries_length1 = len(self.macho_data['Mag'])
        timeseries_length2 = len(self.macho_data['MJD'])

        macho_detail = MachoDetail.objects.filter(macho=macho)

        self.assertEqual(macho_detail.count(), timeseries_length1)
        self.assertEqual(macho_detail.count(), timeseries_length2)

# Test View
