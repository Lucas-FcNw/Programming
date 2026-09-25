Stacherl and Sauzet
International Journal of Health Geographics           (2023) 22:34
https://doi.org/10.1186/s12942-023-00358-z

REVIEW

International Journal of
Health Geographics

Open Access

Gravity models for potential spatial
healthcare access measurement: a systematic
methodological review
Barbara Stacherl1 and Odile Sauzet2,3*

Abstract
Background  Quantifying spatial access to care—the interplay of accessibility and availability—is vital for health-
care planning and understanding implications of services (mal-)distribution. A plethora of methods aims to measure
potential spatial access to healthcare services. The current study conducts a systematic review to identify and assess
gravity model-type methods for spatial healthcare access measurement and to summarize the use of these measures
in empirical research.

Methods  A two-step approach was used to identify (1) methodological studies that presented a novel gravity model
for measuring spatial access to healthcare and (2) empirical studies that applied one of these methods in a healthcare
context. The review was conducted according to the PRISMA guidelines. EMBASE, CINAHL, Web of Science, and Scopus
were searched in the first step. Forward citation search was used in the second step.

Results  We identified 43 studies presenting a methodological development and 346 empirical application cases
of those methods in 309 studies. Two major conceptual developments emerged: The Two-Step Floating Catchment
Area (2SFCA) method and the Kernel Density (KD) method. Virtually all other methodological developments evolved
from the 2SFCA method, forming the 2SFCA method family. Novel methodologies within the 2SFCA family intro-
duced developments regarding distance decay within the catchment area, variable catchment area sizes, outcome
unit, provider competition, local and global distance decay, subgroup-specific access, multiple transportation modes,
and time-dependent access. Methodological developments aimed to either approximate reality, fit a specific context,
or correct methodology. Empirical studies almost exclusively applied methods from the 2SFCA family while other
gravity model types were applied rarely. Distance decay within catchment areas was frequently implemented in appli-
cation studies, however, the initial 2SFCA method remains common in empirical research. Most empirical studies used
the spatial access measure for descriptive purposes. Increasingly, gravity model measures also served as potential
explanatory factor for health outcomes.

Conclusions  Gravity models for measuring potential spatial healthcare access are almost exclusively dominated
by the family of 2SFCA methods—both for methodological developments and applications in empirical research.
While methodological developments incorporate increasing methodological complexity, research practice largely
applies gravity models with straightforward intuition and moderate data and computational requirements.

Keywords  Gravity models, 2SFCA, Kernel density, Methodological review, Potential spatial access, Healthcare, Spatial
access measurement

*Correspondence:
Odile Sauzet
odile.sauzet@uni-bielefeld.de
Full list of author information is available at the end of the article

© The Author(s) 2023. Open Access  This article is licensed under a Creative Commons Attribution 4.0 International License, which
permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the
original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or
other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line
to the material. If material is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory
regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this
licence, visit http:// creat iveco mmons. org/ licen ses/ by/4. 0/. The Creative Commons Public Domain Dedication waiver (http:// creat iveco
mmons. org/ publi cdoma in/ zero/1. 0/) applies to the data made available in this article, unless otherwise stated in a credit line to the data.

Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 2 of 22

Introduction
Access  to  healthcare  is  an  important  determinant  of
health outcomes [1, 2]. Ensuring adequate access is there-
fore a central goal of health systems globally [3]. As part
of  that,  achieving  equitable  geographic  distribution  of
healthcare  services—that  is,  spatial  healthcare  access—
is  a  public  health  priority.  Due  to  the  spatial  configura-
tion  of  health  systems,  i.e.,  fixed  and  limited  locations
of  health  facilities  serving  unevenly  and  continuously
distributed populations, there are inherent disparities in
spatial access to healthcare [4]. The extent to which these
disparities manifest depends on the allocation of health-
care  resources  within  a  health  system  [5].  Against  this
background, quantifying spatial healthcare access serves
the  important  aims  of  describing  disparities  in  spatial
access,  informing  healthcare  planning,  and  investigating
effects  on  health  outcomes.  Consequently,  sound  meas-
urement  of  spatial  healthcare  access  is  crucial  for  ade-
quately addressing these aims.

While there is no uniform definition of “access” or “spa-
tial  access”  to  healthcare,  there  are  generally  accepted
concepts of access that are frequently employed in health
research.  Penchansky  and  Thomas  [6]  described  access
as  the  “degree  of  fit”  between  healthcare  providers  and
patients,  identifying  five  distinct  access  dimensions:
availability  (provider  resources;  patient  needs),  acces-
sibility  (distance  to  provider;  mobility),  accommodation
(organization  of  provider  operation;  perception  of  suit-
ability), affordability (charges; ability to pay), and accept-
ability  (practice  characteristics;  attitudes  toward  them).
These  dimensions  were  further  categorized  into  aspatial
(accommodation,  affordability,  acceptability)  and  spa-
tial  (availability,  accessibility)  components  by  Khan  [7].
Importantly,  in  this  conceptualization  of  spatial  access,
availability  and  accessibility  interact  rather  than  coexist.
Lastly,  potential  and  realized  access  were  distinguished
depending  on  whether  actual  utilization  of  health-
care  (realized)  is  investigated,  or  characteristics  of  the
healthcare system (potential) are of interest [4]. Drawing
upon  these  established  conceptualizations,  the  present
research is concerned with potential spatial access.

Regarding  the  measurement  of  the  spatial  component
of access, three general methodological approaches exist:
(1) The spatial proximity approach quantifies travel costs,
e.g., in terms of distance or travel time between provider
and  population  locations.  (2)  The  container  approach
quantifies  the  presence  or  density  of  providers  within  a
predefined  area.  (3) The  spatial  interaction  approach,  or
gravity  model  approach,  quantifies  both  proximity  and
density  of  providers  [8].  Thus,  while  spatial  proximity
focuses  on  accessibility  and  the  container  approach  on
availability,  the  gravity  model  approach  integrates  both.
The  interdependence  of  availability  and  accessibility

is  especially  relevant  in  the  healthcare  context  [7].  For
example,  the  distance  to  the  closest  physician  is  only
relevant  if  the  practice  has  capacity  to  treat  patients.
For  measuring  potential  spatial  access  as  defined  above,
therefore, the gravity model approach is the most suitable
[8].

The  spatial  dimension  of  health  and  healthcare  has
been  on  the  minds  of  researchers  and  health  policy
makers  for  many  years  [9].  Relatedly,  gravity  model
approaches  for  measuring  potential  spatial  access  to
healthcare have a long history in the field of health geog-
raphy  [7,  10].  Joseph  and  Bantock  [10]  first  proposed  a
gravity  model  which  not  only  accounted  for  provider
density and proximity to providers at the same time, but
also integrated the demand intensity by adjusting for the
population size. Almost two decades later, Luo and Wang
[11]  introduced  another  type  of  gravity  model—the
two-step  floating  catchment  area  (2SFCA)  method.  The
2SFCA  method  produces  a  local  spatial  access  measure
relating  health  services  supply  to  population  demand
by  using  floating  catchment  areas  centered  around  pro-
vider  and  population  locations.  Since  then,  many  meth-
odological  developments  to  the  2SFCA  method  have
been  proposed,  e.g.,  incorporating  distance  decay  [12],
variable  catchment  areas  [13],  or  multiple  transporta-
tion  modes  [14].  Gravity  models  in  general  and  2SFCA
methods  in  particular  have  since  become  standard  for
potential  spatial  access  measurement  [9],  being  applied
for  describing  spatial  healthcare  access  (e.g.,  [15–17]),
and evaluating effects on health outcomes (e.g., [18–20]).
Previous efforts to summarize the literature on potential
spatial access measurement include overviews of health-
care access measurement and 2SFCA developments [21,
22], comparative evaluation of modeling choice in gravity
models [23, 24], as well as systematic reviews of empirical
studies applying spatial access measures [25, 26].

Gravity  models  for  healthcare  access  measurement
have seen numerous developments over the years [21]. To
date,  however,  no  systematic  methodological  review  has
been  conducted  to  comprehensively  describe  and  assess
these developments. Yet, to identify the method that best
fits a research question, intuition, merits, and drawbacks
of  each  method  need  to  be  evaluated.  Relatedly,  while
gravity  models  are  widely  used  in  health  research  [9],  it
is  not  clear  which  of  the  methodological  developments
have  caught  on  in  practice  and  for  which  purposes  are
they applied.

The  aim  of  the  current  study,  therefore,  is  to  conduct
a  systematic  review  of  methodological  developments
and  application  studies  on  potential  spatial  healthcare
access  measurement.  It  is  conducted  in  two  stages.  In
the  first  step,  methodological  studies  presenting  novel
developments  of  potential  spatial  healthcare  access

Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 3 of 22

measurement  will  be  identified,  categorized  by  method-
ological  properties,  and  assessed  by  purpose,  complex-
ity, and data requirements. In the second step, empirical
studies  applying  one  of  these  methods  in  the  healthcare
context  will  be  summarized  and  characterized,  illustrat-
ing to what degree the methodological developments are
applied in research practice.

Methods
We  sought  to  identify  (1)  all  studies  that  presented  a
methodological  development  of  a  gravity  model  for
measuring spatial access to healthcare and (2) all empiri-
cal  studies  that  applied  one  of  these  methodological
developments  in  a  healthcare  context.  This  was  done  in
two  steps.  Both  review  steps  were  conducted  accord-
ing  to  the  PRISMA  guidelines  [27].  The  PROSPERO
registration  details,  and  full  review  protocol  are  pub-
licly  available  with  the  PROSPERO  registration  number
CRD42022334001.

Inclusion criteria

The goal was to identify methodological developments in
step 1 and empirical applications in step 2. Our inclusion
criteria  concerning  both  steps  were:  Original  articles  of
peer-reviewed  journals;  In  the  English  language;  Meas-
uring  spatial  healthcare  access;  Using  a  gravity  model
integrating  availability,  accessibility,  supply,  and  demand
dimensions in one single measure. Studies were included
only in a (human) healthcare context, i.e., articles investi-
gating spatial access to food outlets, daycare facilities, or
veterinary  care  facilities  were  excluded.  In  step  1,  addi-
tionally,  articles  were  included  only  if  they  presented  a
methodological development (detailed below). In step 2,
articles were included only if they presented an empirical
application of one of the methods identified in step 1.

To  identify  methodological  developments  (step  1),  we
used  the  method  put  forward  by  Joseph  and  Bantock
[10] as a starting point. They were the first to propose a
gravity  model  in  the  healthcare  context  that  integrated
demand (in addition to supply) factors. We refer to it as
the base gravity model from here onward. It takes on the
following form:

Rj =

Sj
n
i=1Pi ∗ d
(cid:31)

−β
ij

∗
A
i

m
= (cid:31)

j=1Rj ∗ d

−β
ij

where  Sj  is  the  healthcare  capacity  (= supply,  e.g.,  num-
ber of pediatricians) at location  j (e.g., practice address),
Pi is the demand intensity (= population, e.g., inhabitants
below  age  15)  at  location  i  (e.g.,  municipality  centroid),
−β
 is the distance decay function with dij being the dis-
d
ij
tance  friction  (e.g.,  travel  time)  between  population  and
provider  location  and  with β  being  the  distance  friction
parameter.  Rj  is  thus  the  provider-to-population  ratio  at
location  j and A∗
i  is the final spatial access index at popu-
lation location i.

Modifications of the above formulas were considered a
methodological development. Studies that merely altered
the Sj (e.g., full-time equivalents instead of head counts),
Pi (e.g., health needs weighted population instead of gen-
eral  population),  or  dij  (e.g.,  routing  distance  instead  of
Euclidean  distance)  computation  or  plugged  in  different
values  for  the  friction  parameter  were  not  considered
methodological developments.

Search strategy

Step  1:  To  identify  relevant  literature,  the  medical  lit-
erature  databases  EMBASE  (including  MEDLINE)  and
CINAHL  as  well  as  the  multidisciplinary  databases  Web
of  Science  and  Scopus  were  systematically  searched.  We
consulted survey papers and seminal articles in the field
of spatial access measures to develop our search strategy
[7, 8, 28, 29]. The final search cloud was refined through
an iteration of searches. The search strategy for identifi-
cation of articles was conducted using a combined search
cloud within the title and abstract capturing the concepts
gravity  model,  healthcare,  spatial  access,  and  indicator.
The complete search strategy for step 1 is given in Addi-
tional file 1: Appendix A. Searches for literature identifi-
cation in step 1 were conducted in May 2022.

Step  2:  To  identify  empirical  application  studies,  we
used  forward  citation  search  yielding  studies  that  cited
one  or  more  of  the  methodological  developments  from
step 1. Forward citation search options are implemented
in Web of Science, and Scopus, not, however, in EMBASE,
and CINAHL, allowing us to use only two of the databases
in  step  2.  Database  searches  were  amended  with  stud-
ies  that  had  been  excluded  in  step  1  solely  for  not  pre-
senting  a  methodological  development  but  fulfilling  all
other  inclusion  criteria.  Studies  that  had  been  excluded
in step 1 for other reasons (e.g., because no gravity model
was  presented)  were  automatically  excluded  from  the
step 2 search results. Searches for literature identification
in step 2 were conducted in December 2022.

Study selection

Abstracts  of  articles  eligible  for  screening  were  first  de-
duplicated. Second, one reviewer (author one) conducted

 Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 4 of 22

a title screening excluding titles indicating a non-health-
care  context,  non-suitable  article  type  (e.g.,  review,  edi-
torial),  or  not  written  in  English.  Third,  both  reviewers
screened  the  remaining  article  abstracts  and  full  texts.
During  abstract  and  full  text-screening  for  step  1,  the
reviewers were blinded to each other’s decision. Abstract
and  full  text-screening  to  determine  eligibility  in  step  2
was  conducted  by  one  reviewer  (author  one)  and  cross-
checked  by  the  other  reviewer.  Disagreements  between
regarding the inclusion of articles were resolved through
discussion and consensus. The study selection process is
depicted in Fig. 1.

Data extraction and analysis

Data  on  study  characteristics  (title,  authors,  journal,
year,  and  country  of  publication)  and  study  background
(study  area,  care  sector)  were  independently  extracted
by  one  reviewer  (author  one).  Methodological  details
were  extracted  and  classified  by  both  reviewers.  In  step
1,  methodological  development  studies  were  classified
into  novelty  categories.  For  each  novelty  category  the
specific  methodological  change,  intuition,  subsequent
adaptations within the category, purpose, methodological
complexity, and data requirements were assessed. In step
2,  the  application  frequency  for  each  novelty  category
was  assessed  by  identifying  the  specific  methodologi-
cal  developments  used  in  each  application  study.  Addi-
tionally, study characteristics of application studies were
extracted. Lastly, we classified the purpose of the applica-
tion study and determined whether the spatial healthcare
access  indicator  was  computed,  or  secondary  data  was
used. With this approach we (1) characterized the gravity
model-type  methodological  developments  proposed  for
spatial access measurement in a healthcare context; and
(2) synthesized how these models were applied in empiri-
cal research.

Results
Search results

In  review  step  1,  4059  citations  were  retrieved.  After
exclusion  of  1727  duplicates,  1173  titles  were  excluded
because  they  were  out  of  the  scope  of  this  study.  Upon
abstract  and  full  text-screening,  1116  citations  were
excluded  because  they  either  did  not  include  a  gravity
model, were not in the field of healthcare, did not fit the
journal/language  criteria,  or  did  not  constitute  a  meth-
odological  development.  We  resulted  with  a  final  set  of
43  studies  that  presented  gravity  model-type  methodo-
logical  developments  for  measuring  spatial  healthcare
access (Additional file 1: Appendix B).

For  review  step  2,  we  retrieved  2732  citations  via  for-
ward  citation  search  and  amended  them  with  315  cita-
tions  that  had  been  excluded  in  review  step  1  solely

because they did not constitute a methodological devel-
opment.  Next  to  the  exclusion  of  1517  duplicates,  we
additionally  automatically  excluded  203  citations  that
had  been  excluded  in  review  step  1  because  either  the
title was out of scope, the study showed no gravity model,
or  was  not  in  the  healthcare  field.  We  further  excluded
the  43  studies  that  had  been  included  in  step  1,  since
they  were  not  application  studies.  Upon  title  screening,
an  additional  287  studies  were  excluded.  Upon  abstract
and  full  text-screening,  we  excluded  688  studies  that
were lacking either a gravity model or a healthcare focus.
Finally, 309 studies were included in review step 2. These
309 studies contained a total of 346 individual measures
of spatial access to healthcare (Additional file 2).

Review step 1: methodological developments

Starting from the base gravity model, two major concep-
tual  methodological  developments  were  proposed:  The
Two-Step  Floating  Catchment  Area  (2SFCA)  method
[11],  and  the  Kernel  Density  (KD)  method  [30].  From
2004  onward,  methodological  developments  almost
exclusively  built  on  the  2SFCA  method  and  proposed
developments within this family of methods, thus repre-
senting a second generation of gravity model-type meth-
odological developments. First-generation developments
(= Gravity Model Developments) and second-generation
developments  (= 2SFCA  Developments)  are  discussed
separately.

1st Generation developments

Two  major  conceptual  developments  of  the  base  gravity
model were put forward. The 2SFCA and the KD method
are conceptual developments in that 2SFCA employs pre-
defined catchment areas that are floated over population/
provider locations instead of considering all populations/
providers;  and  KD  overlays  a  provider  and  a  population
density layer. Mathematically however, both methods are
simply  special  forms  of  the  base  gravity  model.  In  addi-
tion  to  these  conceptual  developments,  a  small  number
(N = 2) of methodological papers [7, 31] proposed adap-
tations to the base gravity model while staying conceptu-
ally  similar  to  it.  Key  characteristics  of  these  adaptation
studies are presented in Additional file 1: Appendix B.

Two‑step floating catchment area method  Advancement:
Floating catchment areas for determining access.

Method:  Luo  and  Wang  [11]  introduced  the  Two-Step
Floating  Catchment  Area  (2SFCA)  method.  In  the  first
step,  all  population  locations  within  a  predefined  catch-
ment  area  around  each  provider  location  are  searched.
The  provider  capacity  is  divided  by  the  total  population
within  the  catchment  area  to  create  location-specific
provider-to-population  ratios.  In  the  second  step,  all

Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 5 of 22

Fig. 1  Study selection process

 Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 6 of 22

provider  locations  within  the  same  predefined  catch-
ment area around each population location are searched.
The  provider-to-population  ratios  of  all  provider  loca-
tions within the catchment area are summed up to build
the  spatial  access  measure.  Technically  speaking,  the
2SFCA is a special case of the gravity model proposed by
Joseph  and  Bantock  [10]  using  a  binary  distance  decay
function.  The  function  takes  on  a  value  of  1  if  the  pro-
vider/population  point  lies  within  the  predefined  catch-
ment  area  (complete  access  assumed),  and  a  value  of  0
if it does not (no access assumed). While the base grav-
ity model considers all providers/populations within the
system,  the  2SFCA  method  introduces  the  notion  that
beyond  a  certain  threshold,  providers  are  not  relevant
to  the  population  anymore.  Hence  those  providers  are
deemed not accessible. The reduction of providers/popu-
lations considered to only those within a catchment area
implies a reduction of methodological and computational
complexity. This in turn allows for more complexity and
precision  in  the  distance  computation.  Instead  of  the
Euclidean distance, Luo & Wang use the estimated short-
est path travel time along a road network. Interpretation
of the 2SFCA access measure is in terms of providers per
population,  making  the  measure  easily  understandable.
Adding up all 2SFCA values in the system results in the
total number of providers. However, the 2SFCA measure
also  has  drawbacks.  Namely,  the  catchment  area  deline-
ation is arbitrary. Within the catchment area, all provid-
ers are treated as equally accessible. The binary distance
decay implies sharp edges where providers that are very
close  to  each  other  can  be  treated  as  very  differently
accessible.

Purpose: Approximating reality.
Methodological  complexity:  Introducing  catchment
areas  and  considering  only  those  locations  within  a
catchment  area  implies  a  reduction  of  methodological
complexity.

Data requirements: No additional data requirements.

Kernel  density  method  Advancement:  Overlying  pro-
vider and population density layers.

Method:  Guagliardo  et  al.  [8]  introduced  the  Ker-
nel  Density  (KD)  method,  which  overlays  provider  and
population  density  layers  to  compute  the  spatial  access
measure.  Conceptually,  this  measure  is  thus  closer  to  a
provider-to-population ratio than the base gravity model
or the 2SFCA. The KD method employs the Kernel Den-
sity function to create a density layer of providers out of
the  (in  reality)  discretely  allocated  provider  points.  This
can  be  understood  as  a  smoothing  of  provider  points
over a raster grid. Thus, the reach of providers, and hence
the  distance  decay,  is  considered  via  the  Kernel  Density
function. Similarly, a population density layer is created,

smoothing  out  population  data  to  mimic  the  real  popu-
lation distribution. Overlaying those layers, i.e., dividing
the provider by the population layer results in a provider-
to-population  ratio  for  the  grid  cells.  In  the  final  access
index,  the  provider-to-population  ratios  of  all  grid  cells
within the target area are averaged. Thus, the KD spatial
access  measure  represents  a  localized  provider-to-pop-
ulation  ratio.  The  methodological  simplicity  and  inter-
pretability  are  clear  advantages  of  the  KD  method.  One
downside of the KD method is that for creating the den-
sity  layers,  it  requires  somewhat  arbitrarily  choosing  a
cone radius. Another one is that the KD method does not
integrate real travel behavior as travel friction is only con-
sidered  in  terms  of  Euclidean  distances.  However,  com-
pared to the base gravity model and the 2SFCA method,
the  KD  method  has  the  clear  advantage  of  avoiding  the
circularity  issue  of  other  gravity  models.  Provider  avail-
ability  in  Joseph  and  Bantock  [10]  and  Luo  and  Wang
[11] are adjusted according to the potential demand (i.e.,
size)  of  the  surrounding  population.  One  might  argue,
that  for  the  estimation  of  this  potential  demand  of  the
surrounding population, one would have to adjust for the
potential  availability  of  the  providers  surrounding  those
population  points.  Taking  this  line  of  argument  further,
it becomes circular. By overlaying density layers, the KD
method does not suffer from this circularity issue.

Purpose: Approximating reality.
Methodological  complexity:  Introducing  provider  and
population density layers implies a reduction of method-
ological complexity as it is conceptually close to a stand-
ard provider-to-population ratio.

Data requirements: No additional data requirements.

2nd Generation developments (2SFCA family)
There was a plethora (N = 39) of methodological develop-
ments within the 2SFCA family. We classified them into
novelty  categories  for  which  we  present  intuition,  first
study  introducing  the  type  of  development,  following
adaptations within the category, purpose, methodological
complexity, and data requirements. Additionally, all indi-
vidual studies presenting a methodological development
within the 2SFCA method family are given in Additional
file 1: Appendix B.

Distance  decay  within  catchment  area  Advancement:
Introducing  a  distance  decay  function  within  the  catch-
ment area.

Intuition: A major drawback of the 2SFCA method by
Luo  and  Wang  [11]  is  the  binary  distance  decay  func-
tion  treating  all  providers  within  the  catchment  area
as  completely  accessible  and  all  providers  outside  the
catchment  area  as  not  accessible.  Realistically,  farther
away providers are less likely to be visited. To mitigate

Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 7 of 22

this  problem  and  to  incorporate  the  intuition  that
within  a  catchment  area,  not  all  providers  are  equally
accessible,  distance  decay  within  the  catchment  area
was introduced.

First study: Luo and Qi [12] built on the 2SFCA method
and  introduced  distance  decay  within  the  catchment
area.  This  was  done  to  depict  travel  impedance  more
realistically. Specifically, the catchment area was split into
several catchment radii, with each section being assigned
a  different  weight.  Thus,  population  points  distant  from
the provider are weighted less and thus contribute less to
the  potential  demand.  Provider  points  distant  from  the
population  location  equally  are  weighted  less  and  hence
contribute  less  to  the  spatial  access  measure.  As  a  dis-
crete average weight (computed by a Gaussian function)
is  assigned  to  all  points  lying  within  a  sub-radius,  this
type  of  distance  decay  is  considered  a  discrete  stepwise
distance decay.

Development within category: Several studies have sug-
gested  different  functional  forms  of  the  decay  function.
This includes continuous functions (e.g., power function,
Gaussian function) and a combination of a stepwise and
a  continuous  function.  Schuurman  et  al.  [32]  for  exam-
ple suggested no distance decay for an initial catchment
radius,  linear  decay  for  the  next  catchment  radius,  and
full decay (= no access) after the third threshold. Jin et al.
[33] further introduced a decay function that is depend-
ent  on  the  provider  specialization  degree  (i.e.,  they
assume  slower  distance  decay  for  more  specialized  pro-
viders).  Tao  et  al.  [34]  assumed  that  the  distance  decay
function  varies  by  rurality  (i.e.,  they  assume  slower  dis-
tance  decay  in  rural  areas).  The  developments  concern-
ing distance decay have been synthesized by Wang [21],
who  suggested  a  generalized  2SFCA.  Instead  of  specify-
ing a particular distance decay function, the generalized
2SFCA introduced a general decay function, leaving it up
to  the  researcher  to  decide  which  empirical  functional
form  fits  best  their  context  and  assumptions  about  dis-
tance decay. The generalized 2SFCA consolidated previ-
ous  measures,  formalizing  the  general  principle  used  by
other authors.

Purpose: Approximating reality.
Methodological  complexity:  Introducing  a  (stepwise,
continuous,  or  hybrid)  distance  decay  function  within
the catchment area moderately increases modeling com-
plexity.  In  addition  to  determining  for  each  provider-
population  pair  whether  they  are  within  the  catchment
area  threshold  distance,  a  distance  decay  function  must
be  applied  for  each  provider-population  pair  within  the
catchment area.

Data requirements: No additional data requirements.

Variable  catchment  area  sizes  Advancement:  Variable
catchment size definition.

Intuition:  Luo  and  Wang’s  [11]  2SFCA  formulation
assumed  fixed  and  uniform  catchment  area  sizes  for  all
provider  and  population  locations.  However,  urban  and
rural  populations  might  have  a  differing  willingness  to
travel  due  to  the  presence  of  nearby  providers.  In  other
words,  when  providers  are  far  away,  patients  will  travel
farther to get access to healthcare; when many providers
are nearby, the willingness to travel will be lower.

First  study:  Luo  and  Whippo  [13]  introduced  variable
catchment sizes to the 2SFCA method (= V2SFCA). This
was  done  to  reflect  differences  in  surrounding  provider
density  leading  to  differences  in  accepted  initial  travel
time.  They  proposed  to  dynamically  determine  catch-
ment  sizes  by  increasing  a  catchment  size  until  a  pre-
defined  provider-to-population  threshold  is  met.  This
specification  cannot  result  in  population  locations  with
zero  spatial  access.  This  fully  variable  catchment  size
depends  both  on  the  provider  capacity  and  the  popu-
lation  density  and  results  in  unique  catchment  sizes
for  each  provider/population  location.  More  generally
speaking, in the variable 2SFCA the catchment threshold
is  a  function  of  certain  characteristics  of  the  provider/
population location.

Development  within  category:  Reflecting  differences
in  catchment  thresholds  for  urban  and  rural  popula-
tions  has  been  conducted  in  different  ways.  While  Luo
and Whippo [13] defined catchment sizes dependent on
a  base  provider-to-population  threshold,  McGrail  and
Humphreys [35] chose to define discrete catchment sizes.
They suggested to assign one of five catchment area sizes
to  a  provider/population  location  based  on  the  rurality
classification  of  that  location.  Variable  catchment  sizes
have  not  only  been  implemented  to  depict  urban  and
rural  differences,  but  also  to  account  for  varying  reach
depending  on  provider  specialization  degrees.  Such
approaches reflect that more specialized or larger provid-
ers serve a larger population. Kim et al. [36] for example
used  the  number  of  physicians  per  hospital  as  determi-
nant for the catchment size, while Tao et al. [37] defined
the catchment area size as dependent on the level of hos-
pital specialization.

Purpose: Approximating reality.
Methodological complexity: Introducing variable catch-
ment  sizes  only  slightly  increases  modeling  complexity.
The criterion for determining whether a provider-popu-
lation pair is within a catchment area shifts from a single
condition  (e.g.,  less  than  30  min  driving  time)  to  com-
bined  conditions  (e.g.,  less  than  30  min  driving  time  for
population  in  urban  area  and  less  than  60  min  driving
time for population in rural area).

 Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 8 of 22

Data requirements: Additional data may be required in
some  cases,  e.g.,  a  rurality  classification  for  all  provider
and population locations. Additional data is not required
when  catchment  sizes  are  determined  conditional  on  a
base provider-to-population threshold.

Outcome  unit  modification  Advancement:  Outcome
unit modification to interpretation in relative terms.

Intuition:  Accounting  for  distance  decay  within  a
catchment area (like in the generalized 2SFCA) requires
the  definition  of  a  distance  impedance  parameter.  Since
empirical  verification  of  distance  disutility  is  difficult,
the  choice  of  the  impedance  parameter  is  somewhat
arbitrary. Yet, different values of the distance impedance
parameter  can  vastly  alter  the  magnitude  of  the  spatial
access measure.  To account for this uncertainty, an out-
come unit modification was proposed.

First study: Wan, Zhan et al. [38] proposed to compute
a  spatial  access  ratio  (SPAR)  from  the  2SFCA  measure.
The  SPAR  is  defined  as  the  ratio  between  a  population
location’s  spatial  access  measure  and  the  mean  spatial
access  measure  of  all  population  locations.  SPAR  thus
represents  a  dimensionless  relative  outcome  measure
rather  than  an  absolute  provider-to-population-like
measure. SPAR is stable to different distance impedance
parameter  specifications  and  useful  for  mapping  when
no  absolute  outcome  values  are  needed.  This  develop-
ment comes at no cost in terms of data requirements or
computation.

Development  within  category:  No  further  studies  sug-

gested an outcome unit modification.
Purpose: Correcting methodology.
Methodological  complexity:  Introducing  an  outcome
unit  modification  does  not  increase  modeling  complex-
ity. An additional step is required to compute the Spatial
Access  Ratio.  However,  it  requires  simply  dividing  the
population  location’s  access  index  by  the  mean  access
measure  of  all  population  locations,  thus  not  noticeably
adding complexity.

Data requirements: No additional data requirements.

Provider competition  Advancement: Correcting demand
overestimation  by  introducing  a  provider  competition-
based selection weight.

Intuition:  In  the  first  step  of  2SFCA,  all  population
locations within a provider’s catchment area are consid-
ered  to  contribute  to  the  potential  demand  at  that  pro-
vider  location.  Thus,  population  points  may  be  counted
fully  as  contributing  to  the  potential  demand  at  sev-
eral  provider  locations,  implying  an  overestimation  of
demand.  However,  individuals  do  not  visit  all  accessible
providers, but rather choose one provider. To correct the
implicit  demand  overestimation,  a  provider  competition

scheme  was  suggested. This  scheme  assigns  populations
based on a choice probability, reflecting that populations
face several provider options.

First  study:  Wan,  Zou,  and  Sternberg  [39]  proposed
the three-step floating catchment area method (3SFCA)
which  computes  a  distance  impedance-based  selection
weight  for  each  provider-population  pair  in  an  addi-
tional  first  step. This  approach  considers  all  surround-
ing providers (and distances to them) a population can
choose from in its catchment area. As such, the poten-
tial demand more accurately depicts the actual demand
on  a  provider.  The  closer  a  provider  is  to  a  popula-
tion location, the more likely the population will be to
visit the provider; hence the selection weight assigns a
larger  share  of  the  population  to  closer  providers.  The
additional  step  is  computed  using  a  Huff-model  based
selection weight.

Development within category: While the initial 3SFCA
proposed  by  Wan,  Zou,  and  Sternberg  [39]  considered
only distance impedance as determinant of the selection
probability,  other  developments  incorporated  additional
factors  into  the  provider  competition  scheme.  Luo  [40]
amended the selection weight computed in the first step
by including provider capacity in addition to the distance
impedance  function.  Other  functions  for  the  computa-
tion of the selection probability have also been proposed,
incorporating a plethora of factors determining the selec-
tion  weight  [e.g.,  41–43].  Notably,  Paez,  Higgins,  and
Vivona  [44]  showed  that  standard  2SFCA  methods  not
only overestimate demand, but also overestimate supply
as  the  provider  capacity  computed  in  the  provider-to-
population ratio may be counted to the final access score
at several population locations. Thus, instead of comput-
ing a selection probability to be applied in the provider-
to-population  ratio,  Paez  et  al.  [44]  fully  proportionally
allocated population and providers to account for poten-
tial demand and supply inflation. This is done by stand-
ardizing  the  distance  decay  weights  within  the  distance
decay  function  in  each  catchment  area  to  1.  Hence  the
total  level  of  demand  and  supply  within  the  system  are
preserved in this measure.

Purpose: Correcting methodology.
Methodological  complexity:  Introducing  a  selection
weight  heavily  increases  modeling  complexity.  An  addi-
tional  first  step  is  required  to  compute  the  selection
weight.  In  addition  to  computing  a  provider-to-popula-
tion  ratio  at  each  provider  location  considering  all  sur-
rounding  population  locations,  a  selection  weight  for
each  provider-population  pair  considering  all  surround-
ing  provider  locations  must  be  computed.  This  almost
doubles computational intensity.

Data requirements: No additional data requirements.

Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 9 of 22

Local and global distance decay  Advancement: Correct-
ing  for  sub-optimally  configured  healthcare  system  by
modeling local and global distance decay.

Intuition:  Delamater  [45]  showed  that  the  standard
configuration of 2SFCA methods only considers relative
distances  within  a  catchment  area  and  ignores  absolute
distances.  That  is,  only  the  relative  distance  differences
among providers within the population’s catchment area
impact  the  final  access  score,  not  the  absolute  distance
differences  across  catchment  areas.  In  a  simple  exam-
ple,  population  locations  with  only  one  provider  within
the catchment area would receive the exact same spatial
access score, irrespective of whether the provider is close
by or far away. This implicitly assumes optimally config-
ured  healthcare  systems,  where  population  locations  do
not  face  different  absolute  distances  to  providers.  Argu-
ably, even if two population locations have the same pro-
vider  availability  within  their  catchment  area,  we  might
consider a population location from which those provid-
ers are farther away to have poorer accessibility.

First  study:  Delamater  [45]  put  forward  a  methodo-
logical development to correct for sub-optimally config-
ured  healthcare  systems  as  they  are  found  in  reality.  By
introducing an additional distance decay function in the
first  step,  the  method  produces  specific  pairwise  supply
ratios  rather  than  single  supply  ratios  per  provider  and
thus  accounts  for  both  relative  and  absolute  distances.
Conceptually,  this  can  be  understood  as  having  a  local
distance decay function (= relative distances) and a global
distance decay function (= absolute distances).

Development  within  category:  Bauer  and  Groneberg
[46]  further  advanced  this  method  by  using  two  differ-
ent functional forms for the local and the global distance
decay function. Assumptions about the nature of the rela-
tive distance decay within the catchment area are formal-
ized in the local decay function, while assumptions about
the  role  of  absolute  distance  are  captured  in  the  global
distance decay function. This allows to differentially con-
ceptualize the role of relative and absolute distances.

Purpose: Correcting methodology.
Methodological  complexity:  Introducing  an  additional
distance decay function slightly increases modeling com-
plexity, more so, if different functional forms are used for
the local and global distance decay functions.

Data requirements: No additional data requirements.

Subgroup‑specific  access  Advancement:  Subgroup-spe-
cific  access  measure  for  selective  population-provider
pairing.

Intuition:  Factors  other  than  spatial  impedance  and
provider  capacity  have  an  impact  on  whether  an  indi-
vidual  can  access  a  provider,  i.e.,  not  all  providers  are
available  to  all  populations  equally.  This  might  be  due

to  e.g.,  language  restrictions,  insurance  plans,  or  refer-
ral  systems.  In  turn,  subgroups  of  individuals  compete
for  a  subgroup  of  providers,  both  of  which  may  exhibit
spatial  variation.  Standard  2SFCA  methods,  however,
assume equal non-spatial access for all populations to all
providers.

First study: Wang [47] proposed an additional step after
computing  the  access  measure  for  quantifying  group-
specific access of Chinese immigrants to ethnic Chinese
physicians.  This  was  done  by  considering  the  relative
abundance  of  ethnic  Chinese  physicians  as  well  as  the
share  of  Chinese  immigrants  within  the  catchment  area
of a population location. Thus, demand competition of a
population subgroup for a provider subgroup is reflected.
Development  within  category:  Other  context-specific
methodological  developments  also  reflected  that  not  all
providers  are  available  to  all  populations  equally.  Xiao
et al. [48] integrate referrals within a hierarchical health-
care system where higher specialized providers can only
be  accessed  upon  referral.  Shao  and  Luo  [49]  incorpo-
rated  group-specific  healthcare  access  resulting  from
different health insurance plans. In their method, a pro-
vider’s  resources  are  only  counted  toward  the  accepted
insurance  plan  of  a  population  subscribed  to  that  same
plan. The resulting measure yields access scores by insur-
ance plan.

Purpose: Fitting context.
Methodological  complexity:  Introducing  a  subgroup-
specific  access  index  heavily  increases  modeling  com-
plexity.  An  additional  third  step  is  required  to  compute
the  subgroup-specific  index.  In  addition  to  computing
the  standard  2SFCA  measure,  a  weight  considering  all
surrounding  subgroup-specific  provider  and  population
locations  must  be  computed.  This  almost  doubles  com-
putational intensity.

Data  requirements:  Additional  data  are  required  for
information  on  subgroup-specific  provider  and  popula-
tion shares at each location.

Multiple  transportation  modes  Advancement:  Multiple
transportation modes.

Intuition:  Standard  2SFCA  methods  considered  one
transportation  mode  only—typically,  travel  time  along  a
road  network  by  private  vehicle  was  used  to  model  dis-
tance  impedance.  This  is  a  simplified  assumption.  For
one, traveling by public transport or by foot implies dif-
ferent  travel  times  and  thus  accessibility.  For  another,
population  locations  differ  in  terms  of  mobility,  i.e.,  the
share of individuals using each mode of transport.

First study: Mao and Nekorchuk [14] suggested a multi-
mode 2SFCA which incorporates multiple transportation
modes that individuals might use to reach a provider. The
method captures several transport mode options as well

 Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 10 of 22

as  varying  mobility  by  population  location.  Specifically,
transport-mode specific catchment sizes are defined (e.g.,
30-min  travel  time  by  private  vehicle  and  60-min  travel
time  by  public  transit).  In  the  first  step,  for  each  trans-
port  mode,  only  population  points  within  the  mode-
specific catchment are considered, and only the assumed
mode-using share of the population is counted to build a
mode-specific provider-to-population ratio. These mode-
specific ratios are summed up to form the full provider-
to-population  ratio.  The  same  approach  is  used  for  the
second  step,  additionally  weighting  the  mode-specific
reachable  provider  ratios  by  the  corresponding  mode-
using  share  of  the  population  at  the  location.  As  such,
this  measure  can  also  account  for  competition  among
populations with differing mobility.

Development  within  category:  Producing  a  more  indi-
vidualized  measure,  Langford,  Higgs,  and  Fry  [50]  sug-
gested  computing  separate  access  measures  for  each
transport  mode.  When  computing  provider-to-popu-
lation  ratios  in  the  first  step,  all  transportation  modes
are  considered  (just  like  in  the  Mao  &  Nekorchuk  [14]
method).  In  the  second  step,  only  the  mode-specific
reachable provider ratios are summed up. This allows to
incorporate  demand  competition  for  providers,  while
producing  travel  mode-specific  scores.  Zhou  et  al.  [51]
incorporated  different  travel  mode  choice  probabilities
for  each  provider-to-population  pair  instead  of  simply
using different fractions of mode users by transport type
per population location, thus producing a more detailed
measure.

Purpose: Approximating reality.
Methodological complexity: Introducing multiple trans-
portation  modes  heavily  increases  modeling  complexity.
For  each  provider-population  pair,  travel  distance/time
must be computed for at least two modes of transporta-
tion.  Additionally,  demand  intensity  is  weighted  by  the
mode-specific  user  shares  at  each  population  location.
This at least doubles computational intensity.

Data  requirements:  Additional  data  are  required  for
information on travel distance/time by transport mode as
well as data on mode-specific user shares for each popu-
lation location.

Time‑dependent  access  Advancement:  Spatio-temporal
access measure using time-varying parameters.

Intuition:  Previous  2SFCA  methods  were  static  in  the
sense that no temporal variability of the input parameters
was  considered.  Individuals  might  face  greatly  varying
spatial access depending on the time of day or year due to
e.g., traffic congestion, opening hours, or road conditions.
Spatio-temporal  access  measures  explicitly  model  tem-
poral  variability,  producing  a  range  of  access  measures

rather than relying on one static measure which reflects
spatial access only at a specific time point.

First study: Ma et al. [52] introduced a temporal dimen-
sion in their 2SFCA measure by incorporating time-var-
ying travel times. Using real-time traffic data at different
time  points  within  the  same  day,  they  captured  varying
traffic congestion. Thus, the travel impedance becomes a
time-dependent parameter in this method. While previ-
ous  2SFCA  measures  frequently  assumed  average  travel
speeds  for  road  segments  to  compute  travel  times,  this
method  relies  on  routing  algorithms  using  empirical
travel  speeds.  Importantly,  this  approach  does  not  pro-
duce  one  combined  static  access  measure.  Instead,  it
gives a range of access measures that depict spatial access
at different time points.

Development  within  category:  Instead  of  looking  at
within-day  variability,  Song  et  al.  [53]  incorporated  sea-
sonal  differences  in  average  travel  times  due  to  varying
precipitation  levels.  Further  developments  incorporated
time-varying  demand-size  [54]  and  time-varying  sup-
ply size [55]. The former aims to reflect variable demand
intensity  due  to  commuting  behavior  by  using  mobile
phone GPS data [54]. The latter reflects variable provider
availability throughout the day by incorporating provider
opening hours [55].

Purpose: Approximating reality.
Methodological complexity: Methodological complexity
is not affected by this development as the basic configu-
rations  of  the  2SFCA  method  remain  unchanged.  How-
ever,  as  this  development  requires  generating  a  range  of
access measures with different parameter inputs compu-
tational intensity will be heavily affected.

Data  requirements:  Additional  data  are  required  for
information  on  time-varying  travel  times,  population
size, or provider opening hours (Table 1).

Review step 2: application studies
Study characteristics

The  309  application  studies  entailed  a  total  of  346  indi-
vidual measures that constituted applications of the ear-
lier  identified  methodological  developments.  Since  the
application  of  specific  methods  is  of  interest  here,  the
following  numbers  refer  to  individual  measures  rather
than  studies.  Frequency  statistics  on  the  characteristics
of access measures are given in Table 2. An overview of
the  measures  applied  by  methodological  development
type  is  given  in  Fig.  2.  Most  healthcare  access  meas-
ures were applied either in an Asian (N = 160; 46%) or a
North  American  (N = 136;  39%)  healthcare  setting,  with
USA  (N = 109),  China  (N = 91),  and  Canada  (N = 27)
being the most frequently investigated countries. In 45%
of  the  application  cases  (N = 157),  spatial  access  to  pro-
viders  within  the  primary  care  sector  was  investigated,

Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 11 of 22

s
t
n
e
m
e
r
i
u
q
e
r
a
t
a
D

l

y
t
i
x
e
p
m
o
C

e
s
o
p
r
u
P

†
a
l
u
m
r
o
F

i

s
e
d
u
t
S

t
n
e
m
e
c
n
a
v
d
A

y

l
i

m
a
f

A
C
F
S
2
e
h
t
n

i

s
t
n
e
m
p
o
e
v
e
d

l

l

i

l

a
c
g
o
o
d
o
h
t
e
M

1
e
l
b
a
T

y
r
o
g
e
t
a
C

a
t
a
d

l

a
n
o
i
t
i
d
d
a
o
N

e
s
a
e
r
c
n

i

e
t
a
r
e
d
o
M

i

g
n
i
t
a
m
x
o
r
p
p
A

d
e
r
i
u
q
e
r

l

-
x
e
p
m
o
c
g
n

i
l

e
d
o
m

f

o

y
t
i
l

a
e
R

r

W
∗

i

P
}

j

S

r
d
≤

j
i

d
{
∈

i

(cid:31)
(cid:31)

r

y
t
i

r

W
∗

j

R
}

r

d
≤

j
i

d
{
∈

j

(cid:31)
(cid:31)

r

8
1
0
2

,
.
l

a
t
e
a
v
o
n
k
h
c
a
P

l

i

•

=

j

R

=
∗i
A

]
2
3
[
0
1
0
2

,
.
l

a
t
e
n
a
m
r
u
u
h
c
S
•

,

s
y
e
r
h
p
m
u
H
&

l
i

a
r
G
c
M

•

:

y
r
o
g
e

]
7
6
[
0
1
0
2

,
i

a
D

•

]
2
7
[
9
0
0
2

a
e
r
a

-
t
a
c
n
h
t
i

i

w

t
n
e
m
p
o
e
v
e
D

l

t
n
e
m
h
c
t
a
c
e
h
t
n
h
t
i

i

w

]
2
1
[
9
0
0
2

,
i

Q
&
o
u
L
A
C
F
S
2
E
•

y
a
c
e
d
e
c
n
a
t
s
i
d

f

o

a
e
r
A
t
n
e
m
h
c
t
a
C
n
h
t
i

i

w

:

y
d
u
t
s

t
s
r
i
F

n
o
i
t
c
u
d
o
r
t
n

I

y
a
c
e
D
e
c
n
a
t
s
i
D

l

a
n
o
i
t
i
d
d
a
e
r
i
u
q
e
r
y
a
M

-
d
o
m

f

o
e
s
a
e
r
c
n

i

t
h
g

i
l

S

i

g
n
i
t
a
m
x
o
r
p
p
A

a
t
a
d

l

y
t
i
x
e
p
m
o
c
g
n

i
l

e

y
t
i
l

a
e
R

)
β

,

j
i

d
(
f

∗

j

R
}

)

j

R
(
x
d
≤

j
i

d
{
∈

j

(cid:31)

)
β

,

j
i

d
(
f

∗

i

P
}

j

S

)

i

P
(
x
d
≤

j
i

d
{
∈

i

(cid:31)

=

j

R

=
∗i
A

a
t
a
d

l

a
n
o
i
t
i
d
d
a
o
N

-
d
o
m

f

o
e
s
a
e
r
c
n

i

o
N

-
d
o
h
t
e
M
g
n
i
t
c
e
r
r
o
C

d
e
r
i
u
q
e
r

l

y
t
i
x
e
p
m
o
c
g
n

i
l

e

y
g
o
o

l

)
β

,

j
i

d
(
f

∗

j

R
}

0
d
≤

j
i

d
{
∈

j

(cid:31)

)
β

,

j
i

d
(
f

∗

j

S

i

P
}

0
d
≤

j
i

d
{
∈

i

(cid:31)

=

j

R

=
∗i
A

a
t
a
d

l

a
n
o
i
t
i
d
d
a
o
N

-
d
o
m

f

o
e
s
a
e
r
c
n

i

h
g
H

i

-
d
o
h
t
e
M
g
n
i
t
c
e
r
r
o
C

d
e
r
i
u
q
e
r

l

y
t
i
x
e
p
m
o
c
g
n

i
l

e

y
g
o
o

l

)
β

,

j
i

d
(
f
}

)
β

,

j
i

d
(
f

∗i
A

∅
A

0
d
≤

j
i

d
{
∈

i

(cid:31)

=

=

R
A
P
S
A

i

j
i

b
o
r
P

j

S

j
i

b
o
r
P
∗
)
β

,

j
i

d
(
f

∗

i

P
}

0
d
≤

j
i

d
{
∈

i

(cid:31)

=

j

R

)
β

,

j
i

d
(
f

∗

j

R
}

0
d
≤

j
i

d
{
∈

j

(cid:31)

=
∗i
A

]
6
7
[
0
2
0
2

,
.
l

a
t
e
s
w
e
h
t
t
a
M

]
4
4
[
9
1
0
2

,
.
l

a
t
e
z
e
a
P

]
1
4
[
1
2
0
2

,

g
n
a
J

•

•

•

]
2
4
[
1
2
0
2

,
.
l

a
t
e
n
e
h
S
•

]
3
4
[
7
1
0
2

,
.
l

a
t
e
g
n
a
T
•

]
0
4
[
4
1
0
2

,

o
u
L
•

:

y
r
o
g
e

i

t
h
g
e
w
n
o
i
t
c
e
e
s
d
e
s
a
b

l

-
t
a
c
n
h
t
i

i

w

t
n
e
m
p
o
e
v
e
D

l

]
3
1
[
2
1
0
2

,

s
y
e
r
h
p
m
u
H
&

l
i

a
r
G
c
M

•

]
5
3
[
4
1
0
2

]
8
6
[
5
1
0
2

,
.
l

a
t
e
o
h
s
t

m
a
J

]
6
3
[
8
1
0
2

,
.
l

a
t
e
m
K

i

]
4
7
[
5
1
0
2

,
.
l

a
t
e

i

N

•

•

•

]
5
7
[
1
2
0
2

,
.
l

a
t
e

i

g
r
o
z
o
B

•

]
7
3
[
8
1
0
2

,
.
l

a
t
e
o
a
T
•

:

y
r
o
g
e

-
t
a
c
n
h
t
i

i

w

t
n
e
m
p
o
e
v
e
D

l

]
8
3
[
2
1
0
2

:

y
r
o
g
e

–

,
.
l

a
t
e
n
a
h
Z

,

n
a
W
R
A
P
S

•

s

l

m
r
e
t
e
v
i
t
a
e
r
o
t
n
o
i
t
a
c

n
o
i
t
a
c

:

y
d
u
t
s

t
s
r
i
F

i

-
fi
d
o
m

t
i
n
u
e
m
o
c
t
u
O

i

-
fi
d
o
M

t
i
n
U
e
m
o
c
t
u
O

-
t
a
c
n
h
t
i

i

w

t
n
e
m
p
o
e
v
e
D

l

-
n
o
i
t
i
t
e
p
m
o
c
r
e
d
v
o
r
p
a

i

,
.
l

a
t
e
u
o
Z

,

n
a
W
A
C
F
S
3
•

]
9
3
[
2
1
0
2

n
o
i
t
a
m

i
t
s
e
r
e
v
o

i

g
n
c
u
d
o
r
t
n

i

y
b

:

y
d
u
t
s

t
s
r
i
F

d
n
a
m
e
d
g
n
i
t
c
e
r
r
o
C

n
o
i
t
i
t
e
p
m
o
C
r
e
d
v
o
r
P

i

,

i

o
p
p
h
W
&
o
u
L
A
C
F
S
2
V

•

n
o
i
t
i
n
fi
e
d

s
e
z
i
S
a
e
r
A

]
3
3
[
9
1
0
2

,
.
l

a
t
e
n
i
J

•

]
4
3
[
0
2
0
2

,
.
l

a
t
e
o
a
T
•

]
3
7
[

:

y
d
u
t
s

t
s
r
i
F

e
z
i
s

t
n
e
m
h
c
t
a
c
e
b
a
i
r
a
V

l

t
n
e
m
h
c
t
a
C
e
b
a
i
r
a
V

l

Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 12 of 22

a
t
a
d

l

a
n
o
i
t
i
d
d
a
o
N

-
d
o
m

f

o
e
s
a
e
r
c
n

i

t
h
g

i
l

S

-
d
o
h
t
e
M
g
n
i
t
c
e
r
r
o
C

d
e
r
i
u
q
e
r

l

y
t
i
x
e
p
m
o
c
g
n

i
l

e

y
g
o
o

l

-
b
u
s
n
o
a
t
a
d

l

a
n
o
i
t
i
d
d
A

-
d
o
m

f

o
e
s
a
e
r
c
n

i

h
g
H

i

t
x
e
t
n
o
C
g
n
i
t
t
i
F

i

i

r
e
d
v
o
r
p
c
fi
c
e
p
s
-
p
u
o
r
g

s
e
r
a
h
s
n
o
i
t
a
u
p
o
p
d
n
a

l

d
e
r
i
u
q
e
r

l

y
t
i
x
e
p
m
o
c
g
n

i
l

e

)
β

,

j
i

d
(
f

∗

i

G
P
}

-
e
p
s
-
e
d
o
m
d
n
a
s
e
c
n
a
t
s
i
d

d
e
r
i
u
q
e
r

s
e
r
a
h
s

r
e
s
u
c
fi
c

i

i

c
fi
c
e
p
s
-
e
d
o
m
n
o

l

y
t
i
x
e
p
m
o
c
g
n

i
l

e

a
t
a
d

l

a
n
o
i
t
i
d
d
A

-
d
o
m

f

o
e
s
a
e
r
c
n

i

h
g
H

i

i

g
n
i
t
a
m
x
o
r
p
p
A

y
t
i
l

a
e
R

)
β

,

j
i

d
(
f

∗

)
n
M

(
i
P

)
β

,

j
i

d
(
f

∗

i

P
}

0
d
≤

j
i

d
{
∈

i

(cid:31)

0
d
≤

j
i

d
{
∈

i

(cid:31)
/

)
β

,

j
i

d
(
f

∗

j

R
}

0
d
≤

j
i

d
{
∈

j

(cid:31)

)
β

,

j
i

d
(
f

∗

j

R
}

0
d
≤

j
i

d
{
∈

j

(cid:31)

)
β

,

j
i

d
(
f

∗

j

S

i

P
}

0
d
≤

j
i

d
{
∈

i

(cid:31)

)
β

,

j
i

d
(
f

∗

j

S

)
β

,

j
i

d
(
f

∗

i

P
}

0
d
≤

j
i

d
{
∈

i

(cid:31)

=

j

R

=
∗i
A

=

j

R

=
∗i
A

)
β

,

j
i

d
(
f

∗

j

G
S
}

)
β

,

j
i

d
(
f

∗

j

S
}

0
d
≤

j
i

d
{
∈

j

(cid:31)

0
d
≤

j
i

d
{
∈

j

(cid:31)
∗

∗i
A
=
∗i
G
A

j

S

)
n
M

(
j
i

}

)
n
M
(
0
d
≤

d
{
∈

i

(cid:31)
(cid:31)

n

=

j

R

)
β

,

j
i

d
(
f

∗

j

R

)
n
M

(
j
i

}

)
n
M
(
0
d
≤

d
{
∈

j

(cid:31)

)
n
M

(
i
P

i

P

n

(cid:31)

=
∗i
A

]
1
5
[
0
2
0
2

,
.
l

a
t
e
u
o
h
Z

]
0
8
[
2
2
0
2

,

g
N
&
g
n
X

i

•

•

-
t
a
c
n
h
t
i

i

w

t
n
e
m
p
o
e
v
e
D

l

:

y
r
o
g
e

6
1
0
2

,

g
r
e
b
e
n
o
r
G
&
r
e
u
a
B

•

]
5
4
[

m
e
t
s
y
s
e
r
a
c
h
t
l
a
e
h

l

a
c
o

l

g
n

i
l

e
d
o
m
y
b

e
c
n
a
t
s
i
d

l

l

a
b
o
g
d
n
a

y
a
c
e
d

3
1
0
2

l

,
r
e
t
a
m
a
e
D
A
C
F
S
2
M

•

d
e
r
u
g
fi
n
o
c
y

l
l

a
m

i
t
p
o

y
a
c
e
D

i

A
C
F
S
2
c
fi
c
e
p
s
-
p
u
o
r
g
b
u
S

•

]
7
4
[
7
0
0
2

,

g
n
a
W

:

y
d
u
t
s

t
s
r
i
F

]
6
4
[

l

-
a
u
p
o
p
e
v
i
t
c
e
e
s

l

r
o

f

i

c
fi
c
e
p
s
-
p
u
o
r
g
b
u
S

e
r
u
s
a
e
m

s
s
e
c
c
a

i

c
fi
c
e
p
S
-
p
u
o
r
g
b
u
S

s
s
e
c
c
A

]
8
4
[
1
2
0
2

,
.
l

a
t
e
o
a
X

i

]
9
6
[
1
2
0
2

,
.
l

a
t
e
g
n
a
Y

•

•

]
9
4
[
2
2
0
2

,

o
u
L
&
o
a
h
S
•

:

y
r
o
g
e

-
t
a
c
n
h
t
i

i

w

t
n
e
m
p
o
e
v
e
D

l

g
n
i
r
i
a
p
r
e
d
v
o
r
p
-
n
o
i
t

i

:

y
d
u
t
s

t
s
r
i
F

n
o
i
t
a
t
r
o
p
s
n
a
r
t
e
p
i
t
l
u
M

l

n
o
i
t
a
t
r
o
p
s
n
a
r
T
e
p
i
t
l
u
M

l

-
r
o
k
e
N
&
o
a
M
A
C
F
S
2
-
M
M

•

-
t
a
c
n
h
t
i

i

w

t
n
e
m
p
o
e
v
e
D

l

]
4
1
[
3
1
0
2

,

k
u
h
c

]
0
5
[
6
1
0
2

,
.
l

a
t
e
d
r
o
g
n
a
L
•

f

]
7
7
[
4
1
0
2

,
.
l

a
t
e
n
i
z
l
o
P

•

]
9
7
[
9
1
0
2

,

g
n
e
h
C
&
o
a
T
•

]
8
7
[
9
1
0
2

,
.
l

a
t
e

i

N

•

:

y
r
o
g
e

s
e
d
o
m

s
e
d
o
M

:

y
d
u
t
s

t
s
r
i
F

-
b
u
s

r
o

f

g
n
i
t
c
e
r
r
o
C

e
c
n
a
t
s
i
D

l

a
b
o
G
&

l

l

a
c
o
L

-
u
p
o
p
r
o
y
p
p
u
s

l

i

r
e
d
v
o
r
p

d
e
r
i
u
q
e
r
e
z
i
s
n
o
i
t
a

l

 :
r

W

i

,
r
s
u
d
a
r
-
b
u
s
a
e
r
a
t
n
e
m
h
c
t
a
c
f
o
e
c
n
a
t
s
i
d
d
o
h
s
e
r
h
t

l

 :
r

d

,
j

-
e
m

i
t
n
o
a
t
a
d

l

a
n
o
i
t
i
d
d
A

-
d
o
m

f

o
e
s
a
e
r
c
n

i

o
N

i

g
n
i
t
a
m
x
o
r
p
p
A

,

e
m

i
t

l

e
v
a
r
t
g
n
y
r
a
v

i

l

y
t
i
x
e
p
m
o
c
g
n

i
l

e

y
t
i
l

a
e
R

)
β

,

)
t
T
(
j
i

d
(
f

∗

j

R
}

0
d
≤

)

t

T
(
j
i

d
{
∈

j

(cid:31)

)
β
)

,

t

T
(
j
i

d
(
f

∗

j

S

i

P
}

0
d
≤

)

t

T
(
j
i

d
{
∈

i

(cid:31)

=

t
j

R

=
∗i
t
A

A
C
F
S
2

l

a
r
o
p
m
e
T
-
o
i
t
a
p
S

]
2
5
[
8
1
0
2

,
.
l

a
t
e
a
M

•

•

-
t
a
c
n
h
t
i

i

w

t
n
e
m
p
o
e
v
e
D

l

:

y
r
o
g
e

]
5
5
[
9
1
0
2

,

s
d
r
a
w
d
E
&

l

u
a
P

]
4
5
[
9
1
0
2

,
.
l

a
t
e
a
X

i

•

•

]
3
5
[
8
1
0
2

.
l

a
t
e
g
n
o
S
•

e
r
u
s
a
e
m

s
s
e
c
c
a

s
s
e
c
c
A

:

y
d
u
t
s

t
s
r
i
F

i

g
n
y
r
a
v
-
e
m

i

i
t
c
m
a
n
y
D

t
n
e
d
n
e
p
e
D

-
e
m
T

i

 :
j
i

b
o
r
P

,
i

n
o
i
t
a
c
o

l

t
a
o
i
t
a
R
s
s
e
c
c
A

l

a
i
t
a
p
S
 :

R
A
P
S
A

i

 :
∗i
G
A

i

t
n
o
p
e
m

i
t

t
a

j

n
o
i
t
a
c
o

l

l

t
a
o
i
t
a
r
n
o
i
t
a
u
p
o
p
-
o
t
-
r
e
d
v
o
r
p

i

 :
t
j

R

i

,
t
t
n
o
p
e
m

i
t

t
a

j

n
o
i
t
a
c
o

l

i

r
e
d
v
o
r
p
d
n
a

i

n
o
i
t
a
c
o

l

l

n
o
i
t
a
u
p
o
p
n
e
e
w
t
e
b
e
c
n
a
t
s
i
d

 :
)
t
T
(
j
i

d

,

n
e
d
o
m
n
o
i
t
a
t
r
o
p
s
n
a
r
t

r
o
f
a
e
r
a
t
n
e
m
h
c
t
a
c
f
o
e
c
n
a
t
s
i
d
d
o
h
s
e
r
h
t

l

e
d
o
m
n
o
i
t
a
t
r
o
p
s
n
a
r
t
g
n
i
s
u
n
o
i
t
a
c
o

l

i

r
e
d
v
o
r
p
d
n
a
n
o
i
t
a
c
o

l

l

n
o
i
t
a
u
p
o
p
n
e
e
w
t
e
b
e
c
n
a
t
s
i
d

 :
)
n
M

(
j
i

d

,

n
e
d
o
m
n
o
i
t
a
t
r
o
p
s
n
a
r
t
g
n
i
s
u

i

n
o
i
t
a
c
o

l

l

)
n
o
i
t
a
u
p
o
p
=

(
y
t
i
s
n
e
t
n

i

d
n
a
m
e
d

 :
)
n
M

(
i
P

,
i

n
o
i
t
a
c
o

l

t
a
x
e
d
n

i

s
s
e
c
c
a
c
fi
i
c
e
p
s
-
p
u
o
r
g
b
u
s

,
i

n
o
i
t
a
c
o

l

l

)
n
o
i
t
a
u
p
o
p
=

(
y
t
i
s
n
e
t
n

i

d
n
a
m
e
d
c
fi
i
c
e
p
s
-
p
u
o
r
g
b
u
s

 :
i

G
P

,
j

n
o
i
t
a
c
o

l

t
a
)
y
l
p
p
u
s
=

(
y
t
i
c
a
p
a
c
e
r
a
c
h
t
l
a
e
h
c
fi
i
c
e
p
s
-
p
u
o
r
g
b
u
s

 :
j

G
S

,
r
i
a
p

j

i

r
e
d
v
o
r
p
d
n
a

i

l

n
o
i
t
a
u
p
o
p
r
o
f

i

l

t
h
g
e
w
n
o
i
t
c
e
e
s
d
e
s
a
b
-
e
c
n
a
d
e
p
m

i
-
e
c
n
a
t
s
i
d

,

a
e
r
a
y
d
u
t
s
n

i
x
e
d
n

i

s
s
e
c
c
a
n
a
e
m
∅
A

 :

,

n
o
i
t
a
c
o

l

i

l

r
e
d
v
o
r
p
/
n
o
i
t
a
u
p
o
p
f
o
s
c
i
t
s
i
r
e
t
c
a
r
a
h
c
n
o
t
n
e
d
n
e
p
e
d

,

a
e
r
a
t
n
e
m
h
c
t
a
c
f
o
e
c
n
a
t
s
i
d
d
o
h
s
e
r
h
t

l

 :
)
(
x
d

,

n
o
i
t
c
i
r
f
e
c
n
a
t
s
i
d
d
n
a
e
c
n
a
t
s
i
d

n
o
t
n
e
d
n
e
p
e
d

,

n
o
i
t
c
n
u
f
y
a
c
e
d
e
c
n
a
t
s
i
d

l

a
r
e
n
e
g

 :
)
(
f

,
r
e
t
e
m
a
r
a
p
n
o
i
t
c
i
r
f
e
c
n
a
t
s
i
d

 :

β

,
i

n
o
i
t
a
c
o

l

t
a
x
e
d
n

i

n
o
i
t
a
c
o

l

i

r
e
d
v
o
r
p
d
n
a

i

n
o
i
t
a
c
o

l

l

n
o
i
t
a
u
p
o
p
n
e
e
w
t
e
b
e
c
n
a
t
s
i
d

s
s
e
c
c
a
 :
∗i
A

,
j

n
o
i
t
a
c
o

l

l

t
a
o
i
t
a
r
n
o
i
t
a
u
p
o
p
-
o
t
-
r
e
d
v
o
r
p

i

 :
j

R

i

,
r
s
u
d
a
r
-
b
u
s
a
e
r
a
t
n
e
m
h
c
t
a
c
n
h
t
i

i

w

i

t
h
g
e
w
y
a
c
e
d
e
c
n
a
t
s
i
d

 :
j
i

d

,
i

n
o
i
t
a
c
o

l

l

)
n
o
i
t
a
u
p
o
p
=

(
y
t
i
s
n
e
t
n

i

d
n
a
m
e
d

 :
i

P

,
j

n
o
i
t
a
c
o

l

t
a
)
y
l
p
p
u
s
=

(
y
t
i
c
a
p
a
c
e
r
a
c
h
t
l
a
e
h

 :
j
S

t

i

t
n
o
p
e
m

i
t

t
a

i

n
o
i
t
a
c
o

l

t
a
x
e
d
n

i

s
s
e
c
c
a
 :
t
∗i
A

 :
)
n
M
(
0
d

,

n

,
t

s
n
o
i
t
a
t
o
n
e
h
t

m
o
r
f

i

r
e
ff
d
n
a
c
e
c
n
e
h

,

i

y
c
n
e
t
s
i
s
n
o
c
e
d
v
o
r
p
o
t
d
e
z
i
n
o
m
r
a
h
s
a
w
s
t
n
e
m
p
o
e
v
e
d

l

l

l

a
c
i
g
o
o
d
o
h
t
e
m
e
h
t

f
o
n
o
i
t
a
t
o
n

l

a
m
r
o
f
e
h
T

.

y
r
o
g
e
t
a
c
h
c
a
e
f
o
y
d
u
t
s

t
s
r
fi
e
h
t
n

i

l

d
e
s
o
p
o
r
p
y
g
o
o
d
o
h
t
e
m
e
h
t
o
t

l

s
r
e
f
e
r
a
u
m
r
o
F
†

i

s
e
d
u
t
s
d
e
t
i
c
e
h
t
n

i

n
e
v
g

i

l

g
n
i
t
a
o
F
p
e
t
S
-
o
w
T
d
e
fi
d
o
M
A
C
F
S
2
M

i

,

a
e
r
A
t
n
e
m
h
c
t
a
C
g
n
i
t
a
o
F
p
e
t
S
-
e
e
r
h
T
A
C
F
S
3

l

,

o
i
t
a
R
s
s
e
c
c
A

l

a
i
t
a
p
S
R
A
P
S

,

l

a
e
r
A
t
n
e
m
h
c
t
a
C
g
n
i
t
a
o
F
p
e
t
S
-
o
w
T
e
b
a
i
r
a
V
A
C
F
S
2
V

l

,

l

a
e
r
A
t
n
e
m
h
c
t
a
C
g
n
i
t
a
o
F
p
e
t
S
-
o
w
T
d
e
c
n
a
h
n
E
A
C
F
S
2
E

a
e
r
A
t
n
e
m
h
c
t
a
C
g
n
i
t
a
o
F
p
e
t
S
-
o
w
T
e
d
o
M

l

-
i
t
l
u
M
A
C
F
S
2
-
M
M

,

l

a
e
r
A
t
n
e
m
h
c
t
a
C
g
n
i
t
a
o
F
p
e
t
S
-
o
w
T
c
fi
i
c
e
p
s
-
p
u
o
r
g
b
u
S
A
C
F
S
2
c
fi
i
c
e
p
s
-
p
u
o
r
g
b
u
S

,

a
e
r
A
t
n
e
m
h
c
t
a
C

s
t
n
e
m
e
r
i
u
q
e
r
a
t
a
D

l

y
t
i
x
e
p
m
o
C

e
s
o
p
r
u
P

†
a
l
u
m
r
o
F

i

s
e
d
u
t
S

t
n
e
m
e
c
n
a
v
d
A

y
r
o
g
e
t
a
C

)

d
e
u
n
i
t
n
o
c
(

1
e
l
b
a
T

Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 13 of 22

Table 2  Characteristics of measures applying gravity model developments

Variables

Case numbers

Study area

Africa

Asia

Europe

North America

South America

Care sector

Primary

Secondary

Primary and secondary

Study area region type

Urban

Rural

Urban and rural

Distance type

Travel time

Travel distance

Euclidean distance

Indicator computation

Primary computation

Secondary use

Application case

Descriptive

Covariate

Exploratory

Comparison

Total

346

4 (1%)

160 (46%)

36 (10%)

136 (39%)

10 (3%)

157 (45%)

135 (39%)

54 (16%)

142 (41%)

18 (5%)

186 (54%)

249 (72%)

56 (16%)

41 (12%)

338 (98%)

8 (2%)

189 (55%)

67 (19%)

51 (15%)

39 (11%)

Base gravity model

2SFCA method family

14

0 (0%)

10 (71%)

0 (0%)

3 (21%)

1 (7%)

1 (7%)

8 (57%)

5 (36%)

10 (71%)

2 (14%)

2 (14%)

9 (64%)

2 (14%)

3 (21%)

14 (100%)

0 (0%)

8 (57%)

2 (14%)

2 (14%)

2 (14%)

324

4 (1%)

148 (46%)

36 (11%)

128 (40%)

8 (2%)

153 (47%)

124 (38%)

47 (15%)

127 (39%)

16 (5%)

181 (56%)

238 (73%)

54 (17%)

32 (10%)

316 (98%)

8 (2%)

178 (55%)

63 (19%)

48 (15%)

35 (11%)

Kernel
density
method

8

0 (0%)

2 (25%)

0 (0%)

5 (63%)

1 (13%)

3 (38%)

3 (38%)

2 (25%)

5 (63%)

0 (0%)

3 (38%)

2 (25%)

0 (0%)

6 (75%)

8 (100%)

0 (0%)

3 (38%)

2 (25%)

1 (13%)

2 (25%)

2SFCA two-step floating catchment area

39%  of  the  measures  (N = 135)  were  applied  to  second-
ary  care  providers  and  16%  (N = 54)  to  both  primary
and  secondary  care  providers.  Provider  capacity  was
measured  in  a  variety  of  ways,  including  physician  head
counts  (e.g.,  [56]),  physician  full-time  equivalents  (e.g.,
[15]),  number  of  hospital  beds  (e.g.,  [57]),  number  of
sites  (e.g.,  [29]),  or  number  of  services  (e.g.,  [58])  avail-
able.  Most  spatial  access  measures  (N = 186;  54%)  were
applied  to  a  geographic  scope  covering  both  urban  and
rural  regions,  while  41%  (N = 142)  were  applied  to  an
exclusively urban, and 5% (N = 18) to an exclusively rural
context.  To  operationalize  travel  friction  in  the  gravity
model,  most  applications  (72%;  N = 249)  used  the  esti-
mated shortest travel time along a road network between
population  and  provider  location.  Another  16%  (N = 56)
of  the  measures  incorporated  travel  friction  by  means
of  estimated  shortest  travel  distance,  and  12%  (N = 41)

used Euclidean distance. Almost all spatial access meas-
ures  (98%,  N = 338)  were  computed  within  the  scope  of
the respective studies. However, a small share of studies
relied on secondary data (2%; N = 8), using access indices
that had been previously computed by other researchers.1
There was a range of purposes that the healthcare access
measures were applied for: 55% (N = 189) of the measures
served  the  purpose  of  describing  the  spatial  access  in  a
particular healthcare system. In 19% of the cases (N = 67),
the  spatial  access  measure  was  used  as  a  covariate  to
explain health outcomes (e.g., [59]). Another 15% of the
measures  (N = 51)  were  applied  in  a  methodologically

1  All of the studies concerned were carried out in the French context, using
the so-called "Localized Potential Access" indicators which were computed
by  the  Direction  de  la  recherche,  des  études,  de  l’évaluation  et  des  statis‑
tiques [81] and made available for research. The E2SFCA methodology was
implemented  for  generating  the  access  indicators.  Indicators  were  com-
puted for several professions within primary care.

 Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 14 of 22

Fig. 2  Lineage and application frequency of gravity model developments. Displayed in light blue is the base gravity model, displayed in blue are
the conceptual developments derived from it (2SFCA method, Kernel Density method), displayed in dark blue are categories of methodological
developments derived from the 2SFCA method. Number of access measures that applied the respective methodological development is given
in gray boxes, bubble sizes are weighted by frequency of application. Each applied measure was assigned to either the base gravity model,
the 2SFCA method family, or the Kernel Density method (= mutually exclusive). In addition, for all 324 2SFCA-type measures, the methodological
development(s) applied were identified. One 2SFCA-type measure can implement more than one methodological development (= not mutually
exclusive). Therefore, the sum of 2SFCA-type methodological developments applied exceeds the number of measures classified as 2SFCA-type.
2SFCA Two-Step Floating Catchment Area, E2SFCA Enhanced Two-Step Floating Catchment Area, V2SFCA Variable Two-Step Floating Catchment
Area, SPAR Spatial Access Ratio, 3SFCA Three-Step Floating Catchment Area, M2SFCA Modified Two-Step Floating Catchment Area, MM-2SFCA
Multi-Mode Two-Step Floating Catchment Area

exploratory  way;  that  is,  investigating  model  proper-
ties  by  applying  different  parameters  (e.g.,  [60]).  Lastly,
11% (N = 39) of the measures were applied to conduct a
comparison of methods, either comparing gravity model
indicators to non-gravity type accessibility or availability
measure (e.g., [61]), or comparing several different grav-
ity model methodologies (e.g., [62]).

Application frequency: 1st generation developments

Applications  of  gravity  models  for  spatial  healthcare
access measurement were almost exclusively restricted to
methods  from  within  the  2SFCA  family  (94%,  N = 324).
Only  few  measures  applied  a  base  gravity  model  or  the
KD method: 4% (N = 14) of the applications represented
measures  derived  from  the  base  gravity  model  method

2  It  is  noted  here  that  there  were  several  studies  applying  a  gravity  model
method without considering the population dimension, i.e., omitting poten-
tial  demand  and  thus  only  accounting  for  supply  density.  Equally,  several
studies used Kernel Density method to model provider density, however not
overlaying that with the population density. These application studies were
excluded  as  considering  the  demand  dimension  was  one  of  the  inclusion
criteria.

and 2% (N = 8) applied the KD method to measure poten-
tial spatial access to healthcare.2

Application frequency: 2nd generation developments (2SFCA
family)

Out  of  the  324  measures  implementing  a  2SFCA-type
methodology,  25%  (N = 82)  computed  the  measure
exactly  like  Luo  and  Wang  [11]  had  first  suggested  it.
That  is,  no  distance  decay  within  the  catchment  area,
fixed  catchment  sizes  across  the  study  context,  no  out-
come  unit  modification,  and  no  additional  assumptions
or  corrections  in  terms  of  provider  competition,  sub-
group-specific  access,  multiple  transportation  modes,
or  time-dependent  access  were  made.  For  the  remain-
ing 242 2SFCA-type measures that implemented further
methodological developments, distance decay within the
catchment  area  was  the  most  frequently  applied  (71%,
N = 229), followed by implementations of variable catch-
ment areas (16%, N = 52), and incorporation of provider
competition  (12%,  N = 40).  Modification  of  the  outcome
unit  (5%,  N = 16)  and  considering  local  and  global  dis-
tance  decay  functions  (4%,  N = 13),  subgroup-specific

Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 15 of 22

Table 3  Application frequency of 2SFCA-type methodological developments

Methodological development

N of 2SFCA-type measures applied this
methodological development

% of 2SFCA-type measures applied
this methodological development

2SFCA-type measures applied
(Total)

Initial 2SFCA
(No methodological development)

Distance decay within catchment area

Variable catchment area sizes

Outcome unit modification

Provider competition

Local and global distance decay

Subgroup-specific access

Multiple transportation modes

Time-dependent access

324

82

229

52

16

40

13

2

13

8

100

25

71

16

5

12

4

1

4

2

For all 324 2SFCA-type measures, the methodological development(s) applied were identified. One 2SFCA-type measure can implement more than one
methodological development (= not mutually exclusive). Therefore, the sum of 2SFCA-type methodological developments applied exceeds the number of measures
classified as 2SFCA-type

2SFCA two-step floating catchment area

access  measures  (< 1%,  N = 2),  multiple  transportation
modes  (4%,  N = 13),  and  time-dependent  access  (2.5%,
N = 8)  were  implemented  to  a  small  degree  only.  The
application  frequency  of  2SFCA-type  methodological
developments is given in Table 3.

Distance  decay  With  more  than  half  of  all  the  2SFCA
applications  accounting  for  distance  decay  within  the
catchment  area,  this  methodological  development  has
caught on widely in research practice. The stepwise dis-
crete  approach  as  proposed  by  Luo  and  Qi  [12]  was
implemented in 96 access measures. In it, a fixed distance
decay weight is assigned to each location according to the
catchment area sub-radius it is in. Another 105 measures
applied a continuous distance decay function within the
catchment area. Particularly common examples of func-
tional  forms  were  Gaussian  functions  and  power  func-
tions. The remaining 28 access measures implemented a
hybrid form in which both a fixed distance decay weight
and  a  continuous  distance  decay  function  were  used
within  the  catchment  area.  Such  hybrid  forms  usually
assume zero decay within a certain distance threshold and
apply a continuous decay function thereafter.

Catchment  area  Of  the  52  measures  applying  variable
catchment area definitions, 31 operationalized catchment
areas to depend on a categorical variable. Typical exam-
ples would be catchment sizes depending on a categorical
urban–rural classification or depending on hospital type.
The  other  21  measures  defined  catchment  area  sizes  in
a  continuous  fashion,  e.g.,  dependent  on  the  number  of
doctors  at  a  provider  location  (larger  healthcare  institu-

tions have a wider reach) or dependent on fulfilment of a
minimally  required  provider-to-population  ratio  (higher
distance tolerance in low-density areas).

Outcome unit  A small fraction of the 2SFCA type meth-
ods applied a modification of the outcome unit, i.e., divid-
ing the spatial access measure at a population location by
the mean spatial access measure. That is, these 16 studies
computed  a  relative  access  measure  e.g.,  for  comparing
regions.

Provider  competition  Out  of  the  measures  using  a
selection  weight  to  consider  provider  competition,  34
measures  incorporated  a  Huff-model  based  selection
probability in an additional first step akin to the 3SFCA
proposed by Wan, Zou et al. [39]. In that additional first
step, a selection probability for each provider-population
pairing  is  computed  using  the  surrounding  providers  at
a  particular  population  location.  Computation  of  these
selection probabilities is either based on relative distances
to  surrounding  providers  only  [e.g.,  57],  i.e.,  closer  pro-
viders are assumed to more likely be visited. Or both dis-
tance and capacity are considered [15], i.e., providers with
more  resources  additionally  are  assumed  to  be  visited
more. The remaining 6 measures followed the methodol-
ogy suggested by Paez et al. [44] in fully allocating supply
and demand to account for provider competition. That is,
each demand unit (e.g., one inhabitant) and each supply
unit  (e.g.,  one  pediatrician)  are  considered  only  once  as
contributing to the potential demand on a provider, and
to the potential availability for a population, respectively.

 Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 16 of 22

Local  and  global  distance  decay    Using  both  local  and
global  distance  decay  functions  to  model  both  the  rela-
tive  and  absolute  distances  to  providers  was  rare.  Of
those  measures  implementing  it,  7  measures  accounted
for relative and absolute distances like Delamater [45] by
adding an additional distance decay term with the same
functional form in the first step of the method. The local
and  global  distance  friction  are  assumed  to  show  the
same decay properties. The other 6 measures followed the
methodology  put  forward  by  Bauer  and  Groneberg  [46]
who  introduced  separate  functions  for  the  local  and  the
global distance decay.

Subgroup‑specific  access  Almost  no  measures  imple-
mented  a  methodology  with  a  subgroup-specific  access
measure.  Two  studies  used  an  additional  third  step  to
compute a subgroup specific access to healthcare provid-
ers  with  matching  language  or  ethnicity.  No  measures
were found to provide e.g., insurance-specific access indi-
ces or access indices considering referral within a hierar-
chical healthcare system.

Multiple  transportation  modes  Of  those  measures
incorporating  multiple  transportation  modes,  9  meas-
ures produced an integrated spatial access indicator for all
transportation modes. That is, the final indicator in those
studies was a weighted measure which not only includes
travel  times  differing  by  transport  mode,  but  also  vary-
ing  shares  of  mode-specific  users  per  population  loca-
tion. The remaining 4 measures produced separate spatial
access  indices  for  each  transportation  mode.  Of  those,
3  assumed  no  differences  in  mobility  across  population
locations  and  applied  the  same  methodology  with  the
same parameters once for each transportation mode. The
other  1  study  computed  mode-specific  access  measures
which considered demand competition arising from vary-
ing ranges by different transport-mode users, i.e., which
incorporated  varying  shares  of  mode-specific  users  for
population locations.

Time‑dependent  access  Time-dependent  access  was
incorporated to a relatively small degree so far. However,
this is the youngest category of methodological develop-
ments being proposed for the first time in 2018. Among
the studies applying a time-dependent approach, there was
wide  variation  in  how  time-dependency  was  accounted
for.  Some  measures  (N = 3)  employed  time-dependent
travel times using real-time traffic data. Other measures
used time-dependent demand [63], time-dependent sup-
ply [64], or a combination of time-dependent travel time,
demand, and supply [65, 66].

Discussion
Summary of key findings

In review step 1, we identified 43 studies that proposed a
methodological development in the field of gravity mod-
els  for  measuring  spatial  access  to  healthcare.  Starting
from a base gravity model that integrated availability and
accessibility  as  well  as  supply  and  demand  factors,  first
proposed by Joseph and Bantock [10], two major concep-
tual developments emerged: the two-step floating catch-
ment area (2SFCA) method [11] and the Kernel Density
method  [30].  While  both  methods  are  special  forms
of  the  base  gravity  model,  these  two  developments  are
conceptually  different.  From  2004  onward,  virtually  all
methodological developments were based on the 2SFCA
method.  These  studies  proposed  methodological  devel-
opments regarding distance decay within the catchment
area, variable catchment area sizes, outcome unit modi-
fication,  provider  competition,  local  and  global  distance
decay,  subgroup-specific  access,  multiple  transportation
modes, and time-dependent access.

In  review  step  2,  we  identified  309  application  stud-
ies covering a total of 346 measures. Application studies
focused almost exclusively on measures from the 2SFCA
family.  The  usage  of  2SFCA  type  methods  to  describe
spatial  healthcare  access  has  caught  on  widely  in  the
health  research  practice.  In  comparison,  the  base  grav-
ity  model  (and  its  variants)  as  well  as  the  KD  method
have  found  much  less  application  in  research  practice.
Among  the  studies  employing  an  access  measure  from
the 2SFCA family, most implement some kind of distance
decay within the catchment area. Other frequently imple-
mented  methodological  developments  from  the  2SFCA
family  were  variable  catchment  area  sizes,  and  selection
probabilities  to  account  for  provider  competition.  How-
ever,  usage  of  the  basic  2SFCA  method  as  it  was  devel-
oped by Luo and Wang [11] was still very common.

Appraisal
Review step 1: methodological developments

We identified three types of purpose the methodological
developments were serving: Approximating reality, fitting
context, and correcting methodology.

Approximating  reality:  Many  of  the  methodologi-
cal  developments  stem  from  attempts  to  make  the  spa-
tial  access  measure  better  reflect  reality.  Distance  decay
within  the  catchment  area  (e.g.,  [12,  32,  67])  better
reflects real-world travel friction; variable catchment area
sizes  allow  for  integration  of  real-world  differences  in
willingness to travel (e.g., [13, 35, 68]); multiple transpor-
tation modes allow for modeling real-world travel behav-
ior (e.g., [14, 50, 51]); and time-dependent access captures
real-world  temporal  variability  in  access  (e.g.,  [64–66]).
While this makes spatial access measures more realistic,

Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 17 of 22

it also comes at a cost. Firstly, it often means additional
methodological
computational
complexity,  higher
intensity,  or  additional  data  requirements.  For  example,
accounting  for  multiple  transportation  modes  not  only
means additional computational power required, but also
additional  data  requirements.  Secondly,  within  increas-
ing methodological complexity, also the interpretation of
the final access score may become more complex. In the
case of the Variable 2SFCA for example, varying distance
tolerance  is  assumed  due  to  longer  travel  times  some
populations  must  accept  to  reach  any  provider.  Hence,
the  final  access  score  refers  to  spatial  access  e.g.,  within
a 30-min radius in some locations and a 60-min radius in
others.  Thirdly,  additional  assumptions  mean  additional
uncertainty.  Integrating  methodological  developments
to  approximate  reality  requires  the  researcher  to  take
more  decisions:  Does  she  consider  two  or  three  differ-
ent modes of travel? Does she model fast or slow distance
decay?  How  long  does  she  believe  are  rural  populations
willing to travel more than urban populations? Does she
consider temporal variation only in travel time or also in
demand intensity? This additional uncertainty should be
taken  into  consideration  when  dealing  with  increasingly
complex gravity models.

Fitting  context:  Some  methodological  developments
have  been  created  against  the  background  of  a  specific
healthcare  system  or  context.  These  are  methods  that
model selective population-provider pairings that are not
(only)  dependent  on  spatial  interaction  (i.e.,  subgroup-
specific  access  measures).  They  reflect  context-specific
limitations  in  provider  choice.  Methodological  develop-
ments  have  been  proposed  to  integrate  patient  referral
within  a  hierarchical  healthcare  system  with  gate-keep-
ing functions (e.g., [48, 69]); to depict subgroup-specific
access reflecting a language or ethnicity match [47], and
spatial access for patients of specific insurance plans [49].
Such  methodological  developments  can  prove  useful  in
research practice, however, may not be easily transferable
or relevant across healthcare systems.

Correcting  methodology:  Several  studies  have  unveiled
unintended  flawed  implications  of  earlier  methods  and
changed  the  methodology  to  overcome  those  implicit
limitations.  Four  conceptual  issues  were  addressed  with
the  studies  attempting  to  correct  methodology:  Firstly,
2SFCA-implicit  demand  over-estimation
(stemming
from  counting  full  populations  to  the  potential  demand
at  multiple  provider  sites)  was  rectified  by  allocating
demand  using  a  selection  weight  mimicking  provider
competition  [39].  Secondly,  Delamater  [45]  showed  that
standard 2SFCA methods implicitly relied on relative dis-
tance  friction  only.  An  additional  global  distance  decay
function was introduced to correct the implicit disregard
of  absolute  distance  friction.  Thirdly,  it  was  shown  that

the  spatial  access  scores  of  gravity  models  vary  strongly
with  the  specification  of  the  distance  friction  parameter
[38].  Since  there  is  uncertainty  about  a  true  value  (i.e.,
representing  real-world  travel  preferences),  this  trans-
lates  into  uncertainty  regarding  the  spatial  access  meas-
ure. Wan, Zhan et al. [38] offered a remedy by computing
a  spatial  access  ratio,  i.e.,  interpreting  the  spatial  access
measure in relative terms. This makes the measure stable
to  different  distance  impedance  parameter  definitions.
Lastly, Guagliardo et al. [30] addressed the issue of circu-
larity  that  is  inherent  to  the  family  of  2SFCA  measures.
Provider  availability  is  adjusted  according  to  the  poten-
tial  demand  of  the  surrounding  population;  however,
one could argue that this potential demand first must be
adjusted for the potential availability of surrounding pro-
viders,  leading  to  a  circular  argument.  The  KD  method
avoids circularity by overlaying a provider and a popula-
tion density layer.

Moving forward, we believe that efforts of bringing the
methodological developments under one roof will be par-
ticularly valuable. In the past, Wang [21] for example has
unified  the  developments  on  distance  decay  within  the
generalized 2SFCA framework. Such work applied to the
wider  family  of  gravity  model-type  measures  would  be
beneficial  for  depicting  the  breadth  and  depth  of  meth-
odological developments and understanding them as fac-
ets of a common spatial access measurement framework.
Relatedly,  we  need  critical  reflection  and  assessment  of
the practical implications of the methodological develop-
ments. Several studies have conducted comparative anal-
yses,  e.g.,  to  evaluate  implications  of  different  distance
decay  specifications,  distance  friction  parameters,  or
other methodological choices (e.g., [23, 38, 46, 62]). Such
efforts  can  help  us  judge  which  methodological  choices
require  particular  care  and  deliberation.  A  comprehen-
sive  evaluation  spanning  the  methodological  develop-
ments presented in this study is thus indicated to identify
the  contribution  of  various  methodological  choices  to
changes in measure outcomes.

Review step 2: application studies

While  it  may  seem  striking  at  first  to  see  the  differ-
ence  in  application  frequency  of  2SFCA-type  meas-
ures  compared  to  base  gravity  model  or  Kernel  Density
approaches,  there  are  multiple  factors  explaining  this
resonance  within  applied  health  research.  Technically,
the  basic  2SFCA  method  is  a  special  form  of  the  base
gravity  model  which  disregards  locations  beyond  a  cer-
tain  threshold  and  assumes  equal  access  to  all  locations
within  that  threshold.  That  is,  through  the  catchment
areas,  a  cutoff  is  introduced.  This  has  two  main  advan-
tages over the base gravity model: First, it makes intuitive
sense to simply omit locations that are far away, as those

 Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 18 of 22

are unlikely to be visited. Second, introducing a threshold
in the form of catchment areas is computationally much
less intensive. Moreover, as compared to the KD method,
it  has  been  shown  that  2SFCA  has  a  clear  advantage  of
retaining the total number of providers within a system,
while  KD  is  weaker  in  that  regard,  especially  in  edge
areas [29].

Among  methodological  developments  within  the
2SFCA  family,  the  application  of  distance  decay  within
the  catchment  area  is  widely  used.  We  believe  that  the
intuition  of  distance  decay  within  a  catchment  area  is
convincing  and  makes  the  spatial  access  measure  more
realistic  resulting  in such wide usage in health  research.
In  addition,  implementing  a  distance  decay  function  in
a  2SFCA  framework  is  relatively  easy  conceptually  and
computationally.  Variable  catchment  area  sizes  have
seen moderate uptake within the 2SFCA method family.
At  the  same  time,  more  than  half  of  2SFCA  type  meas-
ures were applied to study areas with a mix of urban and
rural  regions. This  means  that  many  measures  are  com-
puted for areas with varying degrees of urbanicity with-
out  differentiating  them  in  terms  of  catchment  sizes.
Luo  and  Whippo  [13]  have  shown  that  spatial  access  is
overestimated in urban and underestimated in rural areas
when uniform catchment areas are assumed. However, it
remains  unclear  how  to  best  define  the  catchments  that
vary  between  urban  and  rural  areas  or  between  general
and specialized care providers as catchment area thresh-
olds  are  essentially  arbitrary.  The  outcome  unit  modi‑
fication  of  2SFCA  type  measures  (spatial  access  ratio)
to  make  it  interpretable  in  relative  terms  has  not  been
implemented  widely.  While  it  was  shown  that  using  a
relative  measure  makes  the  indicator  less  sensitive  to
the  travel  friction  coefficient  specification  [38],  it  is  not
appropriate  in  all  cases.  As  the  outcome  unit  cannot  be
interpreted in absolute terms anymore, statements on the
number of available providers per population are not pos-
sible. Therefore, the measure allows identifying high- and
low-access  areas  and  comparing  areas  within  a  health-
care  system.  For  healthcare  planning  however,  a  relative
access measure is hardly useful. Next, we observed mod-
erate uptake of methodological developments correcting
the overestimation of demand by incorporating provider
competition.  Generally,  the  inherent  overestimation  of
demand should be of concern for all 2SFCA type meas-
ures.  Yet,  the  majority  of  2SFCA  type  measures  did  not
consider  that.  Methodological  developments  of  this  cat-
egory  do  not  require  additional  data  but  make  intuition
and  computation  more  complex  which  might  impede
wide  use.  Using  a  local  and  global  distance  decay  func‑
tion to consider both relative and absolute distances was
not  commonly  implemented  in  applied  research.  This
methodological  development  offers  a  remedy  to  the

2SFCA-inherent issue of implicitly only modeling relative
distances within a catchment area [45]. There are no addi-
tional data requirements for implementing this approach.
However, the intuition at work here is not as straightfor-
ward as, for example, is the case for distance decay within
the catchment area, possibly preventing its use across the
board. Almost none of the 2SFCA-type measures applied
a subgroup‑specific access measure. Arguably, such meth-
odological  developments  are  context-specific  and  might
not  be  easily  transferable  across  healthcare  contexts.
While  many  studies  proposed  methodological  develop-
ments to account for multiple transportation modes, few
studies  applied  such  methods.  There  might  be  several
reasons  for  this.  Firstly,  additional  data  (mode-specific
transport  users,  mode-specific  distances)  is  required  to
compute  a  multi-mode  2SFCA.  Secondly,  the  computa-
tion  relies  on  somewhat  arbitrary  decisions  (e.g.,  which
modes  of  transportation  to  include  and  whether  catch-
ment  sizes  should  vary  by  mode  of  transport).  Thirdly,
multiple transport modes imply additional computational
complexity. Lastly, some application studies incorporated
time‑dependent access, explicitly modeling temporal vari-
ation in either travel time, demand, or supply. This allows
researchers  to  model  a  time-dependent  distribution  of
access at a population location rather than a single point
estimate. As this is the most recent type of development,
it  is  not  yet  widely  applied.  However,  it  is  expected  that
the share of studies incorporating a temporal perspective
will increase in the future.

More  than  half  of  the  application  studies  followed  a
descriptive  purpose.  Increasingly,  spatial  access  meas-
ures are also used as explanatory factors in observational
studies. It seems that knowledge about and computation
of  gravity  models  has  become  sufficiently  widespread
that  these  gravity  models  are  commonly  used  as  spatial
access  indicators  in  applied  health  research.  However,
there  is  room  for  improvement  when  it  comes  to  the
routine application of gravity models. Almost all studies
generated their spatial access indicator "from scratch" for
the purpose of the study. Only rarely did studies rely on
secondary data using previously computed spatial access
measures.  The  exception  lies  in  the  French  healthcare
context,  in  which  studies  resorted  to  the  same  database
providing  a  "ready-made"  spatial  access  measure.  That
goes  to  show  that  if  gravity  model  measures  are  easily
available,  e.g.,  provided  by  a  healthcare  authority  or  a
research institute, there are good chances of them being
used  in  applied  health  research.  We  believe  this  to  be
potential yet to harness. Relatedly, methodological devel-
opments  that  we  had  categorized  as  corrections  of  the
2SFCA methodology have not been implemented across
the board. We believe this to be rooted in the additional
complexity of the measures as well as less straightforward

Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 19 of 22

intuition. Generally, it seems that methodological devel-
opments  that  are  intuitive  to  understand,  do  not  have
additional  data  requirements,  and  do  not  have  great
impacts on computational complexity tend to be applied
more  frequently.  While  the  intuition  of  these  methodo-
logical  developments  can  be  challenging  to  grasp,  we
believe  that  they  are  valuable  advancements  in  the  fam-
ily of gravity models as they unveil and fix implicit flawed
assumptions.  We  argue  that  researchers  should  apply
such  methodological  corrections  or  instead  transpar-
ently  state  and  acknowledge  the  limitations  of  standard
2SFCA  measures  regarding  demand  and  supply  alloca-
tion,  relative  and  absolute  distance  friction,  distance
friction  parameter  uncertainty,  and  circularity  issues.
To  foster  the  use  of  gravity  models  in  research  practice
in general and the application of what we termed meth-
odological  corrections  in  particular,  further  facilitating
efforts are needed. There are multiple software solutions
and coding packages available for computing some of the
most popular spatial access gravity models (e.g., [70, 71]).
Expanding this, alongside a conceptual unification within
a common framework, a practical unification bringing all
the methodological developments presented in this study
together, e.g., within a software allowing for customizable
methodological  choice  as  well  as  parameter  setting,  will
be useful for research practice.

Strengths and limitations

Our  study  has  some  limitations.  We  focused  on  spa-
tial  access  to  healthcare  in  our  review,  thus  incorporat-
ing literature from the fields of health geography, health
services  research,  health  economics,  and  public  health.
There  may  be  studies  on  gravity  model  developments
from  other  disciplines  that  we  missed.  Additionally,  our
search strategy to identify applications relied on forward
citation  search  based  on  methodological  studies  iden-
tified  in  the  previous  step.  If  we  happened  to  miss  cer-
tain  studies  proposing  methodological  developments,
we might have also missed application studies that cited
those. We believe this to not be of strong concern, how-
ever,  as  most  empirical  studies  cite  not  only  the  exact
method that was applied, but also basic literature on the
topic, which in turn means that they would turn up in the
search results with our strategy, nonetheless.

The major strengths of our review are its two-step pro-
cedure and the depth and scope of analysis. With the two-
step procedure, we were able to identify methodological
developments  and  their  empirical  applications  in  one
study. We could thus describe major developments in the
field  of  potential  spatial  healthcare  access  measurement

and in addition deliver insights into how these measures
are used in research practice. Incorporating results from
over  300  empirical  studies  allowed  us  to  describe  grav-
ity  model  applications  in  a  comprehensive  manner.  We
believe  that  this  large  undertaking  provides  researchers
with  a  valuable  overview  of  the  existing  methods,  their
characteristics, strengths, and drawbacks.

Conclusions
Based  on  a  gravity  model  which  integrated  supply  and
demand as well as accessibility and availability dimensions
[10],  two  major  conceptual  developments  emerged:  The
Two-Step Floating Catchment Area (2SFCA) method and
the Kernel Density (KD) method. Virtually all other meth-
odological  developments  that  were  put  forward  evolved
from the 2SFCA method, thus forming a family of 2SFCA-
type  methods.  Within  this  2SFCA  method  family,  nov-
elty  categories  were  identified:  Distance  decay  within  the
catchment  area,  variable  catchment  area  sizes,  outcome
unit  modification,  provider  competition,  local  and  global
distance  decay,  subgroup-specific  access,  multiple  trans-
portation modes, and time-dependent access. The 2SFCA
method  family  was  commonly  used  in  research  practice:
Empirical studies almost exclusively applied methods from
the 2SFCA family for measuring spatial healthcare access
in  a  gravity  model  framework.  Among  the  2SFCA-type
application  cases,  distance  decay  within  the  catchment
area  was  a  methodological  development  widely  imple-
mented. Variable catchment area sizes and selection prob-
ability to account for provider competition were frequently
integrated into spatial access measurement as well. How-
ever, the use of the basic 2SFCA method remains common.
Most  methodological  developments  served  the  pur-
pose of approximating reality by integrating assumptions
about real-world conditions, such as higher distance tol-
erance in rural areas, or varying travel times by mode of
transportation. A small share of methodological develop-
ments  was  devoted  to  making  context-specific  adapta-
tions. A third group of methodological developments was
geared towards correcting 2SFCA-inherent flaws, such as
the overestimation of demand. Methodological develop-
ments  that  are  conceptually  straightforward  and  simple
to implement have caught on widely in empirical applica-
tion studies, while developments designed to correct the
methodology are not used across the board. Most empiri-
cal  studies  using  a  gravity  model  were  descriptive  stud-
ies,  outlining  the  spatial  access  to  health  services  in  an
area. Increasingly, gravity model measures also served as
potential explanatory factors for health outcomes.

Much potential remains in the secondary use of previ-
ously computed spatial access measures to further foster
their  application  in  research  practice.  Moreover,  wider
application  of  developments  designed  to  rectify  implicit

 Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 20 of 22

methodological  flaws  would  be  desirable.  To  that  end,
future research should aim for a conceptual and practical
unification  of  the  here  presented  methodological  devel-
opments under one roof.

Abbreviations
2SFCA
3SFCA
E2SFCA
KD
M2SFCA
MM-2SFCA
SPAR
V2SFCA

 Two-step floating catchment area
 Three-step floating catchment area
 Enhanced two-step floating catchment area
 Kernel density
 Modified two-step floating catchment area
 Multi-mode two-step floating catchment area
 Spatial access ratio
 Variable two-step floating catchment area

Supplementary Information
The online version contains supplementary material available at https:// doi.
org/ 10. 1186/ s12942- 023- 00358-z.

Additional file 1. Search strategy (Appendix A) and methodological
developments (Appendix B: Table B1).

Additional file 2. Supporting data: Application studies.

Acknowledgements
Not applicable.

Author contributions
BS and OS conceptualized the study and developed the methodology.
BS conducted the literature search. BS and OS extracted, analyzed, and
interpreted the data. BS wrote the original draft of the manuscript. BS and OS
reviewed and edited the manuscript. All authors read and approved the final
manuscript.

Funding
Open Access funding enabled and organized by Projekt DEAL. This research
was partly funded by the Leibniz-ScienceCampus "SOEP RegioHub" (Bielefeld
University, SOEP/DIW Berlin, Leibniz Association). We acknowledge support
for the publication costs by the Open Access Publication Fund of Bielefeld
University and the Deutsche Forschungsgemeinschaft (DFG).

Availability of data and materials
The datasets used and/or analyzed during the current study are included in
the additional information files.

Declarations

Ethics approval and consent to participate
Not applicable.

Consent for publication
Not applicable.

Competing interests
The authors declare that they have no competing interests.

Author details
1 Socio-Economic Panel (SOEP), German Institute for Economic Research
(DIW Berlin), Mohrenstraße 58, 11017 Berlin, Germany. 2 School of Public
Health, Bielefeld University, Universitätsstraße 25, 33615 Bielefeld, Germany.
3 Department of Business Administration and Economics, Bielefeld University,
Universitätsstraße 25, 33615 Bielefeld, Germany.

Received: 13 July 2023   Accepted: 21 November 2023

References
 1.

Levesque JF, Harris MF, Russell G. Patient-centred access to health care:
conceptualising access at the interface of health systems and popula-
tions. Int J Equity Health. 2013. https:// doi. org/ 10. 1186/ 1475- 9276- 12- 18.
 2.  Rosano A, Loha CA, Falvo R, van der Zee J, Ricciardi W, Guasticchi G, et al.
The relationship between avoidable hospitalization and accessibility to
primary care: a systematic review. Eur J Public Health. 2013;23:356–60.
https:// doi. org/ 10. 1093/ eurpub/ cks053.

 3.  WHO. Everybody’s business—strengthening health systems to improve
health outcomes. WHO’s framework for action. Geneva, Switzerland:
World Health Organization; 2007.
Joseph AE, Philips DR. Accessibility and utilization: geographical perspec-
tives on health care delivery. 1984.

 4.

 5.  Delamater PL, Messina JP, Shortridge AM, Grady SC. Measuring geo-

graphic access to health care: raster and network-based methods. Int J
Health Geogr. 2012;11:15. https:// doi. org/ 10. 1186/ 1476- 072X- 11- 15.
 6.  Penchansky R, Thomas JW. The concept of access: definition and relation-

ship to consumer satisfaction. Med Care. 1981;19:127–40.

 7.  Khan AA. An integrated approach to measuring potential spatial access

to health care services. Socioecon Plann Sci. 1992;26:275–87.

 8.  Guagliardo MF. Spatial accessibility of primary care: concepts, methods

and challenges. Int J Health Geogr. 2004;3:1–13.

 9.  McLafferty S. Place and quantitative methods: critical directions in quanti-
tative approaches to health and place. Health Place. 2020;61: 102232.
 10.  Joseph AE, Bantock PR. Measuring potential physical accessibility to gen-

eral practitioners in rural areas: a method and case study. Soc Sci Med.
1982;16:85–90.

 11.  Luo W, Wang F. Measures of spatial accessibility to health care in a GIS

environment: synthesis and a case study in the Chicago region. Environ
Plan B Plan Des. 2003;30:865–84.

 12.  Luo W, Qi Y. An enhanced two-step floating catchment area (E2SFCA)
method for measuring spatial accessibility to primary care physicians.
Health Place. 2009;15:1100–7.

 13.  Luo W, Whippo T. Variable catchment sizes for the two-step floating
catchment area (2SFCA) method. Health Place. 2012;18:789–95.

 14.  Mao L, Nekorchuk D. Measuring spatial accessibility to healthcare
for populations with multiple transportation modes. Health Place.
2013;24:115–22.

 15.  Bauer J, Müller R, Brüggmann D, Groneberg DA. Spatial accessibility of pri-
mary care in England: a cross-sectional study using a floating catchment
area method. Health Serv Res. 2018;53:1957–78.

 16.  Wang L. Analysing spatial accessibility to health care: a case study of

access by different immigrant groups to primary care physicians in
Toronto. Ann GIS. 2011;17:237–51. https:// doi. org/ 10. 1080/ 19475 683.
2011. 625975.

 17.  Gao F, Kihal W, Le Meur N, Souris M, Deguen S. Assessment of the spatial
accessibility to health professionals at French census block level. Int J
Equity Health. 2016;15:125. https:// doi. org/ 10. 1186/ s12939- 016- 0411-z.
 18.  McLafferty S, Wang F, Luo L, Butler J. Rural–urban inequalities in late-stage
breast cancer: spatial and social dimensions of risk and access. Environ
Plan B Plan Des. 2011;38:726–40. https:// doi. org/ 10. 1068/ b36145.
 19.  Delamater PL, Messina JP, Grady SC, WinklerPrins V, Shortridge AM. Do

more hospital beds lead to higher hospitalization rates? A spatial exami-
nation of Roemer’s Law. PLoS ONE. 2013;8: e54900. https:// doi. org/ 10.
1371/ journ al. pone. 00549 00.

 20.  Wan N, Zhan FB, Zou B, Wilson JG. Spatial access to health care services

and disparities in colorectal cancer stage at diagnosis in Texas. Prof Geogr.
2013;65:527–41. https:// doi. org/ 10. 1080/ 00330 124. 2012. 700502.

 21.  Wang F. Measurement, optimization, and impact of health care accessibil-
ity: a methodological review. Ann Assoc Am Geogr. 2012;102:1104–12.
 22.  Vo A, Plachkinova M, Bhaskar R. Assessing healthcare accessibility algo-
rithms: a comprehensive investigation of two-step floating catchment
methodologies family. 2015 Am Conf Inf Syst AMCIS 2015. 2015.
 23.  Chen X, Jia P. A comparative analysis of accessibility measures by the
two-step floating catchment area (2SFCA) method. Int J Geogr Inf Sci.
2019;33:1739–58.

 24.  Apparicio P, Gelb J, Dubé AS, Kingham S, Gauvin L, Robitaille É. The

approaches to measuring the potential spatial access to urban health
services revisited: distance types and aggregation-error issues. Int J
Health Geogr. 2017;16:1–24.

Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 21 of 22

 25.  Bivoltsis A, Cervigni E, Trapp G, Knuiman M, Hooper P, Ambrosini GL. Food
environments and dietary intakes among adults: does the type of spatial
exposure measurement matter? A systematic review. Int J Health Geogr.
2018;17:1–20.

 49.  Shao Y, Luo W. Supply-demand adjusted two-steps floating catchment

area (SDA-2SFCA) model for measuring spatial access to health care. Soc
Sci Med. 2022;296: 114727.

 50.  Langford M, Higgs G, Fry R. Multi-modal two-step floating catch-

 26.  Wood SM, Alston L, Beks H, Mc Namara K, Coffee NT, Clark RA, et al. The
application of spatial measures to analyse health service accessibil-
ity in Australia: a systematic review and recommendations for future
practice. BMC Health Serv Res. 2023;23:330. https:// doi. org/ 10. 1186/
s12913- 023- 09342-6.

 27.  Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD,

et al. The PRISMA 2020 statement: an updated guideline for reporting
systematic reviews. BMJ. 2021;372: n71.

 28.  Vo A, Plachkinova M, Bhaskar R. Assessing healthcare accessibility algo-
rithms: a comprehensive investigation of two-step floating catchment
methodologies family. AMCIS 2015 Proceedings. 2015;17:1–12.

 29.  Yang DH, Goerge R, Mullner R. Comparing GIS-based methods of measur-
ing spatial accessibility to health services. J Med Syst. 2006;30:23–32.
 30.  Guagliardo MF, Ronzio CR, Cheung I, Chacko E, Joseph JG. Physician

accessibility: an urban case study of pediatric providers. Health Place.
2004;10:273–83.

 31.  Siegel M, Koller D, Vogt V, Sundmacher L. Developing a composite index
of spatial accessibility across different health care sectors: a German
example. Health Policy (New York). 2016;120:205–12.

 32.  Schuurman N, Berube M, Crooks VA. Measuring potential spatial access
to primary health care physicians using a modified gravity model. Can
Geogr Can. 2010;54:29–45.

 33.  Jin M, Liu L, Tong D, Gong Y, Liu Y. Evaluating the spatial accessibility and
distribution balance of multi-level medical service facilities. Int J Environ
Res Public Health. 2019;16:1150.

 34.  Tao Z, Cheng Y, Du S, Feng L, Wang S. Accessibility to delivery care in

Hubei Province, China. Soc Sci Med. 2020;260: 113186.

ment area analysis of primary health care accessibility. Health Place.
2016;38:70–81.

 51.  Zhou X, Yu Z, Yuan L, Wang L, Wu C. Measuring accessibility of health-
care facilities for populations with multiple transportation modes
considering residential transportation mode choice. ISPRS Int J Geo-Inf.
2020;9:394.

 52.  Ma L, Luo N, Wan T, Hu C, Peng M. An improved healthcare accessibility
measure considering the temporal dimension and population demand
of different ages. Int J Environ Res Public Health. 2018;15:2421.
 53.  Song Y, Tan Y, Song Y, Wu P, Cheng JC, Kim MJ, et al. Spatial and tem-

poral variations of spatial population accessibility to public hospitals:
a case study of rural–urban comparison. GIScience Remote Sens.
2018;55:718–44. https:// doi. org/ 10. 1080/ 15481 603. 2018. 14467 13.

 54.  Xia T, Song X, Zhang H, Song X, Kanasugi H, Shibasaki R. Measuring

spatio-temporal accessibility to emergency medical services through
big GPS data. Health Place. 2019;56:53–62.

 55.  Paul J, Edwards E. Temporal availability of public health care in

developing countries of the Caribbean: an improved two-step floating
catchment area method for estimating spatial accessibility to health
care. Int J Health Plann Manage. 2019. https:// doi. org/ 10. 1002/ hpm.
2667.

 56.  Wang F, Luo W. Assessing spatial and nonspatial factors for healthcare

access: towards an integrated approach to defining health professional
shortage areas. Health Place. 2005;11:131–46.

 57.  Delamater P, Shortridge AM, Kilcoyne RC. Using floating catchment area
(FCA) metrics to predict health care utilization patterns. BMC Health Serv
Res. 2019;19:144.

 35.  McGrail MR, Humphreys JS. Measuring spatial accessibility to primary

 58.  Zahnd WE, Josey MJ, Schootman M, Eberth JM. Spatial accessibility to

health care services: utilising dynamic catchment sizes. Appl Geogr.
2014;54:182–8.

 36.  Kim Y, Byon YJ, Yeo H. Enhancing healthcare accessibility measurements
using GIS: a case study in Seoul. Korea PLoS One. 2018;13: e0194849.
 37.  Tao Z, Cheng Y, Zheng Q, Li G. Measuring spatial accessibility to health-

care services with constraint of administrative boundary: a case study of
Yanqing District, Beijing, China. Int J Equity Health. 2018;17:1–12.
 38.  Wan N, Zhan FB, Zou B, Chow E. A relative spatial access assessment
approach for analyzing potential spatial access to colorectal cancer
services in Texas. Appl Geogr. 2012;32:291–9.

 39.  Wan N, Zou B, Sternberg T. A three-step floating catchment area

method for analyzing spatial access to health services. Int J Geogr Inf Sci.
2012;26:1073–89.

 40.  Luo J. Integrating the huff model and floating catchment area methods

to analyze spatial access to healthcare services. Trans GIS. 2014;18:436–48.

 41.  Jang H. A model for measuring healthcare accessibility using the behav-
ior of demand: a conditional logit model-based floating catchment area
method. BMC Health Serv Res. 2021;21:660.

 42.  Shen Z, Gao G, Wang Z. Accessibility assessment of prehospital emer-

gency medical services considering supply-demand differences. J Adv
Transp. 2021;2021:1925354.

 43.  Tang J-H, Chiu Y-H, Chiang P-H, Su M-D, Chan T-C. A flow-based statistical
model integrating spatial and nonspatial dimensions to measure health-
care access. Health Place. 2017;47:126–38.

 44.  Paez A, Higgins CD, Vivona SF. Demand and level of service inflation in
Floating Catchment Area (FCA) methods. PLoS ONE. 2019;14: e0218773.
 45.  Delamater P. Spatial accessibility in suboptimally configured health care
systems: a modified two-step floating catchment area (M2SFCA) metric.
Health Place. 2013;24:30–43.

 46.  Bauer J, Groneberg DA. Measuring spatial accessibility of health care

providers—introduction of a variable distance decay function within the
floating catchment area (FCA) method. PLoS ONE. 2016;11: e0159148.
 47.  Wang L. Immigration, ethnicity, and accessibility to culturally diverse fam-

ily physicians. Health Place. 2007;13:656–71.

colonoscopy and its role in predicting late-stage colorectal cancer. Health
Serv Res. 2021;56:73–83.

 59.  Wan N, Zhan FB, Lu Y, Tiefenbacher JP. Access to healthcare and dispari-

ties in colorectal cancer survival in Texas. Health Place. 2012;18:321–9.

 60.  Langford M, Higgs G. Measuring potential access to primary healthcare

services: the influence of alternative spatial representations of popula-
tion. Prof Geogr. 2006;58:294–306.

 61.  Gautam S, Li Y, Johnson TG. Do alternative spatial healthcare access meas-

ures tell the same story? GeoJournal. 2014;79:223–35.

 62.  McGrail MR. Spatial accessibility of primary health care utilising the two
step floating catchment area method: an assessment of recent improve-
ments. Int J Health Geogr. 2012;11:50.

 63.  Jumadi J, Fikriyah VN, Hadibasyir HZ, Sunariya MIT, Priyono KD, Setiyadi

NA, et al. Spatiotemporal accessibility of COVID-19 healthcare facilities in
Jakarta, Indonesia. Sustainability. 2022;14:14478.

 64.  Kim K, Kwon K. Time-varying spatial accessibility of primary healthcare

services based on spatiotemporal variations in demand, supply, and
traffic conditions: a case study of Seoul South Korea. J Transp Health.
2022;27: 101531.

 65.  Brizan-St. Martin R, Paul J. Evaluating the performance of GIS method-

ologies for quantifying spatial accessibility to healthcare in Multi-Island
Micro States (MIMS). Health Policy Plan. 2022;37:690–705.

 66.  Xiong Q, Liu Y, Xing L, Wang L, Ding Y, Liu Y. Measuring spatio-temporal
disparity of location-based accessibility to emergency medical services.
Health Place. 2022;74: 102766.

 67.  Dai D. Black residential segregation, disparities in spatial access to health
care facilities, and late-stage breast cancer diagnosis in metropolitan
Detroit. Health Place. 2010;16:1038–52.

 68.  Jamtsho S, Corner R, Dewan A. Spatio-temporal analysis of spatial
accessibility to primary health care in Bhutan. ISPRS Int J Geo-Inf.
2015;4:1584–604.

 69.  Yang N, Shen L, Shu T, Liao S, Peng Y, Wang J. An integrative method for

analyzing spatial accessibility in the hierarchical diagnosis and treatment
system in China. Soc Sci Med. 2021;270: 113656.

 48.  Xiao Y, Chen X, Li Q, Jia P, Li L, Chen Z. Towards healthy China 2030: Mod-

 70.  Zhu H, Wang F. Appendix 5B: A toolkit for automated spatial accessibility

eling health care accessibility with patient referral. Soc Sci Med. 2021;276:
113834.

measures. In: Wang F, editor. Quant methods socio-economic appl GIS.
2nd ed. Boca Raton, FL: CRC Press; 2014. p. 112–3.

 Stacherl and Sauzet  International Journal of Health Geographics           (2023) 22:34

Page 22 of 22

 71.  Saxon J, Koschinsky J, Acosta K, Anguiano V, Anselin L, Rey S. An open
software environment to make spatial access metrics more accessible.
Data Sci: Univ. Chicago Cent. Spat; 2020.

 72.  McGrail MR, Humphreys JS. A new index of access to primary care ser-

vices in rural areas. Aust N Z J Public Health. 2009;33:418–23.

 73.  Plachkinova M, Vo A, Bhaskar R, Hilton B. A conceptual framework for
quality healthcare accessibility: a scalable approach for big data tech-
nologies. Inf Syst Front. 2018;20:289–302.

 74.  Ni J, Wang J, Rui Y, Qian T. An enhanced variable two-step floating catch-
ment area method for measuring spatial accessibility to residential care
facilities in Nanjing. Int J Environ Res Public Health. 2015;12:14490–504.

 75.  Bozorgi P, Eberth JM, Eidson JP, Porter DE. Facility attractiveness and

social vulnerability impacts on spatial accessibility to opioid treatment
programs in south carolina. Int J Environ Res Public Health. 2021;18:4246.

 76.  Matthews KA, Gaglioti AH, Holt JB, Wheaton AG, Croft JB. Estimating

health service utilization potential using the supply-concentric demand-
accumulation spatial availability index: a pulmonary rehabilitation case
study. Int J Health Geogr. 2020;19:30.

 77.  Polzin P, Borges J, Coelho A. An extended kernel density two-step floating
catchment area method to analyze access to health care. Environ Plann B
Plann Des. 2014;41:717–35.

 78.  Ni J, Liang M, Lin Y, Wu Y, Wang C. Multi-mode two-step floating catch-

ment area (2SFCA) method to measure the potential spatial accessibility
of healthcare services. ISPRS Int J Geo-Inf. 2019;8:236.

 79.  Tao Z, Cheng Y. Modelling the spatial accessibility of the elderly to

healthcare services in Beijing, China. Environ Plan B Urban Anal City Sci.
2019;46:1132–47.

 80.  Xing J, Ng ST. Analyzing spatiotemporal accessibility patterns to tertiary
healthcare services by integrating total travel cost into an improved
E3SFCA method in Changsha, China. Cities. 2022;122: 103541.

 81.  Barlet M, Coldefy M, Collin C, Lucas-Gabrielli V. L’Accessibilité potentielle

localisée (APL) : une nouvelle mesure de l’accessibilité aux soins appli-
quée aux médecins généralistes libéraux en France. Série Études Rech Dir
la Rech des études l’évaluation des Stat. 2012.

Publisher’s Note
Springer Nature remains neutral with regard to jurisdictional claims in pub-
lished maps and institutional affiliations.

• fast, convenient online submission •  thorough peer review by experienced researchers in your ﬁeld•  rapid publication on acceptance•  support for research data, including large and complex data types•  gold Open Access which fosters wider collaboration and increased citations  maximum visibility for your research: over 100M website views per year •  At BMC, research is always in progress.Learn more biomedcentral.com/submissionsReady to submit your researchReady to submit your research  ?  Choose BMC and benefit from: ?  Choose BMC and benefit from:
