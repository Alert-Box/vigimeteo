# vigimeteo
Vigilance Meteo : French West Indies weather awareness level.

This module grabs METEO-FRANCE weather information about the current weather
awareness level to alert people in Guadeloupe, Martinique, Saint Martin and
Saint Barths.

It can be used as command line tool or as python module and imported in a
third party program.

## Vigilance Météo

In France this level is called "Vigilance Météo", and suprisingly there is no
API nor RSS flux to retrieve in realtime this information for French West
Indies. This information is vital for local people. Two specific levels :
*violet* (purple) and *gris* (gray) purple, have been created for these islands
because of the risk of hurricanes.

Actually, this tools works only for Guadeloupe, Martinique and Saint Martin /
Saint Barths. The French Guyane is divided in 4 "vigilance météo" area and the
weather forecast provided by METEO-FRANCE use a different format from the
others.

# install

## using pip

    pip install vigimeteo

## from source

    git clone https://github.com/Alert-Box/vigimeteo
    cd vigimeteo
    python setup.py

# Usage example

## Command Line
    $ vigimeteo <area_alias>

### Vigilance Meteo areas
- Guadeloupe :
    - aliases : guadeloupe, gp, 971
- Martinique :
    - aliases : martinique, mq, 972
- Iles du Nord (St Barths / St Martin)
    - aliases : iles-du-nord, idn, nord  

    $ vigimeteo --help
    $ vigimeteo 971

## Python Module

    >>> from vigimeteo import VigiMeteo
    >>> ia = VigiMeteo()
    >>> ia.get_vigilance('guadeloupe')

# Licence

VigiMeteo is a Free Software and is licensed under the GNU General Public License (GPL) Version 3 or later.

## 	GNU General Public License (GPL) Version 3 or later

[![GNU GPL v3.0](http://www.gnu.org/graphics/gplv3-127x51.png)](http://www.gnu.org/licenses/gpl.html)

View official GNU site <http://www.gnu.org/licenses/gpl.html>.

[![OSI](http://opensource.org/trademarks/opensource/OSI-Approved-License-100x137.png)](http://opensource.org/licenses/mit-license.php)

[View the Open Source Initiative site.](http://opensource.org/licenses/mit-license.php)
