# Oppgave 1

## Mise en place

Installer:

- serverless
- python 3.10, 3.11 eller 3.12
- awscli

For MacOS gjør du dette med: `brew install serverless python3 awscli`

Sjekk at alt funker:

- `serverless --version`
- `python3 --version`
- `aws s3 ls`

## Sett opp AWS CLI

- Åpne IAM i AWS konsollen
- Opprett en ny Access Key, lagre navnet og nøkkelen
- Kjør `aws configure`

## Vår Hello World og litt python-intro

Lag deg en mappe. Den skal du bruke gjennom hele denne workshoppen. F.eks. her i dette repoet og kall den `arbeidsmappa`.

I denne skal vi lage oss en python-fil, f.eks. hello.py. Bruker du andre navn må du ta høyde for det i kommandoene under.

I `hello.py` skriver du:

```python
def hello(event="", context=""):
  print("Hei folkens!")
```

For å kjøre dette lokalt på maskinen bruker du `python3 hello.py`. Da vil ingenting skje. Vi har jo bare definert en funksjon, men vi må kalle på den også. det gjør vi ved å legge til dette på slutten av fila:

```python
if __name__ == '__main__':
  hello()
```

Denne biten er python sin måte å si at hvis du kjører denne fila direkte og ikke importerer den fra en annen fil så skal du kjøre koden som står her.

Nå bør du få opp "Hei folkens!" når du kjører `python3 hello.py`.

## Click-ops for å kjenne på lambda.

Gå til lambda i AWS-konsollen. Velg "Create function". Velg "Author from scratch". Prøv deretter selv å fylle ut resten. Bruk gjerne et navn som inneholder ditt eget fornavn e.l. så det er lett å kjenne ting igjen seinere for deg og andre.

Når funksjonen kjører vil vi laste opp koden vår og få den til å kjøre.
Aller først gjør vi et par endringer for å få det til å fungere som en lambda-funksjon.

```python
def hello(event, context):
  return "Hei folkens!"
```

Vi tar inn to argumenter som alle funksjoner som kalles av lambda får. Deretter returnerer vi en verdi i stedet for å printe den.

Sånn! Nå er vi klare til å laste opp koden vår.

- Zip hello.py fila di (`zip hello-zip hello.py` funker f.eks.).
- Last zipfilen opp til lambdaen din i AWS
- Vi må endre Handler under runtime settings, siden denne stod til boilerplate-verdier. Strukturen her er `<filnavn>.<funksjonsnavn>`.
- Trykk på test og lag en random test-event. Det er likegyldig hva som står i input inntil videre.
- Test i vei!

Da har vi click-opsa oss gjennom
