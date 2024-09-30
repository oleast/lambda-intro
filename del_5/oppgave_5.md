# Oppgave 5

## SQS

Nå har vi en lambda for å oppdatere invetar-lista vår, vi har en s3 bøtte hvor potensielt ekserne kan dumpe oppdateringer til inventory-lista vår. Hvordan skalerer denne løsningen så langt?

la oss utvide funksjonaliteten litt. Først, la oss lage en melding for hver oppdatering vi får inn. Vi kan bruke SQS til dette.

- Lag en SQS kø i serverless.yml.

```yaml
mySQSQueue:
  Type: "AWS::SQS::Queue"
  Properties:
    QueueName: halvor-halvbistro-inventory-received
```

- Skriv en melding til køen når vi gjør en oppdatering som inneholder itemet.
  https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html
- Gå til SQS i aws-konsollen og se om meldingen din er der. Gjør dette gjennom send/receive message i konsollen.
- Legg til følgende i inventory.json og last den opp til s3, så den leses. Sjekk at nye objekter oppdateres riktig.

```json
{
  "type": "condiment",
  "name": "mustard",
  "quantity": 5
}
```

## Ny lambda til å lese køen

La oss lage en ny lambda til å lese køen!

- Lag en fil, `read_queue.py` i `arbeidsmappa` med en lambda-funksjon i `serverless.yml` som leser meldingen fra køen og printer ut innholdet i eventen.
- Legg til en ny trigger i `serverless.yml` som trigger lambdaen når det kommer en melding i køen.

## Skill på meldinger

- Legg til et et felt `update-type`i meldingen. Skriv om inventory-readeren til å legge ved dette feltet i meldingene på køen. Velg `NEW_PRODUCT`for ting som ikke finnes i tabellen fra før, `HIGH_STOCK` hvis det er mer enn 50 av noe og `OUT_OF_STOCK` hvis det er 0 eller under av noe. Ellers setter man `ITEM_UPDATE` Test det ved å legge til eller endre varer i `inventory.json`.
