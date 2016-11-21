# Linux Command 

# Command to use HTTP request
```
curl -i -X POST -H "Content-Type: application/json" -d '{"username":"fatimata2","password":"python"}' http://127.0.0.1:5000/api/users
```

# Kill a process running on a port
```
lsof -i :port_number
```

# Install a virtualenv in mac osx
```virtualenv -p python3.4 venv --distribute```
