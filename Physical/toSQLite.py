## toSQLite.py
## SQLalchemy classes and putting data into SQLite database
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
import re

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import scrape_BS
from scrape_BS import make_conv_lst, scraping_allascii, SQLiteclsdict_allascii, SQLiteclsdict_convfact

#############################################
## Access the SQL database for SQLAlchemy
#############################################

engine = create_engine("sqlite:///Physicallite.db")    
Base = declarative_base()

###################################
## SQLAlchemy class for a "Row"
###################################

def Row(clsname,base,dict):
    Row=type(str(clsname),(base,),dict)
    return Row

def physconst_repr(self):
    return "<Physical constant(Quantity='%s', Value='%s', Uncertainty='%s', Unit='%s'>" % (self.Quantity, self.Value, self.Uncertainty, self.Unit)

def convfact_repr(self):
    return u"<Conversion Factor(To convert from='%r', to='%r', Multiply by='%r'>".encode('utf8') % (self.Toconvertfrom, self.to, self.Multiplyby)


NISTPhysicalConstantLite = Row("NISTPhysicalConstantLite", Base, SQLiteclsdict_allascii("./rawdata/allascii.txt"))
setattr(NISTPhysicalConstantLite,'__repr__', physconst_repr)

NISTConversionFactorLite = Row("NISTConversionFactorLite", Base, SQLiteclsdict_convfact() )
setattr(NISTConversionFactorLite,'__repr__', convfact_repr)

################################################################################
## Once you're done with defining and initiating all your SQLAlchemy classes
## then you can write it into the "metadata" with this create_all command
################################################################################

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

###############################################################################################
## For SQLite
## One must do some particular preprocessing for SQLite because SQLite doesn't like Decimal class
## in Python nor Numeric in SQLAlchemy
###############################################################################################

def liteprocess(scrapedlist):
    tbl = []
    for rawline in scrapedlist:
        line = []
        line.append(rawline[0])
        try:
            line.append(float(rawline[1].replace(" ","")))
        except ValueError:
            value = rawline[1].replace(" ","")
            value = ''.join( re.split(r'[.]{2,}',value))
            line.append( float(value) )
        try:
            line.append(float(rawline[2].replace(" ","")))
        except ValueError:
            # EY : 20150823 for SQLAlchemy, instead of "(exact)" use None type None for 
            # SQLAlchemy to denote "(exact)" in the Uncertainty column
            line.append(None)
        line.append(rawline[3])
        tbl.append(line)

    return tbl

def liteprocessconvfact(scrapedlist):
    tbl = []
    for rawline in scrapedlist:
        line = []
        line.append(rawline[0])
        line.append(rawline[1])
        line.append(float(rawline[2]))
        tbl.append(line)

    return tbl


########################################
## Add all that data rows to the session
########################################

def toSQLitefrompreprocessed(rowcls,headers,list):
    """
    toSQLfrompreprocessed = toSQLfrompreprocessed(row,list)
    INPUTS:
    rowcls is a SQLAlchemy class
    headers is a list of strings that'll tell which column a data pt. in a row belongs to
    list is a list of preprocessed data

    EXAMPLE of Usage
    scrapedascii = scraping_allascii()
    output = toSQLfrompreprocessed(NISTPhysicalConstantLite,scrapedascii[3], scrapedascii[5])
    session.add_all( output )
    session.commit()
    """
    output = []
    for row in list:
        output.append(rowcls(**dict(zip(headers,row))))
    return output


########################################
## main
########################################

def main():
    scrapedascii = scraping_allascii()
    tbl = liteprocess( scrapedascii[4] )
    output = toSQLitefrompreprocessed(NISTPhysicalConstantLite,scrapedascii[3], tbl)

    session.add_all(output)
    session.commit()

    headers, convdata, convdata2 = make_conv_lst()
    output2 = toSQLitefrompreprocessed(NISTConversionFactorLite, headers, liteprocessconvfact(convdata2))
    session.add_all( output2 )
    session.commit()

    session.close()
    return output, output2


if __name__ == "__main__":
    main()

#########################
## Examples of usage:
#########################
"""
scrapedascii = scraping_allascii()
tbl = liteprocess( scrapedascii[4] )
output = toSQLitefrompreprocessed(NISTPhysicalConstantLite,scrapedascii[3], tbl)

OR

output = main()

session.add_all( output )
session.commit()

headers, convdata, convdata2 = make_conv_lst()
output = toSQLitefrompreprocessed(NISTConversionFactorLite, headers, liteprocessconvfact(convdata2))
session.add_all( output )
session.commit()


"""


    
