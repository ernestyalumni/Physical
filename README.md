<h2><i>Physical</i> - web scrape, format and clean data, and (SQL) database Physical Constants, Units, and Conversions.  </h2>

![Alt text](https://ernestyalumni.files.wordpress.com/2015/08/physicalcover.png?raw=true "Physical")

<em>20150824 EY : I'm copying here the tempdoc.doc file, but with formatting.  </em>

<p>Physical requires (minimally) <i>requests, BeautifulSoup</i> for the webscraping.  
For databasing and querying, I used <i>SQLAlchemy</i>.  I highly recommend having a SQL database to have all querying features available; I used <i>PostgreSQL</i>.   </p>

<h4>What I (and you) want and can do now:</h4>

>>> qNISTPhysConst.filter( descNIST.match("Boltzmann") ).all()

<p>i.e. get all the Boltzmann constants and constants that match "Boltzmann" such as the Stefan-Boltzmann constant, sourced from the National Institute of Standards and Technology (NIST), USA.    </p>

<p>Note, “This product uses data provided by the National Institute of Standards and Technology (NIST) but is not endorsed or certified by NIST.”</p>

<p>Then do</p>

>>> Boltzconst = qNISTPhysConst.filter( descNIST.match("Boltzmann") ).all()[0]

<p>and we can treat the Boltzmann constant as a Python object (!!!).  </p>

<p>Then we can obtain numerical and descriptive data on Boltzmann constant by "calling the methods of this Python object" e.g.</p>

>>> Boltzconst.Quantity
u'Boltzmann constant'

>>> Boltzconst.Value
Decimal('1.38064852E-23')

>>> Boltzconst.Uncertainty
Decimal('7.9E-30')

>>> Boltzconst.Unit
u'J K^-1'

<p>Also, the __repr__ method for the Python object, Boltzconst in this case, with type, type(Boltzconst) a Python class called 'Physical.SQLalcls.NISTPhysicalConstant' or NISTPhysicalConstant, prints out all these values as a string:</p>

>>> Boltzconst
<Physical constant(Quantity='Boltzmann constant', Value='1.38064852E-23', Uncertainty='7.9E-30', Unit='J K^-1'>

<p>Notice the Decimal Python class used for the Value and Uncertainty of the Boltzmann constant.  Keep in mind that this feature is only available if one uses a SQL database such as PostgreSQL, not SQLite.  </p>

<p>Round the Boltzmann constant to significant digits as desired:</p>

>>> round(Boltzconst.Value, 28)
1.38065e-23
 
<p>Get the exponent in a sane, civilized manner as a DecimalTuple:</p>

>>> Boltzconst.Value.as_tuple()
DecimalTuple(sign=0, digits=(1, 3, 8, 0, 6, 4, 8, 5, 2), exponent=-31)

>>> Boltzconst.Value.as_tuple()[2]
-31


<b>All Physical Constants are available, directly sourced from NIST</b>: Again, run query.py with python -i query.py in the "lowest" directory of Physical containing query.py.  

>>> for c in qNISTPhysConst.all(): print c.Quantity, c.Value, c.Unit
... 
{220} lattice spacing of silicon 1.920155714E-10 m
alpha particle-electron mass ratio 7294.29954136 
alpha particle mass 6.644657230E-27 kg
alpha particle mass energy equivalent 5.971920097E-10 J
alpha particle mass energy equivalent in MeV 3727.379378 MeV
alpha particle mass in u 4.001506179127 u
alpha particle molar mass 0.004001506179127 kg mol^-1
alpha particle-proton mass ratio 3.97259968907 
Angstrom star 1.00001495E-10 m
atomic mass constant 1.660539040E-27 kg
atomic mass constant energy equivalent 1.492418062E-10 J
atomic mass constant energy equivalent in MeV 931.4940954 MeV
...

<p>and so on.  </p>

<h4>Get Conversions. </h4> You (and I) can get the conversions to SI agreed upon by NIST (and directly sourced from there) from a SQL database stored locally:

qNISTConvFact.all() 

<p>gets all the NIST conversion factors to SI in a SQLAlchemy session query.  Let's print this in a readable format:</p>

>>> for f in qNISTConvFact.all(): print f.Toconvertfrom, f.to, f.Multiplyby
...
abampere ampere (A) 10
abcoulomb coulomb (C) 10
abfarad farad (F) 1000000000
abhenry henry (H) 1.0E-9
abmho siemens (S) 1000000000
abohm ohm (Ω) 1.0E-9
abvolt volt (V) 1.0E-8
acceleration of free fall, standard (gn) meter per second squared (m / s2) 9.80665
...

<p>and so on.  </p>

<p>For example, consider pressure: in SI, it's Pascals, but in U.S. English, it's psi, and you'll have to worry about if it's the psi to the standard atmosphere, or "absolute" psi (I know, it's strange, but the situation is that a lot of U.S. gauges when you want to go and measure pressure in the lab or in industry, you'll have to use this psi or that psi).  Let's find it:</p>

qNISTConvFact.filter( fromNIST.match("psi") ).all()
>>> for f in qNISTConvFact.filter( fromNIST.match("psi") ).all(): print f.Toconvertfrom, f.to, f.Multiplyby
... 
pound-force per square inch (psi) 
    (lbf/in2) pascal (Pa) 6894.757
pound-force per square inch (psi) (lbf/in2) kilopascal (kPa) 6.894757
psi (pound-force per square inch) (lbf/in2) pascal (Pa) 6894.757
psi (pound-force per square inch) (lbf/in2) kilopascal (kPa) 6.894757

<p>Pick the third down psi and we can get the description of the units converted to and from, as a Python string, and the conversion factor as a Python Decimal:</p>

>>> fpsi = qNISTConvFact.filter( fromNIST.match("psi") ).all()[2]
>>> fpsi.Toconvertfrom
u'psi (pound-force per square inch) (lbf/in2)'
>>> fpsi.to
u'pascal (Pa)'
>>> fpsi.Multiplyby
Decimal('6894.757')

<p>Atmospheric pressure is 14.696 psi, so to get that in Pascal, we can do something like this:</p>

>>> Decimal(14.696) * fpsi.Multiplyby
Decimal('101325.3488719999981383725896')

<p>Then use quantize method in Decimal to obtain the desired number of significant digits:</p>

>>> (Decimal(14.696) * fpsi.Multiplyby).quantize(Decimal('0.001'))
Decimal('101325.349')

<p>and print units as well:</p>

>>> print (Decimal(14.696) * fpsi.Multiplyby).quantize(Decimal('0.001')), fpsi.to
101325.349 pascal (Pa)

<p>For Physical, I used SQLAlchemy, and you can construct your own queries with the SQLAlchemy ORM with session and the SQLAlchemy classes, which maps to tables, 'FundamentalPhysicalConstantsCompleteListing', 'NISTConversionFactors', in a SQL database, which I called Physical, </p>

<ul>
<li>NISTPhysicalConstant</li>
<li>NISTConversionFactor</li>
</ul>

<p>i.e.</p>

>>> NISTPhysicalConstant.__tablename__
'FundamentalPhysicalConstantsCompleteListing'
>>> NISTConversionFactor.__tablename__
'NISTConversionFactors'

<p>Examples of your queries would be welcomed.</p>


<h3>Setting up Physical.  </h3>

<p>Keep in mind that this process of setting up Physical wasn't smooth for me at all and I wouldn't expect it to be smooth for you either: please contact me or share with us how to improve this part. </p>

<p>Copy the entire package somewhere.  Be sure to have your SQL database, such as PostgreSQL, up and running.</p>


<h5>-If you have your SQL database up and running</h5>

<p>Then create, with createdb (for postgresql), the database Physical.  For instance, in my case, on my administrator account, I assigned ownership to username as such, at the command prompt:</p>

createdb -O username Physical

<p>Now, you'll have to hard edit these files with the information about your SQL database:</p>

<ul><li>Physical/__init__.py</li>
<li>Physical/toSQL.py</li>
</ul>

<p>In both files, search for _iamuser = and replace for inside the string, your default username, so for instance</p>

   _iamauser = "username"

<p>for the line</p>

engine  = create_engine("postgresql://"+_iamauser+":"+_password+"@localhost/Physical")

<p>you may have to change postgresql into mysql or whatever you use and localhost with the name of your SQL database location.  Otherwise, this setup had worked for me.</p>


<p>Once that's all in place, run these commands:</p>

<ol>
<li>1. Make allascii.txt, in ASCII format, all Fundamental Constants from NIST, in Physical/rawdata/
Do this in the Physical directory:
python -i scrape_BS.py

<li>2. Populate with data directly from NIST your SQL database and SQLite database - 
Do this in the Physical directory
python -i toSQL.py
python -i toSQLite.py
</ol>

<p>Things should be setup now (it worked for me, on a mid-2011 MacBook Air, OS X Yosemite 10.10.5).  

<p>Then go back to the "lowest" directory, containing query.py and run it with this command:</p>

python -i query.py

<p>Then, you can use SQLAlchemy and look up the documentation there and make SQL database queries with the SQL table classes </p>

<ul>
<li>NISTPhysicalConstant</li>
<li>NISTConversionFactor</li>
</ul>

<h3>Rationale for Physical</h3>

I was surprised that, to my knowledge, nobody had databased, ensured the data's integrity, and made more usable, with the file input and output, of Physical Constants and Units and Conversion Factors, from trusted sources like NIST, beyond looking it up manually and writing it down, or downloading the ASCII files.  


<h4>20150824 Current Final Thoughts:</h4>

It does concern me that "on plain face", "on clear type", one has to enter his or her password "in clear type"; any suggestions that someone out there could share about how SQL database programmers enter their password would help.  That was why I wanted a SQLite implementation, that doesn't ask for a username or password.  That SQLite database is saved in Physical/ directory as Physicallite.db.  


