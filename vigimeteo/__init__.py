#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
French West Indies weather awareness, webscrapping info from METEO-FRANCE.

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
others.
"""

__version__ = "0.0.1"

from vigimeteo import VigiMeteo
