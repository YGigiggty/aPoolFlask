let theBody =document.querySelector("#body");
let CleanBut =document.querySelector("#cleanBody");
let titleInput=document.querySelector("#Title");
CleanBut.addEventListener("click",(ev)=>{
   theBody.value="";
   titleInput.value="";
})