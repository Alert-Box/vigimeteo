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

__author__ = "Olivier Watte"
__copyright__ = "Copyright (c) 2016 Olivier Watte"
__license__ = "GPL-V3+"
__all__ = ['VigiMeteo', 'run', ]


def get_version(version, alpha_num=None, beta_num=None,
                rc_num=None, post_num=None, dev_num=None):
    """Crée la version en fonction de la PEP 386.
    On affiche toujours la version la moins aboutie.
    Exemple, si alpha, beta et rc sont spécifié, on affiche la version
    comme alpha.
    Args:
        version: tuple du numéro de version actuel. Ex : (0,0,1) ou (2,0,4)
        alpha_num: définie que la version comme alpha
        beta_num: définie la version comme beta
        rc_num: définie la version comme release candidate
        post_num: definie la version comme post dev
        dev_num: définie la version comme en cour de développement
    Returns:
        numéro de version formaté selon la PET 386
    """
    num = "%s.%s" % (int(version[0]), int(version[1]))
    if version[2]:
        num += ".%s" % int(version[2])

    letter_marker = False  # permet de sortir si on a un marqueur lettre
    if alpha_num:
        num += "a%s" % int(alpha_num)
        letter_marker = True

    if beta_num and not letter_marker:
        num += "b%s" % int(beta_num)
        letter_marker = True

    if rc_num and not letter_marker:
        num += "rc%s" % int(rc_num)

    if post_num:
        num += ".post%s" % int(post_num)

    if dev_num:
        num += ".dev%s" % int(dev_num)

    return num

__version__ = get_version((0, 0, 1), beta_num=1, dev_num=1)
