from django.test import TestCase

from scanner.script_parser import NmapScriptParser
from scanner.scan_parser import ScanImporter

class NmapScriptParseTestCase(TestCase):

    def test_parse_output(self):
        script_id = 'smb-check-vulns'
        script_output = 'bla bla MS08-067: VULNERABLE bla bla'

        nsp = NmapScriptParser()
        output = nsp.parse_output(script_id, script_output)
        self.assertIsNotNone(output)


class ScanParseTestCase(TestCase):

    def test_full_scan_parse(self):
        f = open('test_xml', 'r')
        xml = f.read()
        f.close()
        importer = ScanImporter()
        importer.process()
