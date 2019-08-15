# Virulence Factor Characterization in Metagenomes

###### Virulence Factor Characterization project from 2019 NIH Microbial Virulence in the Cloud Hackathon

# Approach
We used parallel machine learning methods to approach the problem of characterizing virulence factors (VF) in diseased and healthy metagenomes. Using genes from the core set of the Virulence Factor Database (http://www.mgc.ac.cn/VFs/), we used an HMM to profile known virulence factors and apply profiles to diseased and healthy metagenomes. Using the same gene factors, we found pathogen genomes from the VFDB set and commensal genomes from the NHSN organism list and (other source) and masked the VFDB virulence genes from both datasets. We then trained the VF-subtracted genomes on an SVM model to classify pathogenic and non-pathogenic genomes. Both techniques form a complementary approach to VF characterization by using well-characterized virulence factors to profile similar characteristics in the metagenome space (HMM), and by exploring the potential for uncharacterized or weakly characterized genes within the same metagenomes. 

![workflow](https://github.com/NCBI-Hackathons/Virulence_Factor_Characterization/blob/master/VFC%20workflow.png)

## Installing

Currently the VirFac repo is provided as a Python project that can be installed via `setuptools`. It requires Python 3.7 or later and some package dependencies that can be installed via `pip`:

`pip install -r requirements.txt`

```
requests==2.22.0
click==7.0
numpy==1.13.3
pandas=0.25.0
scikit-learn==0.21.3
```

Eventually the project will be available on PyPI.

## Authors

Sherry Bhalla

Ousmane H. Cissé  
ousmane.cisse@nih.gov  
NIH Clinical Center  
Bethesda MD, 20814

Shennan Lu

Liz Norred  
elizabeth.norred@gmail.com  
University of Tennessee, Knoxville  
Knoxville TN, 37922 

Justin Payne  
justin.payne@fda.hhs.gov  
US-FDA Center for Food Safety and Applied Nutrition  
College Park MD, 20710  

Sherry Bhalla  
sherry.bhalla@mssm.edu  
Icahn School of Medicine at Mount Sinai, New York, NY, 20019    
ORCID: 0000-0001-7827-4050  
Bredesen Center for Interdisciplinary Research and Education, University of Tennessee, Knoxville, TN 37922  

## Methods

Experimentally verified virulence factor genes from the Virulence Factor Database (VFDB: Chen et al 2015, Accessed 8/13/19 https://academic.oup.com/nar/article/44/D1/D694/2503049) were used to represent virulence-associated genes. Example metagenomes used for testing were drawn from public datasets listed on NCBI SRA and included healthy and disease-state human skin metagenomic samples. Specifically, diseased metagenomes were drawn from the Diabetic Foot Ulcer metagenome study (BioProject: PRJNA506988) and healthy foot skin metagenomes were drawn from BioProject: PRJEB30094. Metagenomes were assembled using MetaSPADES. (Nurk et al https://www.ncbi.nlm.nih.gov/pubmed/28298430 )

A Hidden Markov Model (HMM) was applied to the VFDB genes to create virulence profiles. Genes were selected for which at least five different bacterial species were available. Multiple sequence alignments were generated using MUSCLE [1] and HMMs using HMMER3 [2]. Genomes and/or corresponding protein coding sequences were screened with HMMSEARCH[2] using pre-computed significance scores. Scores were calculated as 80% of the envelope alignment score of a representative sequence corresponding to its HMM. Alignments were filtered by custom scripts to extract putative virulence factors’ loci. VF sequences were concatenated, aligned and used as input for phylogenetic analyses. Phylogenetic trees were constructed using RAXML-ng [3] and analyzed using R package Ape[4] and Newick Utilities[5]. Virulence tags were assigned based on the number of virulence loci found and phylogenetic classification. All analyses are described in Snakemake pipeline[6].

A SVM model was also developed to classify virulent and non-virulent gene segments by training on a reference set of labelled pathogen and commensal genomes. The pathogen genomes were acquired from an NCBI Assembly search and included the species identified in the VFDB dataset. Commensal genomes were also acquired from an NCBI Assembly search, and included species selected from the NHSN Common Commensals List (https://www.cdc.gov/nhsn/pdfs/pscmanual/4psc_clabscurrent.pdf) and from Busby et al 2012 (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5866053/). 



## Implementation

## Operation

## Use Cases

## Data and software availability

Data is available from the NCBI Sequence Read Archive under projects ERP112507 and SRP170931. "VirFac" software is made available under the MIT License (see [LICENSE](https://github.com/NCBI-Hackathons/Virulence_Factor_Characterization/blob/master/LICENSE).)

## Acknowledgements
Diabetic Foot Ulcer dataset provided courtesy of UMaryland/CosmosID and described at

https://www.ncbi.nlm.nih.gov/bioproject/PRJNA506988

Healthy and diabetic foot microbiomes provided courtesy of CLM and described at

https://www.ncbi.nlm.nih.gov/bioproject/PRJEB30094

## Credits

This package was created with Cookiecutter and the `audreyr/cookiecutter-pypackage` project template.

Cookiecutter: https://github.com/audreyr/cookiecutter  
https://github.com/audreyr/cookiecutter-pypackage

This was a Microbial Virulence in the Cloud Hackathon 2019 project.

