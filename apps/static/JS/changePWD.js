let userEmail= document.querySelector("#userEmail");
let submitData =document.querySelector("#submit");
let Msg =document.querySelector("#changeMsg");
let form =document.querySelector("#changePWD_form");

userEmail.addEventListener("blur",(ev)=>{
    const email = ev.target.value;
    if(!email){
        Msg.innerText="邮箱不可为空"; 
        submitData.classList.replace("btn","boom");
    }else{
        let EmailRegexp = /^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$/
        if(!EmailRegexp.test(email)){
            Msg.innerText="邮箱格式错误，请重新输入";
           
        }else{
            submitData.classList.replace("boom","btn");
        }
    }
})

userEmail.addEventListener("focus",()=>{
    if(Msg.innerText !=""){
        Msg.value="";
    }
    Msg.innerText ="";
})