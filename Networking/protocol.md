# 2FA Network Protocol

## Terminology

- Client refers to the mobile app backend
- Server refers to the website backend

### States

- Client can be in following states:
    - READY
    - CONNECTED
    - SOLVING
    - SOLVED
    - WAITING
    - APPROVED
    - REJECTED

- Server can be in following states:
    - READY
    - CONNECTED
    - WAITING
    - CHECKING
    - CHECKED

### Messages

- There are 4 messages:
    - send task
    - receive response
    - approval

## Initialisation

- Initially, both client and server are in READY state
- When server and client establish connection, they both change to CONNECTED state

## Message contents and encoding

### Format of Task Sent to Phone App
```
TASK: {
"taskId" : <string of task id>,
"circles" : <list of circles -> example shown below>,
"creationDate": <creation date and time>
"expirationDate": <expiration date and time>
"expectedResponse": <list of circle ids>
}

Circles Example:
"circles": [
        {
            "id": "circle-0",
            "color": "red"
        },
        {
            "id": "circle-1",
            "color": "orange"
        },
        {
            "id": "circle-2",
            "color": "pink"
        } ]
```

### Format of Template Sent to Website
```
TEMPLATE: Same as the task sent to phone but without the expectedResponse list
```


### Receive Response
```
RESPONSE: {
            "task_id": <task_id>,
            "user_resp": <user_resp>
            "attempt": <current number of attempt>
          }

User Response Example:
"user_resp": ["circle-0","circle-11","circle-5","circle-8"]

```

### Feedback
```
FEEDBACK:{
            "task_id": <task_id>
            "feedback": <succeeded: 1 / failure: 0>
            "attempt": <the number of attempts this feedback is for>
         }
```

