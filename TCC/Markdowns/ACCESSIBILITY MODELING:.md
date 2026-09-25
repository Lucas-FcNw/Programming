HEALTH CARE ACCESSIBILITY MODELING: EFFECTS OF
CHANGE IN SPATIAL REPRESENTATION OF DEMAND...

QUAESTIONES GEOGRAPHICAE 33(3) • 2014

HEALTH CARE ACCESSIBILITY MODELING: EFFECTS
OF CHANGE IN SPATIAL REPRESENTATION OF DEMAND
FOR PRIMARY HEALTH CARE SERVICES

piotr jankowski1,2, blake brown1

1Department of Geography, San Diego State University, San Diego, CA, USA
2Institute of Geoecology and Geoinformation, Adam Mickiewicz University in Poznań, Poland

Manuscript received: May 5, 2013
Revised version: July 5, 2014

jankowski p., brown B., 2014. Health care accessibility modeling: effects of change in spatial representation of demand
for primary health care services. Quaestiones Geographicae 33(3), Bogucki Wydawnictwo Naukowe, Poznań, pp. 39–
53, 4 tables, 10 figs. DOI 10.2478/quageo-2013-0028, ISSN 0137-477X.

abstract. Health care accessibility can be measured by the number of prospective patients who could reach a medical
facility within a prescribed time limit. The representation of health care demand in estimating accessibility is an impor-
tant consideration since different spatial aggregations of demand have different consequences with regard to accessi-
bility estimates. This article examines the effects of aggregating population demand for primary health care, ranging
from census tract to aggregated census block, on estimates of primary health care accessibility. Spatial representations
of aggregated demand were incorporated into a location-allocation model in order to determine a measure of acces-
sibility represented by the unmet demand for primary health care services. The model was implemented for the U.S.
State of Idaho, based on the allocation of Idaho residents’ demand for primary health care to the state’s existing pri-
mary health care facilities. The results confirm a relationship between the level of demand aggregation and the level
of potential accessibility. In case of a rural state such as Idaho the relationship is positive; higher levels of aggregation
result in higher measures of accessibility.

key words: health care accessibility, GIS, location-allocation, scale, spatial aggregation

Address of the corresponding author: Piotr Jankowski, Department of Geography, San Diego State University, 5500 Campanile
Drive, San Diego, CA 92182-4493, USA; e-mail: pjankows@mail.sdsu.edu

Introduction

This article examines the effect of scale in rep-
resenting  the  demand  for  primary  health  care
services in modeling health care accessibility. The
concept of spatial accessibility in health care ser-
vices  refers  to  the  ability  of  an  individual  to:  1)
reach a location of health care service from a loca-
tion of his/her residency within some prescribed
maximum time interval, and 2) receive a medical
service. In geographical health research, the con-
cept of accessibility has been investigated through
the  lens  of  spatial  analysis  (Wang  2011,  Kwan,

Weber 2008, Laditka, 2004, Martin, Wiliams 1992)
and Geographic Information Systems (GIS) (Bur-
key et al. 2012, Cromley, McLafferty 2002, Lin et
al. 2002, Lovett et al. 2002, Parker, Cambell 1998).
Among  the  modeling  approaches  to  health  care
accessibility,  gravity  models  (Wang,  Roisman
2011)  and  location-allocation  models  (Oppong,
Hodgson 1994, Langford, Higgs 2006) have been
frequently used to account for the effects of dis-
tance, availability of health care, and demand for
service.

Health  care  accessibility  can  be  investigated
from  two  different  perspectives.  First,  potential

piotr jankowski, blake brown

40

PIOTR JANKOWSKI, BLAKE BROWN

accessibility  measures  can  be  derived  based  on
the estimated number of people who could reach
a medical facility within a prescribed time limit.
Second,  realized  accessibility  measures  can  be
computed  showing  how  many  people  actually
did receive medical services. With regard to the
second  perspective,  detailed  patient-level  infor-
mation is typically unavailable. As a result, most
accessibility  studies  have  developed  potential
measures  of  accessibility  based  on  straight-line
distances  or  travel-time  distances  between  loca-
tions of health services and aggregate locations of
the population. These measures can then be used
to identify areas where accessibility is poor and
where  additional  health  facilities  are  needed  to
improve accessibility (Langford, Higgs 2006).

One  of  the  requirements,  and  challenges  at
the same time, of assessing potential accessibili-
ty to health care services with location-allocation
models  has  been  the  choice  of  scale,  at  which
population’s  demand  for  health  care  services
is  represented.  Typically,  demand  for  goods  or
services, health care including, is represented in
location-allocation  models  at  a point  (Rushton
1989).  Because  the  population  data  are  almost
always available at statistical enumeration units
(e.g. zip codes or census tracts), most accessibili-
ty studies have used the centroid of the enumer-
ation  unit  to  represent  that  enumeration  unit’s
population. Verter and Lapierre (2002) used the
centroids  of  638  populated  regions  as  the  de-
mand locations for a location-allocation model in
order to locate preventative health care facilities
that maximized participation in prevention pro-
grams with the rationale that distance is a major
determinant  of  participation  in  such  programs.
In  a study  by  Mitropoulos  et  al.  (2006),  patient
level  data  about  the  annual  number  of  visits  to
existing health care facilities was obtained for all
inhabitants of 228 population regions in semi-ru-
ral Achaia, Greece. The centroids of these regions
were used as the locations of demand for health
care facilities. Brabyn and Skelly (2002) used the
centroids of meshblocks in New Zealand (mesh-
blocks are the most detailed census enumeration
units  available)  as  the  locations  of  demand  in
an  accessibility  model.  In  a study  by  Wang  and
Luo  (2005),  population-weighted  centroids  of
census  tracts  (based  on  block-level  population
data)  were  used  instead  of  simple  geographic

centroids, to represent population locations more
accurately.  This  process  resulted  in  a computa-
tionally  manageable  number  of  demand  points
(2952) and was particularly successful in refining
the locations of population in rural areas where
notable areas of land are unpopulated.

Since  the  demand  for  health  care  services
is  a function  of  population  distribution  across
a geographical  space,  any  area-to-point  trans-
formation  is  inherently  burdened  with  an  error
resulting  from  continuous  demand  distribu-
tion  (statistical  enumeration  zones)  aggregated
into  discrete  (point)  representations  of  demand
(Daskin et al. 1989). It is also possible to distrib-
ute the population evenly across an enumeration
unit (so called pro rata method) as a series of even-
ly spaced points dispersed throughout the entire
enumeration unit (Langford, Higgs 2006). If uni-
form  distribution  is  a valid  assumption,  the  pro
rata  method  may  offer  more  accurate  estimates
of population location than the centroid method.
This  assumption  may  be  valid  in  small,  dense
urban environments but is less likely to be valid
in rural areas where population tends to concen-
trate  in  small  settlements  separated  by  areas  of
unoccupied/unpopulated land. In addition, this
pro-rata  technique  for  representing  population
locations  typically  results  in  a vast  number  of
demand points, which presents a computational
challenge  for  assessing  accessibility  with  a loca-
tion–allocation  model.  The  use  of  large-scale/
small-area statistical enumeration units (e.g. cen-
sus blocks in the U.S.), in order to reduce the ar-
ea-to-point transformation error, results in a sim-
ilar computational challenge and is only practical
for small study areas.

This  article  examines  the  effects  of  area-to-
point  demand  aggregation  in  location-alloca-
tion  model  on  accessibility  to  primary  health
care  service  centers.  The  level  of  accessibility  is
measured by unmet demand for primary health
care services due to distance and/or lack of ser-
vice  capacity.  This  approach  results  in  identify-
ing  areas  without  adequate  accessibility  (given
the  driving  distance  and  service  capacity  con-
straints).  The  article  explores  the  consequences
of  different  demand  representations  from  the
coarsest (small scale) to the finest (large scale) in-
cluding tract centroid, block group centroid, and
block centroid on the amount of unmet demand.

HEALTH CARE ACCESSIBILITY MODELING: EFFECTS OF CHANGE IN SPATIAL REPRESENTATION OF DEMAND...

41

These  progressively  larger-scale  representations
and the resulting accessibilities are examined at
different  driving  times,  beginning  with  30  min-
utes  driving  time,  through  45  and  60  minutes
travel times. In the remainder of the paper a loca-
tion-allocation model adopted for calculating the
unmet demand for primary health care services
is  presented  in  section  two  along  with  data  re-
quirements  and  study  area  description.  Results
of modeling accessibility to primary health care
services  under  different  spatial  representations
of  demand  are  presented  in  section  three.  The
discussion and conclusion are offered in section
four.

Modeling approach, data requirements,
and study area

Accessibility  is  one  of  the  most  widely  used
metrics  in  measuring  the  value  of  location  in
service  delivery  (Church,  Murray  2009).  Acces-
sibility  can  also  be  conceptualized  as  a function
of  allocating  demand  for  services  distributed
among multiple locations to service centers. This
conceptualization has motivated the use of loca-
tion-allocation  models  in  studies  of  accessibil-
ity  to  health  services  and  in  planning  of  health
services with explicit consideration given to the
locations of service providers, service capacities,
geographical distribution of patients, and ease of
access to health services (Mitropoulos et al. 2012,
Harper et al. 2005). In this study a location-allo-
cation  model  maximizing  the  coverage  of  ser-
vice, called Maximal Covering Location Problem
(MCLP) has been used to account for accessibility
to primary health care services. The MCLP model
introduced by Church and ReVelle (1974) is de-
signed  to  maximize  the  demand  for  service  as-
signed to a selected number of service sites with-
in  a specified  distance.  Traditionally,  the  model
has been used to find an optimal subset of service
sites from the set of all possible service sites (Ger-
rard et al. 1997, Oppong, Hodgson 1994). In this
study,  the  model  was  used  in  a non-traditional
way  by  employing  all  existing  service  sites  into
the allocation of demand, thus effectively forcing
the model algorithm to select all existing service
sites and then assign the demand to the sites in

a manner that would maximize the total assigned
demand,  and  hence  the  coverage  of  service  de-
mand.

2.1. Model formulation

A  mathematical  formulation  of  the  MCLP  is

as follows:
Maximize

Subject to:

1)

2)

for all i ∈ I

3)  xj = (0,1) for all j ∈ J
4)  yi = (0,1) for all i ∈ I
where:
I = the set of demand locations,
J = the set of service sites,
Ni = {j ∈ J | dij ≤ S}; the set of service sites j that
can reach demand location i within the maximal
service distance S,
S  =  the  distance  beyond  which  a demand  loca-
tion  is  considered  “uncovered”  (the  value  of  S
can be chosen differently for each demand loca-
tion if desired),
dij = the shortest distance from location i to loca-
tion j;
xj  =  {1  if  a  service  is  allocated  to  site  j,  0  other-
wise};
yi  =  {1  if  a service  is  allocated  to  site  i,  0  other-
wise},
ai = service demand in location i,
p = the number of service facilities to be located.

The  model’s  objective  is  to  maximize  the
amount  of  covered  demand.  Constraint  (1)  en-
sures that demand is covered (allocated to point
of service) if there is at least one service location
available  within  the  admissible  service  distance
S. Constraint (2) requires that p service locations
be  selected  (the  p  number  is  set  by  a modeler).
Constraints  (3)  and  (4)  serve  as  binary  integer
restrictions on model location (xj) and allocation
(yi)  variables.  The  MCLP  model  can  be  solved
on a transportation network, where the network
nodes represent locations of demand and service
centers, and the network links represent linkag-
es between the nodes. Each of the network links

42

PIOTR JANKOWSKI, BLAKE BROWN

has some defined impedance (e.g. travel time or
distance) that represents the separation between
nodes.  The  total  impedance  between  each  de-
mand node and  each  service  node  is  defined as
the  total  impedance  encountered  between  the
two  nodes  while  traveling  the  shortest  distance
over  the  network.  A demand  node  (location)  is
considered covered if it is within some user spec-
ified S distance to a service node.

MCLP model data requirements

The MCLP model that relies on transportation
network  representation  of  demand  and  service
locations  can  be  conveniently  implemented  and
solved  with  GIS  software  supporting  network
data  model.  To  solve  the  MLCP  model  in  a GIS
environment, three different data sets/GIS layers
are required:
 – a road network as a line layer,
 – locations  of  service  centers  in  a point  layer,

and

 – locations of demand, also in a point layer.

The  network  representation  in  GIS  requires
that  all  demand  and  service  locations  be  con-
nected to the road network in order to correctly
model  the  network  flows.  This  requirement  has
practical  implication  on  data  pre-processing  as
demand  locations,  which  are  customarily  rep-
resented  by  centroids  of  geographical  statistical
units (e.g. census tracts or postal codes), are fre-
quently found off the road network and must be
connected to the network in order to facilitate the
model solution.

Four  different  representations  of  demand
were  used  in  this  study.  They  included,  in  the
progression  from  small  to  large  scale;  census
tract,  census  block  group,  aggregated  block  re-
gion – comprised of contiguous populated blocks
within each census block, and aggregated block
region weighted by the block population. In each
four representations, the demand for health care
services  was  assigned  to  a corresponding  cen-
troid. Figure 1 illustrates various representations
of demand used in the study (cases A, B, E, and
F). Cases C and D, not used in the study, repre-
sent populated census blocks with their centroids
(C) and populated blocks aggregated into regions
(D). These two cases are included in Figure 1 for
illustrative  purpose  to:  (1)  demonstrate  a situa-

tion  common  in  rural  areas  where  some  census
blocks do not have any resident population, and
(2)  explain  how  block  regions  (cases  E  and  F)
were  derived  from  aggregating  the  contiguous,
populated blocks.

Study area

The  MCLP  model  was  applied  to  assess  the
accessibility  to  primary  health  care  services
in  the  U.S.  State  of  Idaho.  In  the  U.S.,  access  to
medical  facilities  is  considered  vital  not  only  to
individuals needing medical care, but also to the
communities  in  which  these  individuals  partic-
ipate.  The  federal  guideline  for  adequate  access
to  primary  care  services  states  that  all  individ-
uals  should  reside  within  a 30-minute  driving
distance (roughly 20 miles under normal condi-
tions with primary roads available or 15 miles in
mountainous terrain with only secondary roads
available)  from  a primary  health  care  facility
(PHCF) (U.S. Department of Health and Human
Services 1993). While this is a laudable goal, it is
often difficult to achieve.

The low population density of most rural ar-
eas, along with a low patient to doctor ratio, re-
sults in a large percentage of the rural population
residing  further  than  30  minutes  from  a health
care  facility.  The  resulting  inequality  in  health
care services between urban and rural residents
has been a matter of concern to federal and state
health officials.

The state of Idaho is a good example of the dif-
ficulties of providing access to health care equal-
ly to all residents. In 2010, Idaho had the second
lowest active physician to population ratio of all
(50) U.S. states and the third lowest active prima-
ry care physician to population ratio, with 184.2
active physicians per 100,000 people, and 67.2 ac-
tive primary care physicians per 100,000 people.
These ratios were far below the national rates of
258.7  active  physicians  per  100,000  people  and
90.5  active  primary  care  physicians  per  100,000
people (Association of American Medical Colleg-
es 2011). The low physician to population ratios
might be explained partially by the low popula-
tion density within the state. In 2010, Idaho was
estimated to have a population density of 19 per-
sons  per  square  mile  (7.34  persons  per  square
km), compared to the estimated national average

HEALTH CARE ACCESSIBILITY MODELING: EFFECTS OF CHANGE IN SPATIAL REPRESENTATION OF DEMAND...

43

Fig. 1. Demand representations used in the study

of 87.4 persons per square mile (33.75 persons per
square km) (U.S. Census Bureau 2010). In order
to improve health care accessibility in rural are-
as like Idaho, it is necessary to know where un-
der-serviced areas exist, or in other words, where
demand for healthcare is unmet.

Location-allocation accessibility modeling can
be used to determine where demand for primary
health care services (PHCS) is unmet. This mode-
ling approach can also be used to determine opti-
mal locations for potential new health care facil-
ities  that  would  reduce  unmet  demand  in  rural
areas. In this paper the former use of location-al-
location accessibility modeling is presented.

Data preparation

The implementation of MCLP model in order
to  calculate  the  amount  of  unmet  demand  for
PHCS  (representing  the  accessibility  to  PHCS)
required population data by sex and age groups
at the block, block group, and census tract levels.
The population data was obtained from the pub-
lically available U.S. Census 2010 Summary File
1. The estimated annual rates of primary health
care  visits  based  on  age  and  sex  were  obtained
from the  Center  for Disease Control (2008).  The
rates  were  then  multiplied  by  the  population
figures for each census enumeration unit (block,

44

PIOTR JANKOWSKI, BLAKE BROWN

Fig. 2. Tract model: distance vs. demand

block group, or tract) to arrive at the estimate of
demand  for  primary  health  care  services.  De-
tailed road network coverage in a GIS file format
(ESRI’s line feature layer) was secured from Ida-
ho Department of Transportation. Finally, point-
based  GIS  data  layer  (ESRI’s  shape  file  format)
containing information regarding the locations of
all primary health care facilities in Idaho and the
number of primary care hours they can provide
was obtained from Idaho Department of Health
and Welfare. The estimated number of visits per
year  was  then  calculated  for  all  primary  health
care facilities using the U.S. Public Health Service
standard of 4,200 visits per year for primary care
physicians and 2,100 visits per year for midlevel
providers.  This  calculation  yielded  the  estimate
of service supply for each primary health care fa-
cility in Idaho.

The  MCLP  model  was  implemented  in  GIS
software  (ArcGIS  9.3).  Running  the  model  re-
quired creating a network data layer in GIS with
point-based  demand  locations  (populated  area
centroids) and primary health care service facil-

ities  represented  by  the  network  nodes.  A few
of the block group and aggregated block region
centroids located off the network had to be con-
nected  to  the  network,  in  order  to  maintain  the
network’s  topology.  This  was  accomplished  by
digitizing linear segments ranging in length from
160 m to 805 m (0.1 mile to 0.5 mile). The overall
effect  of  these  artifacts  on  the  modeling  results
was deemed negligible.

Results

The MCLP model was run with four different
representations of demand ranging from census
tract,  through  census  block  group,  aggregated
block region, to aggregated block region weight-
ed by the block population, and with three driv-
ing time constraints; 30 minutes (corresponding
to the federal guideline), 45, and 60 minutes. The
latter  two  driving  time  constraints  were  intro-
duced in order to gain a better understanding of
the amount of unmet demand under the relaxa-

Table 1. Tract model results

Driving time
(min)

Meters

Miles

30
45
60

24,140
36,210
48,280

15.0
22.5
30.0

Met demand:
patient visits

3,179,030
3,513,030
3,778,126

% Met

80.1
88.6
95.2

Unmet demand:
patient visits

% Unmet

787,706
453,702
188,608

19.9
11.4
4.8

HEALTH CARE ACCESSIBILITY MODELING: EFFECTS OF CHANGE IN SPATIAL REPRESENTATION OF DEMAND...

45

Fig. 3. Tract model coverage (dd = driving distance)

tion of the federal guideline. Overall, there were
12  specific  instances  of  the  MCLP  model  repre-
senting  the  combinations  of  scale  of  demand
representation and travel time constraint. These
models are referred to in this paper as determin-
istic  models  (as  opposed  to  predictive  models)
since they were run in order to determine an op-
timal allocation scheme of demand to all existing
service centers rather than to find out, which of
the candidate locations would be selected for sit-
ting new service centers.

As  representation  of  demand  used  in  the
model  moved  from  a low  number  of  enumera-
tion  units  (tract  models)  to  a higher  number  of
enumeration units (weighted and non-weighted

aggregated block models), the amount of unmet
demand for PHCS, representing accessibility, de-
creased. Results of the weighted aggregated block
model, which is assumed to be the most accurate
model because of its potential to more accurately
locate  population/demand,  indicate  that  11.6%
of Idaho’s population is farther than the federal
guideline  of  30  minutes  driving  distance  to  the
nearest primary health care provider. A more de-
tailed presentation of the results follows below.

Tract-based model

Idaho contains 280 census tracts, with an aver-
age census tract size of 772.0 km2 and a standard

46

PIOTR JANKOWSKI, BLAKE BROWN

Fig. 4. Block group model: distance vs. demand

deviation  of  1,994.9  km2.  Each  of  the  three  de-
terministic  tract  models  (30,  45,  and  60  minutes
driving  time  constraint)  was  run  using  a rep-
resentation of demand at the centroid of the tract
resulting in 280 demand points. In the tract mod-
els,  the  average  distance  from  a tract  demand
point to the nearest primary health care facility is
18,415.8 meters (11.44 miles), and the average de-
mand for primary health care services for a tract
is 14,166.9 visits per year.

In Figure 2, all of the 280 tract demand points
are plotted based on their respective distances to
the nearest PHCF and their demand for PHCS.

The tract model at the 30 minute driving dis-
tance  constraint  resulted  in  19.9%  of  the  state’s
demand  for  PHCS  unmet  (80.1  of  the  demand
was  met).  Using  the  45  and  60  minute  driving
distance  constraints  resulted  in  11.4%  and  4.8%
respectively of the demand for PHCS unmet (see
Table 1).

Figure 3 shows the results of the deterministic
tract models. Census tracts that are farther than
60 minutes driving time from the nearest prima-

ry health care service center are shown in black.
Tracts that are between 45 and 60 minutes driv-
ing  distance  from  the  nearest  service  center  are
shown  in  dark  grey.  Tracts  that  are  between  30
and 45 minutes driving distance from the nearest
service center are shown in light grey and tracts
that are within 30 minutes driving distance from
the nearest hospital (tracts that are covered within
the federal guideline) are shown in white. The re-
sulting pattern of accessibility to primary health
care  services,  expressed  by  the  coverage  under
the specific driving time constraints, corresponds
to the distribution of Idaho’s population with the
bulk  of  the  population  located  in  northern  Ida-
ho  (the  region  called  Idaho  Panhandle)  and  in
southern Idaho along the Snake River plane.

Block group model

Idaho contains 952 block groups, with an av-
erage block group size of 226.7 km2, with a stand-
ard deviation of 739.4 km2. The block group mod-
els  were  run  using  a representation  of  demand

Driving time
(min)
30
45
60

Meters

24,140
36,210
48,280

Table 2. Block group model results

Miles

Met demand

% Met

15.0
22.5
30.0

3,401,997.8
3,664,521.3
3,812,745.3

85.8
92.4
96.1

Unmet
Demand
564,736.3
302,212.8
153,988.8

% Unmet

14.2
7.6
3.9

HEALTH CARE ACCESSIBILITY MODELING: EFFECTS OF CHANGE IN SPATIAL REPRESENTATION OF DEMAND...

47

Fig. 5. Block group model coverage

at  the  centroid  of  each  of  the  952  block  groups;
this resulted in 3.4 times the number of demand
points as in the tract models. Manual editing in
GIS was required to properly connect four of the
block group centroid points to the road network.
The average distance from a block group de-
mand location to the nearest primary health care
facility  is  14,592.4  meters  (9.07  miles),  and  the

average demand for primary health care servic-
es for a block group is 4,166.7 visits per year. In
Figure 4 all of the 952 block group demand points
are plotted based on their respective distances to
the nearest PHCF and their demand for PHCS.

The  percentage  of  unmet  demand  for  PHCS
yielded by the block group models at a 30 min-
ute  driving  constraint  is  14.2%  (met  demand  is

Driving time
(min)
30
45
60

Meters

24,140
36,210
48,280

Table 3. Aggregated block model results

Miles

Met demand

% Met

15.0
22.5
30.0

3,527,236.0
3,734,338.3
3,836,851.8

88.9
94.1
96.7

Unmet
Demand
439,497.8
232,395.8
129,882.2

% Unmet

11.1
5.9
3.3

48

PIOTR JANKOWSKI, BLAKE BROWN

Fig. 6. Aggregated block model: distance vs. demand

85.8%).  At  the  45  and  60  minute  driving  times,
7.6% and 3.9% respectively of the state’s demand
for PHCS is unmet (see Table 2).

Figure 5 shows the results of the deterministic
block group model. The pattern of accessibility to
primary health care at the scale of block group is
similar to the pattern at the tract scale (Fig. 3) but
not  identical.  In  the  allocation  pattern  obtained
with the block group models there is a visible ex-
pansion  of  areas  meeting  the  30  and  45  minute
driving time constraints as compared to the allo-
cation pattern produced by the tract models.

Aggregated block model

Idaho contains 1926 aggregated block clusters
(groups  of  contiguous  census  blocks  within  the
existing  census  block  groups).  Using  the  cen-
troids  of  these  aggregated  block  clusters  results
in  roughly  twice  the  number  of  demand  points
present  in  the  block  group  model.  The  aver-
age size of these block clusters is 52.8 km2, with
a standard  deviation  of  188.4  km2.  The  average

distance  from  an  aggregated  block  cluster  de-
mand point to the nearest PHCF is 21,242.5 me-
ters (13.2 miles), and the average demand for pri-
mary health care services for an aggregate block
group  is  2,059.6  visits  per  year.  Manual  editing
in GIS was required to properly connect 68 of the
aggregated  block  cluster  centroids  to  the  road
network. In Figure 6, all of the 1926 aggregated
block group demand points are plotted based on
their  respective  distances  to  the  nearest  PHCF
and their demand for PHCS.

The  percentage  of  unmet  demand  for  PHCS
yielded by the aggregated block group models at
a 30 minute driving constraint is 11.1%. At the 45
and 60 minute driving time constraints, 5.9% and
3.3% respectively of the state’s demand for PHCS
is unmet (see Table 3).

Figure  7  shows  the  results  of  the  aggregat-
ed  block  model.  The  allocation  pattern  at  the
block  scale  reveals  large  unpopulated  areas  in
the  north-eastern,  central,  south-western,  and
south-eastern parts of Idaho, confirming the low
population  density  of  the  state  (7.34  people  per

Table 4. Weighted aggregated block model results

Driving time
(min)
30
45
60

Meters

24,140
36,210
48,280

Miles

Met demand

% Met

15.0
22.5
30.0

3,508,209.8
3,724,111.5
3,887,181.3

88.4
93.9
98.0

Unmet
Demand
458,524.3
242,622.4
79,552.9

% Unmet

11.6
6.1
2.0

HEALTH CARE ACCESSIBILITY MODELING: EFFECTS OF CHANGE IN SPATIAL REPRESENTATION OF DEMAND...

49

Fig. 7. Aggregated block model coverage

square  km).  The  general  pattern  of  the  spatial
distribution of demand for primary health servic-
es, covered by the 30 and 45 minute driving time
constraints,  is  similar  to  the  allocation  patterns
produced  by  the  tract  and  block  group  models.
The difference between the former and the latter
can  be  easily  observed  as  the  pattern  produced
by  the  aggregated  block  model  is  much  more
fragmented  than  the  patterns  produced  by  the
tract and block group models due to small area
size of census block – the fundamental areal unit
used in the aggregate block model.

Weighted aggregated block model

All  the  weighted  aggregated  block  models
used the same number of demand points as the
aggregated block models: 1,926. However, unlike
the aggregate block models that placed demand
at the centroids of the contiguous block clusters,
in  the  weighted  aggregated  block  model,  the
placement of those 1,926 demand points was in-
fluenced (weighted) by the amount of demand in
each  of  the  individual  blocks  that  comprise  the
block  group  clusters,  causing  shift  in  location
of  some  of  the  centroids.  Out  of  1,926  demand
centroids  544  had  no  change  in  their  placement
between  the  non-weighted  and  weighted  ag-

50

PIOTR JANKOWSKI, BLAKE BROWN

Fig. 8. Coverage change from non-weighted aggregated block model to weighted aggregated block model

gregated  block  models.  Of  the  1,382  demand
centroid  that  did  have  a shift  in  placement,  the
average shift was 2,129.6 meters. Figure 8 shows
the  change  in  coverage  from  the  non-weight-
ed  aggregated  block  model  to  the  aggregated
block  model.  Block  clusters  with  negative  val-
ues  showed  a decrease  in  their  degree  of  cov-
erage  from  the  non-weighted  to  the  weighted
block model, block clusters with positive values
showed an increase in their degree of coverage.
A one degree coverage change in Figure 8 corre-
sponds to an increase/decrease by one distance
interval, e.g. from 30 to 45 minutes.

The average distance from a weighted aggre-
gated block cluster demand point to the nearest

primary health care facility is 21,301.6 meters, and
the average demand for primary health care ser-
vices is 2,059.6 visits per year. The percentage of
unmet demand for PHCS yielded by the weight-
ed aggregated block group models at a 30 minute
driving constraint is 11.6% (88.4% of demand is
met). At the 45 and 60 minute driving distances,
6.1% and 2.0% respectively of the state’s demand
for PHCS is unmet (see Table 4).

Figure 9 shows the results of the weighted ag-
gregated block model. Upon a closer inspection,
the  differences  in  the  coverage  pattern  between
the  weighted  and  unweighted  models  emerge.
In  the  weighted  model  there  are  more  aggre-
gated  block  regions  covered  by  the  30  minute

HEALTH CARE ACCESSIBILITY MODELING: EFFECTS OF CHANGE IN SPATIAL REPRESENTATION OF DEMAND...

51

Fig. 9. Weighted aggregated block model coverage

driving  time  from  the  nearest  service  center  in
northern  Idaho  (near  the  border  with  Canada),
north-western  Idaho  (bordering  the  state  line
separating Idaho from Oregon and Washington),
and in the center of the state, than there are in the
unweighted  model.  These  finding,  corroborated
by  Figure  8,  can  be  explained  by  more  accurate
representation  of  demand  distribution  in  the
weighted model than in the unweighted model.

Discussion and conclusion

The  modeling  results  show  that  as  the  rep-
resentation of demand in the MCLP model moved

from a smaller scale/lower number of enumera-
tion  units  (tract  models)  to  a larger  scale/high-
er  number  of  enumeration  units  (weighted  and
non-weighted  aggregated  block  models),  the
amount  of  unmet  demand  for  PHCS  decreased
and  consequently  the  pattern  of  accessibility
improved.  The  tract  model  yielded  the  great-
est  amount  of  unmet  demand.  The  aggregated
block  model  yielded  the  lowest  amount  (except
at  the  furthest  driving  time  constraint),  and  the
weighted aggregated block model yielded slight-
ly  greater  amounts  of  unmet  demand  than  the
non-weighted  aggregated  block  model,  and  it
yielded the least amount of unmet demand at the
furthest driving time constraint. This can be ex-

52

PIOTR JANKOWSKI, BLAKE BROWN

Fig. 10. Results of the models run with four representations of demand. The distances on the horizontal axis represent the
equivalents (in meters) of 30, 45, and 60 minute driving time constraints

plained by the shift of centroids (in the weighted
model) from non-populated to populated blocks.
Figure  10  shows  the  amount  of  unmet  demand
found  in  the  12  deterministic  models  (four  de-
mand  representations  each  at  the  three  driving
time constraints). All models in the study had the
same total demand for PHCS: 3,966,732 visits per
year. It can be seen that the tract model results in
greater amounts of unmet demand at all driving
distance constraints than the other three models.
The results of this study are subject to a num-
ber  of  assumptions  beginning  with  the  driving
time; it is assumed that it takes 30 minutes to drive
15 miles. This assumes that in a rural, mountain-
ous area, typical for much of Idaho, few freeways
exist and roads are narrow, and often windy. This
assumption  does  not  account  for  traffic  conges-
tion,  difficult  intersections,  weather  conditions,
etc.  Another  assumption  was  made  that  all  resi-
dents would travel to their closest primary health
care facility. This may be an acceptable assump-
tion  because  in  many  rural  areas  a secondary
PHCF would likely be quite far away. This study
also assumes that demand exists at the centroids
of enumeration units only and that that demand
travels to service center from that single point. It
is assumed that the Center for Disease Control’s
estimated visits per year for the different age and
sex groups are accurate. It is also assumed that the

conversion  from  PHCF  visit  hours  per  year  into
number of visits per year for each existing PHCF
supply site is accurate.

The major finding of this study with potential
relevance  for  future  studies  of  accessibility,  uti-
lizing  a location-allocation  modeling  approach,
is  that  there  is  a relationship  between  the  scale,
at  which  the  demand  for  service  is  represented
and the level of service accessibility. In the case
of  Idaho,  which  is  predominantly  a rural  state,
this relationship is positive; increasing the scale,
at which the demand is represented, results in an
improved  pattern  of  accessibility.  The  surpris-
ing finding is that the targeted representation of
demand  that  was  achieved  by  means  of  popu-
lation  weighting  did  not  improve  markedly  the
measure of accessibility, with the exception of the
longest driving distance considered (60 minutes).
Future  research  could  explore  the  capabili-
ties  of  dasymetric  mapping  for  improving  the
determination  of  population  location  in  rural,
sparsely  populated  areas  for  use  in  location-al-
location  coverage  models.  Dasymetric  mapping
is a technique used to refine information shown
on  choropleth  maps  by  supplementing  the  data
contained  in  choropleth  maps  with  ancillary
data.  The  ancillary  data  chosen  should  corre-
spond to the information presented in the choro-
pleth map. In this study, for example, the block

HealtH care accessibility modeling: effects of cHange in spatial representation of demand...

53

demand  map  layer  might  be  combined  with  an
ancillary  land-cover  map  that  could  distinguish
developed from undeveloped locations. the use
of dasymetric mapping techniques to determine
locations of demand might allow for a more ac-
curate  placement  of  demand  centroids  within
a populated region.

References

association of american medical colleges, 2011. State Physi-
cian Workforce Data Book. on-line: www.aamc.org/work-
force (accessed 1 may 2013).

brabyn  l.,  skelly  c.,  2002.  modeling  population  access  to
new  Zealand  public  hospitals.  International  Journal  of
Health Geographics 1: 1–9.

burkey m.l., bhadury J., eiselt H.a., 2012. a location-based
comparison of health care services in four U.s. states with
efficiency  and  equity.  Socio-Econnomic  Planning  Sciences
46(2): 157–163.

center for disease control, 2008. National Health Statistics Re-
ports  3:  1–40.  on-line:  www.cdc.gov/nchs/data/nhsr/
nhsr003.pdf (accessed 1 may 2013).

church r., reVelle c., 1974. the maximal covering location
problem. Papers of the Regional Science Association 32: 101–
118.

church r.l., murray a.t., 2009. Business site selection, location

analysis, and GIS. John Wiley, sons, Hoboken.

cromley  e.K.,  mclafferty  s.l.,  2002.  GIS  and  public  health.

guilford press, new york, london.

daskin m., Haghani a., Khanal m., malandraki c., 1989. ag-
gregation effects in maximum covering models. Annals of
Operations Research 18: 115–140.

gerrard  r.,  church  r.,  stoms  d.,  davis  f.,  1997.  selecting
conservation  reserves  using  species-covering  models:
adapting  the  arc/info  gis.  Transactions  in  GIS  2(1):
45–60.

Harper  p.r.,  shahani  a.K.,  gallagher  a.K.,  bowie  c.,  2005.
planning health services with explicit geographical con-
siderations:  a stochastic  location-allocation  approach.
Omega 33(2): 141–152.

Kwan m.-p., Weber J., 2008. scale and accessibility: implica-
tions for the analysis of land use-travel interaction.  Ap-
plied Geography 28: 110–123.

laditka  J.m.,  2004.  physician  supply,  physician  diversity,
and outcomes of primary health care for older persons in
the United states. Health, Place 10(3): 231–244.

langford m., Higgs g., 2006. measuring potential access to
primary healthcare services: The influence of alternative
spatial  representations  of  population.  The  Professional
Geo grapher 58(3): 294–306.

lin  g.,  allan  d.e.,  penning  m.J.,  2002.  examining  distance
effects  on  hospitalizations  using  gis:  a study  of  three
health regions in british columbia, canada. Environment
and Planning a, 34(11): 2037–2053.

lovett a., Haynes r., sunnenberg g., gale s., 2002. car trav-
el  time  and  accessibility  by  bus  to  general  practitioner
services: a study using patient registers and gis. Social
Science and Medicine 55(1): 97–111.

martin  d.,  Williams  H.c.,  1992.  market-area  analysis  and
accessibility to primary health-care centers. Environment
and Planning a, 24(7): 1009–1019.

mitropoulos p., mitropoulos i., giannikos i., 2012. combin-
ing dea with location analysis for the effective consoli-
dation in the health care. Computers, Operations Research.
doi: 10.1016/j.cor.2012.01.008.

oppong J., Hodgson m., 1994. spatial accessibility to health
care facilities in suhum district, ghana. The Professional
Geographer 46(2): 199–209.

parker e.b., campbell J.l., 1998. measuring access to prima-
ry medical care: some examples of the use of geographic
information systems. Health, Place 4(2): 183–193.

rushton g., 1989. applications of location models. Annals of

Operations Research 18: 25–42.

U.s. census bureau, 2010. State, County QuickFacts. on-line:
quickfacts.census.gov/qfd/states/16000.html  (accessed
1 may 2013).

U.s. department of Health and Human services, 1993. Prima-
ry  Medical  Care  Health  Professional  Shortage  Area  (HPSA)
Designation  Criteria.  on-line:  bhpr.hrsa.gov/shortage/
hpsas/designationcriteria/primarycarehpsacriteria.
html (accessed 1 may 2013).

Verter  V.,  lapierre  s.,  2002.  location  of  preventive  Health
care facilities. Annals of Operations Research 110: 123–132.
Wang f., luo W., 2005. assessing spatial and nonspatial fac-
tors for healthcare access: toward an integrated approach
to  defining  health  professional  shortage  areas.  Health,
Place 11: 131–146.

Wang  l.,  2011.  analysing  spatial  accessibility  to  healthcare:
a case study of access by different immigrant groups to pri-
mary care physicians in toronto. Annals of GIS 17(4): 237–251.
Wang l., roisman d., 2011. modeling spatial accessibility of
immigrants  to  culturally  diverse  family  physicians.  The
Professional Geographer 63(1): 73–91.


