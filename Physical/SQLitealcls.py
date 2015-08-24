## SQLitealcls.py
## SQLalchemy classes only for SQLite database
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
############################################################################ 
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


import scrape_BS
from scrape_BS import scraping_allascii, SQLiteclsdict_allascii, SQLiteclsdict_convfact

Base = declarative_base()

###################################
## SQLAlchemy class for a "Row" and 
# NISTPhysicalConstant
###################################

def Row(clsname,base,dict):
    Row=type(str(clsname),(base,),dict)
    return Row

def physconst_repr(self):
    return "<Physical constant(Quantity='%s', Value='%s', Uncertainty='%s', Unit='%s'>" % (self.Quantity, self.Value, self.Uncertainty, self.Unit)

def convfact_repr(self):
    return u"<Conversion Factor(To convert from='%r', to='%r', Multiply by='%r'>".encode('utf8') % (self.Toconvertfrom, self.to, self.Multiplyby)


NISTPhysicalConstantLite = Row("NISTPhysicalConstantLite", Base, SQLiteclsdict_allascii("./Physical/rawdata/allascii.txt"))
setattr(NISTPhysicalConstantLite,'__repr__', physconst_repr)

NISTConversionFactorLite = Row("NISTConversionFactorLite", Base, SQLiteclsdict_convfact() )
setattr(NISTConversionFactorLite,'__repr__', convfact_repr)

