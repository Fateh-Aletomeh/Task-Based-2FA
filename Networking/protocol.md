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

### Send Task
```
TASK: { 
        "attempt": <attempt>,
        "task_id": <task_id>,
        "task_data": <task_data>,
        "task": <task>,
        "curr_time": <curr_time>,
        "exp_time": <exp_time>
      }

<attempt> is either 1, 2 or 3
<task_id> is ...
<task_data> is ...
<task> is ...
<curr_time> is a number of seconds since Unix epoch
<exp_time> is a number of seconds since Unix epoch
```

### Receive Response
```
RESPONSE: {
            "task_id": <task_id>,
            "resp_time": <resp_time>,
            "user_resp": <user_resp>
          }

<task_id> is ...
<resp_time> is a number of seconds since Unix epoch
<user_resp> is ...
```

### User Approved
```
OUTCOME: {
            "outcome": <outcome>
         }

<outcome> is either 0 (for rejected) or 1 (for approved)
```
