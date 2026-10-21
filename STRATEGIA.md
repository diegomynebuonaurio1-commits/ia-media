# @ia.senzafuffa – istruzioni operative

Pagina Instagram italiana "senza volto" sull'IA usata davvero: prompt pronti e strumenti testati. Tono diretto, pratico, un filo ironico, mai da "guru". Vietato: promesse di guadagno facile, contenuti presi da altre pagine, prompt mai provati.

## Formato standard (carosello)
- Generatore: `python3 tools/make_carousel.py postNN/spec.json postNN` (Playwright + font Inter; 1080x1350 PNG), poi conversione in JPG qualità 92 (`slide_XX.jpg`).
- Struttura spec: cover (sticker, huge, line con *evidenziato*, sub, chips), 8-10 items (emoji, title con *evidenziato*, prompt con [segnaposto], time, for), end (title, kw "PROMPT", sub).
- Slide finale: invito a commentare PROMPT. Didascalia: hook breve, come usarlo, 3 call to action (salva, manda a, commenta PROMPT), 6-8 hashtag italiani.
- Guida gratuita per chi commenta PROMPT: https://diegomynebuonaurio1-commits.github.io/ia-media/

## Calendario
- PIANO GRATUITO METRICOOL: massimo 20 post programmati al mese (controlla con getScheduledPosts quanti ce ne sono già nel mese prima di programmarne altri).
- 4 post a settimana: 2 caroselli (mar, gio) e 2 reel (mer, sab). Reel: `python3 tools/make_reel.py postNN/spec.json postNN/reel.mp4 4` (spec con 4 prompt brevi, 1080x1920, ~25 s, con musica originale generata da tools/music.py, senza copyright), su Metricool type REEL con videoCoverMilliseconds 500. Un reel su due può essere TRIAL_REEL per raggiungere chi non segue.
- Vecchia regola sostituita: 4 caroselli a settimana (mar, mer, gio, sab) all'orario migliore indicato da Metricool (getBestTimeToPostByNetwork), brand Metricool 7555398, fuso Europe/Rome.
- Immagini: caricate in questo repo, URL https://raw.githubusercontent.com/diegomynebuonaurio1-commits/ia-media/main/postNN/slide_XX.jpg

## Serie fissa "L'IA per il tuo mestiere" (ispirata ai profili che crescono di più)
Un post su due della serie: "Cosa farei con l'IA se fossi un/una [mestiere]" con sottotitolo "dal [input] al [risultato]" (es. dal vocale al preventivo). Mestieri: commercialista, elettricista, idraulico, parrucchiere, centro estetico, ristoratore, agente immobiliare, fotografo, personal trainer, avvocato, insegnante, fonico/service audio. Solo flussi realistici con strumenti esistenti e prompt concreti; niente promesse di guadagno.

## Idee (segna [x] quando pubblicata, numerazione del piano di lancio)
- [x] 1 I 10 prompt che uso ogni giorno (post01)
- [ ] 2 5 tool IA gratuiti che sembrano illegali
- [ ] 3 Come usare questa pagina
- [ ] 5 Il prompt che riassume un PDF di 50 pagine
- [ ] 6 Smetti di scrivere "fammi un testo": scrivi così
- [ ] 7 Curriculum riscritto dall'IA: prima e dopo
- [ ] 10 La tua settimana pianificata in 2 minuti
- [ ] 11 Come capire se un testo l'ha scritto l'IA
- [x] 12 7 prompt per chi ha una partita IVA (post02)
- [ ] 13 Rispondi alle recensioni negative senza perdere la calma
- [ ] 15 Studia il doppio più veloce con questo metodo
- [ ] 16 ChatGPT, Claude o Gemini: quale usare per cosa
- [ ] 18 Trova un nome per il tuo progetto in 1 minuto
- [x] 20 Prompt per preparare un colloquio (post03, reel)
- [ ] 21 L'IA ha fatto i conti di casa: ecco come
- [ ] 22 Quello che l'IA NON deve sapere di te
- [ ] 26 10 domande da fare all'IA prima di un acquisto
- [ ] 27 Scrivi post per la tua attività per un mese
- [ ] 28 Gli strumenti IA del mese: cosa vale la pena provare
- [ ] 30 Il prompt più utile che conosco
(I reel 4, 8, 9, 14, 17, 19, 23, 24, 25, 29 richiedono registrazioni di Diego: preparare solo i copioni.)

## Registro pubblicazioni
| Data | Post | Idea |
| --- | --- | --- |
| 2026-10-21 10:00 | post01 carosello | 1 |
| 2026-10-22 10:00 | post02 carosello | 12 |
| 2026-10-24 10:00 | post03 reel | 20 |
| 2026-10-21 19:30 | post00 Comincia da qui (da fissare) | - |
| 2026-10-23 18:00 | post04 reel | serie mestieri: elettricista |
| 2026-10-25 18:00 | post05 trial reel | 4 trucchi ChatGPT |
