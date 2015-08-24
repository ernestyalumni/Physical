## __init__.py
## __init__.py file for Physical package
## This website is the BEST explanation of __init__.py
## http://mikegrouchy.com/blog/2012/05/be-pythonic-__init__py.html 
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


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#############################################
## SQLAlchemy sessionmaker, Session as global 
## You're going to have to change the below code to make it work for your postgreSQL setup
# see the SQLAlchemy documentation
#############################################

_sqlchoice = raw_input("Press enter for sqlite; type 1 for postgreSQL: ")
if _sqlchoice == '':
    import SQLitealcls
    from SQLitealcls import NISTPhysicalConstantLite, NISTConversionFactorLite


    engine = create_engine("sqlite:///Physical/Physicallite.db")
    Session = sessionmaker(bind=engine)
else:
    import SQLalcls
    from SQLalcls import NISTPhysicalConstant, NISTConversionFactor

    _iamauser = raw_input("Input your username: ")
    if _iamauser == "":
        _iamauser = "patrickbateman"
    _password = raw_input("Input your password: ")

    engine  = create_engine("postgresql://"+_iamauser+":"+_password+"@localhost/Physical")
    Session = sessionmaker(bind=engine)
