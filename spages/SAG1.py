# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def PebbleRateChart(mt, pb_rate_transient, pb_rate_ma, pb_rate_linear):
    # Add plot
    fig = go.Figure()
    # 绘制散点图
    fig.add_trace(go.Scatter(x = mt, y = pb_rate_transient, 
                            name = 'Transient Pebble Rate', mode = 'lines', opacity = .1, 
                            line = dict(color = 'black') 
                            ))
    # 绘制移动平均线
    fig.add_trace(go.Scatter(x = mt, y = pb_rate_ma, 
                             name = 'Moving Average Pebble Rate', mode = 'lines', 
                             line = dict(color='royalblue', width = 2) 
                             ))
    # 绘制线性拟合曲线
    fig.add_trace(
        go.Scatter(x = mt, y = pb_rate_linear, 
                   name = 'Linear Regression', mode = 'lines',  
                   line = dict(color = 'black', width = 3) 
                   ))
    fig.update_yaxes(title_text = "Pebble Rate (t/h)")
    fig.update_xaxes(title_text = "Cumulative MT Milled")

    # Update axis format
    fig.update_yaxes(range = [100, 650])

    # Update figure format
    fig.update_layout(
        margin = dict(l = 1, r = 1, t = 50, b = 50),
        template="simple_white"
    )

    fig.update_layout(
        showlegend = True,
        font = dict(
            size = 12,
            color = "Black"
        )
    )

    fig.update_layout(legend = dict(
            yanchor = "top",
            y = 0.99,
            xanchor = "left",
            x = 0.03
        )
    )

    return fig


def read_xlsx(path):
    df = pd.read_excel(path, header = None)
    df = df.fillna('')
    df.index = ['' for _ in range(len(df))]  # 动态设置索引长度
    return df


def GrateWearChart(mt, outer_grate, outer_pebble, mid_grate):
    # Add plot
    fig = go.Figure()
    # 绘制散点图
    fig.add_trace(go.Scatter(x = mt, y = outer_grate, 
                            name = '22mm Outer Grate:  OA = 23,082 MT + 147,474 [mm²]', mode = 'lines', 
                            line = dict(color = 'orange', width = 3) 
                            ))
    # 绘制移动平均线
    fig.add_trace(go.Scatter(x = mt, y = outer_pebble, 
                             name = '65mm Outer Grate:  OA = 17,376 MT + 187,877 [mm²]', mode = 'lines', 
                             line = dict(color='royalblue', width = 3) 
                             ))
    # 绘制线性拟合曲线
    fig.add_trace(
        go.Scatter(x = mt, y = mid_grate, 
                   name = '22mm Mid Grate:  OA = 14,679 MT + 128,530 [mm²]', mode = 'lines',  
                   line = dict(color = 'gray', width = 3) 
                   ))
    fig.update_yaxes(title_text = "Open Area - mm²")
    fig.update_xaxes(title_text = "Cumulative MT Milled")

    # Update axis format
    #fig.update_yaxes(range = [100, 650])

    # Update figure format
    fig.update_layout(
        margin = dict(l = 1, r = 1, t = 50, b = 50),
        template="simple_white"
    )

    fig.update_layout(
        showlegend = True,
        font = dict(
            size = 12,
            color = "Black"
        )
    )

    fig.update_layout(legend = dict(
            yanchor = "top",
            y = 0.99,
            xanchor = "left",
            x = 0.03
        )
    )

    return fig



def app():
    ### User Input ###
    sensor1code = "Row2-FE-Lifter"
    sensor2code = "Row3-Mid-Lifter"
    sensor3code = "Row4-FE-Lifter"
    sensor4code = "Row5-Mid-Lifter"
    ### End of User Input ###
    
    
    ###################      Start of App     ###############################
    st.subheader("SAG Mill #1 Wear Sensor Installation", divider = 'rainbow')
    # st.subheader("", divider='red')


    ############################## Section 1 ################################

    st.markdown("1. Wear Sensor Installation Details")

    cl1, cl2 = st.columns([1, 1], gap="medium", vertical_alignment="center")
    with cl1:
        st.image("sagMap.png", use_column_width =True)
    with cl2:
        st.image("shell.png", use_column_width =True)
        st.markdown("The following sensors were installed: ")
        st.success("✅ " + sensor1code)
        st.success("✅ " + sensor2code)
        st.success("✅ " + sensor3code)
        st.success("✅ " + sensor4code)
        
    st.markdown("###")

    ############################## Section 2 ################################
    st.markdown("2. Wear Sensor Live Status")
    totalH = 400
    cl11, cl12 = st.columns(2)
    with cl11:
        st.caption("Latest Reading at: " + " 11:35:20 02-12-2024")
        sensor11 = 400
        dff11 = sensor11-totalH
        cl11.metric(label = sensor1code + " Sensor Reading", value = str(sensor11) + "mm", delta = dff11)
        
        st.caption("Latest Reading at: " + " 11:35:20 02-12-2024")
        sensor12 = 400
        dff12 = sensor12-totalH
        cl11.metric(label = sensor2code + " Sensor Reading", value = str(sensor12) + "mm", delta = dff12)
    with cl12:
        st.caption("Latest Reading at: " + " 11:35:20 02-12-2024")
        sensor21 = 400
        dff21 = sensor21-totalH
        cl12.metric(label = sensor3code + " Sensor Reading", value = str(sensor21) + "mm", delta = dff21)
        
        st.caption("Latest Reading at: " + " 11:35:20 02-12-2024")
        sensor22 = 400
        dff22 = sensor22-totalH
        cl12.metric(label = sensor4code + " Sensor Reading", value = str(sensor22) + "mm", delta = dff22)


################################## plot data ###############################################
    st.markdown("###")
    st.markdown("3. Wear Sensor Plots")
    
    # Specify the file path
    file_path = 'sensorReading.xlsx'

    # Specify the sheet name
    sheet_name = 'Sheet1'

    # Specify the column names as a list
    column_names = ['DateTime', 'P6051', 'P6052']

    # Import via Pandas
    # Read the Excel sheet with specified range and column names
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None,
                    skiprows=1)

    # Assign column names to DataFrame
    df.columns = column_names

    # covert date time format
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    # Plot in plotly
    # Add the second trace with the secondary y-axis
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['DateTime'], y=df['P6051'], name='P6051',  mode='lines+markers') )
    fig.add_trace(go.Scatter(x=df['DateTime'], y=df['P6052'], name='P6052',  mode='lines+markers') )

    # Update axis format
    fig.update_yaxes(title_text="Sensor Thickness - mm")
    fig.update_xaxes(title_text="Date and Time")
    fig.update_yaxes(range=[0, 450])

    # Update figure format
    fig.update_layout(
        margin=dict(l=1, r=1, t=30, b=1),
        template="seaborn"
    )

    fig.update_layout(
        showlegend=True,
        font=dict(
            family="Ubuntu, regular",
            size=12,
            color="Black"
        )
    )

    fig.update_layout(legend=dict(
            yanchor="top",
            y=0.3,
            xanchor="left",
            x=0.03
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    ################################## 3D Model ###############################################
    #st.markdown("###")
    #st.markdown("4. 3D Liner Model")
    #iframeLINK = "https://kitware.github.io/glance/app/?name=millShellWearMonitoring.vtkjs&url=https://webify-1306024390.cos.ap-shanghai.myqcloud.com/millShellWearMonitoring.vtkjs"
    #local_pvModel(iframeLINK)
    #pvOBJ = read_file_from_url(iframeLINK)
    #components.html(pvOBJ, height=1000)
    
    #HtmlFile_tSS1 = open("hydrocyclone.html", 'r', encoding='utf-8').read()
    #components.html(HtmlFile_tSS1, height=1000)

    #st.write(
    #        f'<iframe src=' + iframeLINK + ' height = "800" width = "100%"></iframe>',
    #        unsafe_allow_html=True,
    #)
    ############################## Section Display Dataframe ################################
    st.markdown("###")
    st.markdown("4. Wear Sensor Database")
    file_path1 = 'sensorReading.xlsx'
    # Specify the sheet name
    sheet_name1 = 'Sheet1'
    
    df1 = pd.read_excel(file_path1, sheet_name=sheet_name1, header=None, skiprows= 1)

    # Specify the column names as a list
    column_names1 = ['Datetime', 'P6051 Reading', 'P6052 Reading']

    # Assign column names to DataFrame
    df1.columns = column_names1

    # Display Table
    st.dataframe(df1, hide_index=True, use_container_width=True)
