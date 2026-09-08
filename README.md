# HIT137-Assignment-2-S2-2026
Python solutions for HIT137 Group Assignment 2 featuring a custom file encryption tool `cipher.py` and a functional recursive descent math expression evaluator `evaluator.py`.

## Cipher Development History

Development of `cipher.py` followed several trial approaches. The first version used `ord()`, `chr()` and `% 26` to shift letters within the alphabet. This successfully encrypted the text, but decryption initially produced a large number of errors.

Several decryption methods were tested. One approach directly reversed the encryption shift, while a later approach calculated two possible original characters and checked which alphabet half each result belonged to. Testing reduced the number of verification errors, with commits recording improvements from around **1300 errors to 326**, and another trial reaching **241 errors**.

Input handling was then improved by adding a function that only accepts non-negative integers for `shift1` and `shift2`. UTF-8 encoding was also added when reading and writing files.

During testing, `encrypted_text.txt` and `decrypted_text.txt` were removed from Git tracking because they are generated automatically whenever the program runs.

The latest approach introduced a **decryption map**. The program generates a dictionary mapping encrypted characters back to their original characters. This made the decryption code simpler and also revealed an important problem: some shift values can cause two different original letters to encrypt to the same character. Collision detection was therefore added to identify these cases.

## Evaluator Development History

`evaluator.py` was initially created as a blank scaffold for Question 2. The first working approach added file handling to read `input.txt`, with `sample_input.txt` used as a fallback. Expressions are separated line-by-line and stored for processing. Python's `eval()` is currently used as a temporary method to test expression evaluation and error handling. Results are stored as dictionaries and written to `output.txt` using the required Input, Tree, Tokens and Result format. Tree and token generation are still under development, with the next stage being replacement of `eval()` with the required recursive-descent parser.

# Testing Report - cipher.py

The cipher was tested with shift_1 = 7 and shift_2 = 4, and checking whether the decrypted text matched
the original raw_text.txt file.

## shift_1 = 7, shift_2 = 4

Encrypting with shift_1 = 7 and shift_2 = 4, encrypted_text.txt showed:

```
Epsem iqtvm dplps tiu ameu, cpntecueuvs adiqitcing eliu, ted dp eivtmpd uemqps incididvnu vu labpse eu dplpse magna alirva. Xu enim ad minim weniam, rvit nptusvd eyesciuauipn vllamcp labpsit niti vu alirviq ey ea cpmmpdp cpntervau. Jvit avue isvse dplps in seqsehendesiu in wplvquaue weliu ette cillvm dplpse ev fvgiau nvlla qasiauvs. Kycequevs tinu pccaecau cvqidauau npn qspidenu, tvnu in cvlqa rvi pfficia detesvnu mplliu anim id etu labpsvm.

Epsem Bqtvm it timqlz dvmmz ueyu pf uhe qsinuing and uzqeteuuing indvtusz. 

Epsem Bqtvm hat been uhe indvtusz't tuandasd dvmmz ueyu ewes tince 4299, xhen detignest au Eeusateu and Camet Fptlez, uhe libsasian au Vu Hside Ssinuing Eibsasz in Epndpn, uppk a 4247 Iicesp usantlauipn and tcsambled iu up make dvmmz ueyu fps Eeusateu't Hpdz Wzqe theeut. Bu hat tvswiwed npu pnlz manz decadet, bvu altp uhe leaq inup elecuspnic uzqeteuuing, semaining ettenuiallz vnchanged. Bu xat qpqvlasited uhankt up uhete theeut and mpse secenulz xiuh detkupq qvblithing tpfuxase like Gldvt SageFakes and Ficsptpfu Zpsd inclvding westipnt pf Epsem Bqtvm.

Ipnusasz up qpqvlas belief, Epsem Bqtvm it npu timqlz sandpm ueyu. Bu hat spput in a qiece pf clattical Eauin liuesauvse fspm 78 HI, making iu pwes 5333 zeast pld. Uichasd FcIlinupck, a Eauin qspfettps au Aamqden-Vzdnez Ipllege in Yisginia, lppked vq pne pf uhe mpse pbtcvse Eauin xpsdt, cpntecueuvs, fspm a Epsem Bqtvm qattage, and gping uhspvgh uhe ciuet pf uhe xpsd in clattical liuesauvse, ditcpwesed uhe vndpvbuable tpvsce. Epsem Bqtvm cpmet fspm tecuipnt 4.43.65 and 4.43.66 pf "de Linibvt Hpnpsvm eu Falpsvm" (Whe Kyusemet pf Mppd and Kwil) bz Iicesp, xsiuuen in 78 HI. Whit bppk it a useauite pn uhe uhepsz pf euhict, wesz qpqvlas dvsing uhe Uenaittance. Whe fistu line pf Epsem Bqtvm, "Epsem iqtvm dplps tiu ameu..", cpmet fspm a line in tecuipn 4.43.65.
```

And after decrypting, decrypted_text.txt showed:

```
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem Ipsum is simply dummy text of the printing and typesetting industry. 

Lorem Ipsum has been the industry's standard dummy text ever since 1966, when designers at Letraset and James Mosley, the librarian at St Bride Printing Library in London, took a 1914 Cicero translation and scrambled it to make dummy text for Letraset's Body Type sheets. It has survived not only many decades, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised thanks to these sheets and more recently with desktop publishing software like Aldus PageMaker and Microsoft Word including versions of Lorem Ipsum.

Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.
```

Confirming with raw_text.txt, the results show that the cipher has encrypted the raw_text.txt file, and correctly decrypted the encrypted file using shift_1 = 7 and shift_2 = 4.
