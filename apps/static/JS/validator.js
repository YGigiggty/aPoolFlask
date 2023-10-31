window.onload =function(){
    /*用户名验证*/
    let Username =document.querySelector("#UserName");
    let UsernameError = document.querySelector("#NameP");
    Username.addEventListener("blur",(ev)=>{
        let GetUsername =ev.target.value;
        let FilterUsername = GetUsername.trim();
        
        if(!FilterUsername){
            UsernameError.innerText ="用户名不能为空";
        }else{
            if(FilterUsername.length>14){
                UsernameError.innerText ="名称长度应小于14位"
            }
        }
    })

    Username.addEventListener("focus",(ev)=>{
        if(UsernameError.innerText!=""){
            Username.values ="";
        }
        UsernameError.innerText ="";
    })
 
/*邮箱验证*/
    let Uemail =document.querySelector("#UserEmail");
    let errorEmail =document.querySelector("#UserEmailP");
    Uemail.addEventListener("blur",(ev) => {
        const email = ev.target.value;
        if(!email){
            errorEmail.innerText="邮箱不可为空";
        }else{
             let EmailRegexp = /^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$/
            if(!EmailRegexp.test(email)){
                errorEmail.innerText="邮箱格式错误，请重新输入"
            }
        }
    })
    Uemail.addEventListener("focus",(ev) =>{
        if(errorEmail.innerText!=""){
            errorEmail.value="";
        }
        errorEmail.innerText="";
    })
/*电话号码验证*/
    let phone =document.querySelector("#UserPhone");
    let errorPhone =document.querySelector("#UserPhoneP");
    phone.addEventListener("blur",(ev)=>{
        let Getphone =ev.target.value;

        if(!Getphone){
            errorPhone.innerText ="电话号码不可以为空";
        }else{
            if(Getphone.length <11 || Getphone.length>11)
            {
                errorPhone.innerText="电话号码格式错误";
            }else{
                let PhoneRegexp = /^d{11}$/;
                if(PhoneRegexp.test(Getphone))
                    UsernameError.innerText="电话号码只能含有数字";
                }
            }
        })
    phone.addEventListener("focus",(ev)=>{
         if(errorPhone.innerText !==""){
            phone.value="";
        }
        errorPhone.innerText="";
    })

/*密码验证*/
    let ErrorPwd =document.querySelector("#PassWordP");
    let ConfigPwd =document.querySelector("#configPassword");

    ConfigPwd.addEventListener("blur",(ev)=>{
        let UserPwd = document.querySelector("#PassWord");
        let Pwd =UserPwd.value;
        let config =ev.target.value;
        if(!Pwd){
            ErrorPwd.innerText="密码不可以为空";
        }else{
             if(Pwd !=config){
                ErrorPwd.innerText="密码不一致";
            }
        }
})
ConfigPwd.addEventListener("focus",(ev)=>{
    if(ErrorPwd.innerText !=""){
        ConfigPwd.value ="";
    }
    ErrorPwd.innerText ="";
})

}