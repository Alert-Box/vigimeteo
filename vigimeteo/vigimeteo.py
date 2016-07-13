#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#       vigilance.py
#
#       Copyright 2011-2016 olivier watte  avaland.org
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

u"""French West Indies weather awareness, webscrapping info from METEO-FRANCE.

This module grabs METEO-FRANCE weather information about the current weather
awareness level to alert people in Guadeloupe, Martinique, Saint Martin and
Saint Barths.

In France this level is called "Vigilance Météo", and suprisingly there is no
API nor RSS flux to retrieve in realtime this information for French West
Indies. This information is vital for local people. Two specific levels because
of the risk of hurricanes have been created for these islands.

Actually, this tools works only for Guadeloupe, Martinique and Saint Martin /
Saint Barths. The French Guyane is divided in 4 "vigilance météo" area and the
weather forecast provided by  METEO-FRANCE use a different format from the
others."""


import ConfigParser
import urllib2

from bs4 import BeautifulSoup
import os
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import StringIO
import sys

import gettext

gettext.bindtextdomain('vigie-meteo', 'locale')
gettext.textdomain('vigie-meteo')
_ = gettext.gettext

__all__ = ['VigiMeteo', 'run']

BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'vigimeteo')


class VigiMeteo(object):
    u"""This class grabs French West Indies weather info from METEO-FRANCE."""
    def __init__(self, config_file=os.path.join(BASE_DIR, 'vigimeteo.cfg')):

        # cfg ini file
        self.config_file = config_file
        try:
            cfg = open(self.config_file, 'r')
        except IOError:
            exit(1)

        self.config = ConfigParser.ConfigParser()
        self.config.read(self.config_file)
        cfg.close()
        self.areas = ['guadeloupe', 'martinique', 'iles-du-nord']
        # Pas de connection à twitter par défaut
        self.twitter_api = None

    def _webscrap_previsions_html(self, area):
        u"""webscrap weather forecast html page for the given area.

        Args:
            Area(str): Region in ['guadeloupe', 'martinique', 'iles-du-nord']

            /!\ be careful guadeloupe == iles-du-nord /!\
            there is a different vigilance level between Guadeloupe and
            St Martin/St Barths, but the weather forecast is the same.

        Returns
        previsions(dictionary)
        eg.
        previsions = {'date': u'Jeudi 07 juillet 2016 18:43:01',
                      'title': u'Météo France Guadeloupe, bonsoir',
                      'content' : u'Very long french text ...'}
        """

        html = self._wget(self.config.get(area, 'previsions_html_uri'))
        soup = BeautifulSoup(html, "html.parser")
        if area == 'iles-du-nord':
            area = 'guadeloupe'
        search = soup.find('div', id=area)
        bulletin = search.find_all('div', 'article-row')[0]
        previsions = {'date': bulletin.find('h4').getText(),
                      'title': bulletin.find('h3').getText(),
                      'content': ''.join([p.getText()
                                          for p in bulletin.find_all('p')])}

        return previsions

    def _webscrap_suivi_pdf(self, area):
        u"""webscrap weather forecast pdf for the given area.

        Args:
            Area(str): Region in ['guadeloupe', 'martinique', 'iles-du-nord']

        Returns:
            vigilance(tuple of strings): the cleaned forecast pdf content)
        """

        # downloads the pdf
        pdf = self._wget(self.config.get(area, 'suivi_pdf_uri'))
        # get pdf content
        txt = self._pdf_to_text(pdf).split('\n')
        # clean pdf content
        null = [
            '',
            ' ',
            'METEO-FRANCE, Centre M\xc3\xa9t\xc3\xa9orologique de Guadeloupe.'
            ' BP 451 97183 Abymes Cedex.',
            'Tel : 0590 89 60 60  T\xc3\xa9l\xc3\xa9copieur : 0590 89 60 75'
            '         Site Web de M\xc3\xa9t\xc3\xa9o France aux Antilles '
            'Guyane : www.meteofrance.gp',
            'METEO FRANCE – Centre Météorologique  de Martinique - BP 379 - '
            '97288 Le Lamentin Cedex ',
            ' Téléphone : 0596 57 23 23 Télécopieur : 0596 51 29 40    Site Web'
            ' de Météo France aux Antilles Guyane : www.meteofrance.gp',
            '\x0c'
        ]
        vigilance = [data for data in txt if data not in null]
        # eg. replace 'Département' with 'Guadeloupe'
        rpl = self.config.get(area, 'replace').split('|')
        vigilance[0] = vigilance[0].replace(rpl[0], rpl[1])

        return vigilance

    def _wget(self, url, save_local=False, timeout=5, max_attempts=3):
        u"""Equivalent of the unix wget to download document from url.

        Args:
            url(str): document url
            save_local : save locally a copy
            timeout(int): timeout in seconds
            max_attempts: nb max of tries

        Returns:
            returns the document raw content(str) or False in case of failure
        """

        attempts = 0
        while attempts < max_attempts:
            try:
                response = urllib2.urlopen(url, timeout=timeout)
                content = response.read()
                if save_local:
                    local_file = url.split('/')[-1:][0]
                    local_copy = open(local_file, 'w')
                    local_copy.write(content)
                    local_copy.close()
                return content
            except urllib2.URLError:
                attempts += 1

        return False

    def _pdf_to_text(self, scraped_pdf_data):
        """Converts a pdf in text."""

        fp = StringIO.StringIO()
        fp.write(scraped_pdf_data)
        fp.seek(0)
        outfp = StringIO.StringIO()

        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, outfp, laparams=LAParams())
        process_pdf(rsrcmgr, device, fp)
        device.close()

        t = outfp.getvalue()
        outfp.close()
        fp.close()
        return t

    def get_vigilance(self, area):
        u"""Returns weather vigilance level from web/pdfscrapping

        Args:
        area(str): Region in ['guadeloupe', 'martinique', 'iles-du-nord']

        Returns:
        vigilance level (dictionary)
        eg.
        vigilance = {
        'area': 'Guadeloupe',
        'level': 'Vert',
        'suivi': ['Guadeloupe en vigilance verte',
        'Pas de vigilance particulière'],
        'previsions': {'date': u'Jeudi 07 juillet 2016 18:43:01',
        'title': u'Météo France Guadeloupe, bonsoir',
        'content' : u'Very long french text ...'}
        }
        """
        vigilance = {}
        vigilance['area'] = self.config.get(area, 'replace').split('|')[1]
        vigilance['suivi'] = self._webscrap_suivi_pdf(area)
        vigilance['previsions'] = self._webscrap_previsions_html(area)

        return vigilance


def run():
    usage = '\n'.join(['retrieves weather alert level for French West '
                       'Indies from METEO-FRANCE website',
                       'usage : %prog <area_alias>',
                       'where area_alias in :',
                       '******************************************',
                       '* area         * aliases                 *',
                       '******************************************',
                       '* Iles du Nord * idn, iles-dudnord, nord *',
                       '* Guadeloupe   * gp, guadeloupe, 971     *',
                       '* Martinique   * mq, martinique, 972     *',
                       '******************************************',
                       '',
                       'example for the Guadeloupe:',
                       'vigimeteo 971',
                       'vigimeteo gp'])

    country_aliases = {
        'iles-du-nord': ['iles-du-nord', 'idn', 'nord'],
        'guadeloupe': ['guadeloupe', 'gp', '971'],
        'martinique': ['martinique', 'mq', '972'],
    }

    if len(sys.argv) == 1 or sys.argv[1] in ['-h', '--help']:
        print usage
    else:
        wanted = sys.argv[1].lower()
        try:
            area = [alias for alias in country_aliases.iterkeys()
                    if wanted in country_aliases[alias]][0]
        except IndexError:
            print usage
            sys.exit(1)

        ia = VigiMeteo()
        vigilance = ia.get_vigilance(area)
        for item in vigilance['suivi']:
            print item

if __name__ == '__main__':
    run()
