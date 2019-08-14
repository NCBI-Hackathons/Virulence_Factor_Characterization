import os
import requests
import string
import xml.etree.ElementTree as xml

from os.path import join as j
from time import sleep

from virfac import data_dir


bad_bugs = """Acinetobacter baumannii ACICU
Aeromonas hydrophila subsp. hydrophila ATCC 7966
Aeromonas salmonicida subsp. salmonicida A449
Aeromonas hydrophila ML09-119
Aeromonas veronii B565
Aeromonas hydrophila str. AH-3
Anaplasma phagocytophilum HZ
Bacillus anthracis str. Sterne
Bacillus anthracis
Bacillus cereus ATCC 10987
Bacillus cereus ATCC 14579
Bacillus anthracis str. Ames Ancestor
Bacillus subtilis subsp. subtilis str. 168
Bartonella henselae str. Houston-1
Bartonella quintana str. Toulouse
Bordetella pertussis Tohama I
Brucella melitensis bv. 1 str. 16M
Brucella suis 1330
Burkholderia pseudomallei K96243
Campylobacter jejuni subsp. jejuni NCTC 11168
Campylobacter jejuni subsp. jejuni 81-176
Chlamydia trachomatis D/UW-3/CX
Clostridium perfringens str. 13
Clostridium perfringens ATCC 13124
Clostridium perfringens SM101
Clostridium difficile 630
Clostridium tetani E88
Clostridium perfringens B str. ATCC 3626
Clostridium perfringens str. NCTC 8533B4D
Clostridium perfringens E str. NCIB 10748
Clostridium botulinum C str. 203U28
Clostridium botulinum D str. 1873
Clostridium botulinum Hall 183 (A391)
Clostridium difficile str. CCUG 20309
Clostridium novyi str. ATCC19402
Clostridium septicum str. NH2
Corynebacterium diphtheriae NCTC 13129
Coxiella burnetii CbuK_Q154
Coxiella burnetii RSA 493
Coxiella burnetii RSA 331
Coxiella burnetii CbuG_Q212
Coxiella burnetii Dugway 5J108-111
Enterococcus faecalis V583
Enterococcus faecalis str. MMH594
Enterococcus faecium DO
Enterococcus faecium str. TX2555
Escherichia coli O127:H6 str. E2348/69
Escherichia coli B171
Escherichia coli O157:H7 str. EDL933
Escherichia coli 17-2
Escherichia coli str. 042
Escherichia coli 55989
Escherichia coli O44:H18 042
Escherichia coli CFT073
Escherichia coli O75:K5:H- str. IH11128
Escherichia coli EC7372
Escherichia coli str. A30
Escherichia coli O25b:H4 str. FV9863
Escherichia coli str. C1845
Escherichia coli
Escherichia coli E10703
Escherichia coli O114:H49 str. E29101A
Escherichia coli O159:H4 str. 350C1
Escherichia coli str. E7473
Escherichia coli str. 260-1
Escherichia coli str. ARG-3
Escherichia coli O8:H9 str. WS6788A
Escherichia coli str. H721A
Escherichia coli O18:K1:H7 str. RS218
Escherichia coli UTI89
Escherichia coli str. E-B35
Escherichia coli O111:H- str. E45035
Escherichia coli O78:H11:K80 str. H10407
Escherichia coli O157:H7 str. Sakai
Escherichia coli O55:H7 str. CB9615
Escherichia coli O26 str. C/15333
Escherichia coli ONT:H- str. FV11678
Escherichia coli str. A22
Escherichia coli str. AL 851
Escherichia coli str. 239 KH 89
Escherichia coli O25:H42 str. E11881A
Escherichia coli O114:H- str. WS0115A
Escherichia coli str. 111KH86
Escherichia coli SE11
Escherichia coli O157:H str. 493/89
Escherichia coli ONT:HND str. A16
Escherichia coli C342-62
Escherichia coli O45:K1:H7 str. S88
Haemophilus influenzae Rd KW20
Haemophilus influenzae str. 1007
Haemophilus influenzae AM30 (770235)
Haemophilus influenzae N187
Haemophilus influenzae nontypable strain 3179B
Haemophilus influenzae str. 12
Haemophilus influenzae C54
Haemophilus influenzae TN106
Helicobacter pylori 26695
Helicobacter pylori J99
Klebsiella pneumoniae subsp. pneumoniae NTUH-K2044
Klebsiella pneumoniae subsp. pneumoniae HS11286
Klebsiella pneumoniae subsp. pneumoniae 1084
Legionella pneumophila subsp. pneumophila str. Philadelphia 1
Listeria monocytogenes EGD-e
Listeria ivanovii str. ATCC 19119
Listeria innocua SLCC6294
Mycobacterium tuberculosis H37Rv
Mycoplasma pneumoniae M129
Mycoplasma hyopneumoniae 232
Neisseria meningitidis MC58
Neisseria meningitidis Z2491
Pseudomonas aeruginosa PAO1
Pseudomonas aeruginosa PA103
Rickettsia rickettsii str. Sheila Smith
Rickettsia conorii str. Malish 7
Salmonella enterica subsp. enterica serovar Typhi str. CT18
Salmonella enterica subsp. enterica serovar Typhimurium str. LT2
Salmonella enterica (serovar typhimurium)
Salmonella enterica subsp. enterica serovar Typhimurium str. 14028s
Shigella flexneri 2a str. 301
Shigella dysenteriae Sd197
Staphylococcus aureus subsp. aureus MW2
Staphylococcus aureus subsp. aureus str. Newman
Staphylococcus aureus subsp. aureus COL
Staphylococcus aureus str. Newman D2C (ATCC 25904)
Staphylococcus aureus ZM
Staphylococcus aureus
Staphylococcus aureus S6
Staphylococcus aureus RN4220
Staphylococcus aureus subsp. aureus N315
Streptococcus pyogenes MGAS315
Streptococcus pyogenes M1 GAS
Streptococcus pyogenes MGAS8232
Streptococcus agalactiae 2603V/R
Streptococcus agalactiae A909
Streptococcus pneumoniae TIGR4
Streptococcus pneumoniae R6
Streptococcus agalactiae FM027022
Streptococcus agalactiae NEM316
Streptococcus pyogenes MGAS5005
Streptococcus pneumoniae Taiwan19F-14
Vibrio cholerae O1 biovar El Tor str. N16961
Vibrio parahaemolyticus RIMD 2210633
Vibrio vulnificus CMCP6
Vibrio parahaemolyticus
Vibrio vulnificus YJ016
Yersinia pestis CO92
Yersinia enterocolitica W1024
Yersinia enterocolitica str. 84-50
Yersinia enterocolitica subsp. enterocolitica 8081
Yersinia pestis KIM 10""".split('\n')

good_bugs = """Actinomyces dentalis
Actinomyces israelii
Actinomyces oricola
Actinomyces oris
Aerococcus viridans
Aerococcus urinae
Arthrobacter agilis
Aerococcus sanguicola
Aerococcus viridans
Arcanobacterium bernardiae
Arthrobacter agilis
Bacillus algicola
Bacillus barbaricus
Bacillus firmus
Bacillus funiculus
Bacillus gibsonii
Bacillus horikoshii
Bacillus niacini
Bacillus pasteurii
Bacillus subtilis inaquosorum
Brevibacillus brevis
Brevibacterium epidermidis
Brevibacterium oxydans
Burkholderia_thailandensis_E264_uid58081
Burkholderia_cenocepacia_MC0_3_uid58769 
Burkholderia_phymatum_STM815_uid58699
Burkholderia_CCGE1001_uid42975
Cellulomonas hominis
Cellulomonas turbata
Corynebacterium acnes
Corynebacterium caspium
Corynebacterium flavescens
Corynebacterium genitalium
Corynebacterium imitans
Corynebacterium striatum
Corynebacterium variabilis
Corynebacterium xerosis
Dermabacter hominis
Dermacoccus nishinomiyaensis
Exiguobacterium acetylicum
Flavobacterium arborescens
Flavobacterium maritypicum
Gordonia bronchialis
Escherichia coli str. K-12 substr. MG1655
Escherichia_coli_ED1a_uid59379
Escherichia_coli_SE11_uid59425
Escherichia_fergusonii_ATCC_35469_uid59375
Escherichia_coli_HS_uid58393
Escherichia_coli__BL21_GOLDd_DE3_pLysS_AG__uid59245
Escherichia_coli_IAI1_uid59377
Escherichia_coli_B_REL606_uid58803
Escherichia_coli_K_12_substr__DH10B_uid58979
Exiguobacterium acetylicum
Flavobacterium arborescens
Flavobacterium maritypicum
Gordonia bronchialis
Leifsonia aquatica
Leifsonia xyli
Micrococcus glutamicus
Micrococcus nishinomiyaensis
Micrococcus sedentarius
Pseudomonas_fluorescens_Pf_5_uid57937
Pseudomonas_putida_GB_1_uid58735
Pseudomonas_putida_KT2440_uid57843
Pseudomonas_fluorescens_SBW25_uid62971
Pseudomonas_putida_W619_uid58651
Pseudomonas_brassicacearum_NFM421_uid66303
Pseudomonas_stutzeri_A1501_uid58641
Rhodococcus bronchialis
Rhodococcus erythropolis
Rhodococcus terrae
Staphylococcus albus
Staphylococcus auricularis
Staphylococcus capitis
Staphylococcus epidermidis
Staphylococcus hominis
Staphylococcus nepalensis
Staphylococcus saprophyticus
Staphylococcus vitulinus
Staphylococcus warneri
Streptococcus australis
Streptococcus caprinus
Streptococcus crista
Streptococcus entericus
Streptococcus gordonii
Streptococcus infantarius
Streptococcus mitis
Streptococcus mutans ferus
Streptococcus oralis
Streptococcus salivarius
Streptococcus sanguis
Streptococcus vestibularis
Streptococcus viridans
Tsukamurella inchonensis
Tsukamurella paurometabola
Tsukamurella pulmonis
Virgibacillus pantothenticus"""

esearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
efetch  = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
elink   = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"

api_key = '39bc94a6bd1a989fdaacde696739255d7709'

def get_data_from_ncbi(bug_list=bad_bugs, subdir="pathogens"):
	for bug in bug_list:
		sleep(.1)
		os.makedirs(j(data_dir, subdir), exist_ok=True)
		filename = j(data_dir, subdir, bug.lower().translate(str.maketrans('', '', string.punctuation)).replace(' ','_').strip())
		res = requests.get(esearch, params=dict(tool='hackathon2019', db='assembly', term=bug, retmax=1000, api_key=api_key))
		try:
			rec = xml.fromstring(res.content)
		except xml.ParseError:
			print(res.content)
			break
		
		ids = [i.text for i in rec.findall('.//IdList/Id')]
		print(f'found {len(ids)} genomes for {bug} ...')
		for gb_id in ids:
			res = requests.get(elink, params=dict(tool='hackathon2019', db='nuccore', dbfrom='assembly', Id=gb_id, retmode='xml', api_key=api_key))
			try:
				rec = xml.fromstring(res.content)
			except xml.ParseError:
				print(res.content)
				break
			sleep(.1)
			for fa_id in [e.text for e in rec.findall(r".//*[DbTo='nuccore']//Id")]:
				res = requests.get(efetch, params=dict(tool='hackathon2019', db='nuccore', Id=fa_id, rettype='fasta', api_key=api_key))
				with open(filename, 'wb') as fd:
					for i, chunk in enumerate(res.iter_content(chunk_size=128)):
						fd.write(chunk)
				print(f"{i*128} bytes read.")
				break #just need the first one
			break


if __name__ == '__main__':
	get_data_from_ncbi()