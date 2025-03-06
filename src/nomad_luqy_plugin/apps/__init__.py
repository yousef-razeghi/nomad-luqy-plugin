from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import (
    App,
    Axis,  # added for histogram x-axis
    Column,
    Columns,
    Menu,  # for settings menu
    MenuItemHistogram,
    MenuItemTerms,  # use histogram for numeric data
    MenuSizeEnum,  # for menu sizing
    SearchQuantities,
)

schemas = [
    '*#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',
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
                    quantity='data.samples[0].name#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',  # noqa: E501
                    selected=True,
                ),
                'luqy': Column(
                    quantity='data.results[0].luminescence_quantum_yield#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',  # noqa: E501
                    selected=True,
                    label='LuQY (%)',
                ),
                'bandgap': Column(
                    quantity='data.results[0].bandgap#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',  # noqa: E501
                    selected=True,
                ),
                'quasi_fermi_level_splitting': Column(
                    quantity='data.results[0].quasi_fermi_level_splitting#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',  # noqa: E501
                    selected=True,
                    label='QFLS',
                ),
                'derived_jsc': Column(
                    quantity='data.results[0].derived_jsc#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',  # noqa: E501
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
                            x=Axis(
                                search_quantity='data.settings.laser_intensity_suns#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',  # noqa: E501
                                title='Laser Intensity (suns)',
                            ),
                            show_input=True,
                            nbins=30,
                        ),
                        MenuItemHistogram(
                            x=Axis(
                                search_quantity='data.settings.bias_voltage#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',  # noqa: E501
                                title='Bias Voltage',
                            ),
                            show_input=True,
                            nbins=30,
                        ),
                        MenuItemHistogram(
                            x=Axis(
                                search_quantity='data.settings.smu_current_density#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',  # noqa: E501
                                title='SMU Current Density',
                                unit='mA/cm**2',
                            ),
                            show_input=True,
                            nbins=30,
                        ),
                    ],
                ),
                # New Menu for Entry Information (changed from FilterMenu to Menu)
                Menu(
                    title='Entry Information',
                    items=[
                        MenuItemTerms(
                            search_quantity='entry_id',
                            title='Entry ID',
                        ),
                        MenuItemTerms(
                            search_quantity='authors.name',
                            title='Authors',
                        ),
                        MenuItemHistogram(
                            x=Axis(
                                search_quantity='data.entry_datetime#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',  # noqa: E501
                                title='Datetime',
                            ),
                            show_input=True,
                            nbins=30,
                        ),
                    ],
                    size=MenuSizeEnum.MD,
                ),
                # New Menu for Results Histograms
                Menu(
                    title='Results Histograms',
                    size=MenuSizeEnum.MD,
                    items=[
                        MenuItemHistogram(
                            x=Axis(
                                search_quantity='data.results[0].luminescence_quantum_yield#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',  # noqa: E501
                                title='LuQY (%)',
                            ),
                            show_input=True,
                            nbins=30,
                        ),
                        MenuItemHistogram(
                            x=Axis(
                                search_quantity='data.results[0].bandgap#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',  # noqa: E501
                                title='Bandgap',
                            ),
                            show_input=True,
                            nbins=30,
                        ),
                        MenuItemHistogram(
                            x=Axis(
                                search_quantity='data.results[0].quasi_fermi_level_splitting#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',  # noqa: E501
                                title='QFLS',
                            ),
                            show_input=True,
                            nbins=30,
                        ),
                        MenuItemHistogram(
                            x=Axis(
                                search_quantity='data.results[0].derived_jsc#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',  # noqa: E501
                                title='Jsc',
                                unit='mA/cm**2',
                                format={'decimals': 3, 'mode': 'standard'},
                            ),
                            show_input=True,
                            nbins=30,
                        ),
                    ],
                ),
            ],
        ),
        filters_locked={
            'results.eln.sections': [
                'AbsPLMeasurement',
            ]
        },
    ),
)
