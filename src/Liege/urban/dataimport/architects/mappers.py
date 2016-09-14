# -*- coding: utf-8 -*-

from imio.urban.dataimport.access.mapper import AccessMapper as Mapper
from imio.urban.dataimport.factory import BaseFactory

import re


# Factory
class ArchitectFactory(BaseFactory):
    def getCreationPlace(self, factory_args):
        return self.site.urban.architects

    def getPortalType(self, container, **kwargs):
        return 'Architect'


class TitleMapper(Mapper):
    """ """

    def mapPersontitle(self, line):
        raw_title = self.getData('Titre').lower()
        title_mapping = self.getValueMapping('person_title_map')
        title = title_mapping.get(raw_title, 'society')
        return title


class NameMapper(Mapper):
    """ """

    regex_1 = '([A-Z]+-?[A-Z]+)\s+([A-Z][a-z]+-?[a-z]*)\s*\Z'
    regex_2 = '([A-Z][a-z]+-?[a-z]*)\s+([A-Z]+-?[A-Z]+)\s*\Z'

    def mapName1(self, line):
        raw_name = self.getData('Nom_Archi')
        match = re.search(self.regex_1, raw_name)
        if match:
            name1 = match.group(1)
            return name1

        match = re.search(self.regex_2, raw_name)
        if match:
            name1 = match.group(2)
            return name1

        return raw_name

    def mapName2(self, line):
        raw_name = self.getData('Nom_Archi')
        match = re.search(self.regex_1, raw_name)
        if match:
            name2 = match.group(2)
            return name2

        match = re.search(self.regex_2, raw_name)
        if match:
            name2 = match.group(1)
            return name2

        return ''


class StreetMapper(Mapper):
    """ """

    regex = '(.*?)\s*,?\s*(\d.*)\s*\Z'

    def mapStreet(self, line):
        raw_addr = self.getData('Adresse')
        match = re.search(self.regex, raw_addr)
        if match:
            street = match.group(1)
            return street

        return raw_addr

    def mapNumber(self, line):
        raw_addr = self.getData('Adresse')
        match = re.search(self.regex, raw_addr)
        if match:
            number = match.group(2)
            return number

        return ''


class LocalityMapper(Mapper):
    """ """

    regex = '(\d{4,4})\s+(\w.*)'

    def mapZipcode(self, line):
        raw_city = self.getData('CP Localité')
        match = re.search(self.regex, raw_city)
        if match:
            zipcode = match.group(1)
            return zipcode

        return ''

    def mapCity(self, line):
        raw_city = self.getData('CP Localité')
        match = re.search(self.regex, raw_city)
        if match:
            city = match.group(2)
            return city

        return raw_city
