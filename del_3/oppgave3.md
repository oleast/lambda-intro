## Oppgave 3

## Case

La oss prøve å bygge en mer reell applikasjon hvor vi prøver å sy sammen litt forskjellige tjenester. Målet her er ikke å lage det beste designet, men heller å utforske hvordan vi kan løse oppgaver annerledes gjennom enkel tilgang til skytjenester.

La oss si at vi skal lage en tjeneste for å holde styr på lageret til Halvors Bistro, også kjent som HalvBistro. En litt annerledes bistro, siden vi bruker egenutvikla datasystemer til å holde styr på alt 🤷.

## s3 bøtter og inventar-lister

Først av alt trenger vi et sted å ta imot inventar-lister. Vi har valgt å sette opp s3-bøtter for dette, noe leverandøren har gått med på. De vil "droppe" inn en fil med inventar en gang imellom i bøtta vår.

For vår del ønsker vi da å fange opp dette, og å laste inn filen. I første omgang fokuserer vi på å fange opp og lese inn nye filer og oppdateringer av filer. Så finner vi ut hvordan vi lagrer/persisterer dataen senere.

Vi kan f.eks. sette opp en lambda til å lytte på s3-eventer.

### S3-bøtta

Normalt ville vi brukt IaC her, men i dette tilfellet går vi for serverless for å holde styr på stacken vår.

- Det er mange måter å lage en s3-bøtte i serverless, men la oss lage en s3 bucket under `resources` i `serverless.yml`. (hint: https://www.serverless.com/framework/docs/providers/aws/guide/resources/ og ta en titt i serverless.yml etter et eksempel). Gjør en `serverless deploy` for å deploye endringene.
- Sett opp en trigger for lambdaen din som lytter på s3-eventer. (hint: https://www.serverless.com/framework/docs/providers/aws/events/s3/). Se under "Using existing bucket". Gjør en `serverless deploy` for å deploye endringene.
- La oss printe eventen vi får inn i lambdaen vår.

```python
def load_inventory(event, context):
  print(event)
  return {
      "statusCode": 200,
      "body": "success",
  }

if __name__ == '__main__':
  load_inventory()
```

Gjør en `serverless deploy` for å deploye endringene.

Context er ikke like lett å printe, men er du nysgjerrig kan du se her: https://docs.aws.amazon.com/lambda/latest/dg/python-context.html.

- Test funskjonen din ved å kjøre en test i aws-konsollen.
- Kopier over `inventory.json` til arbeidsmappa og bruk denne som test-filen din fremover.
- Legg en fil i bøtta di og se hva som skjer. `aws s3 cp inventory.json s3://<bøttenavn>`. Trykk på Monitor -> View Cloudwatch Logs, her kan du se alle loggene fra funksjonen din! I funksjonen printer vi "event", så eventet som trigget funksjonen
  og se på den nyeste outputen. Her skal alle loggene fra funksjonen din ligge! Når vi printer "event" i funksjonen vår vil eventet som trigget lambdaen ligge som en egen linje.
- Ta vare på dette eventet som en egen .json fil. Kall den test-event.json. **Vi skal bruke den senere!**
- La oss se om vi kan plukke ut bøtte og fil fra eventen.
- Lagre to variabler i lambdaen din som henter ut bøtte og filnavn fra eventen. Print dem.

### Lokal testing

Det er litt tungvint å måtte kjøre sls deploy hver gang man skal gjøre en endring i koden. La oss gjøre livet vårt litt enklere.

- lag en fil som heter `test.py` e.l.
- Importer funksjonen din, last inn test-eventen vi har og kall funksjonen din med eventen. F.eks. noe som:

```python
from halvbistro import load_inventory
import json

def test_load_inventory():
    with open('test-event.json') as f:
        event = json.loads(f.read())
        result = load_inventory(event, None)
        print(result)

if __name__ == '__main__':
    test_load_inventory()
```

Nå kan vi kjøre `python3 test.py` for å teste endringene våre lokalt.
