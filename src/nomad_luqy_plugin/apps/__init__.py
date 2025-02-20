from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import (
    App,
    Column,
    Columns,
    FilterMenu,
    FilterMenus,
    SearchQuantities,
    Menu,  # for settings menu
    MenuItemHistogram,  # use histogram for numeric data
    MenuSizeEnum,  # for menu sizing
    Axis,  # added for histogram x-axis
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
                    quantity='data.samples[0].name#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',
                    selected=True,
                ),
                'luqy': Column(
                    quantity='data.results[0].luminescence_quantum_yield#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',
                    selected=True,
                    label='LuQY (%)',
                ),
                'bandgap': Column(
                    quantity='data.results[0].bandgap#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',
                    selected=True,
                ),
                'quasi_fermi_level_splitting': Column(
                    quantity='data.results[0].quasi_fermi_level_splitting#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',
                    selected=True,
                    label='QFLS (eV)',
                ),
                'derived_jsc': Column(
                    quantity='data.results[0].derived_jsc#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',
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
                                search_quantity='data.settings.laser_intensity_suns#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',
                                title='Laser Intensity (suns)',
                            ),
                            show_input=True,
                            nbins=30,
                        ),
                        MenuItemHistogram(
                            x=Axis(
                                search_quantity='data.settings.bias_voltage#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',
                                title='Bias Voltage (V)',
                            ),
                            show_input=True,
                            nbins=30,
                        ),
                        MenuItemHistogram(
                            x=Axis(
                                search_quantity='data.settings.smu_current_density#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',
                                title='SMU Current Density (mA/cm²)',
                            ),
                            show_input=True,
                            nbins=30,
                        ),
                    ],
                ),
                # MenuItemHistogram(
                #     x=Axis(
                #         search_quantity='data.results[0].luminescence_quantum_yield#nomad_luqy_plugin.schema_packages.schema_package.AbsPLMeasurement',
                #         title='Luminescence Quantum Yield (%)',
                #     ),
                #     show_input=True,
                #     nbins=30,
                # ),
            ]
        ),
        filters_locked={
            'results.eln.sections': [
                'AbsPLMeasurement',
            ]
        },
    ),
)
