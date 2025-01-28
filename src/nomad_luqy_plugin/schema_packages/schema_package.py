import numpy as np
import plotly.express as px

from nomad.metainfo import (
    Quantity,
    Section,
    SubSection,
    SchemaPackage,
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
from nomad.datamodel.data import (
    EntryData,
    ArchiveSection,
)
from nomad_measurements.general import NOMADMeasurementsCategory

from nomad.config import config

configuration = config.get_plugin_entry_point(
    'nomad_luqy_plugin.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


class AbsPLSettings(ArchiveSection):
    """
    Section containing the metadata/settings for an Absolute Photoluminescence measurement.
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
        description='Delay time, e.g. 0.000.',
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
    laser_spot_size_cm2 = Quantity(
        type=np.float64,
        description='Laser spot size in cm², e.g. 0.10.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, label='Laser spot size (cm²)'
        ),
    )
    subcell_area_cm2 = Quantity(
        type=np.float64,
        description='Subcell area in cm², e.g. 1.000.',
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
    implied_voc = Quantity(
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

    def generate_plots(self, archive, logger):
        """
        Creates two plots of the raw_spectrum_counts vs. wavelength:
        - Linear y-axis
        - Log y-axis
        """
        plots = []
        if self.wavelength is None or self.raw_spectrum_counts is None:
            logger.debug(
                'No data for plotting: wavelength or raw_spectrum_counts is None.'
            )
            return plots

        x = self.wavelength
        y = self.raw_spectrum_counts
        logger.debug('Generating PL plots', x_len=len(x), y_len=len(y))

        # 1) Linear scale plot
        fig_linear = px.line(
            x=x,
            y=y,
            labels={'x': 'Wavelength (nm)', 'y': 'Raw Spectrum (counts)'},
            title='Absolute PL Spectrum (Linear Scale)',
        )
        fig_linear.update_layout(
            template='plotly_white',
            hovermode='closest',
            dragmode='zoom',
            xaxis=dict(fixedrange=False),
            yaxis=dict(fixedrange=False),
            width=600,
            height=500,
        )
        fig_linear.update_traces(
            hovertemplate='Wavelength: %{x} nm<br>Counts: %{y:.2f}'
        )
        plot_json = fig_linear.to_plotly_json()
        plot_json['config'] = dict(scrollZoom=False)

        plots.append(
            PlotlyFigure(
                label='AbsPL Spectrum (linear scale)',
                figure=plot_json,
                description='Raw PL spectrum vs. wavelength with linear y-axis.',
            )
        )

        # 2) Log scale plot
        fig_log = px.line(
            x=x,
            y=y,
            labels={'x': 'Wavelength (nm)', 'y': 'Raw Spectrum (counts)'},
            title='Absolute PL Spectrum (Log Scale)',
            log_y=True,
        )
        fig_log.update_layout(
            template='plotly_white',
            hovermode='closest',
            dragmode='zoom',
            xaxis=dict(fixedrange=False),
            yaxis=dict(fixedrange=False),
            width=600,
            height=500,
        )
        fig_log.update_traces(hovertemplate='Wavelength: %{x} nm<br>Counts: %{y:.2f}')
        plot_json = fig_log.to_plotly_json()
        plot_json['config'] = dict(scrollZoom=False)

        plots.append(
            PlotlyFigure(
                label='AbsPL Spectrum (log scale)',
                figure=plot_json,
                description='Raw PL spectrum vs. wavelength with log y-axis.',
            )
        )
        logger.debug('Created 2 PL plots.')
        return plots


class AbsPLMeasurement(Measurement, EntryData, PlotSection):
    """
    Main section for an Absolute PL measurement, analogous to the XRD schema.
    """

    m_def = Section(
        label='Absolute PL Measurement',
        categories=[NOMADMeasurementsCategory],
        a_eln=ELNAnnotation(
            lane_width='800px',
        ),
    )

    method = Quantity(
        type=str,
        default='Absolute Photoluminescence (AbsPL)',
        description='Type of the measurement method.',
    )

    abs_pl_settings = SubSection(
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

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        logger.debug('Starting AbsPLMeasurement.normalize', data_file=self.data_file)
        if self.abs_pl_settings is None:
            self.abs_pl_settings = AbsPLSettings()

        if self.data_file:
            try:
                # read file in binary mode, decode as cp1252
                with archive.m_context.raw_file(self.data_file, mode='rb') as f:
                    raw_bytes = f.read()
                text = raw_bytes.decode('cp1252', errors='replace')
                lines = text.splitlines()
                logger.debug(
                    'Read data file lines', file=self.data_file, total_lines=len(lines)
                )

                # Prepare arrays for spectral data
                wavelengths = []
                lum_flux = []
                raw_counts = []
                dark_counts = []

                header_map_settings = {
                    'Laser intensity (suns)': 'laser_intensity_suns',
                    'Bias Voltage (V)': 'bias_voltage',
                    'SMU current density (mA/cm2)': 'smu_current_density',
                    'Integration Time (ms)': 'integration_time',
                    'Delay time (s)': 'delay_time',
                    'EQE @ laser wavelength': 'eqe_laser_wavelength',
                    'Laser spot size (cm²)': 'laser_spot_size_cm2',
                    'Subcell area (cm²)': 'subcell_area_cm2',
                    'Subcell': 'subcell_description',
                }
                header_map_result = {
                    'LuQY (%)': 'luminescence_quantum_yield',
                    'iVoc (V)': 'implied_voc',
                    'Bandgap (eV)': 'bandgap',
                    'Jsc (mA/cm2)': 'derived_jsc',
                }

                header_done = False
                data_start_idx = None

                # Read lines up to dashed separator
                for idx, line in enumerate(lines):
                    line_stripped = line.strip()
                    if line_stripped.startswith('---'):
                        data_start_idx = idx + 2  # skip dashed line + header line
                        header_done = True
                        break
                    if '\t' in line:
                        parts = line.split('\t', 1)
                        if len(parts) == 2:
                            key = parts[0].strip()
                            val_str = parts[1].strip()

                            # Map to either abs_pl_settings or results
                            if key in header_map_settings:
                                if key == 'Subcell':
                                    setattr(
                                        self.abs_pl_settings,
                                        header_map_settings[key],
                                        val_str,
                                    )
                                else:
                                    try:
                                        val_float = float(val_str)
                                        setattr(
                                            self.abs_pl_settings,
                                            header_map_settings[key],
                                            val_float,
                                        )
                                    except ValueError:
                                        logger.debug(
                                            'Could not convert header to float',
                                            key=key,
                                            val=val_str,
                                        )
                                        pass
                            elif key in header_map_result:
                                if not self.results:
                                    self.results = [AbsPLResult()]
                                try:
                                    val_float = float(val_str)
                                    setattr(
                                        self.results[0],
                                        header_map_result[key],
                                        val_float,
                                    )
                                except ValueError:
                                    logger.debug(
                                        'Could not convert result to float',
                                        key=key,
                                        val=val_str,
                                    )
                                    pass

                logger.debug(
                    'Header parsed', header_done=header_done, data_start=data_start_idx
                )
                if data_start_idx is not None and data_start_idx < len(lines):
                    # numeric data lines
                    for line in lines[data_start_idx:]:
                        if not line.strip():
                            continue
                        parts = line.split()
                        if len(parts) < 4:
                            continue
                        try:
                            w = float(parts[0])
                            lf = float(parts[1])
                            rc = float(parts[2])
                            dc = float(parts[3])
                            wavelengths.append(w)
                            lum_flux.append(lf)
                            raw_counts.append(rc)
                            dark_counts.append(dc)
                        except ValueError:
                            logger.debug('Could not parse numeric row', row=line)
                            pass

                logger.debug(
                    'Parsed numeric data',
                    w_count=len(wavelengths),
                    lf_count=len(lum_flux),
                    rc_count=len(raw_counts),
                    dc_count=len(dark_counts),
                )

                if not self.results:
                    self.results = [AbsPLResult()]
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

            self.figures = []

            fig = px.line(
                x=self.results[0].wavelength,
                y=self.results[0].luminescence_flux_density,
                labels={'x': 'Wavelength (nm)', 'y': 'Raw Spectrum (counts)'},
                title='Absolute PL Spectrum (Linear Scale)',
            )
            self.figures = [
                PlotlyFigure(
                    label='AbsPL Spectrum (linear scale)',
                    figure=fig.to_plotly_json(),
                )
            ]
        else:
            logger.debug('No results exist to generate plots.')

        logger.debug('Finished AbsPLMeasurement.normalize')


m_package.__init_metainfo__()
