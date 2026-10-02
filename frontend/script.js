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


