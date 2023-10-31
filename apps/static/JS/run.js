window.onload=function(){
    imgCount=0;		//当前图片计数器
    myImg=document.getElementById("ANimalimg");
    myBox=document.getElementById("scrollBar");
    //获取图片所在的位置
    myNumberBox=document.getElementById("number");
    
    myNumberLi=myNumberBox.getElementsByTagName("li");
    //循环添加active样式
    for(i=0;i<myNumberLi.length;i++){
      myNumberLi[i].index=i;
      myNumberLi[i].onclick=function(){
         for(i=0;i<myNumberLi.length;i++){
             myNumberLi[i].classList.remove("active");
         }
         this.classList.add("active");
         imgCount=this.innerHTML-1;
         myImg.src="../static/IMG/"+imgCount+".jpg";
      }
    }
    
    myBox.onmouseover=function(){
     clearInterval(timeOUT);
    }
    myBox.onmouseout=function(){
      //规定时间触发改变图片方法
     timeOUT=setInterval(changeImg,10000);   
    }
    function changeImg(){
        imgCount++;
        imgCount=imgCount%5;
        myImg.src="../static/IMG/"+imgCount+".jpg";
        for(i=0;i<myNumberLi.length;i++){
             myNumberLi[i].classList.remove("active");
         }
        myNumberLi[imgCount].classList.add("active");
    }
    
   timeOUT=setInterval(changeImg,10000);
 }