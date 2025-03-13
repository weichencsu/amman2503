# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from io import BytesIO

def process_sensor_data(file_path):
 
    # 读取Excel文件中的所有Sheet
    xls = pd.ExcelFile(file_path)
    sheets_dict = pd.read_excel(xls, sheet_name=None)
    
    # 初始化结果列表
    results = []
    
    # 遍历每个Sheet进行处理
    for sheet_name, df in sheets_dict.items():
        # 检查是否存在需要过滤的列
        if '总长_DEC' in df.columns:
            # 过滤掉总长_DEC等于12337的行
            filtered_df = df[df['总长_DEC'] != 12337]
        else:
            # 如果列不存在，保留原数据（或根据需求处理）
            filtered_df = df
        
        # 检查过滤后的DataFrame是否为空
        if filtered_df.empty:
            # 记录空数据的情况
            results.append({
                'sensorName': sheet_name,
                'latestTime': None,
                'totalLength': None,
                'actualLength': None
            })
        else:
            # 获取最后一行数据
            last_row = filtered_df.iloc[-1]
            # 提取所需字段，使用.get()避免KeyError
            latest_time = last_row.get('time')
            total_length = last_row.get('总长_DEC')
            actual_length = last_row.get('实际长度_DEC')
            
            results.append({
                'sensorName': sheet_name,
                'latestTime': latest_time,
                'totalLength': total_length,
                'actualLength': actual_length
            })
    
    # 转换结果列表为DataFrame
    result_df = pd.DataFrame(results)
    
    return result_df


def plot_sensor_data(file_path):
    # 读取所有sheet
    sheets = pd.read_excel(file_path, sheet_name=None)
    
    # 创建图形对象
    fig = go.Figure()
    
    # 处理每个sheet
    for sheet_name, df in sheets.items():
        # 过滤数据
        filtered_df = df[df['总长_DEC'] != 12337]
        
        # 转换时间格式
        filtered_df['time'] = pd.to_datetime(filtered_df['time'])
        
        # 添加轨迹到图形
        fig.add_trace(go.Scatter(
            x=filtered_df['time'],
            y=filtered_df['实际长度_DEC'],
            mode='lines+markers',
            name=sheet_name
        ))
        
    # Update axis format
    fig.update_yaxes(title_text="Sensor Length - mm")
    fig.update_xaxes(title_text="Date and Time")
    fig.update_yaxes(range=[0, 450])

    # Update figure format
    fig.update_layout(
        margin=dict(l=1, r=1, t=30, b=1),
        template="seaborn"
    )
    
    # 设置布局
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.1,
            xanchor="right",
            x=1
        )
    )
    
    return fig


def app():
    ######################## User Input #######################
    ### 读取设备名称的传感器数据库结果，并传递至Streamlit 前端进行显示
    databasedPath = './sensorCSV/SAG2_sensor_data_with_decimal_filtered_updated02.xlsx'

    sensorResults = process_sensor_data(databasedPath)
    ##  "sensorName  latestTime  totalLength  actualLength" ###
    ######################## End of User Input ################




    ###################      Start of App     ###############################
    st.subheader("SAG Mill #2 Wear Sensor Installation", divider = 'rainbow')
    # st.subheader("", divider='red')


    ############################## Section 1 ################################

    st.markdown("1. Wear Sensor Installation Details")

    cl1, cl2 = st.columns([1, 1], gap="medium", vertical_alignment="center")
    with cl1:
        st.image("sagMap.png", use_container_width = True)
    with cl2:
        st.image("shell.png", use_container_width = True)
        st.markdown("The following sensors were installed: ")
        for snm in sensorResults["sensorName"]:
            st.success("✅ " + snm)
        
    st.markdown("###")

    ############################## Section 2 ################################n   
    st.markdown("2. Wear Sensor Live Status")
    with st.container():
        for row in sensorResults.itertuples():
            # 检查 totalLength 是否非空（非 NaN）
            if pd.notna(row.totalLength):
                st.caption("Latest Reading at: " + str(row.latestTime))
                st.metric(label = ":material/Sensors: " +  row.sensorName + " Sensor Reading", value = str(row.actualLength) + "mm", delta = row.actualLength - row.totalLength, border=True)
            else:
                st.metric(label = ":material/Sensors: " +  row.sensorName + " Sensor Reading", value = "No Wear Data Received", border=True)
            #st.markdown("###")
    st.markdown("###")
################################## plot data ###############################################
    st.markdown("3. Wear Sensor Plots")
    
    # Specify the file path
    fig = plot_sensor_data(databasedPath)
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

    # 定义新的列名
    NEW_COLUMNS = [
        "Datetime", 
        "TotalLength(HEX)", 
        "SensorID(HEX)", 
        "CurrentLength(HEX)", 
        "CheckCode(HEX)", 
        "TotalLength(mm)", 
        "SensorID", 
        "CurrentLength(mm)", 
        "CheckCode"
    ]

    try:
        # 读取所有工作表（返回字典格式：{sheet_name: DataFrame}）
        with pd.ExcelFile(databasedPath) as excel_file:
            # 创建内存缓冲区
            output = BytesIO()
            
            # 使用ExcelWriter将处理后的数据写入内存
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # 遍历每个工作表
                for sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(excel_file, sheet_name=sheet_name)
                    
                    # 检查列数是否匹配
                    if len(df.columns) != len(NEW_COLUMNS):
                        raise ValueError(f"工作表 '{sheet_name}' 列数不匹配："
                                        f"需要 {len(NEW_COLUMNS)} 列，实际 {len(df.columns)} 列")
                    
                    # 重命名列
                    df.columns = NEW_COLUMNS
                    
                    # 写入新的Excel文件
                    df.to_excel(
                        writer,
                        sheet_name=sheet_name,
                        index=False
                    )
            
            # 创建下载按钮
            st.download_button(
                label=":material/Download:  Download Database",
                data=output.getvalue(),
                file_name='SAG2_sensor_data.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width = True
            )
            
            st.success("Sensor database available. Please click button to download!!!")    



    except FileNotFoundError:
        st.error(f"文件未找到：{databasedPath}")
        st.info("请确认文件路径和权限")
    except Exception as e:
        st.error(f"发生错误：{str(e)}")
