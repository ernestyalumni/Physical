## query.py
## Start here to query your (SQL) database of Physical Constants, Units, Conversion Factors
##  
############################################################################ 
## Copyleft 2015, Ernest Yeung <ernestyalumni@gmail.com>                            
##                                                            
## 20150823
##                                                                               
## This program, along with all its code, is free software; you can redistribute 
## it and/or modify it under the terms of the GNU General Public License as 
## published by the Free Software Foundation; either version 2 of the License, or   
## (at your option) any later version.                                        
##     
## This program is distributed in the hope that it will be useful,               
## but WITHOUT ANY WARRANTY; without even the implied warranty of              
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                 
## GNU General Public License for more details.                             
##                                                                          
## You can have received a copy of the GNU General Public License             
## along with this program; if not, write to the Free Software Foundation, Inc.,  
## S1 Franklin Street, Fifth Floor, Boston, MA                      
## 02110-1301, USA                                                             
##                                                                  
## Governing the ethics of using this program, I default to the Caltech Honor Code: 
## ``No member of the Caltech community shall take unfair advantage of        
## any other member of the Caltech community.''                               
##                                                         
## Donate, and support my other scientific and engineering endeavors at 
## ernestyalumni.tilt.com                                                      
##                          
## Facebook     : ernestyalumni                                                   
## linkedin     : ernestyalumni                                                    
## Tilt/Open    : ernestyalumni                                                    
## twitter      : ernestyalumni                                                   
## youtube      : ernestyalumni                                                   
## wordpress    : ernestyalumni                                                    
## 
## Note, “This product uses data provided by the National Institute of Standards and Technology (NIST) but is not endorsed or certified by NIST.”
## NIST SRD 121 
##
############################################################################ 
import decimal
from decimal import Decimal

import Physical


session = Physical.Session()

#_sqlchoice = raw_input("Press enter for sqlite; type 1 for postgreSQL: ")
if Physical._sqlchoice == '':

    from Physical import NISTPhysicalConstantLite, NISTConversionFactorLite
    qLite = session.query(NISTPhysicalConstantLite)
    desc = NISTPhysicalConstantLite.Quantity # abbreviate the column for the Quantity's description for a NIST Physical Constant 
    qConv  = session.query(NISTConversionFactorLite)
    convto = NISTConversionFactorLite.Toconvertfrom 

else:
    from Physical import NISTPhysicalConstant, NISTConversionFactor 
    qNISTPhysConst = session.query(NISTPhysicalConstant)
    descNIST = NISTPhysicalConstant.Quantity # abbreviate the column for the Quantity's description for a NIST Physical Constant 
    qNISTConvFact = session.query(NISTConversionFactor)
    fromNIST = NISTConversionFactor.Toconvertfrom
"""
EXAMPLES of QUERIES
query and obtain a list of ALL Physical Constants
qNISTPhysicalConstant.all()
for x in qNISTConvFact.all(): print x.Toconvertfrom, x.Multiplyby

Find Boltzmann constant:
qNISTPhysConst.filter( descNIST.match("Boltzmann") ).all()
qNISTPhysConst.filter( descNIST == "Boltzmann constant").all()

For SQLite, SQLite doesn't have the Match functionality, we can only make exact queries:
qLite.filter( desc == "Boltzmann constant").all()
"""

########################################
## !!! Remember to close your sesssion!
# session.close()
########################################
