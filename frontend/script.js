const factText= document.getElementById("fact-text");
const factButton= document.getElementById("fact-button");


    factButton.addEventListener("click", async function(){
        factText.textContent= "Loading a fact...";
try{
    const response= await fetch("https://programming-study-hegpbngya9eba7hb.centralus-01.azurewebsites.net/api/fact");
    if(!response.ok){
        throw new Error("Could not load a fact.")
    }
    const data= await response.json();
    factText.textContent= data.fact;
}catch(error){
    factText.textContent="Could not load a fact. Please try again."
}
});

const studyForm= document.getElementById("study-form");
const studyTopic= document.getElementById("study-topic");
const studyResponse= document.getElementById("study-response");

studyForm.addEventListener("submit", async function(event){
event.preventDefault();
const topic=studyTopic.value.trim();
studyResponse.textContent= "Getting encouragement..."
try{
const response = await fetch("https://programming-study-hegpbngya9eba7hb.centralus-01.azurewebsites.net/api/study", {
    method: "POST",
    headers:{"Content-Type": "application/json"},
    body: JSON.stringify({topic: topic})
    
})
const data= await response.json();
if(!response.ok){
    throw new Error(data.error || "Could not get encouragement");
}
studyResponse.textContent= data.message;
}catch(error){
    studyResponse.textContent= error.message;
}
});

async function checkLoginStatus() {
    const loginLink=document.getElementById("login-link");
    const userGreeting=document.getElementById("user-greeting");
    const logoutLink=document.getElementById("logout-link");

    try{
        const response=await fetch("/.auth/me");
        if(!response.ok){
            throw new Error("Could not check login status.")
        }
        const data=await response.json();
        const user= data.clientPrincipal;

        if(user && user.userRoles.includes("authenticated")){
            const username=user.userDetails || "User";
            userGreeting.textContent="Hello, " +username+ "!";
            userGreeting.hidden=false;
            loginLink.hidden=true;
            logoutLink.hidden=false;
        }else {
            loginLink.hidden=false;
            userGreeting.hidden=true;
            logoutLink.hidden=true;
        }
    }catch (error){
        console.error("Authentication error: ", error);
        loginLink.hidden=false;
        userGreeting.hidden=false;
        logoutLink.hidden=true;
    }
}
checkLoginStatus();
