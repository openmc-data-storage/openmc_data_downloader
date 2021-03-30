#!/usr/bin/env python3

__author__ = "Jonathan Shimwell"


import os
import unittest
from pathlib import Path

import openmc
from openmc_data_downloader import just_in_time_library_generator


class test_usage_with_openmc_python_api(unittest.TestCase):

    def test_simulation_with_destination(self):

        os.system('rm *.h5')
        os.system('rm my_custom_nuclear_data_dir/*.h5')

        # Define material
        my_mat = openmc.openmc.Material()
        my_mat.add_nuclide('Pu239', 3.7047e-2)
        my_mat.add_nuclide('Pu240', 1.7512e-3)
        my_mat.add_nuclide('As75', 1.3752e-3)
        openmc.openmc.Materials([my_mat]).export_to_xml()

        # Create a sphere of my_mat
        surf = openmc.Sphere(r=6.3849, boundary_type='vacuum')
        main_cell = openmc.Cell(fill=my_mat, region=-surf)
        openmc.Geometry([main_cell]).export_to_xml()

        # Define settings for the simulation
        settings = openmc.Settings()
        settings.particles = 10
        settings.batches = 2
        settings.inactive = 0
        center = (0., 0., 0.)
        settings.source = openmc.Source(space=openmc.stats.Point(center))
        settings.export_to_xml()

        # this clears the enviromental varible just to be sure that current
        # system settings are not being used
        os.environ["OPENMC_CROSS_SECTIONS"] = ''

        just_in_time_library_generator(
            destination='my_custom_nuclear_data_dir',
            libraries=['TENDL-2019'],
            materials=my_mat,
            set_OPENMC_CROSS_SECTIONS=True
        )

        os.system('echo $OPENMC_CROSS_SECTIONS')
        openmc.run()

        assert Path('my_custom_nuclear_data_dir/TENDL-2019_Pu239.h5').is_file()
        assert Path('my_custom_nuclear_data_dir/TENDL-2019_Pu240.h5').is_file()
        assert Path('my_custom_nuclear_data_dir/TENDL-2019_As75.h5').is_file()

        assert Path('summary.h5').is_file()
        assert Path('statepoint.2.h5').is_file()

        assert len(list(Path('my_custom_nuclear_data_dir').glob('*.h5'))) == 3

    def test_photon_simulation_with_single_mat(self):

        os.system('rm *.h5')

        # Define material
        my_mat = openmc.openmc.Material()
        my_mat.add_element('Fe', 1)
        openmc.openmc.Materials([my_mat]).export_to_xml()

        # Create a sphere of my_mat
        surf = openmc.Sphere(r=6.3849, boundary_type='vacuum')
        main_cell = openmc.Cell(fill=my_mat, region=-surf)
        openmc.Geometry([main_cell]).export_to_xml()

        # Define settings for the simulation
        settings = openmc.Settings()
        settings.particles = 10
        settings.batches = 2
        settings.inactive = 0
        settings.run_mode = 'fixed source'
        settings.photon_transport = True

        source = openmc.Source()
        source.space = openmc.stats.Point((0, 0, 0))
        source.angle = openmc.stats.Isotropic()
        # This is a Co60 source, see the task on sources to understand it
        source.energy = openmc.stats.Discrete([1.1732e6], [1.])
        source.particle = 'photon'

        settings.source = source
        settings.export_to_xml()

        # this clears the enviromental varible just to be sure that current
        # system settings are not being used
        os.environ["OPENMC_CROSS_SECTIONS"] = ''

        just_in_time_library_generator(
            libraries=['FENDL-3.1d'],
            materials=my_mat,
            # TODO find out why neutrons are needed here
            particles=['photon', 'neutron'],
            set_OPENMC_CROSS_SECTIONS=True
        )

        os.system('echo $OPENMC_CROSS_SECTIONS')
        openmc.run()

        assert Path('FENDL-3.1d_Fe.h5').is_file()

        assert Path('summary.h5').is_file()
        assert Path('statepoint.2.h5').is_file()

        assert len(list(Path('.').glob('*.h5'))) == 7  # normally 3 if just photons used

    def test_photon_neutron_simulation_with_single_mat(self):

        os.system('rm *.h5')

        # Define material
        my_mat = openmc.openmc.Material()
        my_mat.add_element('Fe', 1)
        openmc.openmc.Materials([my_mat]).export_to_xml()

        # Create a sphere of my_mat
        surf = openmc.Sphere(r=6.3849, boundary_type='vacuum')
        main_cell = openmc.Cell(fill=my_mat, region=-surf)
        openmc.Geometry([main_cell]).export_to_xml()

        # Define settings for the simulation
        settings = openmc.Settings()
        settings.particles = 10
        settings.batches = 2
        settings.inactive = 0
        settings.photon_transport = True
        center = (0., 0., 0.)
        settings.source = openmc.Source(space=openmc.stats.Point(center))
        settings.run_mode = 'fixed source'
        settings.export_to_xml()

        # this clears the enviromental varible just to be sure that current
        # system settings are not being used
        os.environ["OPENMC_CROSS_SECTIONS"] = ''

        just_in_time_library_generator(
            libraries=['FENDL-3.1d'],
            materials=my_mat,
            particles=['neutron', 'photon'],
            set_OPENMC_CROSS_SECTIONS=True
        )

        os.system('echo $OPENMC_CROSS_SECTIONS')
        openmc.run()

        assert Path('FENDL-3.1d_Fe54.h5').is_file()
        assert Path('FENDL-3.1d_Fe56.h5').is_file()
        assert Path('FENDL-3.1d_Fe57.h5').is_file()
        assert Path('FENDL-3.1d_Fe58.h5').is_file()
        assert Path('FENDL-3.1d_Fe.h5').is_file()

        assert Path('summary.h5').is_file()
        assert Path('statepoint.2.h5').is_file()
        assert len(list(Path('.').glob('*.h5'))) == 7  # summary and statepoint

    def test_simulation_with_single_mat(self):

        os.system('rm *.h5')

        # Define material
        my_mat = openmc.openmc.Material()
        my_mat.add_nuclide('Pu239', 3.7047e-2)
        my_mat.add_nuclide('Pu240', 1.7512e-3)
        my_mat.add_nuclide('As75', 1.3752e-3)
        openmc.openmc.Materials([my_mat]).export_to_xml()

        # Create a sphere of my_mat
        surf = openmc.Sphere(r=6.3849, boundary_type='vacuum')
        main_cell = openmc.Cell(fill=my_mat, region=-surf)
        openmc.Geometry([main_cell]).export_to_xml()

        # Define settings for the simulation
        settings = openmc.Settings()
        settings.particles = 10
        settings.batches = 2
        settings.inactive = 0
        center = (0., 0., 0.)
        settings.source = openmc.Source(space=openmc.stats.Point(center))
        settings.export_to_xml()

        # this clears the enviromental varible just to be sure that current
        # system settings are not being used
        os.environ["OPENMC_CROSS_SECTIONS"] = ''

        just_in_time_library_generator(
            libraries=['TENDL-2019'],
            materials=my_mat,
            particles='neutron',
            set_OPENMC_CROSS_SECTIONS=True)

        os.system('echo $OPENMC_CROSS_SECTIONS')
        openmc.run()

        assert Path('TENDL-2019_Pu239.h5').is_file()
        assert Path('TENDL-2019_Pu240.h5').is_file()
        assert Path('TENDL-2019_As75.h5').is_file()

        assert Path('summary.h5').is_file()
        assert Path('statepoint.2.h5').is_file()
        assert len(list(Path('.').glob('*.h5'))) == 5  # summary and statepoint

    def test_wmp_simulation_with_single_mat(self):

        os.system('rm *.h5')

        # Define material
        my_mat = openmc.openmc.Material()
        my_mat.add_element('P', 1)
        openmc.openmc.Materials([my_mat]).export_to_xml()

        # Create a sphere of my_mat
        surf = openmc.Sphere(r=6.3849, boundary_type='vacuum')
        main_cell = openmc.Cell(fill=my_mat, region=-surf)
        openmc.Geometry([main_cell]).export_to_xml()

        # Define settings for the simulation
        settings = openmc.Settings()
        settings.particles = 10
        settings.batches = 2
        settings.inactive = 0
        center = (0., 0., 0.)
        settings.source = openmc.Source(space=openmc.stats.Point(center))
        settings.export_to_xml()

        # this clears the enviromental varible just to be sure that current
        # system settings are not being used
        os.environ["OPENMC_CROSS_SECTIONS"] = ''

        just_in_time_library_generator(
            libraries=['ENDFB-7.1-WMP'],
            materials=my_mat,
            particles='neutron',
            set_OPENMC_CROSS_SECTIONS=True)

        os.system('echo $OPENMC_CROSS_SECTIONS')
        openmc.run()

        assert Path('ENDFB-7.1-WMP_P31.h5').is_file()

        assert Path('summary.h5').is_file()
        assert Path('statepoint.2.h5').is_file()
        assert len(list(Path('.').glob('*.h5'))) == 3

    def test_simulation_with_single_mat_list(self):

        os.system('rm *.h5')

        # Define material
        my_mat = openmc.openmc.Material()
        my_mat.add_nuclide('Pu239', 3.7047e-2)
        my_mat.add_nuclide('Pu240', 1.7512e-3)
        my_mat.add_nuclide('As75', 1.3752e-3)
        openmc.openmc.Materials([my_mat]).export_to_xml()

        # Create a sphere of my_mat
        surf = openmc.Sphere(r=6.3849, boundary_type='vacuum')
        main_cell = openmc.Cell(fill=my_mat, region=-surf)
        openmc.Geometry([main_cell]).export_to_xml()

        # Define settings for the simulation
        settings = openmc.Settings()
        settings.particles = 10
        settings.batches = 2
        settings.inactive = 0
        center = (0., 0., 0.)
        settings.source = openmc.Source(space=openmc.stats.Point(center))
        settings.export_to_xml()

        # this clears the enviromental varible just to be sure that current
        # system settings are not being used
        os.environ["OPENMC_CROSS_SECTIONS"] = ''

        just_in_time_library_generator(
            libraries=['TENDL-2019'],
            materials=[my_mat],
            particles='neutron',
            set_OPENMC_CROSS_SECTIONS=True)

        os.system('echo $OPENMC_CROSS_SECTIONS')
        openmc.run()

        assert Path('TENDL-2019_Pu239.h5').is_file()
        assert Path('TENDL-2019_Pu240.h5').is_file()
        assert Path('TENDL-2019_As75.h5').is_file()

        assert Path('summary.h5').is_file()
        assert Path('statepoint.2.h5').is_file()

        assert len(list(Path('.').glob('*.h5'))) == 5  # summary and statepoint

    def test_simulation_with_multi_mat_list(self):

        os.system('rm *.h5')

        # Define material
        my_mat1 = openmc.openmc.Material()
        my_mat1.add_nuclide('Pu239', 3.7047e-2)
        my_mat1.add_nuclide('Pu240', 1.7512e-3)

        my_mat2 = openmc.openmc.Material()
        my_mat2.add_element('As', 1.3752e-3)
        openmc.openmc.Materials([my_mat1, my_mat2]).export_to_xml()

        # Create a sphere of my_mat
        surf1 = openmc.Sphere(r=1)
        surf2 = openmc.Sphere(r=6, boundary_type='vacuum')
        main_cell = openmc.Cell(fill=my_mat1, region=-surf1)
        outer_cell = openmc.Cell(fill=my_mat2, region=+surf1 & -surf2)
        universe = openmc.Universe(cells=[main_cell, outer_cell])
        openmc.Geometry(universe).export_to_xml()

        # Define settings for the simulation
        settings = openmc.Settings()
        settings.particles = 10
        settings.batches = 2
        settings.inactive = 0
        center = (0., 0., 0.)
        settings.source = openmc.Source(space=openmc.stats.Point(center))
        settings.export_to_xml()

        # this clears the enviromental varible just to be sure that current
        # system settings are not being used
        os.environ["OPENMC_CROSS_SECTIONS"] = ''

        just_in_time_library_generator(
            libraries=['TENDL-2019'],
            materials=[
                my_mat1,
                my_mat2],
            set_OPENMC_CROSS_SECTIONS=True)

        os.system('echo $OPENMC_CROSS_SECTIONS')
        openmc.run()

        assert Path('TENDL-2019_Pu239.h5').is_file()
        assert Path('TENDL-2019_Pu240.h5').is_file()
        assert Path('TENDL-2019_As75.h5').is_file()

        assert Path('summary.h5').is_file()
        assert Path('statepoint.2.h5').is_file()

        assert len(list(Path('.').glob('*.h5'))) == 5  # summary and statepoint
