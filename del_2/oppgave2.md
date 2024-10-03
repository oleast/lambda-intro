## Oppgave 2

## serverless

Neste er serverless for å holde styr på ting!

- `serverless create --template aws-python3 --name hello-world`

Pass på å gjøre følgende endringer til serverless.yml:

- sett service-navn (noe gjenkjennelig og unikt for deg)
- sett region til eu-west-1
- sett stage til dev
- sett runtime til python3.12
- sett handler riktig.

Vi kan deploye med `sls deploy`.

La oss ta en titt på hva serverless gjorde for oss i consollen. Test den!

Deretter kan du finne stacken din i cloudformation.
