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

# Generate an SSH key 
```ssh-keygen -t rsa -b 4096 -C "lemzoba@gmail.com"````

# Add the SSH key to the ssh client
```ssh-add ~/.ssh/id_rsa````

# Copy the SSH agent to the clipboard
```pbcopy < ~/.ssh/id_rsa.pub ````

# Add the ssh agent to github
Goto Setting -> New SSH key and paste the copied ssh agent there
