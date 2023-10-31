var showInfo =document.querySelector(".show_avatarInfo");
var avatarImg =document.querySelector("#avatarSubmit");

const fileTypes = [
    "image/gif",
    "image/jpeg",
    "image/pjpeg",
    "image/png",
    "image/webp",
  ];

function validFileType(file) {/*判断文件是否包含允许的文件类型*/
    return fileTypes.includes(file.type);
  }

function returnFileSize(number) {/*计算上传文件大小*/
    if (number < 1024) {
      return `${number} bytes`;
    } else if (number >= 1024 && number < 1048576) {
      return `${(number / 1024).toFixed(1)} KB`;
    } else if (number >= 1048576) {
      return `${(number / 1048576).toFixed(1)} MB`;
    }
}

avatarImg.addEventListener("change",updateImageDisplay);/*监听文件输入变化*/

function updateImageDisplay()
{
    while(showInfo.firstChild)
    {/*清空预览区 <div> 留下的内容*/
        showInfo.removeChild(showInfo.firstChild);
    }
    const curFiles = avatarImg.files;
    if(curFiles.length ===0)
    {
        const para = document.createElement('p');
        para.textContent = '未找到最近上传的文件';
        showInfo.appendChild(para);
    }else
    {
        const list = document.createElement('ol');
        showInfo.appendChild(list);

        for (const file of curFiles) {
            const listItem = document.createElement('li');
            const para = document.createElement('p');
            if(validFileType(file)){
                para.textContent=`文件名： ${file.name}, 文件大小： ${returnFileSize(file.size)}.`;
                const image = document.createElement('img');
                image.src = URL.createObjectURL(file);/*绑定图片*/
                listItem.appendChild(image);
                listItem.appendChild(para);
            }else
            {
                para.textContent = `文件名： ${file.name}: 是一个非法命名文件. 请重新选择文件.`;
                listItem.appendChild(para);
            }
            list.appendChild(listItem);
        }
    }
}
let Error_name =document.querySelector("#username_error");
let userName_box=document.querySelector("#username");

userName_box.addEventListener("focus",()=>{
  Error_name.innerHTML="";
})

let User_phone =document.querySelector("#userphone");
let phone_error =document.querySelector("#phone_error");
let PhoneValidator =/^1[3456789]\d{9}$/;

User_phone.addEventListener("blur",(ev)=>{
  if(!PhoneValidator.test(User_phone.value)){
      phone_error.innerHTML="电话格式错误!";
  }
})
User_phone.addEventListener("focus",(ev)=>{
    phone_error.innerHTML="";
})


