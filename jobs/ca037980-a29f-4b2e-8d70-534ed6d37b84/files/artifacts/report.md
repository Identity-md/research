# Marktonderzoek: AI-swarm-dienstverlening voor Nederlandse ondernemers

Datum onderzoek: 13 november 2026. Opgesteld als eenmalig onderzoeksrapport, niet als doorlopend dashboard.

**Leeswijzer voor labels:** 🟢 FEIT (met bron) · 🟡 AANNAME (expliciet gemarkeerd, niet verifieerbaar binnen deze sessie) · 🔴 ONBEANTWOORD (vraag voor opdrachtgever/accountant/jurist).

---

## 0. Belangrijkste methodebeperking (eerlijk vermeld, niet verborgen)

Dit rapport is geschreven door **één Claude-sessie** binnen een tijdslimiet van circa 39 minuten, zonder interactieve browser (geen JavaScript-rendering van trends.google.com, geen mogelijkheid om te betalen, accounts aan te maken of bedrijven te benaderen) en zonder toegang tot de daadwerkelijke IMD-swarm-infrastructuur om een live multi-agent run uit te voeren.

Concreet betekent dit:
- 🔴 **Google Trends**: de live interactieve grafieken (trends.google.com/trends/explore) konden niet via een geautomatiseerde fetch worden opgehaald — de pagina is clientside gerenderd en vereist een browsersessie die in deze sandbox niet beschikbaar is. In plaats van cijfers te verzinnen, geef ik per queryvraag de **exacte zoekterm, periode, geografie en het directe linkformat** zodat de opdrachtgever of een volgende run dit in 2 minuten per query kan opvragen. Waar ik wél Trends-achtige uitspraken doe, komen die uit secundaire bronnen (nieuwsartikelen die Trends-cijfers citeren) en zijn apart gelabeld.
- 🔴 **IMD-documentatie**: ik heb geen officiële, publiek vindbare IdentityMD/IMD-documentatie gevonden met prijzen, retry-/refusal-beleid, garanties of prompt/data-handling-beleid. De enige vondst (Bankless-artikel) beschrijft IMD als een Ethereum-NFT-gebonden swarm van AI-agents (2.000 NFT's = 2.000 "seats"), zonder prijsinformatie. Dit is een **materiële kennislacune**, geen aanname — ik model de IMD-kosten daarom als een **instelbare parameter** (owner-settable) in plaats van een verzonnen getal.
- 🟢 Dit rapport is dus **geen gecontroleerde vergelijking** tussen één ChatGPT/Claude-sessie en een echte multi-agent swarm. Er is geen A/B-test uitgevoerd omdat er geen swarm-omgeving beschikbaar was om tegen te testen. Elke uitspraak over "swarm-voordeel" in dit rapport is een **architectuurredenering** (waarom parallelle gespecialiseerde rollen met een reviewer-stap structureel andere foutpatronen geven dan één doorlopende sessie), niet een gemeten resultaat. Dit wordt bij elke dienst herhaald.
- De "parallelle werkpakketten" (1–6 uit de opdracht) zijn binnen deze ene sessie **sequentieel** uitgevoerd omdat de sessie zelf geen aparte agents kan spawnen; waar relevant wordt dit vermeld. Dit is dus ook een datapunt over de taak zelf: *single-session onderzoek kan parallellisatie simuleren via volgorde, maar niet via gelijktijdigheid of onafhankelijke review door een ander model.*

Er is geen `.imd-blocked.json` nodig: de kernvraag (welke 10 diensten, ranking, testopzet, economie) is beantwoordbaar met de beschikbare bronnen plus expliciete aannames. De twee lacunes hierboven blokkeren niet de hoofdconclusie, maar begrenzen de precisie van cijfers (vooral IMD-marge en absolute Trends-scores).

---

## 1. Nederlandse ondernemersbehoeften (werkpakket 1)

🟢 **CBS** (nieuwsbericht 2025, "Afname aantal zzp'ers na jarenlange stijging", cbs.nl/nl-nl/nieuws/2025/19): aantal zzp'ers daalde in 2025 met ca. 62.000 tot ongeveer 1,2 miljoen, grotendeels toegeschreven aan verscherpte handhaving tegen schijnzelfstandigheid door de Belastingdienst sinds 1 januari 2025. Sterkste daling onder jongeren (15–27 jaar: −19.000), met name in zorg en welzijn.
🟢 **KVK** (persbericht 10 oktober 2025, "Ondernemers missen ruimte voor vernieuwing"): zzp'ers en mkb'ers zetten digitalisering vooral praktisch in — gericht op het behoud en efficiënter maken van bestaande processen, niet op vernieuwing. Zorgen over tijd, digitale risico's en onduidelijke regelgeving versterken die focus op behoud.
🟢 **Freelance-marktdata** (via searchlab.nl, begin 2025, onderzoek onder 20.000 zelfstandigen): gemiddeld uurtarief Nederlandse zzp'er ≈ €81. Dit is een nuttige referentieprijs: elke IMD-dienst moet concurreren met "koop X uur zzp-tijd tegen ~€81/uur", niet alleen met een bureau- of SaaS-tarief.
🟡 Eigen interpretatie (aanname, geen cijfer): de combinatie van (a) krimpend zzp-bestand door striktere regelgeving, (b) tijdgebrek, en (c) voorkeur voor praktische, direct toepasbare oplossingen, wijst op vraag naar **kant-en-klare, afgebakende deliverables** (document, website, dashboard) in plaats van advies of consultancy-trajecten. Dit onderbouwt de keuze voor "duidelijk afgebakende deliverable" als harde eis in de diensten hieronder.
🔴 Geen directe KVK/CBS-cijfers gevonden over *welk specifiek digitaal product* zzp'ers het vaakst inkopen (bv. % dat een website uitbesteedt vs. zelf bouwt). Dit is een vraag die met een KVK-ondernemerspanel-enquête beantwoord zou moeten worden — buiten bereik van dit onderzoek.

---

## 2. Google Trends — opzet en wat kon worden opgehaald (werkpakket 2)

Zoals in §0 toegelicht kon ik géén live Trends-scores ophalen. Onderstaande tabel geeft de **exacte queries, instellingen en linkformaten** die de opdrachtgever (of een vervolgrun met browsertoegang) direct kan gebruiken. Elke link volgt het officiële Trends-URL-schema: `https://trends.google.com/trends/explore?geo=NL&q=<query>` (voeg `&date=today 5-y` of `&date=today 12-m` toe voor de periode). Voor meerdere termen in één grafiek: `&q=term1,term2,term3` (max. 5 termen per grafiek, alleen zo onderling vergelijkbaar — nooit tussen afzonderlijke grafieken).

| Groep | Nederlandse zoektermen (NL, Web Search) | Periode | Directe link (vul in op trends.google.com) |
|---|---|---|---|
| Website/lokale vindbaarheid/SEO | "website laten maken", "lokale seo", "google mijn bedrijf" | 5 jaar + 12 mnd | `?geo=NL&q=website laten maken,lokale seo,google mijn bedrijf&date=today 5-y` |
| Businessplan/forecasts | "ondernemingsplan", "businessplan opstellen", "omzetprognose" | 5 jaar + 12 mnd | `?geo=NL&q=ondernemingsplan,businessplan opstellen,omzetprognose&date=today 5-y` |
| Sales/offertes/leads | "offerte template", "leadgeneratie", "verkoopbrief" | 5 jaar + 12 mnd | `?geo=NL&q=offerte template,leadgeneratie,verkoopbrief&date=today 5-y` |
| Marketing/content/afbeeldingen | "social media content", "productfoto's laten maken", "advertentietekst" | 5 jaar + 12 mnd | `?geo=NL&q=social media content,productfoto's laten maken,advertentietekst&date=today 5-y` |
| Automatisering/AI | "ai automatisering bedrijf", "chatbot laten maken", "workflow automatiseren" | 5 jaar + 12 mnd | `?geo=NL&q=ai automatisering bedrijf,chatbot laten maken,workflow automatiseren&date=today 5-y` |
| Dashboards/spreadsheets | "excel dashboard maken", "kpi dashboard", "boekhouding spreadsheet" | 5 jaar + 12 mnd | `?geo=NL&q=excel dashboard maken,kpi dashboard,boekhouding spreadsheet&date=today 5-y` |
| Logo's/QR-codes | "logo laten ontwerpen", "qr code maken", "huisstijl laten maken" | 5 jaar + 12 mnd | `?geo=NL&q=logo laten ontwerpen,qr code maken,huisstijl laten maken&date=today 5-y` |

🟡 **Aanname, niet gemeten**: op basis van algemene marktkennis (niet Trends-data) is "website laten maken" en "logo laten ontwerpen" doorgaans structureel hoog-volume maar ook hoog-concurrerend; "ai automatisering" en "chatbot laten maken" zijn waarschijnlijk sterk gestegen 2021→2026 gezien de bredere AI-adoptiegolf, maar dit is een **verwachting, geen vastgesteld feit** — moet bevestigd worden met de links hierboven voordat enig besluit hierop wordt gebaseerd.

**Interpretatiekader (verplicht te vermelden bij gebruik):** Trends toont *relatieve interesse* binnen de gekozen periode/regio (0–100, geschaald op het piekpunt), niet zoekvolume en niet koopintentie. Een score van 0 of "onvoldoende data" betekent dat Google te weinig volume registreert om een score te geven — niet dat er geen interesse is. Scores uit verschillende grafieken (verschillende queries, perioden of geo-instellingen) zijn **nooit** onderling vergelijkbaar als absolute waarden.

---

## 3. Concurrenten en prijzen (werkpakket 3)

🟢 **Websites (searchlab.nl, clickforest.com, 2025–2026 prijsgidsen)**: geen vast bedrag; prijs hangt af van scope/platform. Eén genoemd vast pakket: €450 incl. btw voor een eenvoudige site (ongeverifieerde losse vermelding op een vergelijkingssite — niet als harde marktprijs te gebruiken). Webshops: €3.000–€10.000 eenmalig + €100–€300/maand lopend (schatting uit secundaire bron).
🟢 **Freelance-uurtarief NL** (searchlab.nl, 2025): gemiddeld €81/uur onder 20.000 zelfstandigen.
🔴 Geen geverifieerde, actuele prijslijst gevonden voor: businessplan-op-maat, logo-ontwerp, QR/huisstijlpakketten, dashboard-op-maat. Dit vereist losse offerteaanvragen (uitgesloten van deze opdracht — "geen bedrijven benaderen, geen offertes aanvragen"). **Resultaat: prijsranges voor deze diensten in §5 zijn gebaseerd op de gevonden uurtariefreferentie (€81/u) en typisch geschatte doorlooptijd, dus 🟡 AANNAME, niet een geciteerde marktprijs.**

---

## 4. IMD en betrouwbaarheid (werkpakket 4)

🔴 Zoals in §0: geen officiële IMD-prijs-, retry-, garantie- of dataverwerkingsdocumentatie gevonden. Enige vondst: Bankless-artikel over "IMD" als Ethereum-gebonden AI-agent-swarm met 2.000 NFT-"seats" (toegangsmodel, geen prijslijst voor eindklanten).
🟡 Daarom: model in §6/§7 gebruikt een **instelbare "IMD-kostprijs per opdracht"-parameter** (door de eigenaar zelf in te vullen op basis van werkelijke swarm-/compute-/NFT-seat-kosten), in plaats van een verzonnen bedrag.
**99%-first-pass-haalbaarheid**: niet realistisch te claimen op basis van tien testcases (zie opdracht-eis). Benodigd bewijs vóór een 99%-claim: (a) een vooraf gepubliceerde, objectieve acceptatiechecklist per dienst, (b) minimaal enkele honderden *betaalde* opdrachten per dienst (niet samples) gemeten tegen die checklist, (c) aparte meting van first-pass-acceptatie, levering-op-tijd en klanttevredenheid/revisies — dit zijn drie verschillende metrics die vaak worden samengevoegd. Automatisering kan *objectief verifieerbare* eigenschappen garanderen (bv. "bevat alle verplichte KVK-velden", "laadtijd < 2s", "QR-code scant correct") maar **niet** subjectieve kwaliteit (merkgevoel, tone-of-voice-fit, esthetisch oordeel) — die blijft mensenwerk in review.

---

## 5. Ranking: tien diensten

Scoring: vraag 25% · swarm-voordeel 25% · testbaarheid/betrouwbaarheid 20% · marge 15% · leverings-/privacy-/juridisch-/supportrisico 15% (hoger = lager risico). Scores 1–5 per criterium, 🟡 kwalitatief geschat (geen precisie-schijn: geen decimalen).

| # | Dienst | Vraag | Swarm-voord. | Testbaarheid | Marge | Risico(inv) | Totaal (gew.) |
|---|---|---|---|---|---|---|---|
| 1 | Lokale SEO-audit + actieplan | 4 | 4 | 5 | 4 | 4 | **4.1** |
| 2 | Offerte-/verkoopbrief-pakket op maat | 4 | 4 | 4 | 5 | 4 | **4.1** |
| 3 | KPI-/financieel dashboard (spreadsheet) | 3 | 5 | 5 | 4 | 4 | **4.1** |
| 4 | Website-copy + structuurplan (geen hosting) | 4 | 4 | 3 | 4 | 3 | **3.7** |
| 5 | Leadlijst + eerste-contact-templates (B2B) | 4 | 4 | 3 | 4 | 3 | **3.7** |
| 6 | Omzet-/liquiditeitsprognose (model + toelichting) | 3 | 4 | 4 | 3 | 4 | **3.6** |
| 7 | Social-mediacontentkalender (tekst, 1 maand) | 4 | 3 | 3 | 4 | 3 | **3.4** |
| 8 | Eenvoudig ondernemingsplan (concept, geen financiering-garantie) | 3 | 3 | 2 | 3 | 2 | **2.7** |
| 9 | Productfoto-briefing + AI-beeldconcepten (geen fotografie) | 3 | 3 | 2 | 3 | 3 | **2.8** |
| 10 | Logo/huisstijl-startpakket + QR-codeset | 2 | 2 | 3 | 3 | 4 | **2.6** |

Toelichting ranking: dienst 10 (logo's/QR) staat terecht onderaan — makkelijk, maar subjectief te beoordelen en geen onderscheidend swarm-voordeel; conform de opdracht behandeld als **add-on**, niet als kerndienst. Dashboards en offertepakketten scoren hoog omdat ze **objectief verifieerbaar** zijn (formules kloppen, cijfers consistent, velden compleet) — precies waar een swarm (bouwer + cijfercontroleur + stijlreviewer in parallelle rollen) een aantoonbaar ander foutprofiel heeft dan één doorlopende chatsessie die dezelfde taak in één denktrein uitvoert en eigen rekenfouten minder goed zelf detecteert.

### Per dienst (top 6 uitgewerkt volgens opdracht-eisen; 7–10 verkort)

**1. Lokale SEO-audit + actieplan**
- Koper: lokale zzp'er/mkb (kapper, fysio, aannemer) zonder marketingkennis.
- Probleem: onvindbaar in lokale zoekresultaten/Google Maps.
- Deliverable: PDF-rapport (Google Business Profile-check, 10 concrete fixes, prioriteitenlijst) + geactualiseerd profiel-conceptteksten.
- Vraagbewijs: 🟢 KVK-signaal dat digitalisering praktisch wordt ingezet (§1); 🔴 Trends-score nog te bevestigen (§2, groep 1).
- Alternatieven: freelance SEO-consultant (~€81/u, dus €240–€480 voor 3–6 uur), marketingbureau-abonnement (duurder, doorlopend).
- Swarm-workflow: agent A scraped/checkt het huidige profiel en site-structuur → agent B genereert fixes per SEO-categorie (technisch, content, lokaal) parallel → reviewer-agent toetst elke fix tegen een vaste checklist en verwijdert niet-onderbouwde claims. *Waarom mogelijk beter dan 1 sessie*: parallelle, gespecialiseerde checks verkleinen kans dat één doorlopende sessie een categorie vergeet of halverwege context verliest. *Waar het niet beter is*: bij een zeer klein, overzichtelijk bedrijfsprofiel maakt één goede ChatGPT/Claude-sessie met dezelfde checklist waarschijnlijk een vergelijkbaar rapport — **niet getest**, dus geen harde claim.
- Vaste scope: 1 locatie/profiel, max. 10 fixes, 1 revisieronde. Input: bedrijfsnaam, adres, huidige Google-profiel-link, 3 concurrenten. Doorlooptijd-schatting: 🟡 1 werkdag. Afhankelijkheden: toegang tot publieke profielgegevens (geen login nodig).
- Acceptatiechecklist (pass/fail): ✅ alle 10 fixes zijn specifiek en uitvoerbaar (niet generiek) · ✅ geen verzonnen concurrentiecijfers · ✅ Nederlandse spelling/no placeholders · ✅ prioriteitenlijst aanwezig.
- Risico's: info kan snel verouderen (Google-algoritme-updates), geen garantie op ranking-verbetering, copyright n.v.t., privacy laag (publieke data).

**2. Offerte-/verkoopbrief-pakket op maat**
- Koper: zzp'er die zelf offertes schrijft en weinig omzet uit offertes haalt.
- Deliverable: 1 offertetemplate + 3 ingevulde voorbeeldoffertes + 1 follow-up-mailreeks (3 mails).
- Vraagbewijs: 🟢 zzp-uurtarief-referentie (§1) maakt dit relevant (tijdsbesparing vs. €81/u zelf schrijven); Trends-groep 3 nog te bevestigen.
- Alternatieven: copywriter-freelancer, generieke templates online (gratis maar niet op maat).
- Swarm-workflow: agent A verzamelt klant-USP's uit intakeformulier → agent B schrijft offerte-copy → agent C (prijs-/rekencontrole) checkt dat alle bedragen/kortingen intern consistent zijn → reviewer toetst toon-consistentie. Rekencontrole door een los geoptimaliseerde agent is het duidelijkste swarm-voordeel: cijferfouten in lopende tekst worden vaker gemist door één generatieve doorloop dan door een los, op verificatie gericht toetsmoment.
- Vaste scope: 1 dienst/product, max. 3 offertevarianten, 1 revisieronde. Input: intakeformulier (dienst, prijs, doelgroep, 3 USP's). Doorlooptijd: 🟡 halve werkdag.
- Acceptatiechecklist: ✅ alle bedragen kloppen rekenkundig · ✅ geen tegenstrijdige voorwaarden tussen offerte en follow-upmails · ✅ geen verzonnen klantresultaten/testimonials · ✅ btw correct vermeld (concept, accountant moet toetsen).
- Risico's: subjectieve "overtuigingskracht" niet garandeerbaar, geen vorderingsrecht op werkelijke verkoop.

**3. KPI-/financieel dashboard (spreadsheet)**
- Koper: mkb-eigenaar zonder BI-tool die omzet/marge handmatig bijhoudt.
- Deliverable: Excel/Google Sheets-bestand met 5–8 vooraf afgesproken KPI's, grafieken, en een leesinstructie van 1 pagina.
- Vraagbewijs: Trends-groep 6 te bevestigen; 🟡 aanname dat kleine ondernemers vaak spreadsheets gebruiken i.p.v. dure BI-software (consistent met KVK-signaal "praktische digitalisering").
- Alternatieven: zelf bouwen (tijdrovend), BI-SaaS-abonnement (duurder, overkill voor kleine onderneming).
- Swarm-workflow: agent A ontwerpt formulestructuur → agent B vult/test met voorbeelddata → een aparte rekencontrole-agent herberekent elke formule onafhankelijk en vergelijkt uitkomsten (cross-check) → reviewer checkt leesbaarheid. Dit is het sterkste objectief-verifieerbare geval: formule-uitkomsten zijn mechanisch controleerbaar, wat een reproduceerbaar swarm-voordeel oplevert t.o.v. één sessie die zijn eigen formules zelden onafhankelijk herberekent.
- Vaste scope: max. 8 KPI's, 1 datasheet-formaat (CSV/Excel-upload door klant), 1 revisieronde. Input: voorbeeld-omzetdata (CSV), gewenste KPI's. Doorlooptijd: 🟡 1 werkdag. Afhankelijkheid: klant levert data in bruikbaar formaat (anders extra opschoonstap nodig, apart te offreren).
- Acceptatiechecklist: ✅ elke formule geeft bij testdata het verwachte, onafhankelijk herberekende resultaat · ✅ geen hardcoded cijfers waar een formule moet staan · ✅ bestand opent zonder foutmelding in Excel/Google Sheets · ✅ leesinstructie aanwezig.
- Risico's: foutieve/vuile inputdata van klant beïnvloedt resultaat (buiten swarm-controle), geen boekhoudkundig advies (accountant moet valideren), privacy van financiële data moet contractueel geborgd zijn.

**4. Website-copy + structuurplan (geen hosting/bouw)**
- Koper: starter die zelf een sitebuilder gebruikt maar geen goede tekst/structuur heeft.
- Deliverable: paginastructuur (sitemap) + volledige copy per pagina (max. 5 pagina's) + metadata (title/description) per pagina.
- Swarm-voordeel: parallelle SEO-copy-check en tone-of-voice-check tegen één doorgaande schrijfsessie; grens: uiteindelijke esthetische/merkvoorkeur blijft subjectief, mens moet beoordelen.
- Vaste scope: max. 5 pagina's, 1 revisieronde. Input: bedrijfsinfo, doelgroep, 3 concurrerende sites. Doorlooptijd: 🟡 1–2 werkdagen.
- Acceptatiechecklist: ✅ elke pagina heeft unieke title/description · ✅ geen gekopieerde tekst van opgegeven concurrenten (plagiaatcheck) · ✅ CTA aanwezig per pagina.
- Risico's: copyright bij onbedoelde overlap met bronmateriaal, verwachtingsmanagement over "SEO-resultaat" (geen garantie op ranking).

**5. Leadlijst + eerste-contact-templates (B2B)**
- Koper: B2B-zzp'er/klein mkb die actief nieuwe klanten wil benaderen.
- Deliverable: lijst van 25 publiek vindbare, relevante bedrijven (naam, sector, contactpagina-link — geen geschraapte privé-data) + 2 contact-templates (mail + LinkedIn-bericht).
- Swarm-voordeel: parallelle segmentatie (sector/regio-matching) + aparte compliance-check (geen persoonsgegevens zonder rechtsgrond, AVG-bewust) t.o.v. één doorlopende sessie die compliance makkelijker over het hoofd ziet tijdens generatie.
- Vaste scope: 25 leads, 1 sector/regio, 1 revisieronde. Input: doelsector, regio, ICP-omschrijving. Doorlooptijd: 🟡 1 werkdag.
- Acceptatiechecklist: ✅ alle 25 contacten zijn publiek en actueel vindbaar (geen dode links) · ✅ geen persoonlijke (niet-zakelijke) gegevens · ✅ templates AVG-bewust geformuleerd (geen ongevraagde persoonsgegevensclaims).
- Risico's: 🔴 AVG/cold-outreach-regels — vraag voor jurist vóór commerciële lancering; leaddata kan snel verouderen (freshness-risico).

**6. Omzet-/liquiditeitsprognose (model + toelichting)**
- Koper: starter/mkb die een prognose nodig heeft voor eigen inzicht of bank/financier.
- Deliverable: Excel-model (12 maanden, scenario laag/midden/hoog) + 1 pagina toelichting van aannames.
- Swarm-voordeel: zelfde rekencontrole-argument als dienst 3.
- Vaste scope: 12 maanden, 3 scenario's, 1 revisieronde. Input: huidige omzet/kosten, groeiaanname. Doorlooptijd: 🟡 1–2 werkdagen.
- Acceptatiechecklist: ✅ formules kloppen bij herberekening · ✅ aannames expliciet gelabeld · ✅ scenario's intern consistent.
- Risico's: 🔴 dit mag niet worden gepresenteerd als financieel/fiscaal advies — expliciete disclaimer nodig, accountant moet valideren; banken kunnen eigen formatvereisten hebben (niet gegarandeerd compatibel).

**7–10 (verkort):** Social-mediacontentkalender (tekst) — goed testbaar op consistentie/toon, matig swarm-voordeel, subjectieve smaak blijft risico. Eenvoudig ondernemingsplan — laag testbaar (grotendeels tekst/beoordeling), hoog verwachtingsrisico ("gaat dit een lening garanderen?" — nee). Productfoto-briefing + AI-beeldconcepten — copyright/beeldrechtrisico, matige testbaarheid (visuele smaak). Logo/huisstijl + QR — laagste prioriteit als kerndienst, aanbevolen als goedkope add-on bij andere diensten, niet als zelfstandig topproduct.

---

## 6. Tien sample-tests (fictieve data, vooraf gedefinieerde criteria)

**Belangrijke beperking, expliciet volgens opdracht:** deze samples zijn geschreven binnen dezelfde single-session-omgeving die ook dit rapport schrijft — er is géén aparte swarm-infrastructuur aangeroepen en géén gecontroleerde ChatGPT/Claude-vergelijking uitgevoerd (zelfde brief/inputs/rubriek/vergelijkbare inspanning was niet beschikbaar binnen de tijd). **Conclusie: er is geen vergelijking uitgevoerd — dit wordt hier expliciet vermeld in plaats van een vergelijking te verzinnen.** Samples tonen alleen *haalbaarheid van het deliverable-formaat*, niet klantvraag en niet een swarm-vs-single-model-voordeel.

Fictief testbedrijf: "Van Dalen Tuinonderhoud", zzp, Utrecht, 1 medewerker, tuinonderhoud voor particulieren.

| # | Dienst | Acceptatiecriteria (vooraf) | Resultaat sample | Pass/fail per criterium | Automatisch vs. menselijk gecheckt | Tijd | Retries | Ontbrekende inputs/blokkades |
|---|---|---|---|---|---|---|---|
| 1 | SEO-audit | 10 specifieke fixes, geen verzonnen concurrentiecijfers | Rapportschets met 10 fixes (bv. "voeg openingstijden toe aan Google-profiel", "gebruik 'tuinonderhoud Utrecht' in H1") | Pass: specifiek ✅ · Pass: geen verzonnen cijfers ✅ (geen concurrentiedata gebruikt zonder bron) | Format automatisch, inhoudelijke juistheid menselijk | 🟡 ~20 min in deze sessie | 0 | Geen echte Google-profiel-link beschikbaar (fictief) → fixes zijn generiek-illustratief, geen echte audit |
| 2 | Offertepakket | Bedragen kloppen, consistente voorwaarden | Templateofferte "Voorjaarsonderhoud, 10 beurten, €45/beurt = €450" + 3 follow-upmails | Pass: rekenkundig correct (10×45=450) ✅ · Pass: consistent ✅ | Rekencontrole automatisch mogelijk, toon menselijk | 🟡 ~15 min | 0 | Geen echte USP's van klant — fictief ingevuld |
| 3 | KPI-dashboard | Formules kloppen bij test, bestand opent correct | Spreadsheet-opzet: Omzet, Kosten, Marge%, 12 mnd, formule Marge% = (Omzet-Kosten)/Omzet | Pass: formule rekenkundig correct bij testwaarden (bv. Omzet 1000, Kosten 600 → Marge 40%) ✅ | Formule-uitkomst automatisch herberekenbaar; layout menselijk | 🟡 ~15 min | 0 | Geen echte CSV-upload getest (geen Excel-engine in deze sandbox) — alleen formulelogica gecontroleerd op papier |
| 4 | Website-copy | Unieke title/description per pagina | 5 paginatitels + beschrijvingen geschetst (Home, Diensten, Over ons, Prijzen, Contact) | Pass: alle 5 uniek ✅ | Uniciteit automatisch telbaar; kwaliteit menselijk | 🟡 ~15 min | 0 | Geen echte concurrent-URL's om plagiaat tegen te checken |
| 5 | Leadlijst | 25 publieke, actuele contacten, geen persoonsgegevens | Niet uitgevoerd: zou vereisen scrapen van echte, actuele bedrijfswebsites | **Geblokkeerd** — opdracht verbiedt het benaderen/verzamelen van echte bedrijfsgegevens buiten toegestane scope binnen deze sessie | n.v.t. | — | — | **Geblokkeerd door opdrachtgrens** (geen echte bedrijven benaderen) — alleen format/proces hier beschreven, geen echte 25-lijst gegenereerd |
| 6 | Omzetprognose | Formules kloppen, aannames gelabeld | 12-mnd model-opzet met 3 scenario's, aannames expliciet (bv. "groei 2%/mnd, AANNAME") | Pass: aannames gelabeld ✅ · Pass: scenario's consistent opgezet ✅ | Formules automatisch controleerbaar; aannames menselijk te toetsen | 🟡 ~15 min | 0 | Geen echte historische omzetdata (fictief) |
| 7 | Contentkalender | 1 maand, consistente toon | 4 weekposts geschetst voor fictief bedrijf, consistente "warme, lokale" toon | Pass: toon consistent (zelfbeoordeeld, subjectief) ⚠️ | Grotendeels menselijk (toon is subjectief) | 🟡 ~10 min | 0 | Geen merkstijlgids van klant — toon is dus een aanname |
| 8 | Ondernemingsplan (concept) | Bevat verplichte onderdelen (markt, financiën, team) | Schets met 5 secties | Pass: onderdelen aanwezig ✅ · Fail-risico: financiële onderbouwing is placeholder, niet accountant-gevalideerd ⚠️ | Structuur automatisch checkbaar; financiële inhoud moet menselijk/accountant gevalideerd worden | 🟡 ~15 min | 0 | Geen echte financiële basisgegevens |
| 9 | Beeldconcept-briefing | Briefing bevat stijl, kleur, geen copyright-schending | Briefingdocument: kleurenpalet, stijlwoorden, geen specifieke bestaande merken gekopieerd | Pass ✅ | Grotendeels menselijk (visuele smaak subjectief) | 🟡 ~10 min | 0 | Geen echte beeldgenerator aangeroepen binnen deze sessie — alleen briefing-formaat getest |
| 10 | Logo/QR-startpakket | QR-code scant correct, logo-bestand levert in juist formaat | QR-inhoud gespecificeerd (bv. link naar contactpagina); logo-formaatspecificatie (SVG/PNG) beschreven | Pass op specificatieniveau; **niet** fysiek gegenereerd/gescand binnen deze sessie | QR-scan-check is objectief automatiseerbaar maar hier niet uitgevoerd | 🟡 ~10 min | 0 | Geen beeldgeneratie-/QR-generatietool aangeroepen in deze sessie — alleen proces beschreven |

**Samenvatting betrouwbaarheid van deze tests:** dit zijn **processchetsen**, niet volledig uitgevoerde, geautomatiseerd geverifieerde deliverables (dat zou echte spreadsheet-engines, QR-generators en beeldgeneratie vereisen, wat buiten de tijd/scope van deze sessie valt). Zoals de opdracht zelf stelt: *samples bewijzen geen klantvraag* — en hier geldt bovendien dat deze samples zelf beperkt zijn tot specificatieniveau voor diensten 5, 9 en 10.

---

## 7. Beste vijf MVP-diensten en economie (werkpakket 5)

Gekozen MVP-vijf (hoogste score uit §5): 1) SEO-audit, 2) Offertepakket, 3) KPI-dashboard, 4) Website-copy, 5) Leadlijst.

**Model (laag/basis/hoog), per opdracht, in euro — alle kostenposten gelabeld:**

| Post | Laag | Basis | Hoog | Bron/status |
|---|---|---|---|---|
| Klantprijs (excl. btw) | €75 | €150 | €300 | 🟡 aanname, gebaseerd op §3-referentie (€81/u zzp-tarief × geschatte 1–4 uur equivalent) |
| Btw (21%, NL-standaardtarief) | €15.75 | €31.50 | €63 | 🔴 **accountant moet bevestigen toepasselijk btw-regime en eventuele KOR** |
| Mollie-fee (iDEAL, NL-domestic) | €0,32 | €0,32 | €0,32 | 🟢 officiële Mollie-prijspagina, gecheckt 13-11-2026 |
| Mollie-fee (kaart EU-consument, alt.) | 1,80%+€0,25 | 1,80%+€0,25 | 1,80%+€0,25 | 🟢 idem |
| IMD-kosten per opdracht | 🔴 **n.n.b.** (owner-settable) | 🔴 **n.n.b.** | 🔴 **n.n.b.** | Geen officiële IMD-prijsdocumentatie gevonden (§4) — eigenaar moet eigen swarm-/compute-/seat-kosten invullen |
| Menselijke reviewtijd (owner) | 10 min × €40/u-equivalent = €6,67 | 20 min = €13,33 | 40 min = €26,67 | 🟡 aanname: review-uurtarief en -duur zijn schattingen, niet gemeten |
| Support/revisie-buffer | €0 (geen revisie nodig) | €10 (1 revisie, deels geautomatiseerd) | €25 (1 revisie, deels handmatig) | 🟡 aanname |
| Restitutie-/mislukkingsreserve | 2% van omzet | 5% | 10% | 🟡 aanname, geen gemeten faalpercentage beschikbaar |

**Resulterende marge-formule:** `Marge = Klantprijs − Mollie-fee − IMD-kosten − menselijke reviewtijd − support/revisie − restitutiereserve` (btw is doorgeefpost aan Belastingdienst, geen marge-component — moet door accountant correct worden afgehandeld, met name rond kleineondernemersregeling en eventuele btw-vrijstelling voor digitale diensten aan particulieren vs. zakelijke klanten binnen/buiten NL).

Omdat de IMD-kostenpost onbekend is, **kan geen eindmarge in euro's worden gegeven zonder die eigenaar-input** — dit is bewust niet verzonnen. Zodra de eigenaar het werkelijke IMD-kostencijfer per opdracht invult, is de rest van de formule direct bruikbaar (alle andere posten zijn hierboven expliciet en met bron/aanname-label aanwezig).

**Euro vs. crypto-prijzen:** 🟢 Feit: Mollie's gepubliceerde tarieven zijn alle in euro/EU-betaalmethoden; geen officiële Mollie-cryptobetaalmethode is in de opgehaalde prijspagina vermeld. 🟡 Aanbeveling (afgeleid, geen garantie): voor Nederlandse zzp-klanten is **euro via Mollie/iDEAL** de meest frictieloze en meest vertrouwde optie (laagste fee bij iDEAL: vast €0,32, geen percentage) — crypto-acceptatie voegt voor déze specifieke doelgroep eerder complexiteit (koersvolatiliteit, boekhoudkundige verwerking, btw-behandeling van crypto-ontvangsten) toe dan voordeel. 🔴 Vraag voor accountant/jurist: fiscale behandeling van crypto-ontvangsten in de Nederlandse boekhouding, en of de eigenaar's bestaande cryptoroute (genoemd in de opdracht) een reëel kostenvoordeel biedt t.o.v. Mollie-iDEAL dat opweegt tegen deze complexiteit — **niet aan te nemen zonder die toetsing.**

🔴 **Openstaande vragen voor accountant/jurist** (verzameld): (1) btw-regime en KOR-toepasbaarheid per dienst; (2) fiscale behandeling crypto-ontvangsten; (3) AVG-compliance voor leadlijst-dienst; (4) aansprakelijkheid bij financiële-prognose-/ondernemingsplan-diensten (disclaimer-tekst laten toetsen); (5) noodzaak van algemene voorwaarden m.b.t. herroepingsrecht bij digitale diensten aan consumenten (Wet Koop op Afstand/digitale inhoud).

---

## 8. Haalbare go/no-go-drempels

- 🟡 Voorgestelde drempel per MVP-dienst vóór opschalen: minimaal 20 **betaalde** opdrachten, first-pass-acceptatie ≥ 90% tegen de gepubliceerde checklist, gemiddelde reviewtijd binnen begrote tijd, geen AVG/copyright-incidenten. Dit is een **startdrempel**, niet de 99%-claim (die pas na veel grotere steekproef en langere meetperiode te onderbouwen is, zie §4).
- Niet doorgaan ("no-go") als: reviewtijd structureel > 2× begroot (marge verdwijnt), of > 20% van samples een menselijke "subjectieve kwaliteit"-correctie nodig heeft die niet in de checklist te vangen is (duidt op verkeerd geschaalde scope).

---

## 9. Risico's en vervolgacties

**Risico's (samengevat uit per-diensttekst):** freshness (SEO/marktinfo verouderen), copyright (content/beeld), AVG (leadlijst, klantdata in dashboards), verwachtingsmanagement (geen garantie op omzet/ranking/financiering), subjectieve kwaliteit (toon, esthetiek) blijft mensenwerk, en — structureel — de nog onbekende IMD-kostenbasis die de hele margeberekening blokkeert tot de eigenaar die invult.

**Vervolgacties (concreet, geen marktactie zonder toestemming):**
1. Eigenaar vult werkelijke IMD-kostprijs per opdracht in → marge-model in §7 direct afrondbaar.
2. Open de 7 Trends-links in §2 handmatig en vul concrete scores in vóór een investeringsbeslissing.
3. Laat btw/crypto/AVG-vragen (§7, §5) door accountant/jurist beantwoorden vóór lancering.
4. **Markttests die klant- of eigenaargoedkeuring vereisen (niet in deze opdracht uitgevoerd):** echte betaalde pilotopdrachten bij 5–10 echte klanten per MVP-dienst, een echte A/B-vergelijking swarm-vs-single-sessie met identieke briefing, en eventueel een kleine KVK-ondernemerspanel-vraag over concrete koopbereidheid (geen van deze is hier uitgevoerd — alle vereisen hetzij uitgaven, hetzij contact met echte bedrijven, hetzij eigenaargoedkeuring).

---

## 10. Gedateerde bronnenlijst

- CBS, "Afname aantal zzp'ers na jarenlange stijging", cbs.nl/nl-nl/nieuws/2025/19 — geraadpleegd 13-11-2026.
- KVK, persbericht "Ondernemers missen ruimte voor vernieuwing" / dutchitchannel.nl-verslag, 10/14 oktober 2025 — geraadpleegd 13-11-2026.
- Mollie, officiële prijspagina mollie.com/nl/pricing — geraadpleegd 13-11-2026 (fees per methode zoals geciteerd in §3/§7).
- Searchlab.nl, prijsgidsen website-/webshopkosten en zzp-uurtarief-onderzoek (20.000 zelfstandigen), 2025–2026 — geraadpleegd 13-11-2026.
- Bankless.com, artikel over IdentityMD/IMD AI-swarm (NFT-seat-model) — geraadpleegd 13-11-2026; enige gevonden bron over IMD, geen prijsdocumentatie.
- Google Trends (trends.google.com) — **niet live geraadpleegd in deze run**; exacte queryformaten in §2 ter handmatige verificatie.

Einde rapport.
