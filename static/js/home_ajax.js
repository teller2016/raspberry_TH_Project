
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
                                    
                                updateCycle(data);
                                    
                                $('#table_data').empty();
                                
                                let state_run_id = $('#state_id').html();
                                let table_head_html =
                                    "<tr class='tr-bar2'>" +
                                    "<th><font>NO.</font></th>" +
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

            
