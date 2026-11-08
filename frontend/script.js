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
            profileCard.hidden=false;
            notesCard.hidden=false;

            try {
                const response=await fetch("/api/me");
                if(!response.ok){
                    throw new Error("Could not load profile.");
                }
                const profile = await response.json();

                if (profile.displayName){
                    userGreeting.textContent= "Hello, "+profile.displayName+"!";
                    document.getElementById("display-name").value=profile.displayName;
                }
            }catch (error){
                console.error("Could not load saved profile:", error);
            }
        }else {
            loginLink.hidden=false;
            userGreeting.hidden=true;
            logoutLink.hidden=true;
            profileCard.hidden=true;
            notesCard.hidden=true;
        }
    }catch (error){
        console.error("Authentication error: ", error);
        loginLink.hidden=false;
        userGreeting.hidden=false;
        logoutLink.hidden=true;
        profileCard.hidden=true;
    }
}
const profileCard=document.getElementById("profile-card");
const notesCard= document.getElementById("notes-card");

checkLoginStatus();

const profileForm=document.getElementById("profile-form");
const displayNameInput=document.getElementById("display-name");
const profileResponse=document.getElementById("profile-response");

profileForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    const displayName=displayNameInput.value.trim();
    profileResponse.hidden=false;

    if (
        displayName.length <1 ||
        displayName.length >80 ||
        /[\u0000-\u001F\u007F]/.test(displayName)
    ){
        profileResponse.textContent="Please enter a valid name.";
        return;
    }
    profileResponse.textContent="Saving your profile...";

    try{
        const response=await fetch("/api/profile", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({displayName: displayName})
        });
        if(!response.ok){
            throw new Error("Could not save your profile.")
        }
        const data=await response.json();
        profileResponse.textContent="Profile saved successfully!";
        document.getElementById("user-greeting").textContent= "Hello, "+data.displayName+"!";
    }catch (error){
        profileResponse.textContent=error.message;
    }
});