
//NUMBER OF PI
		const PI = 3

//Color of PI's GRAPH
const fixedColor = {
        '1' : '#eb4034',
        '2' : '#36c93e',
        '3' : '#493af2',
    }

function getDate(){
            let time = new Date();

            let year = time.getFullYear();
            let month = '' + (time.getMonth()+1);
            let date = '' + time.getDate();
            
            if(month.length<2)
                month = '0' + month;
            if(date.length<2)
                date='0'+date;
            
            return `${year}-${month}-${date}`;
           
        }
        
function getTime(){
            let time = new Date();
        
            let hours = '' + time.getHours();
            let minutes = '' + time.getMinutes();
            let seconds = '' + time.getSeconds();
            
            if(hours.length<2)
                hours = '0'+hours;
            if(minutes.length<2)
                minutes = '0'+minutes;
            if(seconds.length<2)
                seconds = '0'+seconds;
                
            return `${hours}:${minutes}:${seconds}`;
        }

function getHMS(HMS){

            var gmt = new Date(HMS); //err ( GMT + 9 + 9 is current value)
            var date = new Date(gmt.getTime() + (gmt.getTimezoneOffset() * 60000)); //-9 hours ( GMT + 9 )
            
            let hours = ('0' + date.getHours()).slice(-2);
            let minutes = ('0' + date.getMinutes()).slice(-2);
            let seconds = ('0' + date.getSeconds()).slice(-2);
            
            let time = hours+':'+minutes+':'+seconds;
            
            return time;
        }
function getDateHMS(HMS){
    var gmt = new Date(HMS); //err ( GMT + 9 + 9 is current value)
    var date = new Date(gmt.getTime() + (gmt.getTimezoneOffset() * 60000)); //-9 hours ( GMT + 9 )
    
    let years = date.getFullYear();
    let months = ('0' + (date.getMonth()+1)).slice(-2);
    let days = ('0' + date.getDate()).slice(-2);
    
    let hours = ('0' + date.getHours()).slice(-2);
    let minutes = ('0' + date.getMinutes()).slice(-2);
    let seconds = ('0' + date.getSeconds()).slice(-2);
            
    let totalDate = years+'-'+months+'-'+days+' '+hours+':'+minutes+':'+seconds;
            
    return totalDate;
}

function setCycle(){
            let cycle = document.getElementById('cycle');
                  
            let cycleLabel = document.getElementById('cycleLabel');
            cycleLabel.innerHTML = cycle.value;
                           
                  }
                  
function clock(startTime, run_state){

            let currentDate = document.getElementById("cur_date");
            let currentTime = document.getElementById("cur_time");

            if(run_state == 1){
                getRunTime(startTime);
            }
           
           currentDate.innerText = getDate();
           currentTime.innerText = getTime();
        }

function getRunTime(startTime){ //?????? ?????? ???????????? ??????
            let runTime = document.getElementById('run_time');
            
            let end = new Date(startTime);
            
            let cur = new Date();
            let milisecond = cur-end;
            let run = new Date(milisecond);
            
            let hours = ('0' + parseInt(milisecond /1000 /60/60)).slice(-2);
            let minutes = ('0' + run.getMinutes()).slice(-2);
            let seconds = ('0' + run.getSeconds()).slice(-2);
            
            let time = hours+':'+minutes+':'+seconds;
            //console.log(time);
            runTime.innerText = time;

        }
        
//*********** summary.html , home.html **************
function redirectPage(piNum){ //Redirct Page if PI no.1 is disconnected
    
    if(piNum > PI){
        alert('All failed to connect Summary Page!');
    }
    
    $.ajax({
      url: 'http://192.168.243.' + piNum + ':80/checkRunning',
      type: 'POST',
      headers:{
          'X-CSRFToken': '{{csrf_token}}'
      },
      timeout: 1000,
      success: function(data){
          //alert(`redirect to ${piNum}`);
          location.href= 'http://192.168.243.' + piNum + ':80/summary';
      },
      error: function(){
          console.log(`PI no.${piNum} Summary Page Connect Failed`);
          redirectPage(piNum + 1);
      }
    })
}

function checkRunning(){ //check the running state and change color of the box
            
            function changeColor(piNum){
                $.ajax({
                    url: 'http://192.168.243.' + piNum +':80/checkRunning',
                    type: 'POST',
                    headers:{
                        'X-CSRFToken': '{{csrf_token}}'
                         },
                    timeout: 3000,
                    success: function(data){ //data == run_state
						if(data == 2){ // not running
							$('.connection'+piNum).css('background-color','#6eff3d');
						}
                        else if(data == 1){
                            $('.connection'+piNum).css('background-color','#0ea800');
                        }
                    },
                    error: function(){
                        // error - change connection state to red
                        $('.connection'+piNum).css('background-color','#ff2b2b');
                        console.log("checkRunning Error occured!!");
                    }
                })
            }
            
            for(piNum=1; piNum <= PI; piNum++)
            {
                changeColor(piNum);
            }
            
        }


//*********** summary.html, beforeResult.html ***********//
function updateCycle(data){ //+home_ajax.js
            if(data.length>1){
                let last = data[0].fields.run_time;
                let before = data[1].fields.run_time;
                let cycleHtml = document.getElementById('dataCycle');
                cycleHtml.innerHTML = `????????????: ??? ${last-before}???`
            }
        }

function xAxisLabel(time){
                var hours = Math.floor(time / 3600);
                time = time - hours * 3600;
                var minutes = Math.floor(time/60);
                var seconds = time - minutes * 60;
                
                if(hours<10)
                    hours = '0' + hours;
                if(minutes<10)
                    minutes = '0' + minutes;
                if(seconds<10)
                    seconds = '0' + seconds;

                if(hours>0)
                    str = hours + "?????? " + minutes+ "??? ";
                else
                    if(minutes>0)
                        str = minutes+ "??? " + seconds + "???";
                    else
                        str = seconds + "???";
                
                return str;
        }

//************** home.html, result.html ******************//
function csv_name(piNum, date){
            let defaultName = `No.${piNum}_${date}`
            var userInput = prompt("????????? ????????? csv????????? ????????? ??????????????????.\n(????????? ????????? ???????????? ??????????????? ?????????.)", defaultName);
            if(userInput == null){
                alert("?????????????????????.");
            } else{
                alert("??????????????? ???????????????.");
                location.href="/th_csv/"+userInput;
            }
        }
