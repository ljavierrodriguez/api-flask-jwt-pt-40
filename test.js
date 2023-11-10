const getData = async () => {
    let token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTY1NjQ5OSwianRpIjoiODY5NWVhZmQtYTY3YS00MmI3LWE5ZWYtZmZiOWU3NjUzNWZjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjk5NjU2NDk5LCJleHAiOjE2OTk5MTU2OTl9.o-zLFSrkfAxG1Oh_bf54POY-WTh-S_M-vbz7Tml8RXU";
    let headersList = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    
    let response = await fetch("http://127.0.0.1:5000/api/profile", {
        method: "GET",
        headers: headersList
    });
    
    let data = await response.text();
    console.log(data);
}

getData();
