from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import (
    App,
    Axis,  # added for histogram x-axis
    Column,
    Columns,
    Dashboard,
    Layout,
    Menu,  # for settings menu
    MenuItemCustomQuantities,
    MenuItemHistogram,
    MenuItemOptimade,
    MenuItemPeriodicTable,
    MenuItemTerms,  # use histogram for numeric data
    MenuSizeEnum,  # for menu sizing
    SearchQuantities,
    WidgetPeriodicTable,
    WidgetScatterPlot,
    WidgetTerms,
)

schemas = [
    '*#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurementELN',
]

app_entry_point = AppEntryPoint(
    name='Absolute Luminescence',
    description='A search app for absolute photoluminescence experiments.',
    app=App(
        label='Absolute Luminescence',
        path='abs-luminescence',
        category='Measurements',
        breadcrumb='Explore Absolute Luminescence Measurements',
        search_quantities=SearchQuantities(include=schemas),
        columns=Columns(
            selected=[
                'entry_id',
            ],
            options={
                'entry_id': Column(
                    quantity='entry_id',
                    selected=False,
                ),
                'sample_name': Column(
                    quantity='data.samples[0].name#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurementELN',  # noqa: E501
                    selected=True,
                    label='Sample Name',
                ),
                'luqy': Column(
                    quantity='data.results[0].luminescence_quantum_yield#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurementELN',  # noqa: E501
                    selected=True,
                    label='LuQY (%)',
                ),
                'bandgap': Column(
                    quantity='data.results[0].bandgap#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurementELN',  # noqa: E501
                    selected=True,
                ),
                'quasi_fermi_level_splitting': Column(
                    quantity='data.results[0].quasi_fermi_level_splitting#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurementELN',  # noqa: E501
                    selected=True,
                    label='QFLS',
                ),
                'derived_jsc': Column(
                    quantity='data.results[0].derived_jsc#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurementELN',  # noqa: E501
                    selected=True,
                    format={'decimals': 3, 'mode': 'standard'},
                    unit='mA/cm**2',
                    label='Jsc',
                ),
            },
        ),
        menu=Menu(
            items=[
                Menu(
                    title='Measurement Settings',
                    size=MenuSizeEnum.MD,
                    items=[
                        MenuItemHistogram(
                            x={
                                'search_quantity': 'data.settings.laser_intensity_suns#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurementELN'
                            },  # noqa: E501
                            title='Laser Intensity (suns)',
                            show_input=True,
                            nbins=30,
                        ),
                        MenuItemHistogram(
                            x=Axis(
                                search_quantity='data.settings.bias_voltage#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurementELN',  # noqa: E501
                            ),
                            title='Bias Voltage',
                            show_input=True,
                            nbins=30,
                        ),
                        MenuItemHistogram(
                            x=Axis(
                                search_quantity='data.settings.smu_current_density#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurementELN',  # noqa: E501
                                unit='mA/cm**2',
                            ),
                            title='SMU Current Density',
                            show_input=True,
                            nbins=30,
                        ),
                    ],
                ),
                # New Menu for Entry Information (changed from FilterMenu to Menu)
                Menu(
                    title='Author | Sample | Dataset',
                    size='md',
                    items=[
                        MenuItemTerms(search_quantity='authors.name'),
                        MenuItemTerms(
                            search_quantity='data.samples.name#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurementELN',
                            title='Sample Name',
                        ),
                        MenuItemHistogram(x={'search_quantity': 'upload_create_time'}),
                        MenuItemTerms(search_quantity='datasets.dataset_name'),
                    ],
                ),
                # New Menu for Results Histograms
                MenuItemHistogram(
                    x=Axis(
                        search_quantity='data.results.luminescence_quantum_yield#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurementELN',  # noqa: E501
                    ),
                    title='LuQY (%)',
                    show_input=True,
                    nbins=30,
                ),
                MenuItemHistogram(
                    x=Axis(
                        search_quantity='data.results.bandgap#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurementELN',  # noqa: E501
                    ),
                    title='Bandgap',
                    show_input=True,
                    nbins=30,
                ),
                MenuItemHistogram(
                    x=Axis(
                        search_quantity='data.results.quasi_fermi_level_splitting#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurementELN',  # noqa: E501
                    ),
                    title='QFLS',
                    show_input=True,
                    nbins=30,
                ),
                MenuItemHistogram(
                    x=Axis(
                        search_quantity='data.results.derived_jsc#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurementELN',  # noqa: E501
                        unit='mA/cm**2',
                        format={'decimals': 3, 'mode': 'standard'},
                    ),
                    title='Jsc',
                    show_input=True,
                    nbins=30,
                ),
            ],
        ),
        dashboard=Dashboard(
            widgets=[
                WidgetScatterPlot(
                    title='Bandgap vs. LuQY',
                    autorange=True,
                    layout={
                        'lg': Layout(h=4, minH=3, minW=3, w=6, x=0, y=0),
                        'md': Layout(h=5, minH=3, minW=3, w=7, x=0, y=0),
                        'sm': Layout(h=6, minH=3, minW=3, w=6, x=0, y=0),
                        'xl': Layout(h=6, minH=3, minW=3, w=6, x=0, y=0),
                        'xxl': Layout(h=6, minH=3, minW=3, w=6, x=0, y=0),
                    },
                    x=Axis(
                        search_quantity='data.results[0].bandgap#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurementELN',  # noqa: E501
                    ),
                    y=Axis(
                        search_quantity='data.results[0].luminescence_quantum_yield#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurementELN',  # noqa: E501
                        title='LuQY (%)',
                    ),
                    color='data.results[0].quasi_fermi_level_splitting#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurementELN',  # noqa: E501s
                    size=1000,
                ),
            ]
        ),
        filters_locked={
            'results.eln.sections': [
                'AbsPLMeasurementELN',
            ]
        },
    ),
)
