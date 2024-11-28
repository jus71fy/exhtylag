from dash import dcc, html

# Макет приложения с добавленными стилями
def create_layout():
    return html.Div(children=[
        # Заголовок дашборда
        html.H1('Анализ данных о посещении сайта', className='dashboard-title'),
        
        # Описание дашборда
        html.Div(
            'Этот дашборд позволяет загружать данные, выбирать диапазон дат и отображать различные графики для анализа посещаемости и взаимодействия с контентом.',
            className='dashboard-description'
        ),
        
        # Основной контент
        html.Div(className='upload-container', children=[
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Перетащите или ',
                    html.A('Выберите Файл')
                ]),
                className='upload-box',
                multiple=False
            ),
            html.Div(id='output-data-upload'),

            dcc.Loading(id='loading-container', children=[
                html.Div([
                    html.H3('Фильтры', className='filter-title'),

                    # Выбор диапазона дат
                    dcc.DatePickerRange(
                        id='date-picker-range',
                        className='date-picker',
                        display_format='YYYY-MM-DD'
                    ),

                    # Переключатель для отображения графиков
                    dcc.RadioItems(
                        id='show-graphs',
                        options=[
                            {'label': 'Показать графики', 'value': 'show'},
                            {'label': 'Скрыть графики', 'value': 'hide'}
                        ],
                        value='show',
                        labelStyle={'display': 'inline-block', 'margin-right': '20px'},
                        className='radio-items'
                    )
                ], className='filter-block'),

                # Кнопка сброса фильтров
                html.Button('Сбросить фильтры', id='reset-button', className='button-primary'),

                # График посещений
                dcc.Graph(id='visits-graph'),

                # Дропдаун для выбора страницы
                dcc.Dropdown(id='page-dropdown', options=[], placeholder="Выберите страницу"),

                # Ключевые показатели
                html.Div(id='key-metrics', className='key-metrics'),

                # Графики просмотров и времени в две колонки
                html.Div(className='graphs-container', children=[
                    dcc.Graph(id='views-graph', className='graph'),
                    dcc.Graph(id='time-graph', className='graph'),
                ])
            ]),
                    ]),
            
    ])

