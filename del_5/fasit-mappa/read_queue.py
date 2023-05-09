def read_queue(event, context):
  body = event['Records'][0]['body']
  print(body)


  return "Read a message from the queue"
