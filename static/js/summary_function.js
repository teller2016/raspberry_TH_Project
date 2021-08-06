function start_pi(){ //start selected pi
            var result = confirm("측정을 시작하시겠습니까? 시작시 이전의 데이터는 모두 백업됩니다.");
            if(result){
                
                
                let checkedList = ['1'];// pi 1 is necessary
                //get list of checked pi
                $("input:checkbox[name=checkbox_pi]:checked").each(function(){
					checkedList.push($(this).val());
				});
            
                let currentDate = getDate();
                let currentTime = getTime();
                
                let dateAndTime = currentDate + " " + currentTime;
                //dateAndTime: ex> "2021-07-06 17:13:00"

                let second = document.getElementById('cycle').value;
                
                //start all checked pi
                
                requestPi_start(0,checkedList, dateAndTime, second);
                
                return true;
                //checkedList.forEach( piNum => requestPi_start(piNum, dateAndTime, second));

                return true;
            }
            
            
            return false;
        }
        
        function requestPi_start(index, checkedList, time, second){
			//when last one from the pi list started, refresh page
            if(index > checkedList.length - 1){
                 location.reload();
                 return;
            }
            $.ajax({
                        url: 'http://192.168.243.' + checkedList[index] +':8000/restartAll/'+ time + '/' + second,
                        type: 'POST',
                        headers:{
                            'X-CSRFToken': '{{csrf_token}}',
                            
                            },
                        timeout: 3000,
                        success:function(data){
                            requestPi_start(index+1, checkedList, time, second);
                        },
                        error: function(){
                            console.log(`Ajax requestPi_start-${index+1} Error!!`);
                            alert(`No.${checkedList[index]} failed to start!!!\n***Please Restart or Turn On Manually***`);
                            requestPi_start(index+1, checkedList, time, second);
                        }
                });
            
            }
        
        
        function end_all(){ //end all pi
            var result = confirm("전체 종료 하시겠습니까?");
            if(result){
                
                requestPi_end(1);

                return true;
            }
            return false;
        }
        
        function requestPi_end(pi_num){
            if(pi_num > PI){
                location.reload();
                return;
            }
            
                $.ajax({
                            url: 'http://192.168.243.' + pi_num +':8000/endAll',
                            type: 'POST',
                            headers:{
                                'X-CSRFToken': '{{csrf_token}}',
                                },
                            timeout: 4000,
                            success:function(data){
                                    
                                console.log(data);
                                requestPi_end(pi_num+1);
                                
                            },
                            error: function(){
                                console.log(`Ajax requestPi_end-${pi_num} Error!!`);
                                alert(`No.${pi_num} failed to end!!!\n***Please Turn Off Manually***`);
                                requestPi_end(pi_num+1);
                            }
                        });
            
            }

function checkRunning(){ //check the running state and change color of the box
            
            function changeColor(piNum){
                $.ajax({
                    url: 'http://192.168.243.' + piNum +':8000/checkRunning',
                    type: 'POST',
                    headers:{
                        'X-CSRFToken': '{{csrf_token}}'
                         },
                    timeout: 3000,
                    success: function(data){ //data == run_state
						if(data == 2){ // not running
							$('.connection'+piNum).css('border-bottom-color','#6eff3d');
						}
                        else if(data == 1){
                            $('.connection'+piNum).css('border-bottom-color','#0ea800');
                        }
                    },
                    error: function(){
                        // error - change connection state to red
                        $('.connection'+piNum).css('border-bottom-color','#ff2b2b');
                        console.log("checkRunning Error occured!!");
                    }
                })
            }
            
            for(piNum=1; piNum <= PI; piNum++)
            {
                changeColor(piNum);
            }
            
        }

function hideElement(piNum){// hide data that is not running
			$.ajax({
                    url: 'http://192.168.243.' + piNum +':8000/checkRunning',
                    type: 'POST',
                    headers:{
                        'X-CSRFToken': '{{csrf_token}}'
                         },
                    timeout: 3000,
                    success: function(data){ //data == run_state
						if(data == 2){
							
                            $('#summary'+piNum).hide();
						}
                    },
                    error: function(){
                        console.log("hideElement Error occured!!");
                    }
                })
		}   

function getAllThState(piNum, run_state){
            
            if(piNum>PI)
                return;
            
            $.ajax({
                        url: 'http://192.168.243.'+piNum+':8000/getAllThState/'+ run_state,
                        type: 'POST',
                        headers:{
                            'X-CSRFToken': '{{csrf_token}}'
                            },
                        timeout: 3000,
                        success:function(data){
                            //console.log(data);
                            $('#error-pi'+piNum).remove();
                            
                            if(data == 'None'){
                                //console.log(`PI No.${piNum} not running`);
                            }
                            else{
                                let lastRunTime = $(`#maxRunTime${piNum}`).text();
                                
                                $('#maxHumidity'+piNum).html(data[0].fields.max_hum);
                                $('#maxRunTime'+piNum).html(data[0].fields.run_time_str);
                                
                                
                                // if Data is changed - change color
                                if(lastRunTime != data[0].fields.run_time_str){ 
									if(lastRunTime == '-')
										d3.selectAll(`#maxHumidity${piNum}, #maxRunTime${piNum}`).style('color','gray');
									else
										d3.selectAll(`#maxHumidity${piNum}, #maxRunTime${piNum}`).style('color','red');
                                    d3.selectAll(`#maxHumidity${piNum}, #maxRunTime${piNum}`).transition().style('color','black').duration(3000);
                                }
                                
                            
                            }
                            
                            getAllThState(piNum+1, run_state);
                            
                        },
                        error: function(){
                            console.log(`PI No.${piNum} Ajax getThState Error!!`);

                            // show error when connection is lost
                            if($('#error-pi'+piNum).length==0){
                                $('#summary-pi'+piNum).prepend(
                                "<strong id='error-pi"+piNum+ "'" + " style='color:red; font-size:25px;'>Connection Lost!</strong>"
                                )
                            }
                            
                            getAllThState(piNum+1, run_state);
                        }
                    });
            
        }

function getLastThData(piNum, run_state){
          
                if(piNum>PI){
                    d3.select('#chart svg')
                        .datum(th_data)
                        .call(chart); //draw chart when getting data is done

                    nv.utils.windowResize(chart.update);
                    
                    th_data=[];
                    return;
                }
                
                $.ajax({
                            url: 'http://192.168.243.'+piNum+':8000/getLastThData/'+ run_state,
                            type: 'POST',
                            headers:{
                                'X-CSRFToken': '{{csrf_token}}'
                                },
                            timeout: 3000,
                            success:function(data){
                                
                                //show data on table
                                if(data.length==0){
                                    //console.log(`PI No.${piNum} no data`);
                                }
                                else if(data == "None"){
                                    //console.log(`PI No.${piNum} not running`);
                                }
                                else{
                                    //show cycle
                                    updateCycle(piNum, data);

                                    let lastRunId = $(`#curRunId${piNum}`).text();

                                    // if Data is new - change Data and Color
                                    if(lastRunId != data[0].fields.run_id){ 
                                        //add data to the table
                                        $('#curHumidity'+piNum).html(data[0].fields.humidity);
                                        $('#curTemperature'+piNum).html(data[0].fields.temperature);
                                        $('#curRunId'+piNum).html(data[0].fields.run_id);
                                        
                                        d3.selectAll(`#curHumidity${piNum}, #curTemperature${piNum}`).style('color','gray');
                                        d3.selectAll(`#curHumidity${piNum}, #curTemperature${piNum}`).transition().style('color','black').duration(3000);
                                    }
                                    
                                    //add data on graph
                                    updateGraph(data, piNum);
                                    
                                }
                                
                                
                                getLastThData(piNum+1, run_state);
                                
                            },
                            error: function(){
                                console.log(`PI No.${piNum} Ajax getLastThData Error!!`);
                                getLastThData(piNum+1, run_state);
                            }
                        });
            
            }

function getLastTwoThData(piNum){
                
                if(piNum>PI){
                    moveData(); // update th_data by th_data_save
                    
                    d3.select('#chart svg')
                        .datum(th_data)
                        .call(chart); //draw chart when getting data is done

                    nv.utils.windowResize(chart.update);
                    
                    th_data=[];
                    return;
                }
                
                $.ajax({
                            url: 'http://192.168.243.'+piNum+':8000/getLastTwoThData',
                            type: 'POST',
                            headers:{
                                'X-CSRFToken': '{{csrf_token}}'
                                },
                            timeout: 3000,
                            success:function(data){
                                
                                //show data on table
                                if(data.length==0){
                                    //console.log(`PI No.${piNum} no data`);
                                }
                                else if(data == "None"){
                                    //console.log(`PI No.${piNum} not running`);
                                }
                                else{
                                    
                                    //show cycle
                                    updateCycle(piNum, data);
                                    
                                    let lastRunId = $(`#curRunId${piNum}`).text();
                                    let lastHumidity = $(`#curHumidity${piNum}`).text();

                                    // if Data is new - change Data and Color
                                    if(lastRunId != data[0].fields.run_id){ 
                                        //add data to the table
                                        $('#curHumidity'+piNum).html(data[0].fields.humidity);
                                        $('#curTemperature'+piNum).html(data[0].fields.temperature);
                                        $('#curRunId'+piNum).html(data[0].fields.run_id);
                                        
                                        if(lastHumidity > data[0].fields.humidity)
											d3.selectAll(`#curHumidity${piNum}, #curTemperature${piNum}`).style('color','blue');
										else if(lastHumidity == data[0].fields.humidity)
											d3.selectAll(`#curHumidity${piNum}, #curTemperature${piNum}`).style('color','gray');
										else
											d3.selectAll(`#curHumidity${piNum}, #curTemperature${piNum}`).style('color','red');
												
                                        d3.selectAll(`#curHumidity${piNum}, #curTemperature${piNum}`).transition().style('color','black').duration(3000);
                                        
                                        //show data on graph
                                        pushDataToGraph(data, piNum);
                                    }
                                    
                                    
                                    
                                }
                                
                                
                                getLastTwoThData(piNum+1);
                                
                            },
                            error: function(){
                                console.log(`PI No.${piNum} Ajax getLastTwoThData Error!!`);
                                getLastTwoThData(piNum+1);
                            }
                        });
            
            }

//**************** GRAPH Function
function updateGraph(data, piNum){
            
            var dataList = new Array();
            
            let reversedData = data.reverse();
            
            $.each(reversedData, function(key, value){
                var graph = new Object();
                graph.x = value.fields.run_time;
                graph.y = value.fields.humidity;
                graph.series = piNum;  
                                          
                dataList.push(graph);                            
                })
             
            
            let graphData = {
                "key": `PI-${piNum} 습도(%)`,
                "color": fixedColor[piNum],
                "values": dataList
            }
            
            th_data.push(graphData);
            th_data_save[piNum] = graphData;
            

            return chart;
                
            
        }

function pushDataToGraph(data, piNum){ // add newest data to th_data_save
            
            if(th_data_save[piNum] == undefined){

                let graphData = {
                    "key": `PI-${piNum} 습도(%)`,
                    "color": fixedColor[piNum],
                    "values": []
                }
                th_data_save[piNum] = graphData;
            }
            
            let values = th_data_save[piNum].values;

            values.push({
               x: data[0].fields.run_time,
               y: data[0].fields.humidity,
               series: piNum 
            });
            return;
        }

function moveData(){ // move 'th_data_save' datas to 'th_data' (( th_data is empty ))
            for(const piNum in th_data_save){
                th_data.push(th_data_save[piNum]);
            }
        }
