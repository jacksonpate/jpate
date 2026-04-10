---
course: Microbiology (BIOL 3201)
topic: Weeks 10-11 + Lab 3 and 6-7
---

# Microbiology — Weeks 10–11 & Lab Readings

## Week 10 — Bacterial DNA Replication & PCR

### 7.3 DNA Replication — Overview
- Microbial DNA must replicate accurately and quickly before cell division
- Bacterial replication uses many proteins and genes forming a complex machine
- E. coli doubling time: ~20 minutes, but takes 40 minutes to copy its chromosome
- Solution: before one round of replication ends, the bacterium initiates the next one (or two)

### Key Features of Bacterial DNA Replication
- **Semiconservative**: each daughter cell receives one parental strand + one newly synthesized strand
- **Bidirectional**: starts at a fixed origin (oriC) and progresses in opposite directions
- **5' to 3' synthesis only**: DNA polymerase can only add nucleotides to the 3' end
- DNA bases are added only to a preexisting 3'-OH group

### Replication Puzzles
**Puzzle 1**: E. coli has a 40-min doubling time, but only a 20-min doubling time. Answer: initiates the next round before finishing the current one.

**Puzzle 2**: If polymerases synthesize only 5'→3' and the two strands are antiparallel, how are both strands synthesized simultaneously at a moving fork?
- Answer: Leading strand is synthesized continuously; lagging strand is synthesized discontinuously via **Okazaki fragments** (Tsuneko and Reiji Okazaki)

### 8 Key Enzymes to Know
| Enzyme | Function |
|--------|----------|
| **DnaA** | Initiator protein — initiates replication at oriC |
| **DnaB (helicase)** | Unwinds the double helix |
| **DNA primase** | Synthesizes the RNA primer |
| **DNA Pol III** | Major replication enzyme; adds nucleotides 5'→3' |
| **DNA gyrase** | Relieves DNA supercoiling (topoisomerase II) |
| **DNA Pol I** | Removes RNA primers and replaces with DNA |
| **DNA ligase** | Joins Okazaki fragments |
| **Topoisomerase IV** | Separates concatenated chromosomes at termination |

### Leading vs. Lagging Strand
- **Leading strand**: synthesized continuously in the 5'→3' direction toward the fork
- **Lagging strand**: synthesized discontinuously in Okazaki fragments (synthesized away from the fork, then ligated)
- Okazaki fragments order example: 4→2→1→3 (last made = first listed from fork)

### DNA Replication Summary
- DNA Pol III adds nucleotides in the 5'→3' direction
- Initiated by an RNA primer (made by DNA primase)
- Leading strand: continuous; Lagging strand: discontinuous (Okazaki fragments)
- DNA Pol I removes RNA primers; DNA ligase joins Okazaki fragments

### Termination of Replication
- E. coli has up to 10 terminator sequences (ter)
- **Tus protein** (terminus utilization substance) binds ter sequences, acts as a counter-helicase
- **Topoisomerase IV + XerCD proteins** separate ringed catenanes (interlinked chromosomes) formed at completion

### When Replication Begins (Replication Puzzle — Ask ChatGPT)
- What determines when/where DNA replication begins in bacteria?
- Key proteins: **SeqA** and **DnaA**
- DnaA binds oriC to initiate replication; SeqA delays re-initiation

### Plasmids
- Two kinds of extragenomic DNA: horizontally transferred plasmids & bacteriophage genomes
- Plasmids can carry traits like antibiotic resistance
- Found in archaea, bacteria, and eukaryotic microbes
- Usually circular; need host proteins to replicate
- Plasmids replicate through **Rolling Circle Mechanism**

**Rolling Circle Replication — Concept Check**
1. Is there a lagging strand in rolling circle replication? — No (one strand is nicked and used as template; the other is synthesized continuously)
2. Is an RNA primer required? — No (in many rolling circle systems)

### DNA Replication in Eukaryotes
- Eukaryotic genomes are linear, larger, and more complex
- Replication starts from **multiple origins** of replication
- **DNA Pol epsilon (Pol ε)**: copies the leading strand
- **DNA Pol delta (Pol δ)**: copies the lagging strand

### End Replication Problem in Eukaryotes
- Linear chromosomes lose sequences at ends with each replication
- **Telomeres** protect chromosome ends
- **Telomerase** enzyme contains an RNA template (TERC) and extends telomeres

### Comparison: Bacteria vs. Eukaryotes vs. Archaea
| Feature | Bacteria | Eukaryotes | Archaea |
|---------|----------|------------|---------|
| Chromosome | Single circular | Linear, multiple | Single circular (some multiple) |
| Origins | Single | Multiple | 100–150 |
| Telomeres | None | Yes | None (some resemble telomerase) |
| Main polymerase | DNA Pol III | DNA Pol ε/δ | DNA Pol B and Pol D |

### PCR (Polymerase Chain Reaction)
- Amplifies specific genes >1 million-fold within hours
- Source: **Thermus aquaticus** — heat-tolerant bacteria
- Key enzyme: **Taq DNA polymerase** (heat-resistant)
- Process: Denature (heat) → Anneal primers → Extend with Taq

**PCR Concept Checks**
- Does PCR involve Okazaki fragments? **No** — PCR uses heat to denature, not a replication fork
- Can helicase replace thermal cycler? **No** — helicase cannot withstand PCR temperatures
- DNA synthesized by Taq from a human template would look like **human DNA** (template determines sequence)

### Chapter Summary
DNA replication phases:
1. **Initiation**: at oriC
2. **Elongation**: at replication forks
3. **Termination**: at terminus (ter)
- Plasmids = autonomously replicating extrachromosomal DNA
- PCR copies DNA outside the cell using heat-stable Taq polymerase

---

## Week 11 — Transcription & RNA

### Chapter Overview
- Transcription: DNA → RNA
- RNA polymerases and sigma factors
- The genetic code, ribosomes, and tRNAs
- Process of Transcription
- Prokaryotic Gene Regulation
- Antibiotics that affect bacterial transcription

### The Central Dogma
- **Transcription**: DNA template → RNA copy (mRNA)
- **Translation**: mRNA decoded → protein assembled
- Cells access their genome through these two steps

### RNA Structure
- Usually single-stranded
- RNA-RNA double strands form **hairpin** structures
- Contains **ribose sugar** (vs. deoxyribose in DNA)
- **Uracil replaces thymine**

### Classes of RNA
| RNA Class | Function |
|-----------|----------|
| **mRNA** (messenger RNA) | Encodes proteins |
| **rRNA** (ribosomal RNA) | Integral part of ribosomes |
| **tRNA** (transfer RNA) | Shuttles amino acids to ribosome |
| **sRNA** (small RNA) | Regulates transcription or translation |
| **tmRNA** | Frees ribosomes stuck on damaged mRNA |
| **Catalytic RNA** | Carries out enzymatic reactions |

### Bacterial Genome Organization
- **Monocistronic**: one promoter → one gene → one RNA transcript (gene operates independently)
- **Polycistronic (operon)**: one promoter → multiple genes transcribed together

### Transcription Big Picture
- RNA polymerase (RNA pol) reads the DNA template strand (3'→5') and synthesizes RNA (5'→3')
- The coding strand (non-template strand) has the same sequence as the RNA (with T→U)

### RNA Polymerases and Sigma Factor
- RNA pol is a complex enzyme
- In bacteria composed of:
  - **Sigma factor (σ)**: recognizes promoter; required for **initiation** phase
  - **Core polymerase (2α, β, β')**: required for **elongation** phase
- **Sigma-70 (σ70)** = housekeeping sigma factor in E. coli
  - Recognizes consensus sequences at **−10** and **−35** positions upstream of the transcription start site (+1)
  - All sigma factors compete for the same core RNA polymerase
  - Different sigma factors respond to different environmental conditions

### Three Phases of Transcription
1. **Initiation**: RNA pol (aided by sigma factor) binds to promoter → helix unwinds → first nucleotide synthesized
2. **Elongation**: RNA chain extended; DNA unwinds ahead forming a ~17-bp transcription bubble; RNA pol moves at ~45 bases/sec; positive supercoils ahead removed by topoisomerases (DNA gyrase)
3. **Termination**: RNA pol detaches after transcript is complete

### Termination Signals
1. **Rho-dependent**: Relies on Rho protein; contact between Rho and RNA pol causes termination
2. **Rho-independent**: Inverted repeat sequence on DNA template forms a stem-loop (hairpin) structure in RNA, causing termination

### Prokaryotic Gene Regulation
- Structural genes of related function organized in operons; transcribed together under one promoter
- Operon regulatory region = **promoter + operator**
- **Repressor** binds to operator → structural genes NOT transcribed
- **Activator** binds to regulatory region → genes ARE transcribed

### Repressible Operon: trp Operon
- Genes are normally ON
- **Tryptophan (trp) operon**: classic repressible example
- When trp accumulates → trp molecules bind the trp repressor → repressor changes shape → binds trp operator → RNA synthesis blocked → genes turn OFF
- Logic: make tryptophan until there's enough, then stop

### Inducible Operon: lac Operon
- Genes are normally OFF
- **lac operon** encodes 3 genes for lactose hydrolysis (→ glucose + galactose)
- In absence of lactose: lac repressor binds operator → blocks RNA pol → genes OFF
- When lactose present: lactose binds repressor → repressor changes shape → falls off operator → genes turn ON
- **Maximal activation** requires:
  1. Lactose present (releases Lac repressor)
  2. Glucose absent (allows CAP activator to bind — catabolite activator protein)

### Eukaryotic Transcription Regulation (comparison)
- Transcriptional regulators can act from a distance
- Activator proteins bound to distant **enhancers** attract RNA pol and general transcription factors to promoter
- Also recruit chromatin-modifying proteins

### Antibiotics That Affect Transcription
| Antibiotic | Source | Mechanism |
|-----------|--------|-----------|
| **Rifamycin B** | Amycolatopsis mediterranei | Selectively binds bacterial RNA pol → inhibits transcription (bacterial RNA pol is different from eukaryotic) |
| **Actinomycin D** | Actinomycete | Non-selectively binds DNA → inhibits transcription → used in cancer treatment (harms humans) |

### Chapter Summary
- Transcription = DNA template → RNA transcript, carried out by RNA polymerase
- Sigma factor recognizes promoter; core polymerase elongates RNA until termination signal
- Many RNA classes; mRNA, rRNA, and tRNA directly involved in protein synthesis
- Prokaryotes regulate transcription via repressors (repressible genes) and inducible systems (substrate-regulated genes)

---

## Week 11 — Translation & Proteins

### Chapter Overview
- Translation: mRNA → amino acid sequence (protein)
- The genetic code, ribosomes, and tRNAs
- Process of Translation (Initiation, Elongation, Termination)
- Coupling of Bacterial Transcription and Translation
- Post-translational modifications
- Antibiotics that target bacterial translation

### Translation Overview
- mRNA message is read in triplets of nucleotides called **codons**
- Ribosomes are the machines that read mRNA and translate it into protein
- tRNA molecules decode the RNA language into the protein language

### The Genetic Code
- 4³ = **64 possible codons**
- 61 codons specify amino acids (including start codons)
- 3 are **stop codons**: UAA, UAG, UGA
- The code is **degenerate/redundant**: multiple codons can encode the same amino acid
  - Example: GCU, GCC, GCA, GCG all code for **Alanine**
- **Start codon**: AUG (methionine) — sets the reading frame

### tRNA Structure and Function
- tRNA has a **cloverleaf shape**
- Two functional regions:
  1. **Anticodon**: hydrogen bonds with the mRNA codon (antiparallel)
  2. **3' acceptor end**: binds the amino acid ("charged" tRNA)
- tRNAs contain many unusual, modified bases
- Cell has 20 tRNA types — one for each amino acid
- tRNA anticodon binds mRNA codon in antiparallel fashion

### The Ribosome
- Two subunits containing rRNA and proteins
- **Prokaryotes**: 30S + 50S = 70S ribosome
  - 30S subunit contains **16S rRNA** (1540 nucleotides in E. coli)
  - 50S subunit contains 23S and 5S rRNA
- "S" = Svedberg unit (measures sedimentation rate, not size)

### 16S rRNA and Evolutionary Significance
- Carl Woese used 16S rDNA (small subunit) to construct the tree of life
- rDNA sequences used to determine evolutionary distance among species
- 16S rRNA serves as a **molecular clock** for bacterial species identification

### Shine-Dalgarno Sequence — Finding the Reading Frame
- Every mRNA has 3 potential reading frames
- mRNA contains a purine-rich sequence upstream of start site: **5'-AGGAGGU-3'** (Shine-Dalgarno sequence)
- Located 4–8 bases upstream of the start codon in E. coli
- Complementary to the 3' end of **16S rRNA** → guides ribosome to correct reading frame

### Three Stages of Protein Synthesis

**1. Initiation**
- 30S and 50S subunits come together
- tRNA carrying first amino acid (fMet) pairs with start codon (AUG) on mRNA at the **P site**
- Second aminoacyl-tRNA approaches the **A site**
- Requires initiation factors (IF1, IF2, IF3) and GTP

**2. Elongation**
- A site: second codon pairs with a tRNA carrying the second amino acid
- First amino acid joins to second via **peptide bond** — attaches polypeptide to tRNA in P site
- Ribosome translocates: second tRNA moves to P site, first tRNA moves to E site (exit)
- Next codon brought into A site
- Process repeats: amino acids added, peptide chain grows
- Requires elongation factors (EF-Tu, EF-G) and GTP

**3. Termination**
- Ribosome reaches a **stop codon** (UAA, UAG, UGA)
- No tRNA matches a stop codon — **release factors** bind instead
- Polypeptide released
- Last tRNA released; ribosome disassembles into 30S and 50S subunits
- Released polypeptide folds into a new protein

### Practice Problems
- Template strand 5' CTA GCA CTT AAC 3' → mRNA = 3' GAU CGU GAA UUG 5' → reading 5'→3': GUU GAA GUC GAU
- Coding strand 5' AAT CGT CAA TTC 3' → mRNA = 5' AAU CGU CAA UUC 3' → amino acids: Asn-Arg-Gln-Phe

### Coupled Transcription and Translation (Bacteria)
- In bacteria, ribosomes bind to the 5' end of mRNA **before transcription is complete**
- Multiple ribosomes can translate the same mRNA simultaneously (polyribosomes/polysomes)
- In **eukaryotes**, coupling is **impossible** — transcription in nucleus, translation in cytoplasm

### Prokaryote vs. Eukaryote Comparison
| Feature | Prokaryote | Eukaryote |
|---------|------------|-----------|
| Location of transcription/translation | Cytoplasm (coupled) | Nucleus (transcription) / cytoplasm (translation) |
| Ribosome size | 70S (30S + 50S) | 80S (40S + 60S) |
| mRNA processing | None (polycistronic) | 5' cap, poly-A tail, splicing (monocistronic) |
| Coupling | Yes | No |

### Post-Translational Modifications
1. After translation, proteins fold to functional 3D structure
2. Incorrectly made or folded proteins get **degraded**
3. Others are secreted via protein traffic control
   - Transmembrane proteins
   - Protein export to the periplasm
   - Secretion of proteins outside the cell

### Protein Traffic Control / Secretion
- Proteins destined for cell membrane/envelope require special export systems
- Tagged with **hydrophobic N-terminal signal sequences** (15–30 amino acids)
- Bound by **Signal Recognition Particle (SRP)**
- Then undergo co-translational or post-translational export

**Transmembrane Proteins**
- Some inserted directly via ribosome "paralyzed" by SRP → resumes translation when encountering FtsY in membrane
- Others inserted via the **Sec system**

**Protein Export to Periplasm**
- Via **SecA-dependent general secretion pathway**
  - SecB: keeps protein unfolded
  - SecA: moves protein to SecYEG
  - SecYEG: exports proteins across cell membranes

**Journeys Through the Outer Membrane**
- Gram-negative bacteria export proteins completely outside (e.g., digestive enzymes, toxins)
- **Seven secretion systems** (Type I–VII) have evolved
- Type I exports proteins to the outside environment

### Antibiotics That Affect Translation
| Antibiotic | Target |
|-----------|--------|
| **Streptomycin** | Inhibits 70S ribosome formation |
| **Tetracycline** | Binds 30S subunit → inhibits translation |
| **Chloramphenicol** | Binds 23S rRNA of 50S subunit |
| **Erythromycin** | Binds 23S rRNA of 50S subunit |

### Chapter Summary
- Ribosomes composed of two subunits (30S + 50S in bacteria)
- Translation phases: Initiation → Elongation → Termination
- Proteins may be modified, folded, or secreted after translation
- Cells possess protein-degrading machines
- Bacterial translation is a prime antibiotic target

---

## Lab 3 Lecture — Gram Positive Cocci and Rods

### Quiz Review (Gram Stain)
- Mordant for Gram stain: **Iodine**
- Counter stain for Gram stain: **Safranin**
- Simple stain uses one stain (False — simple stain uses one stain, but the question implies two — answer is False)
- Brightfield microscopes have three lens systems: **oculars, objectives, and condenser**
- Disinfectants destroy: **Vegetative cells and viruses**

### Lab 3 Procedure Overview
**Step 1**: Use primary tests to identify family of Gram positive unknown bacterium
**Step 2**: Perform secondary tests to identify Gram positive unknown bacterium
**Step 3**: Interpret results from Lab 3 to identify Gram positive unknown bacterium

### Smear Preparation Protocol
1. Flood water slide with a large amount of DI water
2. Flame loop, transfer one loopful of water to middle of slide
3. Flame loop again, grab bacteria from unknown plate and spread into the water drop
4. Heat-fix the slide
5. Gram stain procedure:
   - Crystal violet (primary stain) → 60 seconds
   - Wash with DI water
   - Iodine (mordant) → 60 seconds
   - Wash with DI water
   - Ethanol (decolorizer) → wash
   - Safranin (counter stain) → wash
   - Blot with bibulous paper

### Primary Tests for Family Identification
Perform catalase, oxidase, and KOH first (while smear air-dries), then Gram stain:

| Family | Morphology | Catalase | Oxidase |
|--------|-----------|---------|---------|
| **Streptococcaceae** | Cocci | − | − |
| **Staphylococcaceae** | Cocci | + | − |
| **Bacillaceae** | Rod | + | +/− |

### Catalase Test
- Purpose: detects catalase enzyme (breaks H₂O₂ → H₂O + O₂)
- Procedure: transfer 3–5 colonies to dry slide → add one drop H₂O₂ → observe
- Positive: **bubbles** (O₂ production)
- Negative: no bubbles
- Caution: too much H₂O₂ can water down the reaction → false negative

### Oxidase Test
- Purpose: detects **cytochrome c oxidase** (part of electron transport chain)
- Procedure: Use OxiStick (swab with oxidase reagent) → collect 3–4 well-isolated colonies (must be 18–24 hours old) → observe for 30 seconds
- Positive: **blue color within 30 seconds**
- Negative: no color change (blue after 30 seconds = negative)

---

## Lab 6-7 Reading — Gram Negative Rods

### Learning Objectives
- Understand selective and differential media for isolation/identification of Gram negative bacteria
- Understand hydrolytic and degradative reactions for identification
- Understand oxidative and fermentative reactions for identification

### Selective vs. Differential Media
- **Selective medium**: allows only certain microorganisms to grow; inhibits others
  - Example: **EMB (Eosin Methylene Blue)** — eosin and methylene blue inhibit Gram positive bacteria but allow Gram negative bacteria to grow
- **Differential medium**: contains substances that cause bacteria to show distinguishing appearances
  - EMB is also differential:
    - **Metallic-green sheen / purple colonies**: vigorous lactose fermenters (primarily E. coli)
    - **Purple colonies**: moderate lactose fermenters
    - **Pink or colorless colonies**: non-lactose-fermenting bacteria
    - Note: colorless colonies are see-through; purple colonies are not

### Carbohydrate Metabolism Tests

**Phenol Red Carbohydrate Tests**
- If organism can break down carbohydrates (oxidation or fermentation), acid is produced
- Acid turns phenol red indicator from **red (alkaline) → yellow (acidic)**

**O/F (Oxidative-Fermentation) Test**
- Determines whether organism produces acid through fermentation or only oxidation
- Uses semisolid agar to create anaerobic environment in F tube
- F tube: sterile mineral oil added to top (anaerobic)
- O tube: no oil (aerobic)
- Medium color: green → yellow if acid produced
- Results:
  - Both O and F tubes yellow → **fermentation** (organism ferments carbohydrates)
  - Only O tube yellow → **oxidation only** (respiration; cannot ferment)

### IMViC Tests
Used to differentiate organisms — especially E. coli from Klebsiella aerogenes

| Test | E. coli | K. aerogenes |
|------|---------|-------------|
| **I**: Indole | + | − |
| **M**: Methyl Red | + | − |
| **V**: Voges-Proskauer | − | + |
| **C**: Citrate | − | + |

### Methyl Red (MR) Test
- Purpose: detects stable acid end products from **mixed acid fermentation** of glucose
- Applies to: Escherichia, Salmonella, Proteus
- These organisms ferment glucose → lactic, acetic, succinic, formic acids + CO₂, H₂, ethanol
- pH drops to ≤5.0 in MRVP broth
- Positive: **red color** (acid present)
- Negative: yellow color

### Voges-Proskauer (VP) Test
- Purpose: detects **2,3-butanediol** fermentation (neutral end product)
- Applies to: Klebsiella, Serratia, some Bacillus species
- If VP positive → usually MR negative
- Procedure: grow in MRVP broth 3–5 days → add VP-A (alpha-naphthol) + VP-B (40% KOH) → shake vigorously → wait 30 min
- Positive: **pink to red color** (acetoin detected)
- Negative: no color or yellow/brown

### Citrate Test
- Purpose: tests ability to use **citrate as sole carbon source** and ammonium salts as sole nitrogen source
- Organisms that degrade citrate: Klebsiella aerogenes, Salmonella typhimurium
- Citrate → oxaloacetate + pyruvate → fermentation end products (formate, acetate, lactate, acetoin, CO₂)
- Ammonium salts used for nitrogen → produces ammonia → medium becomes alkaline
- pH indicator: **bromothymol blue** (dark green → Prussian blue when alkaline)
- Positive: **deep blue color + growth**
- Negative: no growth / no color change (remains green)

### SIM Medium (3-in-1 Test)
SIM = **Sulfur, Indole, Motility** — one medium provides 3 separate diagnostic results

**H₂S Production (Sulfur Reduction)**
- Bacteria couple sulfur reduction to oxidation of Krebs cycle intermediates
- SIM contains ferrous ammonium sulfate + sodium thiosulfate as indicators
- H₂S gas + ferrous ammonium sulfate → **ferrous sulfide (black precipitate)**
- Positive: **blackening along or throughout stab line**
- Negative: no color change

**Indole Production (Tryptophan Degradation)**
- Some bacteria degrade tryptophan → indole + ammonia + pyruvic acid
- Enzyme: **tryptophanase**
- Detected with **Kovac's reagent** → deep red color if indole present
- Positive: **red coloration at top of agar**
- Negative: no color change

**Motility**
- Flagella allow directed movement (chemotaxis) toward nutrients or away from harmful substances
- Flagellum = rigid helical structure, extends ~10 microns, <0.2 microns wide (below light microscope resolution without special stain)
- Flagella rotate (like a boat screw) to propel the cell
- Methods for determining motility:
  1. **Wet mount** under phase-contrast microscope — true swimming vs. Brownian motion (wiggling without vector movement)
  2. **SIM tube stab inoculation** — if motile, organism swims away from stab line (medium turns turbid); non-motile = growth only along stab line
  3. **Swarming motility** (Proteus mirabilis) — extreme motility creates concentric rings (swarms) on agar plates; grows over entire plate

### Phenylalanine Test
- Purpose: detects **phenylalanine deaminase** enzyme
- Differentiates Proteus from other Enterobacteriaceae
- Proteus oxidatively deaminates phenylalanine → **phenylpyruvic acid + ammonia**
- Add 10% ferric chloride → green complex with phenylpyruvic acid (α-keto acid)
- Positive: **green coloration**
- Negative: yellow coloration

### Urea Test (Urease)
- Purpose: tests for **urease** enzyme
- Urea = waste product of animal metabolism
- Urease splits urea → CO₂ + ammonia
- Medium contains yeast extract, urea, buffer, phenol red (pH 6.8)
- Ammonia → alkaline → phenol red turns bright pink/cerise (pH ≥8.1)
- Positive: **intense pink-red color**
- Negative: no color change

### Biochemical Tests Summary Table

| Test | Purpose | Positive Result | Negative Result |
|------|---------|-----------------|-----------------|
| **Catalase** | Catalase enzyme | Bubbles | No bubbles |
| **Citrate** | Citrate as sole carbon source | Blue color + growth | Green (no change) |
| **EMB** | Selective/differential for Gram− | Metallic green sheen or purple (lactose+ varies) | Pink/colorless (non-fermenter) |
| **KOH** | Confirms Gram reaction | Strings (Gram−) | No strings (Gram+) |
| **Methyl Red** | Mixed acid fermentation | Red (immediate) | Yellow |
| **Nitrate Reduction** | Nitrate → nitrite or gas | Red after A+B reagents, or no red after zinc | Red after zinc |
| **O/F Glucose** | Oxidative vs. fermentative | Yellow (O only = oxidative; O+F = fermentative) | Green (neither) |
| **Oxidase** | Cytochrome c oxidase | Blue within 30 sec | No color |
| **Phenylalanine** | Phenylalanine deaminase | Green | Yellow |
| **SIM H₂S** | Sulfur reduction | Black precipitate | No change |
| **SIM Indole** | Tryptophan degradation | Red at top (Kovac's) | No change |
| **SIM Motility** | Bacterial motility | Turbid (diffuse from stab) | Growth along stab only |
| **Starch Hydrolysis** | Amylase (starch breakdown) | Clear zone around streak (dark agar surrounds) | Dark agar to streak line |
| **Urea** | Urease production | Intense pink-red | No change |
| **Voges-Proskauer** | 2,3-butanediol fermentation | Red within 30 min | No color/yellow-brown |

### KOH Test Procedure
- Purpose: confirms Gram stain (Gram-negative cell walls lyse in 3% KOH, releasing DNA)
- Procedure: transfer bacteria to slide → add 3% KOH → mix 5–10 sec → lift loop
- Positive: **strings present** (Gram negative)
- Negative: no strings (Gram positive)

### Nitrate Reduction Test
- Purpose: ability to reduce nitrate → nitrite, ammonia, or nitrogenous gas
- Procedure: inoculate nitrate broth 24–48h → add reagent A + B
  - Red color → reduced to nitrite (positive)
  - No color → add zinc: red = failed to reduce (negative); no red = reduced to ammonia/gas (positive)

### Starch Hydrolysis
- Purpose: ability to hydrolyze starch (amylase)
- Procedure: streak starch agar → incubate → flood with Gram's iodine
- Positive: dark agar with **clear zone around streak** (starch broken down)
- Negative: dark agar up to the streak line

---

## Class Notes — Feb 3

> Note: The PDF for "Note Feb 3, 2026.pdf" contained no extractable text (image-only scan). Content could not be auto-extracted. Review the original handwritten notes in iCloud at: `notes-inbox/Notability (1)/Class Notes/MicroBiology/Note Feb 3, 2026.pdf`

---

## Related
- [[academic-hub]]
- [[01-school]]
- [[identity]]
- [[microbio-lab-procedures]]
- [[microbio-lectures-exams]]
- [[Microbiology/index]]
