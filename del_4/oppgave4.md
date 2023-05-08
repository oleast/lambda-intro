## Oppgave 4

## Lese innholdet
Kanskje vi har lyst til å lese innholdet i bøtta vår? Det kan vi gjøre med boto3. I lambda har runtimen boto3 installert, men ikke på maskinen vår. Last ned boto3 `pip3.10 install boto3`.

- Prøv litt på egenhånd her. https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/get_object.html. Du må hente objektet og så lese innholder. 
for å hjelpe litt på vei:
Du leser innholder ved å kalle `.read()` på streaming-objektet du får. Hvis du importerer json kan du bruke `json.loads` for å få innholdet som et python-objekt.
- Prøv å gjøre en `serverless dpeloy` og se hva som skjer når du kjører den samme koden i lambda. Feiler det? Hvorfor? Hva kan du gjøre for å fikse det?


## Tilgangsmorro.
En lambda får lov til å se eventen den har mottatt, men det betyr ikke at den har tilgang til objektet den peker til. 
Lambda bruker en executionrole, som er satt opp av serverless. Denne har ikke tilgang til bøtta vår. La oss gjøre noe med det. 
- Gi lambdaen tilgang til GetObject for alle filer i bøtta vår. Bruk https://www.serverless.com/framework/docs/providers/aws/guide/iam for å finne ut hvordan du gjør det.

## Lagre dataen på vår måte. 
La oss lagre dataen litt mer strukturert. 

Vi lager oss en DynamoDB-tabell. DynamoDB er en NoSQL-database som er enkel å bruke.

Da trenger vi følgende:
- Vi trenger en tabell og å skrive dataen vi mottar til DynamoDB.
Bruk eksempelet her til å legge til en ny tabell under `resources` i `serverless.yml`: https://www.serverless.com/guides/dynamodb
- Legg til muligheten til å kalle på putItem i iam-rollen i serverless.yml. Når du deployer endringen pass på å bruke `serverless deploy --force` for å overskrive den gamle rollen. 
- Nå må vi skrive dataen til dynamodb. 
Sett nøkkelen i tabellen til å hete `id` og sett verdien til å være `<type>-<name>` fra objektet du får fra S3.
```python
...
  dynamodb_resurce = boto3.resource('dynamodb', region_name='eu-west-1')
  inventory_table = dynamodb_resurce.Table('halvors-halvbistro-inventory')
...
  for item in content:
    item['id'] = item['type'] + '-' + item['name']
    inventory_table.put_item(Item=item)
```
- Deploy og test at det funker.

## Additiv og ikke overskrivende
Vi ønsker at vi heller legger til tingene vi får inn, hvis vi allerede har noe av det på lager. 

Bruk boto3 dokumentasjonen til å finne ut hvordan du jobber med dynamoDB for å sjekke om noe finnes og tar det med i beregningen før du eventuelt legger det til. https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html

Hint: Hvis du ender opp med å bruke update_item, så er denne kodeblokken kanskje nyttig.
```python
      inventory_table.update_item(
        Key={'id': item['id']},
        UpdateExpression='set quantity = quantity + :val',
        ExpressionAttributeValues={':val': Decimal(str(item['quantity']))}
      )
```