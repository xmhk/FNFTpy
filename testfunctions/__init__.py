"""
This file is part of FNFTpy.
FNFTpy provides wrapper functions to interact with FNFT,
a library for the numerical computation of nonlinear Fourier transforms.

For FNFTpy to work, a copy of FNFT has to be installed.
For general information, source files and installation of FNFT,
visit FNFT's github page: https://github.com/FastNFT

For information about setup and usage of FNFTpy see README.md or documentation.

FNFTpy is free software; you can redistribute it and/or
modify it under the terms of the version 2 of the GNU General
Public License as published by the Free Software Foundation.

FNFTpy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

Contributors:

Christoph Mahnke, 2018-2021

"""

from .kdvv_tests import KdvvExampleTest, KdvvExampleTestMex4BoundStates, KdvvExampleTestProvideBoundStateGuesses
from .nsev_tests import NsevExampleTest, NsevDstCstInputTest, NsevExampleTestBoundStateGuesses, NsevExampleTestBoundStateGuessesMex4, NsevExampleTestRF
from .manakovv_tests import ManakovvExampleTest, ManakovvMexExampleTest, ManakovvProvideBoundStateGuessesTest
from .nsep_tests import NsepExampleTest
from .nsev_inverse_tests import NsevInverseExample, NsevInverseExample2, NsevInverseExampleMex1,NsevInverseExampleMex3, NsevInverseInputVariation
from .options_tests import FnftpyOptionsTest
from .array_test import relnorm
