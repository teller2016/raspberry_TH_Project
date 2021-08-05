        function start_check(){
            var result = confirm("정말로 시작하시겠습니까? 시작시 이전의 데이터는 모두 백업됩니다.");
            if(result){

                let currentDate = getDate();
                let currentTime = getTime();


                let dateAndTime = currentDate + " " + currentTime;
                //dateAndTime: ex> "2021-07-06 17:13:00"
                
                let second = document.getElementById('cycle').value;
                
                location.href="/restart/" + dateAndTime + "/" + second;
                return true;

            }
             return false;
        }
        
        
        function end_check(){
            var result = confirm("정말로 종료하시겠습니까?");
            if(result){
                location.href="/end";
                return true;
            }
             return false;
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
                            timeout: 3000,
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



function getThData(){
                
                $.ajax({
                            url: '/getThData/',
                            type: 'POST',
                            headers:{
                                'X-CSRFToken': '{{csrf_token}}'
                                },
                            success:function(data){
                                if(data.length==0)
                                    return;
                                    
                                let lastRunId = $(`#curRunId`).text();
                                let lastHumidity = $(`#curHumidity`).text();
                  
                                // if Data is new - change Data and Color
                                if(lastRunId != data[0].fields.run_id){
                                    //add data to the table
                                    $('#curHumidity').html(data[0].fields.humidity);
                                    $('#curTemperature').html(data[0].fields.temperature);
                                    $('#curRunId').html(data[0].fields.run_id);
                                    
                                    if(lastHumidity > data[0].fields.humidity)
                                        d3.selectAll(`#curHumidity, #curTemperature`).style('color','blue');
                                    else if(lastHumidity == data[0].fields.humidity || lastHumidity == '-')
                                        d3.selectAll(`#curHumidity, #curTemperature`).style('color','gray');
                                    else
                                        d3.selectAll(`#curHumidity, #curTemperature`).style('color','red');
                                    
                                    d3.selectAll(`#curHumidity, #curTemperature`).transition().style('color','black').duration(3000);
                                }

                                
                                 $('#table_data').empty();
                                    
                                //console.log($('#state_id').html());
                                let state_run_id = $('#state_id').html();
                                let table_head_html =
                                    "<tr class='tr-bar2'>" +
                                    "<th><font>no.</font></th>" +
                                    "<th><font>경과 시간</font></th>" +
                                    "<th><font>습도(%)</font></th>" +
                                    "<th><font>온도(°C)</font></th>" +
                                    "<th><font>측정 시간</font></th>" +
                                    "</tr>"
                                $('#table_data').append( table_head_html )
                                
                                $.each(data, function(key, value){
                                
                                    let run_id = value.fields.run_id;
                                    let run_time_str = value.fields.run_time_str;
                                    let humidity = value.fields.humidity;
                                    let temperature = value.fields.temperature;
                                    let run_time_date = value.fields.run_time_date;
                                    
                                    let tr_html = '';
                                    
                                    if( run_id == state_run_id)
                                        tr_html = "<tr class='peak'>";
                                    else
                                        tr_html = "<tr>";
                                   
                                        
                                    $('#table_data').append( tr_html +
                                        "<td><font>" + run_id + "</font></td>" +
                                        "<td><font>" + run_time_str + "</font></td>" +
                                        "<td><font>" + humidity + "</font></td>" +
                                        "<td><font>" + temperature + "</font></td>" +
                                        "<td><font>" + getHMS(run_time_date) + "</font></td>" +
                                        "</tr>"
                                    );
                                
                                });

                                
                            },
                            error: function(){
                                console.log('Ajax getThData Error!!');
                            }
                        });
            
            }
            
function getThState(){
                
                $.ajax({
                            url: '/getThState/',
                            type: 'POST',
                            headers:{
                                'X-CSRFToken': '{{csrf_token}}'
                                },
                            success:function(data){
                                
                                let lastRunTime = $(`#maxRunTime`).text();
                                
                                $('#maxHumidity').html(data[0].fields.max_hum);
                                $('#maxRunTime').html(data[0].fields.run_time_str);
                                
                                if(lastRunTime != data[0].fields.run_time_str){
                                    if(lastRunTime == '-')
                                        d3.selectAll(`#maxHumidity, #maxRunTime`).style('color','gray');
                                    else
                                        d3.selectAll(`#maxHumidity, #maxRunTime`).style('color','red');
                                        
                                    d3.selectAll(`#maxHumidity, #maxRunTime`).transition().style('color','black').duration(3000);
                                }

                            },
                            error: function(){
                                console.log('Ajax getThState Error!!');
                            }
                        });
            
            }
 
function getAllThData(){
                $.ajax({
                    url: '/getAllThData/',
                    type: 'POST',
                    headers:{
                        'X-CSRFToken': '{{csrf_token}}'
                         },
                    success: function(data){
                        updateCycle(1, data);
                        update(data);

                    },
                    error: function(){
                        console.log("getAllThData Error occured!!");
                    }
                })
            }
            
function update(data) {
                                         
                var dataList = new Array();
                var dataList2 = new Array();
                                        
                let reversedData = data.reverse(); //reverse data in correct order;
                $.each(reversedData, function(key, value){
                    
                    var graph = new Object();
                    graph.x = value.fields.run_time;
                    graph.y = value.fields.humidity;
                    graph.series = 0;
                    dataList.push(graph);
                                            
                    var graph2 = new Object();
                    graph2.x = value.fields.run_time;
                    graph2.y = value.fields.temperature;
                    graph2.series = 1;
                    dataList2.push(graph2);
                                            
                    })
                var th_data = [
                    {
                        "key": "습도(%)",
                        "color": "#00ace6",
                        "values": dataList
                        },
                {
                        "key": "온도(°C)",
                        "color": "#FF4765",
                        "values": dataList2
                        }
                ]

                d3.select('#chart svg')
                .datum(th_data)
                .call(chart);

                nv.utils.windowResize(chart.update);
        
                return chart;
                }
