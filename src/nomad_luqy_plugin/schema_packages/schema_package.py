import numpy as np
import plotly.express as px
from nomad.config import config
from nomad.datamodel.data import (
    ArchiveSection,
    EntryData,
)
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    ELNComponentEnum,
)
from nomad.datamodel.metainfo.basesections import (
    Measurement,
    MeasurementResult,
    ReadableIdentifiers,
)
from nomad.datamodel.metainfo.plot import (
    PlotlyFigure,
    PlotSection,
)
from nomad.metainfo import (
    Quantity,
    SchemaPackage,
    Section,
    SubSection,
)
from nomad_measurements.general import NOMADMeasurementsCategory

from .abspl_normalizer import parse_abspl_data

configuration = config.get_plugin_entry_point(
    'nomad_luqy_plugin.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


class AbsPLSettings(ArchiveSection):
    """
    Section containing the metadata/settings for an Absolute
    Photoluminescence measurement.
    """

    m_def = Section(label='AbsPLSettings')

    laser_intensity_suns = Quantity(
        type=np.float64,
        description='Laser intensity in suns, e.g. 0.91.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
            label='Laser intensity (suns)',
        ),
    )
    bias_voltage = Quantity(
        type=np.float64,
        description='Bias voltage in volts, e.g. 0.0000.',
        unit='V',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, label='Bias Voltage'
        ),
    )
    smu_current_density = Quantity(
        type=np.float64,
        description='SMU current density in mA/cm².',
        unit='mA/cm**2',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, label='SMU current density'
        ),
    )
    integration_time = Quantity(
        type=np.float64,
        unit='ms',
        description='Integration time, e.g. 100.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, label='Integration Time'
        ),
    )
    delay_time = Quantity(
        type=np.float64,
        unit='s',
        description='Delay time of collection from illumination, 2.0.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, label='Delay time (s)'
        ),
    )
    eqe_laser_wavelength = Quantity(
        type=np.float64,
        description='EQE at the laser wavelength, e.g. 0.90.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
            label='EQE @ laser wavelength',
        ),
    )
    laser_spot_size = Quantity(
        type=np.float64,
        unit='cm**2',
        description='Laser spot size.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, label='Laser spot size (cm²)'
        ),
    )
    subcell_area = Quantity(
        type=np.float64,
        unit='cm**2',
        description='Subcell area.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, label='Subcell area (cm²)'
        ),
    )
    subcell_description = Quantity(
        type=str,
        description='Subcell description, e.g. "--" or some text if needed.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.RichTextEditQuantity, label='Subcell'
        ),
    )


class AbsPLResult(MeasurementResult):
    """
    Section containing the measured spectra from the absolute PL measurement.
    """

    m_def = Section(label='AbsPLResult')

    luminescence_quantum_yield = Quantity(
        type=np.float64,
        description='Luminescence quantum yield in percent, e.g. 0.0677.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, label='LuQY (%)'
        ),
    )
    quasi_fermi_level_splitting = Quantity(
        type=np.float64,
        unit='eV',
        description='iVoc, e.g. 1.532 (units eV or V).',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, label='Implied Voc'
        ),
    )
    bandgap = Quantity(
        type=np.float64,
        unit='eV',
        description="""Bandgap in eV, e.g. 1.532.""",
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, label='Bandgap'
        ),
    )
    derived_jsc = Quantity(
        type=np.float64,
        unit='mA/cm**2',
        description='Jsc, e.g. 10.32.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity, label='Jsc'),
    )

    wavelength = Quantity(
        type=np.float64,
        unit='nm',
        shape=['*'],
        description='Wavelength in nm.',
    )
    luminescence_flux_density = Quantity(
        type=np.float64,
        unit='s / (cm**2 * nm)',
        shape=['*'],
        description='Luminescence flux density in photons/(s cm² nm).',
    )
    raw_spectrum_counts = Quantity(
        type=np.float64,
        shape=['*'],
        description='Raw spectrum counts.',
    )
    dark_spectrum_counts = Quantity(
        type=np.float64,
        shape=['*'],
        description='Dark spectrum counts.',
    )


class AbsPLMeasurement(Measurement, PlotSection):
    """
    Absolute PL measurement.
    """

    method = Quantity(
        type=str,
        default='Absolute Photoluminescence',
        description='Type of the measurement method.',
    )

    settings = SubSection(
        section_def=AbsPLSettings,
        description='Settings/metadata related to the AbsPL measurement.',
    )

    results = Measurement.results.m_copy()
    results.section_def = AbsPLResult

    measurement_identifiers = SubSection(
        section_def=ReadableIdentifiers,
        description='Identifiers for the measurement (sample ID, etc.)',
    )

    data_file = Quantity(
        type=str,
        description='Path to the raw data file containing the absolute PL data.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.FileEditQuantity, label='AbsPL data file'
        ),
    )

    def normalize(self, archive, logger):  # noqa: PLR0912, PLR0915
        super().normalize(archive, logger)

        if self.results:
            # Plotting remains unchanged
            self.figures = []
            fig = px.line(
                x=self.results[0].wavelength,
                y=self.results[0].luminescence_flux_density,
                labels={'x': 'Wavelength', 'y': 'Luminescence Flux'},
            )
            fig.update_layout(
                xaxis={
                    'title': {'text': 'Wavelength (nm)'},
                    'mirror': 'ticks',
                    'showline': True,
                    'linecolor': 'darkgray',
                    'ticks': 'inside',
                    'tickcolor': 'darkgray',
                    'automargin': True,
                },
                yaxis={
                    'title': {
                        'text': 'Luminescence Flux (cm⁻² s⁻¹ nm⁻¹)',
                    },
                    'exponentformat': 'power',
                    'nticks': 5,
                    'mirror': 'ticks',
                    'showline': True,
                    'linecolor': 'darkgray',
                    'ticks': 'inside',
                    'tickcolor': 'darkgray',
                    'automargin': True,
                },
                updatemenus=[
                    {
                        'buttons': [
                            {
                                'label': 'Linear scale',
                                'method': 'update',
                                'args': [
                                    {},
                                    {
                                        'yaxis': {
                                            'type': 'linear',
                                            'exponentformat': 'power',
                                            'nticks': 5,
                                            'mirror': 'ticks',
                                            'showline': True,
                                            'linecolor': 'darkgray',
                                            'ticks': 'inside',
                                            'tickcolor': 'darkgray',
                                            'title': {
                                                'text': 'Luminescence Flux (cm⁻² s⁻¹ nm⁻¹)'  # noqa: E501
                                            },
                                            'automargin': True,
                                        }
                                    },
                                ],
                            },
                            {
                                'label': 'Log scale',
                                'method': 'update',
                                'args': [
                                    {},
                                    {
                                        'yaxis': {
                                            'type': 'log',
                                            'exponentformat': 'power',
                                            'nticks': 5,
                                            'mirror': 'ticks',
                                            'showline': True,
                                            'linecolor': 'darkgray',
                                            'ticks': 'inside',
                                            'tickcolor': 'darkgray',
                                            'title': {
                                                'text': 'Luminescence Flux (cm⁻² s⁻¹ nm⁻¹)'  # noqa: E501
                                            },
                                            'automargin': True,
                                        }
                                    },
                                ],
                            },
                        ],
                        'type': 'buttons',
                        'direction': 'left',
                        'showactive': True,
                        'x': 1.0,
                        'xanchor': 'right',
                        'y': 1.15,
                        'yanchor': 'top',
                    }
                ],
                template='plotly_white',
                margin={'t': 100},
            )
            self.figures = [
                PlotlyFigure(
                    label='AbsPL Spectrum (dynamic y-axis)',
                    figure=fig.to_plotly_json(),
                )
            ]
        else:
            logger.debug('No results exist to generate plots.')

        logger.debug('Finished AbsPLMeasurement.normalize')


class AbsPLMeasurementEntry(AbsPLMeasurement, EntryData):
    m_def = Section(
        label='Absolute PL Measurement',
        categories=[NOMADMeasurementsCategory],
        a_eln=ELNAnnotation(
            lane_width='800px',
        ),
    )

    def normalize(self, archive, logger):  # noqa: PLR0912, PLR0915
        logger.debug('Starting AbsPLMeasurement.normalize', data_file=self.data_file)
        if self.settings is None:
            self.settings = AbsPLSettings()

        if self.data_file:
            try:
                # Call the new parser function
                (
                    settings_vals,
                    result_vals,
                    wavelengths,
                    lum_flux,
                    raw_counts,
                    dark_counts,
                ) = parse_abspl_data(self.data_file, archive, logger)

                # Set settings
                for key, val in settings_vals.items():
                    setattr(self.settings, key, val)

                # Set results header values
                if not self.results:
                    self.results = [AbsPLResult()]
                for key, val in result_vals.items():
                    setattr(self.results[0], key, val)

                # Set spectral array data
                self.results[0].wavelength = np.array(wavelengths, dtype=float)
                self.results[0].luminescence_flux_density = np.array(
                    lum_flux, dtype=float
                )
                self.results[0].raw_spectrum_counts = np.array(raw_counts, dtype=float)
                self.results[0].dark_spectrum_counts = np.array(
                    dark_counts, dtype=float
                )

            except Exception as e:
                logger.warning(f'Could not parse the data file "{self.data_file}": {e}')
        super().normalize(archive, logger)


m_package.__init_metainfo__()
