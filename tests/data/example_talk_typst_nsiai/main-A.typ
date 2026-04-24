// https://github.com/typst/packages/tree/main/packages/preview/pinit/0.1.3
//#import "@preview/pinit:0.1.3": *

#import "@preview/lovelace:0.1.0": *
#show: setup-lovelace

// https://github.com/typst/packages/tree/main/packages/preview/colorful-boxes/1.2.0
#import "@preview/colorful-boxes:1.2.0": *
#import "@preview/cetz:0.1.2": canvas, plot

#import "@preview/polylux:0.3.1": *
#import themes.simple: *
// #set text(font: "Inria Sans")
#set text(font: "Arial")


#show: simple-theme.with(aspect-ratio: "4-3", footer: "Neuroscience-Inspired Artificial Intelligence, Artur Andrzejak, January 8, 2024")

// ====== Settings ======
// The Following does not work for #xpause
//#enable-handout-mode(true)
//#let xpause = {pause} // enable pause
#let xpause = []    // disable pause

// ===== Own functions =====
#import "shared.typ": *


 
// ==== Styling ====
// From  https://typst.app/docs/reference/model/emph/
#show emph: it => {
//  text(blue, style: "italic", weight:"semibold",  it.body)
  text(blue, weight: "semibold",  it.body)
}


// ==== Abbreviations ====
#show "xmul": $times.circle$
#show "xrho": $rho(x)$



// ===== Slides =====

#aip_title_slide_content(
  title: "Neuroscience-inspired Artificial Intelligence",
  subtitle: "Cognitive Science - Heidelberg University Lecture Series",
  subtitle2: "Winter 2023/24",
  date: "January 8, 2024",
  show_credentials: true
)

#centered-slide[
  = Motivation and Overview
] #slide[
 == Why Neuroscience-inspired AI?
//#v(0.75cm)

- Human brain is a proof that intelligence is possible at all

- Modelling it is an alternative or a complement to creating AI "from scratch"

- Unfortunately, we do not really know how the brain works
 - We even do not even understand the mechanics of some fundamental processes, e.g. learning, memory, reasoning, …
#xpause

- However, understanding nervous systems of simpler organisms like _drosophila melanogaster_  (fruit fly) is more advanced

- We can use this knowledge to create building blocks of AI systems

 - General principles: e.g. sparse distributed representations, noise tolerance, …
 - Concrete algorithms: e.g. FlyHash, continual learning, …
 
  
] #slide[
== Different Levels of Abstraction

- Modeling biological intelligence is a multi-level problem
 - From the level of _neurons_ to the level of _behavior_ (and beyond)
 - The distinction is the proximity to the biological "hardware" (neurons, synapses, …) 

- There are many interesting projects/approaches at different levels of abstraction
 - From _neurons_: Blue Brain Project, Human Brain Project, …
 - To _brains structures_: SPAUN (Semantic Pointer Architecture Unified Network), Nengo, …
 - To _principles_ and _algorithms_: VSAs, sparsity, FlyHash, ...

- Today we will focus on the _principles_ and _algorithms_ level because it is the most practical one
 - Lower abstraction levels do not (yet) scale to real-world problems

] #slide[
== Example of the Level _Brain Structures_ 

- Projects: Neural Engineering Framework, Semantic Pointer Architecture Unified Network (SPAUN), How to Build a Brain 
 - Chris Eliasmith at Computational Neuroscience Research Group, University of Waterloo

- Book: Chris Eliasmith, *How to Build a Brain: A Neural Architecture for Biological Cognition*, 2013 (El13)

#v(-0.2cm)
#align(center)[
#image("figs\how-to-build-a-brain.png", width: 5.5cm)
]

] #slide[
== Aspects Covered in This Lecture

- _Examples of successful transfers_ from neuroscience to AI 
 1. Solutions to fundamental algorithmic problems uncovered by studying drosophila and their generalizations
   - *FlyHash*, (*FlyModel* for *continual learning*)

 2.  General principles of the representation and processing of information in the brain
   - *Hyperdimensional computing* (aka VSAs), (*sparsity*) 

#xpause

 
- _Discussion of the differences_ between biological and AI systems
 - What are the differences on the level of observable behavior?
 - Which current "building blocks" of AI are biologically implausible?
 - => Which AI mechanisms are missing or should be improved?
// - Today: _learning_, sparsity, energy usage
] #slide[


] #centered-slide[
= _FlyHash_:   A Neuroscience-inspired Algorithm  for Similarity Search

] #slide[
== Similarity Search (Nearest Neighbor Search)
// #v(0.75cm)

- _Similarity search_ is the task of finding similar items in a collection
 - E.g. similar images in a database or similar documents on the web

- It is a fundamental computing problem, especially relevant for  large-scale information retrieval systems
 - Think of Google search, Amazon product recommendations, ...
#xpause

- A trivial solution is to compare a query item with each collection item 
 - But this is not feasible for large collections (e.g. millions of images, billions of documents) of high-dimensional items (e.g. images)

 - Also not energy efficient (e.g. for mobile devices)

] #slide[
== Similarity Search via Locality Sensitive Hashing
 

- Luckily, there is a class of algorithms that can solve this problem efficiently: _Locality Sensitive Hashing_ (LSH)

 - LSH algorithms map items to a set of _buckets_ (or _bins_) such that similar items are mapped to the same bucket with high probability

 - => Similarity search is reduced to finding similar items in a bucket



#v(-0.1cm)
#align(center)[
#image("figs\FlyHash\LSH-A.drawio.svg", width: 15.5cm)
]
#xpause

- There are many variants of LSH algorithms, e.g. _MinHash_, _SimHash_, _Random Projection Hashing_, _Multi-Probe LSH_,  ...
] #slide[
== FlyHash Algorithm
// #v(0.75cm)
// #xpause

- In 2017, a new variant of an LSH algorithm was proposed: _FlyHash_ 

 - Found by studying the neural circuits of a _fruit fly olfactory system_

 - Sanjoy Dasgupta et al., *A neural algorithm for a fundamental computing problem*, Science 2017 (Da17)


#v(0.3cm)
#align(center)[
//  https://www.stockvault.net/photo/201013/fruit-flies
#image("figs\FlyHash\stockvault-fruit-flies-c.png", width: 12.5cm)
]
] #slide[
== Fruit Fly Olfactory System /1

- Fruit can learn to associate odors with rewards or punishments

- Their olfactory circuits generate a _"tag"_ for each odor
  - The tag is a set of neurons that fire when that odor is present
  - These neurons are called _Kenyon cells_ (KC) (about 2,000 KCs)
#xpause

- Interestingly, this tag is a _sparse high-dimensional vector_
  - Only about 5% or 100 neurons out of 2,000 fire for a given odor
//  - We will see later that both properties are important 
- Similar odors generate similar tags (see ethanol vs. methanol)
  
#v(0.3cm)
#align(center)[
//  https://www.stockvault.net/photo/201013/fruit-flies
#image("figs\FlyHash\odor-tags.drawio.svg", width: 12.5cm)
]

] #slide[ 
== Fruit Fly Olfactory System /2

The tags are generated as follows:

 1. The odor is detected by _olfactory receptor neurons_ (_ORNs_)
  - \~50 types, each with different sensitivity and selectivity to odors
 
 2. ORNs are connected to _projection neurons_ (_PNs_) 
  - \~150, these remove dependence of the signal on concentration
 3. PNs connect to _Kenyon cells_ (_KCs_) in a sparse and random way
  - Each of the KCs receives input from about 6 different ORNs
  - => Dimensionality is expanded from \~50 to \~2,000
 4. Sparsity of the tags is achieved by a single inhibitory neuron called _APL_ (_anterior paired lateral_ neuron)
  - All but the 5% most active KCs are silenced by APL
  - It is a _Winner-Take-All_ (_WTA_) circuit



] #slide[ 
== Fruit Fly Olfactory System /3

 #v(0.3cm)
#align(center)[
//  Inspired by https://www.cell.com/current-biology/fulltext/S0960-9822(13)00424-7#figures
#image("figs\FlyHash\fly-wiring-nose-to-KCs.drawio.svg") // , width: 18.5cm)
]


] #slide[ 
== From Fruit Fly to FlyHash

- The fruit fly olfactory system is a _biological_ LSH algorithm
 - It maps odors to sparse high-dimensional vectors (tags) such that similar odors are mapped to similar tags

- The key elements are:
 - _Random projections_ of the inputs (ORNs) to outputs (KCs)
 - _Expansion_ of the input space ($d~$50) to a high-dim. space ($d ~$2,000)
 - _Sparsity_ of the output (tags) via a WTA circuit (APL)
#xpause

- Based on this principles, a new  _computational_ LSH algorithm was proposed: _FlyHash_
  - It maps items to sparse high-dimensional vectors (tags) such that similar items are mapped to similar tags (LSH property)
  - Similar performance as state-of-the-art LSH algorithms, but requires about 20x less computations

] #slide[
== FlyHash Algorithm 

#pseudocode(
  line-numbering: false,
  [*Input:* vector $bold(x) in RR^d$],
  [\ ],
  [*Parameters:* hash length $m$, sparsity factor $k$, sampling rate $alpha$],
  // \ for the random projection], 
  [\ ],
  [\ ],
  [\# Generate $m k$ sparse, binary random projections], 
//  [\# by summing from $q =  floor(alpha d)$ random indices each], ind,
//  [$q =  floor(alpha d)$], 
  [$ S = {S_i | S_i = {floor(alpha d)$ random integers in $[0,d]$  $} } $], 
  

  [\ ],
  [\ ],
  [\# Compute high-dimensional projection $P(bold(x))$ (dimension $m k$)], 
  [*for* $j = 1$ *to* $m k$ *do*], ind,
  [\ ],
    [$P_j (bold(x))$ = sum of $bold(x)$ components at indices $S_j$], ded,
  [\ ],
  [*end for*],
  [\ ],
  [\ ],
  [\# Sparsify the result - retain $m$ largerst entries], 
  [\ ],
  $h_1(bold(x)) = op("WTA")(P(bold(x)), m)$, 

  [\ ],
  [\ ],
  [*return* $h_1(bold(x))$]
)

_Fruit fly_: we have $d=50$, $alpha=6/50$, $k=20$, $m=100$ => the output is a vector $h_1(bold(x))$ of dimension $m k = 2000$ with $m=100$ non-zero entries

 
] #slide[
== Binning with the FlyHash Algorithm 

- Remaining difficulty: since the tags (output $h_1(bold(x))$) is high-dimensional, even similar input vectors  are unlikely to have same tags (i.e. be mapped to the same bucket)

- For example, for the data set SIFT-1M (1 million images) with $k=20$ and $m=16$ (tags have dimensionality $m k = 320$), FlyHash produces about 860,000 unique tags 
 - => almost all images are mapped to different buckets
#xpause

- A solution is a so-called _multi-probe LSH_, where nearest neighbors of a query are searched also in "nearby"  buckets

- This approach adapted for FlyHash is detailed in the follow-up paper:
 - Jaiyam Sharma and Saket Navlakha, *Improving Similarity Search with High-dimensional Locality-sensitive Hashing*, 2018, (Sh18)
 
] #slide[ 
== Lessons Learned from the Biological Paragon

-  The fruit fly LSH algorithm uses a _combination_ of random projections, high dimensionality, and sparsity
- Used separately in computational LSH algorithms, but not together

- Why binary, sparse random projections?
 - _Energy efficiency_: computational savings of factor 20 vs. dense, Gaussian random projections 

- Why sparsity?
 - _Fault tolerance_: if a few neurons fail, the tag is still similar to the original one
 - Supports _learning_ of associations between odors and rewards/punishments => FlyModel by Y. Shen et al. (2021)

- Why high dimensionality?
 - A general principle of neural computation => _HD computing_
]
#centered-slide[
  = Computing with High-Dimensional Vectors
  == Basic Concepts 
] #slide[
 == Traditional Computing vs. Brain Computing
//#v(0.75cm)

- What _computers_ are good at, but brains are not  
 - Raw speed  

 - Fast and accurate arithmetic  
 - Following instructions literally  

#xpause
#v(1.5cm)
- What _brains_ are good at (and energy efficient as well)
 - Recognizing people and things  

 - Learning from examples, reason by analogy  
 - Learn to use language and reason by logic  
 - Control our interaction with the world

] #slide[

== Computing with Huge Vectors: Vector Symbolic Architectures (VSAs)
//#v(0.75cm)
- _Fan-in_ and _fan-out_: number of input/output signals entering/leaving a circuit
- Neuroscience studies observed that nervous systems have huge fan in’s/fan out’s: *On the order of 1,000 – 200,000 nerves*
#xpause

- This motivated investigation of data processing with huge vectors: dimensions 1,000 – 10,000 
#xpause

- Umbrella terms:
 - _Vector Symbolic Architectures_ (VSAs, R. Gayler)
 - _Hyperdimensional Computing_ (HDC, P. Kanerva)
 - _Semantic Pointer Architecture_ (SPA, C. Eliasmith)
#xpause

- Considered as a “closest shot” at brain-like AI technology
//- Hot but still a niche area

] #slide[
== Why are VSAs Interesting? /1
//#v(0.75cm)

- VSAs use _distributed representation_ to encode information 
 - Concepts or symbols are represented by patterns of activity across a large number of elements (vectors), similarly as in the brain


- _Hierarchical and uniform representation of aggregates_ 
 - VSAs can represent combinations of concepts and/or their sequences as a single vector => individual concepts and their collections are represented in the same way

- VSAs can use _sparse representation_ (only few entries are non-zero) //, which helps to reduce the computational load and noise sensitivity

  - => Noise tolerance: If one neuron fails, the representation of the concept can still be maintained by the remaining neurons


- _Generalization_: Similar concepts can share overlapping representations, allowing for the generalization of knowledge

] #slide[
== Why are VSAs Interesting? /2
//#v(0.75cm)

- _Symbolic_ methods: explicit algorithms, rule-based systems with “hard” knowledge, (logic) programming languages,…
- _Sub-symbolic_ methods: neural networks, probabilistic methods, … 
// - These areas are mostly disjoint, but there is recent interest in neural-symbolic methods

#align(center)[
#table(  
  columns: (auto, auto),
  inset: 10pt,
  align: horizon,
  [*Symbolic*], [*Syb-symbolic*],
[#text(size: 16pt)[
  Symbols \
  Logical \
  Serial \
  Reasoning \ 
  von Neumann machines \
  Localised \
  Rigid and static \
  Concept composition and expansion \
  Model abstraction \
  Human intervention \
  Small data \
  Literal/precise input  ]
],
[
  #text(size: 16pt)[
  Numbers \
  Associative \ 
  Parallel  \
  Learning  \
  Dynamic Systems  \ 
  Distributed  \
  Flexible and adaptive  \
  Concept creation and generalization  \
  Fitting to data  \
  Learning from data  \ 
  Big data  \
  Noisy/incomplete input  ]
]
)]

] #slide[
== Why are VSAs Interesting? /3
- VSAs can bridge _symbolic_ and _sub-symbolic_ representations and methods

- Example: heterogenous learning methods:
 - [Sub] Learning from data via _backpropagation_

 - [Sym] Learning _holistic transformations_ (functions manipulating data structures) from only 1 example (or few ones)
 - [Sym] _Manually engineering functions_ for manipulating symbolic and continuous data
- Different options, but same framework

 - => Usable in a unified system


] #slide[
== How to Compute with HD Vectors?
// #v(0.75cm)
- A few components and few operations make a surprising powerful system of computing
#xpause

- Components
 - _Representational space_, e.g. binary/complex vectors

 - _Operations_ on these representations (4 key operations)
 - _Item memory_ (or associative memory)
 - _Measure of similarity_ $op("sim")()$ between vectors (distance-based) 
#xpause

- Mandatory properties
 - High-dimensionality, typically $d=1000  …  10,000$

 - Randomness

] #slide[
#let im_width = 2.7cm
== Representational Space: Options
// #v(0.75cm)
#grid(columns: (1fr, 5fr), gutter: 0.25fr)[#image("figs\vsa\mr-smolensky.png", width: im_width)][ 
  - _TPR_: Tensor Product Variable Binding 
   - Paul Smolensky, 1989]
// #xpause
 
#grid(columns: (1fr, 5fr), gutter: 0.25fr)[#image("figs\vsa\mr-plate.png", width: im_width)][ 
  - _(F)HRR_: (Fourier) Holographic Reduced Representation
   - Tony Plate, HRR: 1990, Fourier: 1995
   - C. Eliasmith: Semantic Pointer Architectures (SPA) 
   ]
// #xpause
 
#grid(columns: (1fr, 5fr), gutter: 0.25fr)[#image("figs\vsa\mr-kanerva.jpg", width: im_width)][ 
  - _BSC_: Binary Spatter Codes
   - Paul Smolensky, 1989]
// #xpause
 
#grid(columns: (1fr, 5fr), gutter: 0.25fr)[#image("figs\vsa\mr-gayler.png", width: im_width)][ 
  - _MAP_: Multiply Add Permute
   - Ross Gayler, 1998
]

] #slide[
== Representational Space: Options /2
- Less common representations:
 - _MBAT_: Matrix Binding of Additive Terms  

 - _SBDR_: Sparse Binary Distributed Repr., Kussul et al.
 - _SBC_: Sparse Block-Codes, M. Laiho et al.
 - _GAHRR_: Geometric Analogue of Holographic Reduced Representations, D. Aerts  et al. 

- More information and a historical overview:
 - Denis Kleyko, Module 2 at Seminar *Computing with HD Vectors*, UC Berkeley, 2021, (Kl21)


] #slide[
== VSA Operations
//#v(0.75cm)
- _Bundling_ or _superposition_ or _“add”_: $x+y$
 - For creating sets
 - E.g. via component-wise addition
#xpause

- _Binding_ or _multiply_: $x$ xmul $y$
 - For “labeling” a vector/value $x$ with $y$ or vice versa
 - E.g. via component-wise multiplication
#xpause

- _Unbinding_ or _release_: xmul $x^(-1)$
 - Essentially, an inverse of binding: $(y times.circle x) times.circle x^(-1) = y$
 - For retrieving a labelled value
#xpause

- _Permutation_ or _“protect”_: xrho
 - For creating sequences
 - E.g. cyclic shift of a vector



] #slide[
== Example 1 of a VSA Representation: MAP
// #v(0.75cm)
- _Multiply / Add / Permute (MAP)_ representation (Ross Gayler, 1998)

- Vectors are “bipolar”, i.e. their elements are $+1$'s and $-1$'s
 - Essentially correspond to binary $0\/1$-vectors

- E.g. three random vectors with dimensionality $d = 10,000$
 - $A = (-1 +1 -1 +1 +1 +1 -1 #h(0.4cm) ... #h(0.4cm) +1 -1 -1)$
 - $B = (+1 -1 +1 +1 +1 -1 +1  #h(0.4cm) ... #h(0.4cm)  -1 -1 +1)$
 - $C  =  underbrace((+1 -1 +1 +1 -1 -1 +1  #h(0.4cm) ... #h(0.4cm)  +1 -1 -1), "10,000 dims")$

- Each vectors represents a _symbol_, e.g. "cake", "red", "man"

] #slide[
== Multiply Add Permute (MAP) - Operations
// #v(0.75cm)
- _Superposition_
 - Component-wise addition $x + y$ = $(x_1 + y_1, x_2 + y_2, ..., x_d + y_d)$
 - Depending on the variant may be normalized or not

- _Binding_
  - Component-wise multiplication $x$ xmul $y$ = $(x_1 y_1, x_2 y_2, ..., x_d y_d)$
- _Unbinding_
 - Same as binding, i.e. component-wise multiplication

- _Permutation_
 - Any (random but fixed) permutation of the vector components

] #slide[
== Example 2 of a VSA Representation: FHRR
//#v(0.75cm)
- _Fourier Holographic Reduced Representations (FHRR)_ (Tony Plate, 1995)

- _Representational space_: Vectors have as components complex numbers $e^(i phi)$ with $phi$ $~$  $U(-pi, pi)$ 
  - i.e. $phi$ is drawn from the uniform distribution in $[-pi, pi]$
- _Superposition_: Component-wise addition with normalization (to have unit magnitude)

- _Binding_: Component-wise multiplication $dot.circle$
- _Unbinding_: Component-wise multiplication with the complex conjugate of the binding vector

- _Permutation_: Any (random but fixed) permutation of the vector components


] #slide[
== Similarity of Vectors
//#v(0.75cm)

- *MAP*: Similarity $op("sim")(x,y)$ between two vectors $x$ and $y$ is measured by the _dot product_ 

 - I.e. sum of component-wise products: $op("sim")(x,y) = x dot.c y = sum^d_(i=1) x_i y_i$

 - Essentially, not normalized  _cosine similarity_ 
#xpause

#v(2cm)
- *FHRR*: Similarity is _mean of sum of cosines of angle differences_:
  $ op("sim")(x,y) = (op("Real")(x^𝑇 dot.c y^∗))/d $




] #slide[
== Similarity of Random HD Vectors

- For two random vectors $x$ and $y$ with a large number of dimensions, the expected value of their similarity is nearly $0$: $ E[op("sim")(x,y)] approx 0 $

// - Intuition: high-dimensional random vectors are nearly orthogonal
#xpause 

#v(2cm)
#align(center)[
#stickybox(
  rotation: 2deg,
  width: 18cm
)[
*Key property of high-dimensional vectors*: \

Almost any two of such vectors are dissimilar, approximately orthogonal!
]
]

] #slide[
== Similarity of Random HD Vectors: Intuition

Given a random vector $x$ in $R^2$ or $R^3$, what are the sets of vectors _dissimilar_ (or _approximately orthogonal_) to $x$?
#v(1cm)
#align(center)[
#grid(columns: (1fr, 1fr), gutter: 0.1fr)[
#image("figs\vsa\dissimilar-vecs-R2.png", width: 8cm)][
#image("figs\vsa\dissimilar-vecs-R3.png", width: 8cm)]
]
#v(1cm)
#text(size: 12pt)[
From: Peer Neubert et al., An Introduction to Vector Symbolic Architectures and Hyperdimensional Computing, ECAI 2020, (Ne20)]

] #slide[
== Similarity of Random HD Vectors: Intuition

Probabilities that two random vectors are almost orthogonal (red) vs. similar (blue) by the number of dimensions
#v(0.2cm)
// #align(center)[
// #image("figs\vsa\approx-orthogonal-vecs-by-dim.png", width: 14cm)
// ] 
// #v(0.1cm)
// #text(size: 12pt)[
// From: Peer Neubert, Kenny Schlegel, Stefan Schubert, An Introduction to Vector Symbolic Architectures and Hyperdimensional Computing, ECAI 2020, https://www.tu-chemnitz.de/etit/proaut/workshops_tutorials/vsa_ecai20/rsrc/vsa_slides.pdf]
 
#align(center)[
#canvas(length: 1cm, {
  plot.plot(size: (12, 8),
    x-tick-step: 200,
    x-ticks: (0,1000),
    y-tick-step: 0.5,
    x-label: "Dimensionality",
    y-label: "Probability",
    {
      plot.add(
        domain: (0, 1000), d => 0.000005*d,
        style: (stroke: (paint: blue,  thickness: 5pt))) 
      plot.add(
        // domain: (0, 1000), d =>calc.pow(d/100, 1/4)/1.7,
        domain: (0, 1000), d => calc.ln(1+d)/6.9,
        style: (stroke: (paint: red,  thickness: 5pt)) 
        )
    })
})

#text(size: 16pt)[
#rect[Dissimilar vectors:  #text(red)[red ---] \
Similar vectors:  #text(blue)[blue ---]
]]]

] #slide[
== Properties of VSA Operations in Terms of Similarity
//#v(0.75cm)
- _Bundling_ or _superposition_ or _“add”_: $+$
 - Sum of VSA vectors is _similar_ each of the summands: $op("sim")(x+y, x) approx 1$ and $op("sim")(x+y, y) approx 1$
 - => We can easily test for set membership 
#xpause

- _Binding_ or _multiply_: xmul
 - "Product" of VSA vectors is _dissimilar_ to each of the factors: $op("sim")(x times.circle y, x) approx 0$ and $op("sim")(x times.circle y, y) approx 0$
 - => Essentially, we can label and "protect" a vector  
#xpause


- _Permutation_ or _“protect”_: xrho
 - As with binding, the result is _dissimilar_ to the argument: $op("sim")(rho^k (x), x) approx 0$ for any $k>0$
 - Allows to label an element with its position $k$ in a sequence, and distinguish it from other positions of same element


 
 
] #centered-slide[
  = Data Structures with VSA Vectors
] #slide[
== Traditional vs. VSA-based Data Structures
// #v(0.75cm)

- VSA vectors can be used to represent "collection-like" data structures
 - E.g. records, lists, trees, graphs, …
#xpause

- Let us store a record with 3 fields $x, y, z$ (values are $a, b, c$):
 - $h = {x: a, y: b, z: c}$
#xpause

- Traditional computing 
 - Each $x, y, z$ is a named field (= offset address), i.e. $h.x$, $h.y$, $h.z$ are different storage locations
 - So each $a, b, c$ is a value stored at a _separate_ offset address
 - Of course, $h$ needs more memory than each of $a, b, c$
#xpause

- As we will see shortly, with VSAs we store a record $h$ in a _holographic_, _superposed_ way
 - ... as a single vector of the _same_ dimensionality as each of $a, b, c$!

] #slide[ 
== VSA-based Records

- With VSAs, we store record $h$ in a superposed way, without fields:

 1. The first part is the HD vector $H$ representing the record $h$: \
  _*$H = x$ xmul $a + y$ xmul $b + z$ xmul $c$*_ (recall that xmul is the "bind" operation)

 2. The second part is an item memory storing all active HD vectors, especially $a, b, c, x, y, z$
  - For cleaning up after retrieval (comes later)
#xpause

- Note that $H$ is a _superposition_ of three HD vectors  $x$ xmul $a$, ..., $z$ xmul $c$ and has the same dimensionality as each of $a, b, c$

- *=> This gives a uniform representation of individual values and their collections*
- However, in total we do not save memory (in this case), because we need the item memory

] #slide[
== Retrieving from VSA-based Records /1

- Given a query $q$ and a record $H = x$ xmul $a + y$ xmul $b + z$ xmul $c$, how to retrieve the value labeled with e.g. $q = x$?
  - Traditional computing:  let res = $h.x$

- In VSAs, we have two steps: (1) unbind, and (2) clean up
#xpause

1. Unbinding for $q = x$ (we assume MAP, as unbind and bind operations are the same, i.e. each element is its own inverse under xmul) \
  $ x times.circle H &=  x times.circle (x times.circle a + y times.circle b + z times.circle c) \
  &= #text(blue)[$x times.circle x times.circle a$] + #text(maroon)[$x times.circle y times.circle b$] + #text(red)[$x times.circle z times.circle c$] \
  &= #text(blue)[$a$] + #text(maroon)[$op("noise")$] + #text(red)[$op("noise")$] \
  &= #text(blue)[$a'$] 
  approx a $
  

] #slide[
== Retrieving from VSA-based Records /2

2. Clean up the result $a'$ (which we expect to be $approx a$)

 - Find among the  vectors stored in the item memory $M$ a nearest neighbor to $a'$ (i.e. vector with the highest similarity to $a'$)

 - If done right: $op("sim")(a', a)$ is significantly higher than $op("sim")(a', v)$ for any other vector $v eq.not a$ 
  


] #slide[
== Observations /1
- Why are the noise terms in not a problem for retrieving?
 - $ x times.circle H &=  x times.circle (x times.circle a + y times.circle b + z times.circle c) \
  &= #text(blue)[$x times.circle x times.circle a$] + #text(maroon)[$x times.circle y times.circle b$] + #text(red)[$x times.circle z times.circle c$] \
  &= #text(blue)[$a$] + #text(maroon)[$op("noise")$] + #text(red)[$op("noise")$] 
  $
#xpause

- Because a binding operation xmul produces a vector which is _dissimilar_ to any of the arguments:
 -   $op("sim")(p, p times.circle r) approx 0$ and also $op("sim")(p, p times.circle r times.circle s) approx 0$ for any $p, r, s$
 - This is a key property of the binding operation xmul
#xpause

- So, in particular, $op("sim")(b, x times.circle y times.circle b) approx 0$ and $op("sim")(c, x times.circle z times.circle c) approx 0$
- => The 2nd and 3rd terms will not interfere: They won’t erroneously give us values of $b$ or $c$


] #slide[
== Observations /2

- Why can we reliably clean up, i.e. $a$ is a vector in $M$ with highest similarity $op("sim")$ to $a'$?
#xpause

- Recall: Almost any pair of random HD vectors is dissimilar (approximately orthogonal)
#xpause

- In particular, each of $x, y, z, a, b, c$ stored in $M$ are mutually approximately orthogonal
- => #text(blue)[$a$] + #text(maroon)[$op("noise")$] + #text(red)[$op("noise")$] will be most similar to #text(blue)[$a$] and not to any other vector in $M$

// == Low Influence of Noise on Clean-Up
//- Optional, see MMD s14, slides 26+27

 
] #slide[
== Hierarchical Data Structures

- VSAs can be used to store (arbitrarily deep) hierarchies of data

- Example: Concept dog as hierarchy of different parts

#v(1cm)
#align(center)[
#image("figs\vsa\image-dog-hierarchy.png", width: 16cm)
]
#v(1cm)
#text(size: 12pt)[
From: Ashwinkumar Ganesan et al., "Learning with Holographic Reduced Representations", 2021, (Ga21)
]

]

#slide[
== Representing Hierarchies

- Encode 𝑑𝑜𝑔 as a superposition vector:
 - 𝑑𝑜𝑔 = $h$ xmul ℎ𝑒𝑎𝑑 + $b$ xmul 𝑏𝑜𝑑𝑦 + $l$ xmul 𝑙𝑒𝑔𝑠
 - $h, b, l$ are HD-vectors representing key (fields)
 - ℎ𝑒𝑎𝑑, 𝑏𝑜𝑑𝑦, 𝑙𝑒𝑔𝑠 are values, e.g. “pointers” to image parts
- ℎ𝑒𝑎𝑑 is itself a superposition of “deeper” parts
- Note: all vectors have the same dimension => We can create hierarchies of any depth!

#v(-0.8cm)
#align(center)[
#image("figs\vsa\hierarchy-representation-dog.png", width: 14.5cm)
]
#v(-0.65cm)
#text(size: 10pt)[
From: Ashwinkumar Ganesan et al., "Learning with Holographic Reduced Representations", 2021, (Ga21)
]

] #slide[
== Querying in  Hierarchies

- Given 𝑑𝑜𝑔 and item memory M, you can ask e.g.:
 - What is the vector (or “pointer” to image) for the nose?
1. Decode the HD-vector ℎ𝑒𝑎𝑑:
 - Compute  ℎ𝑒𝑎𝑑 $approx r_1 = h' times.circle $ 𝑑𝑜𝑔 
 - Then clean up: retrieve ℎ𝑒𝑎𝑑 from $M$ (most similar vector to $r_1$)    
2. Given ℎ𝑒𝑎𝑑, decode 𝑛𝑜𝑠𝑒:
 𝑛𝑜𝑠𝑒 $approx r_2 = n' times.circle$  ℎ𝑒𝑎𝑑, then clean up

#v(-0.2cm)
#align(center)[
#image("figs\vsa\hierarchy-representation-dog.png", width: 14.5cm)
]
#v(-0.65cm)
#text(size: 10pt)[
From: Ashwinkumar Ganesan et al., "Learning with Holographic Reduced Representations", 2021, (Ga21)
]


] #slide[
== Data Structures for Sequences

- How can we store a sequence like $a, b, c, a, q, ...$ using VSAs?
#xpause

- We could use records, with labels acting as positions:
  $ v_1 times.circle a + v_2 times.circle b + v_3 times.circle c + v_4 times.circle a + v_5 times.circle q $
- But it is more common and flexible to use permutations xrho:
   $ rho^1(a) + rho^2(b) + rho^3(c) + rho^4(a) + rho^5(q) $
- Note: We use the property of permutations that the result and argument are dissimilar: $ op("sim")(x, rho^k (x)) approx 0 $
- … To disambiguate every element from each other, including double occurrence of $a$

] #centered-slide[
  = Applications of VSAs
] #slide[
== Applications in Deep Learning
// #v(0.75cm)

- Recall that a sum of vectors is similar to each of the summands
 - => We can replace some operations for each vector in a set by a single operation on the vector sum

- This was exploited e.g. in the following papers 
- Ashwinkumar Ganesan et al., *Learning with Holographic Reduced Representations*, 2021, (Ga21)
 - A “classical” deep NN outputs a single VSA-vector which represents a set of up to 670k labels
- Mohammad Mahmudul Alam et al., *Recasting Self-Attention with Holographic Reduced Representations*, ICML'23, (Al23)
 - Self-attention mechanism of a Transformer is replaced by VSA operations on bundled key-value pairs
 - Seemingly speeds up transformer training up to 370 times (???)


] #slide[
== Duality of Symbolic and Sub-symbolic Learning

- A binding operation $ y = f times.circle x$ can be considered as a mapping from a vector $x$ to vector $y$, with $f$ being a function representing the mapping

- Given $x$ and $y$, we can immediately compute a suitable mapping $f$ as $f = y times.circle x^(-1)$ (we use here the unbinding operation $times.circle x^(-1)$)
- This can be also used for complex transformations on VSA-encoded data structures, e.g. reasoning on logical formulas:
  1. $x_1 arrow.r x_2$ VSA-encoded as $op("ante") times.circle x_1 + op("cons") times.circle x_2$
  2. $not x_1 or x_2$ VSA-encoded as $op("first") times.circle op("not") times.circle x_1 + op("sec") times.circle x_2$
  - We can compute the mapping $f$ from the first to the second formula as $f = op("ante")^(-1) times.circle op("first") times.circle op("not") + op("cons")^(-1) times.circle op("sec")$

- Such _one-shot learning_ (from one/few examples) is dual to _sub-symbolic_ learning of $f$ from data (e.g. via backpropagation)
- Largely unexplored area of _neural-symbolic_ learning (Ne01, Ne02)

] #slide[
== Other Applications of VSAs

- _Semantic Pointer Architecture Unified Network_ (SPAUN) of Eliasmith et al. 2008,  (El13)
 - A framework for building systems which resemble specific brain regions, such as the prefrontal cortex, basal ganglia, and thalamus
 - Uses VSAs (called there SPAs) for representing concepts and their combinations
 - A brain model with 2.5 million simulated neurons can recognize numbers, remember them, figure out numeric sequences, and write them down with a robotic arm
  
- VSAs have been used to implement _Finite State Machines_
- Also a _universal_ (Turing-complete) _computer_ should be possible with VSA (but not yet implemented)
 - Advantage: Learning from examples, not programming
]
// ] #centered-slide[
// = The FlyModel: Continual Learning Approach Modelled by the Fruit Fly Olfactory System
// ] #slide[

// ] #slide[
// == Todo or skip
// // #v(0.75cm)
//  ] #slide[

#centered-slide[
//= Differences between Biological and Computational Mechanisms for Intelligence
= Discussion: How can Inspiration from Neuroscience Help? 
] #slide[
== Is it Worth It?

- Major advances in AI in recent years come from computer science, and are only remotely inspired by neuroscience (if at all)

 - E.g. deep learning, algorithms in computer vision, generative AI, transformers,  …
 
#xpause

#v(2cm)
#align(center)[
#stickybox(
  rotation: -2deg,
  width: 12cm
)[
*Is it worth it to look at neuroscience at all?*  
]
]
] #slide[
== Persistent Problems of Current Machine Learning / AI

- On the level of observed phenomena, current ML/AI faces many problems compared to biological intelligence, e.g.: 
 - No _one-shot learning_, i.e. learning from one/few examples
 - No _continual learning_, i.e. learning new concepts without forgetting old ones in arbitrary order
 - Lack of _interpretability_, i.e. ability to relate cause and effect in the model
 - Lack of _trustworthiness_: 
  - models don't know what they know, and what they don't know
  - => Hallucinations of GPT3/4, and almost all ML models
 - Low robustness to _adversarial examples_, i.e. models are easily fooled by small perturbations of input data
 - Low _energy efficiency_
 - No theory: we don't really know _why_ e.g. GPT works so well

] #slide[
== Hypothesis: Core Mechanisms of AI / ML are Fundamentally Insufficient

- It seems that the core mechanisms in current machine learning / AI face some fundamental problems

- *Possibly inspiration from neuroscience can help to overcome these problems*
#xpause

- Example of such ML/AI mechanisms:
 - _Learning_: mostly via _backpropagation_ with _end-to-end_ training 

 - _Information representation/storage_: as weights of neurons, with no control where  information is stored in the model

] #slide[
== Learning in AI: Backpropagation

- ML/AI: _backpropagation_ (BP) compares a correct output with the actual output of the model, and updates the weights over the whole model computes 

 - Based on the gradient of the error with respect to the weights of the model (i.e. how much does each weight contribute to the error)

- BP is biologically implausible, e.g. because it requires backlinks to every "storage location", and is computationally expensive
- Geoffrey Hinton (Turing-Award 2018), one of the inventors of backpropagation and deep learning, repeatedly attempted to replace BP by other learning mechanisms
 - E.g. Forward-Forward Algorithm from 2022 (Hi22)
// - E.g. todo: hypothesis about the backlinks in the neurons

] #slide[
== Learning in Biological Organisms: Fruit Fly, again! /1

- Fruit fly olfactory circuitry uses another mechanism based on _associative learning_ (Mo20)
 - It connects odors (as high-dimensional tags discussed before) with rewards/punishments 

- The fly olfactory system is a _continual learning_ system, i.e. it can learn new associations without forgetting old ones
 - I.e. it can learn new associations in arbitrary order, without forgetting old ones 
 - Contrary to current ML/AI, which requires shuffled training data 

- Btw: this mechanism was also successfully transferred to AI as the _FlyModel_ (Sh23)


 
] #slide[
== Learning in Biological Organisms: Fruit Fly /2

- Fruit fly stores associations between odors and behaviours in synapses between the _KCs_ (_Kenyon cells_) and the _MBONs_ (_Mushroom Body Output Neurons_) (Fe18, Sh23)
#xpause

- How does fly associates an odor A with an electric shock? 

 - Initially, synapses from odor activated Kenyon Cells (KCs) have equal weights to both the "approach" MBON and the "avoid" MBON
 - Pairing odor A with punishment weakens _only_ the synapses between the "approach" MBON and the KCs
  - This is achieved via releasing dopamine to a compartment containing only such synapses 
 - _All other synapses remain "frozen"_, especially the synapses between the "avoid" MBON and the KCs
 - Over time, the reduced synaptic weights between odor A KCs and the approach MBON reliably establish the avoidance association 


// - Initially, the synapses from KCs activated by odor A to both the “approach” MBON and the “avoid” MBON have equal weights. 
// - When odor A is paired with punishment, the KCs representing odor A are activated around the same time that a punishment-signaling dopamine neuron fires in response to the shock. 
//  - The released dopamine causes the synaptic strength between odor A KCs and the approach MBON to decrease, resulting in a net increase in the avoidance MBON response. 
//  - Eventually the synaptic weights between odor A KCs and the approach MBON are sufficiently reduced to reliably learn the avoidance association (Fe18, Sh23)
 
] #slide[
  == Learning in Biological Organisms: Fruit Fly /3
 #v(0.3cm)
#align(center)[
#image("figs\FlyHash\KCs-to-MBONs.png", width: 22.5cm)
]
#v(1cm)
#text(size: 12pt)[
From: Yang Shen, Sanjoy Dasgupta, Saket Navlakha; Reducing Catastrophic Forgetting With Associative Learning: A Lesson From Fruit Flies. 2023, (Sh23)]

] #slide[
== Learning in Biological Organisms: Fruit Fly /4

- There are multiple differences between this approach and backpropagation

- Learning is _highly localized_ to only the synapses between the KCs and the MBONs
 - Low energy cost, also mechanistically interpretable

- Because we learn to associate to simultaneous events, there is no need for backlinks or "error computation"

- No changes of already correct associations (e.g. different to the perceptron algorithm) 
 - Experiments show that this is essential for  _continual learning_ 


] #slide[
  == There is Much More to Learn from Neuroscience

  // - Learning
  //  - Hintons approaches, why backpropagation is not biologically plausible
  //  - Example from FlySystem: Learning associations between odors and rewards/punishments
  //  - Continual learning
  //  - One-shot learning
  //  - AI: Adversarial examples
  //  - We know what we know, and what we don't => this "meta-knowledge" is 
  //  - Learning sequences and hierarchical Markov chains (Roy Kurzweil, book "How to Create a Mind"?)
  //   - Consider similarity to transformers
  // - Similarity of Transformers to activities in the brain
  // - Energy efficiency
  // - Space vs. computation
  // - Fault tolerance: training with noisy data creates sparse activations
  // - Fazit: consider sparsity, associative learning, energy efficiency, fault tolerance
  // - high dimensionality is already there in deep learning
 
 - Hierarchical Temporal Memory (HTM) by Numenta
 
 - Sparse Distributed Memory (SDM) by Pentti Kanerva
 
 - Unintended analogies to brain mechanisms
  - Transformer model architecture might be similar to brain structures
   - Caucheteux, C., Gramfort, A. & King, JR. Evidence of a predictive coding hierarchy in the human brain listening to speech, 2022, (Ca22)

- Hierarchical Markov chains advocated by Roy Kurzweil in his book "How to Create a Mind" (2012)
 
#centered-slide[
= Thank you! 
] 

// - Hypothesis of major, fundamental differences
//  - How information is stored (local vs. distributed in the model)
//  - Learning: backpropagation vs. associative learning or other (unknown) mechanisms

// - Hypothesis: Locality of storage of the information
//  - Biology: FlySystem
//  - Seeing is believing
//  - Sparse representation of activation patterns reveals the monoliguistic representations of concepts
//  - Why it makes sense?
//   - Selective updates of information in the brain, allows continual learning
//   - Lower energy consumption to change/update information
//   - For AI: Interpretable representations, easier correction

// - Transition of our research 
//  - Central project: C2C translation
//  - Focus now on the interpretability and intervention in Transformer models
//   - Understanding where/how information is stored in TF
//   - Manipulation of information in TF, e.g. to correct errors
//   - Evolution of TF models to improve interpretability and intervention
  
] #slide[
] #slide[
= References
#v(0.75cm)

/ Al23: Mohammad Mahmudul Alam, Edward Raff, Stella Biderman, Tim Oates, and James Holt. 2023. Recasting self-attention with holographic reduced representations. ICML'23, Vol. 202, Article 23, 490-507, https://dl.acm.org/doi/10.5555/3618408.3618431

/ Ca22: Caucheteux, C., Gramfort, A. & King, JR. Evidence of a predictive coding hierarchy in the human brain listening to speech. Nat Hum Behav 7, 430–441 (2023). https://doi.org/10.1038/s41562-022-01516-2

/ Da17: Sanjoy Dasgupta et al. ,A neural algorithm for a fundamental computing problem. Science 358,793-796(2017). DOI:10.1126/science.aam9868

/ El13: Chris Eliasmith, How to Build a Brain: A Neural Architecture for Biological Cognition, Oxford University Press, 2013 

/ Fe18: Johannes Felsenberg et al, Integration of parallel opposing memories underlies memory extinction, Cell 2018 Oct 18;175(3):709-722.e15. doi: 10.1016/j.cell.2018.08.021. 

/ Ga21: Ashwinkumar Ganesan et al., "Learning with Holographic Reduced Representations", NeurIPS 2021,  arxiv.org/abs/2109.02157

/ Hi22: G. Hinton, The Forward-Forward Algorithm: Some Preliminary Investigations,  https://arxiv.org/abs/2212.13345, 2022.

/ Kl21: Denis Kleyko, Module 2 at Seminar “Computing with HD Vectors”, 2021,  UC Berkeley, https://www.hd-computing.com/course-computing-with-high-dimensional-vectors#h.hh2loih13jrc

/ Li20:  Lillicrap, T., Santoro, A., Marris, L., Akerman, C., and Hinton, G. E., Backpropagation and the brain. Nature Reviews Neuroscience, 21:335-346, 2020.

/ Mo20: Mehrab N. Modi, Yichun Shuai, Glenn C. Turner, The Drosophila Mushroom Body: From Architecture to Algorithm in a Learning Circuit, Annual Review of Neuroscience 2020 43:1, 465-484

/ Ne01: Jane Neumann. 2001. Holistic Processing of Hierarchical Structures in Connectionist Networks. Ph. D. Dissertation. The University of Edinburgh.

/ Ne02: Jane Neumann. 2002. Learning the systematic transformation of holographic reduced representations. Cogn. Syst. Res 3, 2 (2002), 227-235.

/ Ne20: Peer Neubert, Kenny Schlegel, Stefan Schubert, An Introduction to Vector Symbolic Architectures and Hyperdimensional Computing, ECAI 2020, https://www.tu-chemnitz.de/etit/proaut/workshops_tutorials/vsa_ecai20/rsrc/vsa_slides.pdf


/ Sh23: Yang Shen, Sanjoy Dasgupta, Saket Navlakha; Reducing Catastrophic Forgetting With Associative Learning: A Lesson From Fruit Flies. Neural Comput 2023; 35 (11): 1797-1819. doi: https://doi.org/10.1162/neco_a_01615

/ Sh18: Jaiyam Sharma and Saket Navlakha, Improving Similarity Search with High-dimensional Locality-sensitive Hashing, http://arxiv.org/abs/1812.01844, 2018


]
 