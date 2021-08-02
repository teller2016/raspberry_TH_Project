
//NUMBER OF PI
		const PI = 3


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

function setCycle(){
            let cycle = document.getElementById('cycle');
                  
            let cycleLabel = document.getElementById('cycleLabel');
            cycleLabel.innerHTML = cycle.value+'초';
                           
                  }


//*********** summary.html, beforeResult.html ***********//
function updateCycle(piNum, data){
            if(piNum==1 && data.length>1){
                let last = data[0].fields.run_time;
                let before = data[1].fields.run_time;
                let cycleHtml = document.getElementById('dataCycle');
                cycleHtml.innerHTML = `측정주기: 약 ${last-before}초`
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
                    str = hours + "시간 " + minutes+ "분 ";
                else
                    if(minutes>0)
                        str = minutes+ "분 " + seconds + "초";
                    else
                        str = seconds + "초";
                
                return str;
        }

//************** home.html, result.html ******************//
function csv_name(){
            var userInput = prompt("저장을 원하는 csv파일의 이름을 입력해주세요.\n(이름은 영어와 숫자로만 구성되어야 합니다.)")
            if(userInput == null){
                alert("취소되었습니다.");
            } else{
                alert("다운로드를 시작합니다.");
                location.href="/th_csv/"+userInput;
            }
        }
