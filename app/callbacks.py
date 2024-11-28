import io
import base64
import pandas as pd
import dash
from dash import html, Input, Output
import plotly.express as px


def register_callbacks(app):
    # Функция для парсинга загруженного файла
    def parse_contents(contents):
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        return pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    # Callback для загрузки данных
    @app.callback(
        Output('output-data-upload', 'children'),
        Output('page-dropdown', 'options'),
        Output('key-metrics', 'children'),
        Output('visits-graph', 'figure'),
        Input('upload-data', 'contents')
    )
    def update_output(contents):
        if contents is not None:
            df = parse_contents(contents)
            options = [{'label': page, 'value': page} for page in df['page'].unique()]
            
            # Получаем имя файла и его размер
            file_size = len(base64.b64decode(contents.split(',')[1])) 

            # Ключевые показатели
            total_visits = df['visits'].sum()
            total_views = df['views'].sum()
            total_time = df['time'].sum()
            
            key_metrics = html.Div([
                html.H4(f"Общее количество посещений: {total_visits}"),
                html.H4(f"Общее количество просмотров: {total_views}"),
                html.H4(f"Общее время на странице: {total_time} часов")
            ])
            
            # График посещений
            fig_visits = px.bar(df, x='date', y='visits', title='Посещения по дням')

            return f"Размер файла: {file_size} байт", options, key_metrics, fig_visits
        
        return "Загрузите файл.", [], "", {}

    # Callback для обновления графиков на основе выбора страницы и диапазона дат
    @app.callback(
        Output('views-graph', 'figure'),
        Output('time-graph', 'figure'),
        Input('page-dropdown', 'value'),
        Input('upload-data', 'contents'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')
    )
    def update_graphs(selected_page, contents, start_date, end_date):
        if contents is not None:
            df = parse_contents(contents)

            # Фильтрация по диапазону дат
            if start_date and end_date:
                df['date'] = pd.to_datetime(df['date'])
                df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            
            if selected_page:
                filtered_df = df[df['page'] == selected_page]
                
                fig_views = px.line(filtered_df, x='date', y='views', title=f'Просмотры для {selected_page}')
                fig_time = px.line(filtered_df, x='date', y='time', title=f'Время на странице для {selected_page}')
                
                return fig_views, fig_time

        return {}, {}

    # Callback для управления отображением графиков
    @app.callback(
        Output('views-graph', 'style'),
        Output('time-graph', 'style'),
        Input('show-graphs', 'value')
    )
    def toggle_graphs(show_graphs):
        if show_graphs == 'show':
            return {'display': 'block'}, {'display': 'block'}
        else:
            return {'display': 'none'}, {'display': 'none'}

    # Callback для сброса фильтров
    @app.callback(
        Output('page-dropdown', 'value'),
        Output('date-picker-range', 'start_date'),
        Output('date-picker-range', 'end_date'),
        Input('reset-button', 'n_clicks')
    )
    def reset_filters(n_clicks):
        if n_clicks is not None:
            return None, None, None  # Сброс значений

        return dash.no_update, dash.no_update, dash.no_update
